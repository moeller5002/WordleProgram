'''Contains a bunch of the base functions used in other files'''
import random
import string
import math
import time
import numpy
from wordleListManager import *

'''-----------Functions to get user input--------------'''

def getGameWordLength():
    from wordleListManager import gameWordLengths
    posWordLengths = gameWordLengths.copy()
    print('Choose from: ', posWordLengths)
    
    wordLength = None
    while (wordLength not in posWordLengths):
        try:
            wordLength = int(input('Input desired word length: '))
        except ValueError:
            print('')
    
    
    if wordLength >= 6:
        reducedYN = None
        while (reducedYN not in [0, 1]):
            try:
                reducedYN = int(input('Play with simplified word lists? (Y = 1, N = 0)  '))
            except ValueError:
                print('')
    else:
        reducedYN = 0
    
    
    return wordLength, reducedYN


def getNumRuns(posAnswers):
    maxRuns = len(posAnswers)
    print('Maximum of ', maxRuns)
    
    numRuns = None
    while numRuns not in range(maxRuns+1):
        try:
            numRuns = int(input('How many games to simulate? '))
            
        except ValueError:
            print('')
        
    return numRuns

def getGuess(posGuesses):
    guess_word = []
    wordLength = len(posGuesses[0])
    
    while (guess_word not in posGuesses):
        guess_word = input('Guess a word: ').lower()
          
        if len(guess_word) != wordLength:
            print('That is not ', wordLength, ' letters!')
        if len(guess_word) == wordLength and (guess_word not in posGuesses):
            print('That is not a valid word')
    
    return guess_word


def getOutput(posGuesses):
    given_output = []
    wordLength = len(posGuesses[0])
    
    while len(given_output) != wordLength:
        given_output = list(input('Enter the response. 1 =Yellow, 0 =Grey, Letter =Green: '))
        
        if len(given_output) != wordLength:
            print('Need output of length ', wordLength)
    
    return given_output
        

def getHelpYN():
    helpYN = None
    
    while (helpYN not in [0, 1]):
        try:
            helpYN = int(input('Will you want suggestions? Y=1  N=0  :'))
            
        except ValueError:
            print('')

    return helpYN



def getAlgorithmCode():
    algorithmCode = None
    posAlgorithmCodes = [1, 2, 3, 4, 5, 6, 7]
    
    print('Choose which Algorithm to use! ', '\n')
    print(' Algorithm 1: Random guess from remaining', '\n',
          
          'Algorithm 2: MaxParts with posAnswers', '\n',
          'Algorithm 3: MaxParts with posGuesses', '\n',
          
          'Algorithm 4: average_elim2 with posAnswers' , '\n',
          'Algorithm 5: average_elim2 with posGuesses' , '\n',
         
          'Algorithm 6: MaxEntropy with posAnswers', '\n',
          'Algorithm 7: MaxEntropy with posGuesses', '\n',
          )
    
    while algorithmCode not in posAlgorithmCodes:
        try:
            algorithmCode = int(input('Algorithm '))
        except ValueError:
            print('')
    return algorithmCode
    


def suggestedWord(algorithm, num_guesses, posAnswers, posGuesses, reducedYN):
    suggested = ''
    wordLength = len(posAnswers[0])
        
    
    if algorithm == 1:
        #Random_guess
        suggested = random_guess(posAnswers)
        return suggested
    
    if num_guesses == 0:
        suggested_stats = firstSuggestedWord(wordLength, algorithm, reducedYN) 
        print('I would pick, ' , suggested_stats)
        suggested = suggested_stats[0]
        return suggested
    
    elif len(posAnswers) in [1, 2]:
        suggested = posAnswers[0]
        return suggested
    
    else:
        if algorithm == 2:
            suggested_stats = max_parts(posAnswers, posAnswers, 0)
        elif algorithm == 3:
            suggested_stats = max_parts(posGuesses, posAnswers, 0) 
        elif algorithm == 4:
            suggested_stats = average_elim_guess2(posAnswers, posAnswers, 0) 
        elif algorithm == 5:
            suggested_stats = average_elim_guess2(posGuesses, posAnswers, 0) 
        elif algorithm == 6:
            suggested_stats = max_entropy(posAnswers, posAnswers, 0) 
        elif algorithm == 7:
            suggested_stats = max_entropy(posGuesses, posAnswers, 0) 
        else:
            print('---Error: Invalid algorithm code---')
    
    print('I want to pick, ' , suggested_stats)
    suggested = suggested_stats[0]  
        
    return suggested
    


#############################




'''-----------Core grading functions----------'''

def greenIndex(guessed, checked):#Gives the list of indeces of greens when passed two words in the form of a list
    greens = []
    
    for i in range(len(guessed)):
        if guessed[i] == checked[i]:
            greens.append(i)
    
    return greens
       


def yellowIndex3(guessed, checked):#Gives the list of indeces of yellows when passed two words in the form of a list
    yellows = []
    
    for i in range(len(guessed)):
        if guessed[i] != checked[i]:
            if guessed[i] in checked:
                    inGuessed = [j for j, x in enumerate(guessed) if x == guessed[i]]
                    inChecked = [j for j, x in enumerate(checked) if x == guessed[i]]
                    
                    nonSharedinGuess = list(set(inGuessed) - set(inChecked))
                    nonSharedinCheck = list(set(inChecked) - set(inGuessed))
                    
                    x = min(len(nonSharedinGuess), len(nonSharedinCheck))
                    
                    ###########
                    #when you subtract the sets to get nonSharedinGuess, it will flip the order so later indeces are first
                    #need to remedy this by sorting low to high
                    #change was made after all algorithms & best words run. dont believe it has effect on findings though
                    nonSharedinGuess.sort()
                    ###########
                    
                    if x != 0:
                        for i in range(x):
                            if nonSharedinGuess[i] not in yellows:
                                yellows.append(nonSharedinGuess[i])

                    
    return yellows #does not the greys. anything not green or yellow is grey by defult



def outputGenerator(guessed_word, checked_word):#Takes in two words as strings and gives the output as a list
    guessed = list(guessed_word)
    checked = list(checked_word)
    
    if len(guessed) != len(checked):
        return ValueError('Error: Words must be same length')
    
    output = []
    
    for i in range(len(guessed)):
        output.append('0') #They are grey by default 
    
    for i in greenIndex(guessed, checked):
        output[i] = guessed[i]
    
    for i in (yellowIndex3(guessed, checked)):
        output[i] = '1' 
    
    return output



#print("Yellow indexes" , yellowIndex3("certainties", "reorganized"))
#print(outputGenerator("certainties", "reorganized"))
#Yellows should be 2,4,5. If you dont sort, it will give 2,4,8



'''Returns a properly filtered list of possible answer words'''
def filter_posAnswers(guessed_word, output, posAnswers):
    posAnswers_updated = []
    
    for i in posAnswers:
        if output == outputGenerator(guessed_word, i):
            posAnswers_updated.append(i)
            
    return posAnswers_updated
            


'''Function to simulate game and return number of guesses it took'''
def simulate_game3(answer_word, algorithm, posAnswers, posGuesses, reducedYN):   
    num_guesses = 0
    gameDone = 0
    print('The secret word is: ', answer_word)
    
    while gameDone == 0:
        guess_word = '' 
        
        #-----------Guess Selection Stuff ----------         
        guess_word = suggestedWord(algorithm, num_guesses, posAnswers, posGuesses, reducedYN)
        
        print('Our guess is: ', guess_word)
        
        #----------- End Guess Selection Stuff -----------
        num_guesses += 1


        #Now we have a valid guess. 
        if guess_word == answer_word:
            print ('You got the word!   Solved in ', num_guesses, 'guesses', '\n') 
            gameDone = 1
            break
    
        else:
            output = outputGenerator(guess_word, answer_word)

            # remove words that are no longer able
            posAnswers = filter_posAnswers(guess_word, output, posAnswers)
            print('There are now ', len(posAnswers), ' words remaining') 
        
    
    return num_guesses



'''Input number of games, the list of possibleAnswers, and algorithm code'''
def testAlgorithm():
    #Gets the number of letters we play with and imports corresponding answer
    wordLength, reducedYN = getGameWordLength()
    wordLists = importassignWordLists(wordLength, reducedYN)
    allAnswers = wordLists[0]
    
    numGames = getNumRuns(allAnswers)
    algorithmCode = getAlgorithmCode()
    
    #Start the timer and we're off simulating
    start_time = time.perf_counter()
    guess_data = []

    for i in range(numGames):
        #Need to reassign our word lists for each game
        posAnswers = wordLists[0]
        posGuesses = wordLists[1]
        
        print('Run Number: ', i+1)
        num_guess = simulate_game3(allAnswers[i], algorithmCode, posAnswers, posGuesses, reducedYN)
        guess_data.append(num_guess)
 
    #Stop the timer and compile and print our results
    end_time = time.perf_counter()
    run_time = end_time - start_time

    average_guess = sum(guess_data) / len(guess_data)
    
    print('It took ', str(run_time/60), ' minutes to play ', len(guess_data), ' games.', '\n')
    print('\n', 'The average number of guesses was ', average_guess)
    print('Word Length: ', wordLength, '\n',
          'Reduced List: ', reducedYN, '\n',
          'Using Algorithm: ', algorithmCode, '\n')
    
    
    print('\n', numpy.histogram(guess_data, range(20)))
    
    return



'''Guess Suggestion Algorithms'''

def random_guess(list):
    guess = str(random.choice(list))
    return guess



#Max parts is essentially max_entropy but we dont care about frequency of each output
def max_parts(posGuesses, posAnswers, printYN):
    maxParts = 0
    bestWord = ''
    locator = 0
    L = len(posAnswers)
    
    for guessed_word in posGuesses:
        distinctOutputs = []
        locator += 1
        
        for checked_word in posAnswers:
            output = outputGenerator(guessed_word, checked_word)
            
            if output not in distinctOutputs:
                distinctOutputs.append(output)
        
        partitions = len(distinctOutputs)
        
        if printYN == 1:
            print('Word No. ', locator, ' was ', guessed_word, ' Partitions: ', partitions)
        
         #Maximum possible partitions is length of posAnswers, test for that first
        if partitions == L and guessed_word in posAnswers:
            maxParts = partitions
            bestWord = guessed_word
            return bestWord, maxParts
        elif partitions > maxParts:
            maxParts = partitions
            bestWord = guessed_word
        elif partitions == maxParts and guessed_word in posAnswers:
            maxParts = partitions
            bestWord = guessed_word
            
    
    return bestWord, maxParts





#This is mathematically equivalent to old one. Works must faster
def average_elim_guess2(posGuesses, posAnswers, printYN):
    bestElimFactor = 1
    bestWord = ''
    locator = 0
    L = len(posAnswers)
    
    for guessed_word in posGuesses:
        distinctOutputs = []
        countOfOutputs = []
        locator += 1
        
        for checked_word in posAnswers:
            output = outputGenerator(guessed_word, checked_word)
            
            if output in distinctOutputs:
                countOfOutputs[distinctOutputs.index(output)] += 1
            else: distinctOutputs.append(output), countOfOutputs.append(1)
        
        ourSum = sum(countOfOutputs) #this is also just the length of posAnswers
        
        elimFactor = (sum(i*i for i in countOfOutputs)/(ourSum*ourSum))
        
        if printYN == 1:
            print('Word No. ', locator, ' was ', guessed_word, ' ElimFactor: ', elimFactor)
    
      
        if elimFactor == 1/L and guessed_word in posAnswers:
            bestElimFactor = elimFactor
            bestWord = guessed_word
            return bestWord, bestElimFactor
        elif elimFactor < bestElimFactor:
            bestElimFactor = elimFactor
            bestWord = guessed_word
        elif elimFactor == bestElimFactor and guessed_word in posAnswers:
            bestElimFactor = elimFactor
            bestWord = guessed_word
            
    return bestWord, bestElimFactor





def max_entropy(posGuesses, posAnswers, printYN):
    maxExpEntropy = 0
    bestWord = ''
    locator = 0
    L = len(posAnswers)
    
    for guessed_word in posGuesses:
        distinctOutputs = []
        countOfOutputs = []
        locator += 1
        
        for checked_word in posAnswers:
            output = outputGenerator(guessed_word, checked_word)
            
            if output in distinctOutputs:
                countOfOutputs[distinctOutputs.index(output)] += 1
            else: distinctOutputs.append(output), countOfOutputs.append(1)
        
        ourSum = sum(countOfOutputs) #this is also just the length of posAnswers
        
        totalEntropy = 0
        for i in countOfOutputs:
            entropy = (i/ourSum)*math.log((ourSum/i), 2)
            totalEntropy += entropy
        
        if printYN == 1:
            print('Word No. ', locator, ' was ', guessed_word, ' Entropy: ', totalEntropy)
        
        
        if totalEntropy == math.log(L, 2) and guessed_word in posAnswers:
            maxExpEntropy = totalEntropy
            bestWord = guessed_word
            return bestWord, maxExpEntropy
        elif totalEntropy > maxExpEntropy:
            maxExpEntropy = totalEntropy
            bestWord = guessed_word
        elif totalEntropy == maxExpEntropy and guessed_word in posAnswers:
            maxExpEntropy = totalEntropy
            bestWord = guessed_word
    
    return bestWord, maxExpEntropy





##All the real algorithms rely on the same data, can combine all 3 so only have to do comparisons once
##Use this for autobestFirstGuess() in mastermindTesting. Greatly reduces computation time
def comboAlgorithm(posGuesses, posAnswers, printYN):
    maxParts = 0
    bestWordParts = ''
    
    bestElimFactor = 1
    bestWordElim = ''
    
    maxExpEntropy = 0
    bestWordEnt = ''
    
    locator = 0
    L = len(posAnswers)
    
    for guessed_word in posGuesses:
        distinctOutputs = []
        countOfOutputs = []
        locator += 1
        
        for checked_word in posAnswers:
            output = outputGenerator(guessed_word, checked_word)
            
            if output in distinctOutputs:
                countOfOutputs[distinctOutputs.index(output)] += 1
            else: distinctOutputs.append(output), countOfOutputs.append(1)
        
        ourSum = sum(countOfOutputs) #this is also just the length of posAnswers
        
        ###PARTS
        
        partitions = len(distinctOutputs)
        
        if partitions > maxParts:
            maxParts = partitions
            bestWordParts = guessed_word
        if (partitions == maxParts) and (bestWordParts not in posAnswers) and (guessed_word in posAnswers):
            maxParts = partitions
            bestWordParts = guessed_word
        
        
        ###
        
        ###ELIM
        elimFactor = (sum(i*i for i in countOfOutputs)/(ourSum*ourSum))
        
        if elimFactor < bestElimFactor:
            bestElimFactor = elimFactor
            bestWordElim = guessed_word
        if (elimFactor == bestElimFactor) and (bestWordElim not in posAnswers) and (guessed_word in posAnswers):
            bestElimFactor = elimFactor
            bestWordElim = guessed_word
        ###
        
        
        ###ENTROPY
        totalEntropy = 0
        for i in countOfOutputs:
            entropy = (i/ourSum)*math.log((ourSum/i), 2)
            totalEntropy += entropy
            
        if totalEntropy > maxExpEntropy:
            maxExpEntropy = totalEntropy
            bestWordEnt = guessed_word
        if (totalEntropy == maxExpEntropy) and (bestWordEnt not in posAnswers) and (guessed_word in posAnswers):
            maxExpEntropy = totalEntropy
            bestWordEnt = guessed_word 
        ###
            
        if printYN == 1:
            print('Code No. ', locator, ' was ', guessed_word, ' Partitions: ', partitions, 
                  ' ElimFactor: ', elimFactor,' Entropy: ', totalEntropy)
    
    ##Results for each algorithm either reduced or not reduced list. posAnswers or posGuesses, depends on what you feed in
    wholeCell = [[bestWordParts, maxParts], [bestWordElim, bestElimFactor], [bestWordEnt, maxExpEntropy]]
    
    return wholeCell





#Gives the quality of a guess by giving Entropy, Partitions, ElimFactor, extra stuff
def giveGuessDist():
    
    wordLength, reducedYN = getGameWordLength()
    wordLists = importassignWordLists(wordLength, reducedYN)
    posAnswers = wordLists[0]
    posGuesses = wordLists[1]
    
    guessed_word = getGuess(posGuesses)
    
    
    distinctOutputs = []
    countOfOutputs = []
    
    for checked_word in posAnswers:
        output = outputGenerator(guessed_word, checked_word)
        
        if output in distinctOutputs:
            countOfOutputs[distinctOutputs.index(output)] += 1
        else: distinctOutputs.append(output), countOfOutputs.append(1)
    
    res = list(map(''.join, distinctOutputs))
    print(res, '\n')
    print(countOfOutputs, '\n')
    
    
    ourSum = sum(countOfOutputs) #this is also just the length of posAnswers

    totalEntropy = 0
    for i in countOfOutputs:
        entropy = (i/ourSum)*math.log((ourSum/i), 2)
        totalEntropy += entropy
    
    print('Word was: ', guessed_word)
    print('Entropy is ', totalEntropy)
    
    partitions = len(distinctOutputs)
    print('Parititions are ', partitions)
    
    elimFactor = (sum(i*i for i in countOfOutputs)/(ourSum*ourSum))
    print('Elim Factor is ', elimFactor)
    
    return
