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
    posAlgorithmCodes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    print('Choose which Algorithm to use! ', '\n')
    print(
          ' Algorithm 1: Random guess from remaining', '\n',
          
          'Algorithm 2: MaxParts with posAnswers', '\n',
          'Algorithm 3: MaxParts with posGuesses', '\n',
          
          'Algorithm 4: average_elim with posAnswers' , '\n',
          'Algorithm 5: average_elim with posGuesses' , '\n',
         
          'Algorithm 6: MaxEntropy with posAnswers', '\n',
          'Algorithm 7: MaxEntropy with posGuesses', '\n',
          
          'Algorithm 8: MiniMax with posAnswers', '\n',
          'Algorithm 9: MiniMax with posGuesses', '\n'
          )
    
    while algorithmCode not in posAlgorithmCodes:
        try:
            algorithmCode = int(input('Algorithm '))
        except ValueError:
            print('')
    return algorithmCode
    
#############################

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
            suggested_stats = average_elim(posAnswers, posAnswers, 0) 
        elif algorithm == 5:
            suggested_stats = average_elim(posGuesses, posAnswers, 0) 
        elif algorithm == 6:
            suggested_stats = max_entropy(posAnswers, posAnswers, 0) 
        elif algorithm == 7:
            suggested_stats = max_entropy(posGuesses, posAnswers, 0) 
        elif algorithm == 8:
            suggested_stats = MiniMax(posAnswers, posAnswers, 0) 
        elif algorithm == 9:
            suggested_stats = MiniMax(posGuesses, posAnswers, 0)    
        else:
            print('---Error: Invalid algorithm code---')
    
    print('I want to pick, ' , suggested_stats)
    suggested = suggested_stats[0]  
        
    return suggested
    



'''-----------Core grading function----------'''
'''Returns a properly filtered list of possible answer words: ChatGPT failed to make faster'''
def outputGenerator2(guessed_word, checked_word):
    if len(guessed_word) != len(checked_word):
        return ValueError('Error: Words must be same length')
    
    
    'Initialize output as all 0s (greys)'
    output = ['0'] * len(guessed_word)
    
    'Puts in the green letters'
    'This is 5% faster than using list comprehension'
    for i in range(len(guessed_word)):
        if guessed_word[i] == checked_word[i]:
            output[i] = guessed_word[i]
    
    
    'Determines what indeces in the output should be yellows'
    'This is 40% faster than old algorithm'
    yellows = []
    
    guessedMod = guessed_word
    checkedMod = checked_word
    
    for i in range(len(checkedMod)):
        if checked_word[i] == guessedMod[i]:
            guessedMod = guessedMod[:i] + '*' + guessedMod[i+1:]
            checkedMod = checkedMod[:i] + '^' + checkedMod[i+1:]
    
    for i in range(len(checkedMod)):
        if (checkedMod[i] in guessedMod):
                firstIndex = guessedMod.find(checkedMod[i])
                yellows.append(firstIndex)
                guessedMod = guessedMod[:firstIndex] + '#' + guessedMod[firstIndex+1:]
    
    'Puts in the yellow letters as 1'
    for i in yellows:
        output[i] = '1' 
    
    
    return output




'''Returns a properly filtered list of possible answer words: ChatGPT failed to make faster'''
def filter_posAnswers(guessed_word, output, posAnswers):
    posAnswers_updated = []
    
    for i in posAnswers:
        if output == outputGenerator2(guessed_word, i):
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
            output = outputGenerator2(guess_word, answer_word)

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


def testAlgorithm_OneWord():
    #Gets the number of letters we play with and imports corresponding answer
    wordLength, reducedYN = getGameWordLength()
    wordLists = importassignWordLists(wordLength, reducedYN)
    posAnswers = wordLists[0]
    posGuesses = wordLists[1]
    
    answer_word = ''
    while (len(answer_word) != wordLength):
        answer_word = input('What is the answer for the game you want to simulate?: ').lower()
          
        if len(answer_word) != wordLength:
            print('That is not ', wordLength, ' letters!')
        if len(answer_word) == wordLength and (answer_word not in posAnswers):
            posAnswers.append(answer_word)
            
            if (answer_word not in posGuesses):
                posGuesses.append(answer_word)
            
            print('That is not in the original answer list, added anyway...')
	
    algorithmCode = getAlgorithmCode()
    
    num_guess = simulate_game3(answer_word, algorithmCode, posAnswers, posGuesses, reducedYN)
    
    return



'''Guess Suggestion Algorithms'''

'Doesnt get simpler than this...'
def random_guess(list):
    guess = str(random.choice(list))
    return guess



'Max parts is essentially max_entropy but we dont care about frequency of each output'
def max_parts(posGuesses, posAnswers, printYN):
    maxParts = 0
    bestWord = ''
    locator = 0
    L = len(posAnswers)
    
    for guessed_word in posGuesses:
        distinctOutputs = []
        locator += 1
        
        for checked_word in posAnswers:
            output = outputGenerator2(guessed_word, checked_word)
            
            if output not in distinctOutputs:
                distinctOutputs.append(output)
        
        partitions = len(distinctOutputs)
        
        if printYN == 1:
            print('Word No.', locator, ' was ', guessed_word, ' Partitions: ', partitions)
        
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





'This is mathematically equivalent to old one. Works must faster'
def average_elim(posGuesses, posAnswers, printYN):
    bestElimFactor = 1
    bestWord = ''
    locator = 0
    L = len(posAnswers)
    
    for guessed_word in posGuesses:
        distinctOutputs = []
        countOfOutputs = []
        locator += 1
        
        for checked_word in posAnswers:
            output = outputGenerator2(guessed_word, checked_word)
            
            if output in distinctOutputs:
                countOfOutputs[distinctOutputs.index(output)] += 1
            else: distinctOutputs.append(output), countOfOutputs.append(1)
        
        ourSum = sum(countOfOutputs) #this is also just the length of posAnswers
        
        elimFactor = (sum(i*i for i in countOfOutputs)/(ourSum*ourSum))
        
        if printYN == 1:
            print('Word No.', locator, ' was ', guessed_word, ' ElimFactor: ', elimFactor)
    
      
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




'Another algorithm'
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
            output = outputGenerator2(guessed_word, checked_word)
            
            if output in distinctOutputs:
                countOfOutputs[distinctOutputs.index(output)] += 1
            else: distinctOutputs.append(output), countOfOutputs.append(1)
        
        ourSum = sum(countOfOutputs) #this is also just the length of posAnswers
        
        totalEntropy = 0
        for i in countOfOutputs:
            entropy = (i/ourSum)*math.log((ourSum/i), 2)
            totalEntropy += entropy
        
        if printYN == 1:
            print('Word No.', locator, ' was ', guessed_word, ' Entropy: ', totalEntropy)
        
        
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




'Try to minimize the maximum possible words remaining after this guess'
def MiniMax(posGuesses, posAnswers, printYN):
    minimizeMe = 1000000000000
    bestCountOfOutputs = [0, 1000000000000]
    bestWord = ''
    locator = 0
    L = len(posAnswers)
    
    for guessed_word in posGuesses:
        distinctOutputs = []
        countOfOutputs = []
        locator += 1
        aborted = 0
        
        for checked_word in posAnswers:
            output = outputGenerator2(guessed_word, checked_word)
            
            if output in distinctOutputs:
                countOfOutputs[distinctOutputs.index(output)] += 1
            else: distinctOutputs.append(output), countOfOutputs.append(1)
            
            'If our value goes over the current best, give up and go onto next guess word. We are trying to minimize here!'
            'Cuts the time to compute in half!!'
            if max(countOfOutputs) > minimizeMe:
                aborted = 1
                break
        
        
        ###MiniMax
        maxNumberOfRemainingCodes = max(countOfOutputs)
        bestCountOfOutputsSorted = sorted(bestCountOfOutputs)
        countOfOutputsSorted = sorted(countOfOutputs)
          
        if printYN == 1:
            if aborted == 1:
                print('Word No.', locator, ' was ', guessed_word, ' maxNumberOfRemainingCodes:   >', minimizeMe) 
            else: 
                print('Word No.', locator, ' was ', guessed_word, ' maxNumberOfRemainingCodes: ', maxNumberOfRemainingCodes)
        
        
        if maxNumberOfRemainingCodes == 1 and (guessed_word in posAnswers):
            'Found the best possible. Return it now'
            return guessed_word, maxNumberOfRemainingCodes        
        elif (countOfOutputsSorted == bestCountOfOutputsSorted) and (bestWord not in posAnswers) and (guessed_word in posAnswers):
            'If its a dead even tie, see if one word is a possible answer but the another isnt'
            minimizeMe = maxNumberOfRemainingCodes
            bestCountOfOutputs = countOfOutputs
            bestWord = guessed_word
        else:
            maxDepthCompare = min(len(bestCountOfOutputs), len(countOfOutputs))
            for i in range(1, maxDepthCompare):
                'sorted(countOfOutputs)[-i] gives iTh largest value in a list'
                if countOfOutputsSorted[-i] < bestCountOfOutputsSorted[-i]:
                    'print("Old best: ", sorted(bestCountOfOutputs), "  New best: ", sorted(countOfOutputs))'
                    minimizeMe = maxNumberOfRemainingCodes
                    bestCountOfOutputs = countOfOutputs
                    bestWord = guessed_word
                    break
                elif  countOfOutputsSorted[-i] > bestCountOfOutputsSorted[-i]:
                    break
            ###
      
    return bestWord, minimizeMe








'Other functions'

'MaxParts, average_elim, Max_Entropy all rely on the same data, can combine all 3 so only have to do comparisons once'
'Use this for autobestFirstGuess() in mastermindTesting. Greatly reduces computation time'
def comboAlgorithm(posGuesses, posAnswers, printYN):
    maxParts = 0 #Initalize to 0
    bestWordParts = ''
    
    bestElimFactor = 1 #Initialize to 1
    bestWordElim = ''
    
    maxExpEntropy = 0 #Initalize to 0
    bestWordEnt = ''
    
    minimizeMe = 1000000000000
    bestCountOfOutputs = [0, 1000000000000]
    bestWordMiniMax = ''
    
    
    
    locator = 0
    L = len(posAnswers)

    for guessed_word in posGuesses:
        distinctOutputs = []
        countOfOutputs = []
        locator += 1
        
        for checked_word in posAnswers:
            output = outputGenerator2(guessed_word, checked_word)
            
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
        
        
        ###MiniMax
        maxNumberOfRemainingCodes = max(countOfOutputs)
        bestCountOfOutputsSorted = sorted(bestCountOfOutputs)
        countOfOutputsSorted = sorted(countOfOutputs)
        
  
        if (countOfOutputsSorted == bestCountOfOutputsSorted) and (bestWordMiniMax not in posAnswers) and (guessed_word in posAnswers):
            minimizeMe = maxNumberOfRemainingCodes
            bestCountOfOutputs = countOfOutputs
            bestWordMiniMax = guessed_word
        else:
            'If the worst case scenarios are equal, look at the 2nd worse scenarios, 3rd case...'
            maxDepthCompare = min(len(bestCountOfOutputs), len(countOfOutputs))
            for i in range(1, maxDepthCompare):
                'sorted(countOfOutputs)[-i] is iTh largest value in a list'
                if countOfOutputsSorted[-i] < bestCountOfOutputsSorted[-i]:
                    'print("Old best: ", sorted(bestCountOfOutputs), "  New best: ", sorted(countOfOutputs))'
                    minimizeMe = maxNumberOfRemainingCodes
                    bestCountOfOutputs = countOfOutputs
                    bestWordMiniMax = guessed_word
                    break
                elif  countOfOutputsSorted[-i] > bestCountOfOutputsSorted[-i]:
                    break
            ###
        
        
        
        if printYN == 1:
            print('Code No. ', locator, ' was ', guessed_word, ' Partitions: ', partitions, 
                  ' ElimFactor: ', elimFactor,' Entropy: ', totalEntropy, ' MiniMax maxNumberOfRemainingCodes: ', maxNumberOfRemainingCodes)
    
    
    ##Results for each algorithm either reduced or not reduced list. posAnswers or posGuesses, depends on what you feed in
    wholeCell = [[bestWordParts, maxParts], [bestWordElim, bestElimFactor], [bestWordEnt, maxExpEntropy], [bestWordMiniMax, minimizeMe]]
    
    return wholeCell




'Gives the quality of a guess by giving Entropy, Partitions, ElimFactor, MiniMax, extra stuff'
def giveGuessDist():
    
    wordLength, reducedYN = getGameWordLength()
    wordLists = importassignWordLists(wordLength, reducedYN)
    posAnswers = wordLists[0]
    posGuesses = wordLists[1]
    
    guessed_word = getGuess(posGuesses)
    
    
    distinctOutputs = []
    countOfOutputs = []
    
    for checked_word in posAnswers:
        output = outputGenerator2(guessed_word, checked_word)
        
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
    
    print('MaxNumberOfRemainingCodes is ', max(countOfOutputs))
    
    return


