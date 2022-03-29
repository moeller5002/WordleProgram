'''Objective is to solve an unknown wordle by you guessing and giving the response
Can be used in runProcedure() in wordleMainFile file'''
import random
import string
import math
from wordleListManager import *
from wordleMainFunctions import *



def wordleComputerPlus():
    print('Lets crack the Wordle!')
    
    #Gets the number of letters we play with and imports corresponding word lists
    wordLength, reducedYN = getGameWordLength()
    wordLists = importassignWordLists(wordLength, reducedYN)
    posAnswers = wordLists[0]
    posGuesses = wordLists[1]
    
    algorithmCode = getAlgorithmCode()
    

    num_guesses = 0
    
    for i in range(10):
    
        '''-----------Suggested Guess Stuff ----------'''
        
        suggested_word = suggestedWord(algorithmCode, num_guesses, posAnswers, posGuesses, reducedYN)
        print('The recommended word is ', suggested_word, '\n')   
        
        '''----------- End Suggested Guess Stuff -----------'''
    
        #Gets a valid guess
        print('Guess No. ', num_guesses + 1)
        guess_word = getGuess(posGuesses)     
        num_guesses += 1
    
        '''Gets the response'''
        given_output = getOutput(posGuesses)
    
        posAnswers = filter_posAnswers(guess_word, given_output, posAnswers)
    
        print(posAnswers)
        print('There are now ', len(posAnswers), ' words remaining')        
        
        if len(posAnswers) in [0, 1]:
            return