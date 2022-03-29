'''Wordle Base Game. Takes you through a game but proposes best guess based on different algorithms
Can be used in runProcedure() in wordleMainFile file'''
import random
import string
import math
from wordleListManager import *
from wordleMainFunctions import *

def letsPlayGame():
    print('Lets play some Wordle!')
    
    #Gets the number of letters we play with and imports corresponding word lists
    wordLength, reducedYN = getGameWordLength()
    wordLists = importassignWordLists(wordLength, reducedYN)
    posAnswers = wordLists[0]
    posGuesses = wordLists[1]

    getHelp = getHelpYN()
    
    if getHelp == 1:
        algorithmCode = getAlgorithmCode()
    
    
    print('\n', 'Playing with ', wordLength, 'letters. Suggestions: ', getHelp)
    
    #Generates Secret Word
    answer_word = random.choice(posAnswers).lower()
    print('The secret word is: ', answer_word)
    
    print('There are', len(posAnswers)-1, 'words to eliminate!')
    
    
    #Game actually starts
    num_guesses = 0
    
    for i in range(6):
        
        '''-----------Suggested Guess Stuff ----------'''
        if getHelp == 1:
            suggested_word = suggestedWord(algorithmCode, num_guesses, posAnswers, posGuesses, reducedYN)
            print('The recommended word is ', suggested_word)   
        
        '''----------- End Suggested Guess Stuff -----------'''
        
        #Gets a valid guess
        print('Guess No. ', num_guesses + 1)
        guess_word = getGuess(posGuesses)              
        num_guesses += 1
    
        #Now we have a valid guess.   
        if guess_word == answer_word: #If its correct: Game is done; Break out.
            print ('\n\n', 'It took you ', num_guesses, 'guesses', '\n',
                   'You got the word!!! -------------------------------------------------\n\n\n')
            return 0
        
        else: #If not correct: Print the output and optionally provide help
            output = outputGenerator(guess_word, answer_word)
            print('Output is:', output, '\n\n')
    
            # Remove words that are no longer possible
            posAnswers = filter_posAnswers(guess_word, output, posAnswers)
            
            if getHelp == 1:
                print(posAnswers)
                print('There are now ', len(posAnswers), ' words remaining')        
              
    
    if guess_word != answer_word and num_guesses == 6:
        print('\n', 'The correct word was ', answer_word, '.  Better luck next time!', '\n\n\n')
        
    return
    

    