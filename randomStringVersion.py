'''Instead of using actual words, this allows to test acgainst random strings.
Can be used in runProcedure() in wordleMainFile file'''
import random
import string
import math
from wordleListManager import *
from wordleMainFunctions import *
from wordleBaseGamePlus import *
from wordleSolver import *
from wordfreq import *

letters = string.ascii_lowercase

'''New stuff '''

def getStrLength():
    strLength = None
    
    while strLength not in range(100):
        try:
            strLength = int(input('Enter length of "word" string (please < 100): '))
            
        except ValueError:
            print('')

    return strLength


def getNumStr():
    numStr = None
    
    while numStr not in range(10000):
        try:
            numStr = int(input('Enter length of guess list (please < 10000): '))
            
        except ValueError:
            print('')

    return numStr


def generateStringList(strLength, numStr):
    stringList = []

    while len(stringList) < numStr:
        newStr = ''.join(random.choice(letters) for i in range(strLength))
    
        if newStr not in stringList:
            stringList.append(newStr)
    
    return stringList, stringList





'''Should prob guess a fresh random string, rather than one we know is a possible answer '''
def simulate_gameRandomStr(answer_word, posAnswers):
    num_guesses = 0
    gameDone = 0
    print('The secret string is: ', answer_word)
    X = len(answer_word)
    
    while gameDone == 0:
        guess_word = '' 
        
        #-----------Guess Selection Stuff ----------  ########       
        guess_word = random.choice(posAnswers)
        '''
        if len(posAnswers) == 1:
            guess_word = posAnswers[0]
        else:
            guess_word = ''.join(random.choice(letters) for i in range(X))
        '''
        
        print('Our guess is: ', guess_word)
        
        #----------- End Guess Selection Stuff -----------
        
        num_guesses += 1


        #Now we have a valid guess. 
        if guess_word == answer_word:
            print ('You got the string!   Solved in ', num_guesses, 'guesses', '\n') 
            gameDone = 1
            break
    
        else:
            output = outputGenerator(guess_word, answer_word)

            # remove words that are no longer able
            posAnswers = filter_posAnswers(guess_word, output, posAnswers)
            print('There are now ', len(posAnswers), ' words remaining') 
        
    
    return num_guesses
    
    
    


'''Input number of games, the list of possibleAnswers, and algorithm code'''
def testAlgorithmRandomStr():
    #Gets the number of letters we play with and imports corresponding answer
    wordLength = getStrLength()
    numWords = getNumStr()
    wordLists = generateStringList(wordLength, numWords)
    allAnswers = wordLists[0]
    
    print(allAnswers)
    
    numGames = getNumRuns(allAnswers)
   
    
    
    #Start the timer and we're off simulating
    start_time = time.perf_counter()
    guess_data = []

    for i in range(numGames):
        #Need to reassign our word lists for each game
        posAnswers = wordLists[0]
        posGuesses = wordLists[1]
        
        print('Run Number: ', i+1)
        num_guess = simulate_gameRandomStr(allAnswers[i], posAnswers)
        guess_data.append(num_guess)
 
    #Stop the timer and compile and print our results
    end_time = time.perf_counter()
    run_time = end_time - start_time

    average_guess = sum(guess_data) / len(guess_data)
    
    print('It took ', str(run_time/60), ' minutes to play ', len(guess_data), ' games.', '\n')
    print('\n', 'The average number of guesses was ', average_guess)
    print('Word Length: ', wordLength, '\n',
          'Using Algorithm: 1', '\n')
    
    
    print('\n', numpy.histogram(guess_data, range(30)))
    
    return







