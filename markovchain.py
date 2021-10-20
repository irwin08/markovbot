import numpy as np
import random as ran
import string

class MarkovChain:
    
    dictionary = []

    def __init__(self, dictionary_set, transition_matrix, stop_char) -> None:
        self.dictionary_set = dictionary_set
        self.transition_matrix = transition_matrix
        self.stop_char = stop_char
        self.current_state = self.create_random_current_state()

    def next_state():
        pass

    def create_random_current_state(self):
        r = [ran.random() for i in range (1, len(self.dictionary_set))]
        normalizer = sum(r)
        return list(map((lambda x : x/normalizer), r))
        

class TransitionMatrixGenerator:
    def __init__(self, raw_data_handle) -> None:
        self.clean_data(raw_data_handle)
        self.generate_dictionary()

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
        print(self.cleaned_data)

    def generate_dictionary(self):
        self.dictionary = set(self.cleaned_data.split(' '))
        print(self.dictionary)
        
if __name__ == '__main__':
    chain = MarkovChain(['hi','ho','lets','go'], [],'.')
    print(chain.create_random_current_state())

    matrix = TransitionMatrixGenerator("raw_data.txt")