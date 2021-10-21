import numpy as np
import random as ran
import string
from more_itertools import peekable

class MarkovChain:
    
    dictionary = []

    def __init__(self, dictionary_set, transition_matrix, stop_chars) -> None:
        self.dictionary_set = dictionary_set
        self.transition_matrix = transition_matrix
        self.stop_chars = stop_chars
        self.current_state = self.create_random_current_state()

    def next_state(self):
        new_state = np.array(self.current_state).dot(self.transition_matrix)
        rng = np.random.default_rng()
        choice = rng.choice(np.array(self.dictionary_set), p=new_state)
        loc = self.dictionary_set.index(choice)
        self.current_state = [ 0 if word != choice else 1 for word in self.dictionary_set]
    
    def get_current_word(self):
        return self.dictionary_set[self.current_state.index(1)]

    def check_stop(self):
        return self.dictionary_set[self.current_state.index(1)] in self.stop_chars


    def create_random_current_state(self):
        r = [ran.random() for i in range (0, len(self.dictionary_set))]
        normalizer = sum(r)
        probs = list(map((lambda x : x/normalizer), r))
        rng = np.random.default_rng()
        choice = rng.choice(self.dictionary_set, p=probs)
        return [0 if word != choice else 1 for word in self.dictionary_set]

class TransitionMatrixGenerator:
    def __init__(self, raw_data_handle) -> None:
        self.clean_data(raw_data_handle)
        self.generate_dictionary()
        self.generate_transition_matrix()

    def clean_data(self, raw_data_handle):
        data = ""
        with open(raw_data_handle, 'r') as raw_file:
            data = raw_file.read()

        translation_table = dict.fromkeys(string.punctuation)
        translation_table['.'] = ' .'
        translation_table['!'] = ' !'
        translation_table['?'] = ' ?'
        translation_table["'"] = "'"
        translation_table['\n'] = " "

        self.cleaned_data = data.translate(str.maketrans(translation_table))
        

    def generate_dictionary(self):
        cleaned_set = set(self.cleaned_data.split(' '))
        cleaned_set.remove('')
        self.dictionary = list(cleaned_set)
        

    def generate_transition_matrix(self):
        starting_matrix = np.zeros((len(self.dictionary), len(self.dictionary)))

        cleaned_data_with_spaces = self.cleaned_data.split(' ')
        cleaned_without_spaces = list(filter(lambda a : a!="", cleaned_data_with_spaces))
        clean_data_iter = peekable(cleaned_without_spaces)
        for word in clean_data_iter:
            if word in ['!', '.', '?']:
                continue
            word_loc = self.dictionary.index(word)
            next_word = clean_data_iter.peek(default="")
            if(next_word == ""):
                break
            next_word_loc = self.dictionary.index(next_word)
            starting_matrix[word_loc, next_word_loc] += 1

        for i in range(0, starting_matrix.shape[0]):
            total = sum(starting_matrix[i])
            if total == 0:
                continue
            for j in range(0, starting_matrix.shape[1]):
                starting_matrix[i,j] = (starting_matrix[i,j]/total)

        self.transition_matrix = starting_matrix
        

            
            

        
if __name__ == '__main__':

    matrix = TransitionMatrixGenerator("raw_data.txt")

    chain = MarkovChain(matrix.dictionary, matrix.transition_matrix,['.', '?', '!'])

    print('============')

    chain.create_random_current_state()

    print(chain.get_current_word())
    while not chain.check_stop():
        chain.next_state()
        print(chain.get_current_word())