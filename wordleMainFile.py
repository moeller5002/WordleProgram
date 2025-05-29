import random
import string
import math
import time
from wordleListManager import *
from wordleMainFunctions import *
from wordleBaseGamePlus import *
from wordleSolver import *
from randomStringVersion import *
from wordfreq import *

'''Good place to play'''
# https://wordleplay.com/

'''Have to install this package into console!!'''
#pip install wordfreq (in the console)


'''5 main functions to choose from. runProcedure() below is prettier interface'''
#letsPlayGame()
#wordleComputerPlus()
#testAlgorithm()
#testAlgorithmRandomStr()
#giveGuessDist()



def runProcedure():
    choice = []
    validChoice = [1,2,3,4,5,6,0]
    
    while choice != 0:
        
        print('\n\n\n', 'Please choose what you would like to do...  ', '\n',
          '1: Play a game of Wordle', '\n',
          '2: Solve a game of Wordle (Cheat)','\n',
          '3: Test an algorithm','\n',
          '4: Test an algorithm against random strings', '\n',
          '5: Test an algorithm against a specific word', '\n',
          '6: Check quality of first guess', '\n',
          '0: Exit to console')
        
        while (choice not in validChoice):
            try:
                choice = int(input('What would you like to do?  '))
            
            except ValueError:
                print('Invalid input')
                
        if choice == 1:
            letsPlayGame()
        elif choice == 2:
            wordleComputerPlus()
        elif choice == 3:
            testAlgorithm()
        elif choice == 4:
            testAlgorithmRandomStr()
        elif choice == 5:
            testAlgorithm_OneWord()
        elif choice == 6:
            giveGuessDist()
        elif choice == 0:
            return
        
        choice = []
        
        
runProcedure()




'''Use this to fill out the tables in the excel file.'''

def autoBestFirstGuess():
    wordLength, reducedYN = getGameWordLength()
    wordLists = importassignWordLists(wordLength, reducedYN)
    
    posAnswers = wordLists[0]
    posGuesses = wordLists[1]
    
    
    search = []
    '### Will determine if we get results for 2,4,6 or 3,5,7. Only matters with reduced lists'
    if reducedYN == 1 or wordLength == 5:
        
        while search not in [0,1]:
            try:
                search = int(input('Search through guesses or answers? guesses = 0, answers = 1 '))
            except ValueError:
                print(' ')
        
        if search == 1:
            posGuesses = posAnswers
    
    
    
    start_time = time.perf_counter()
    
    results = MiniMax(posGuesses, posAnswers, 1)    
    
    end_time = time.perf_counter()
    run_time = end_time - start_time
    
    print('\n', 'CodeLength: ', wordLength, ' ReducedYN: ', reducedYN)
    print('Best Guesses according to... MaxParts, AverageElim, MaxEntropy, MiniMax', '\n', results, '\n')
    
    printSearch = ''
    if search == 0: 
        printSearch = 'posGuesses' 
    else: printSearch = 'posAnswers'
    print('Searched through ', printSearch)
    
    print('It took ', str(run_time/60), ' minutes to compute ', '\n')
    
    
    return results


#autoBestFirstGuess()






