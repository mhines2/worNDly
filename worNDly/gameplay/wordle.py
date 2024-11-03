#!/usr/bin/env python3

import random

''' Define classes for the guess and solution '''

class Guess:
    def __init__(self, string, length):
        self.string = string.upper()
        self.length = length

class Solution:
    def __init__(self, string, length, yellowLetters = [], grayLetters = [], greenLetters = ['', '', '', '', '']):
        self.string = string
        self.length = length
        self.yellowLetters = yellowLetters
        self.grayLetters = grayLetters
        self.greenLetters = greenLetters

    def evaluateLetters(self, guessedString): # Evaluate the solution string against the guessed one to find what letters work.
        self.yellowLetters = []
        self.greenLetters = ['', '', '', '', '']
        self.grayLetters = []

        for index, letter in enumerate(guessedString):
            
            for correctIndex, correctLetter in enumerate(self.string):
                if correctLetter == letter and correctIndex == index:
                    self.greenLetters[index] = letter

            if letter in self.string and letter not in self.yellowLetters and letter not in self.greenLetters:
                self.yellowLetters.append(letter)

            if letter not in self.string and letter not in self.grayLetters:
                self.grayLetters.append(letter)
            

        return self.yellowLetters, self.grayLetters, self.greenLetters

''' Read the file of words '''
def readWordSet():
    return {word.strip() for word in open('new_words.txt')}

''' Main execution '''
def main():
    wordSet = readWordSet()
    wordOfDay = random.choice(list(wordSet))
    solution = Solution(wordOfDay, len(wordOfDay))
    found, guesses = False, 0
    allguesses = {}
    
    while guesses < 6 and not found: # Loop until maximum number of guesses or the word is found.

        string = input(f'{guesses + 1}. ')
        userGuess = Guess(string, len(string))
        assert userGuess.length == 5
        guesses += 1
        yellow, gray, green = solution.evaluateLetters(userGuess.string)
        
        found = all(green)
        if found:
            print()
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            print()
            if guesses > 1:
                print(f'You found the word of the day in {guesses} guesses!')
            else:
                print(f'You found the word of the day in {guesses} guess!')
            
            print()
        else:
            print()   
            print('Good letters = ', yellow)
            print('Bad letters = ', gray)
            print('Correct letters = ', green)
            print()
        
        '''for letter in green:
            if letter :
                print(letter, end = ' ')
            else:
                print('_', end = ' ')'''
        
        print()

    if not found:
        print()
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print()
        print(f'Out of guesses :( the word of the day was {wordOfDay}.')
        print()
        
if __name__ == '__main__':
    main()
