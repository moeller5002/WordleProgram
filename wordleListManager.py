'''Contains functions for importing word lists from txt files and retrieving already computed 
best first words from the excel file'''

from wordfreq import *
import pandas as pd
import ast

firstGuessReduced = pd.read_excel('wordleBestFirstGuess.xlsx', sheet_name='ReducedWordLists')
firstGuessFull = pd.read_excel('wordleBestFirstGuess.xlsx', sheet_name='FullWordLists')
#Retrieve with .iloc[row][column]


def firstSuggestedWord(wordLength, algorithmCode, reducedYN):
    if (wordLength > 6):
        suggested_stats = firstGuessReduced.iloc[algorithmCode-1][wordLength]
        print('Best we have is: ', suggested_stats)
    
    elif (wordLength == 6):
        if (reducedYN == 0):
            suggested_stats = firstGuessFull.iloc[algorithmCode-1][6]
        elif (reducedYN == 1):
            suggested_stats = firstGuessReduced.iloc[algorithmCode-1][6]
    
    elif (wordLength < 6):
        suggested_stats = firstGuessFull.iloc[algorithmCode-1][wordLength]
    
    #Suggested_stats are confusingly stored as string even though it looks like a list    
    return ast.literal_eval(suggested_stats)



gameWordLengths = [3, 4, 5, 6, 7, 8, 9, 10, 11, 13]
# All non-5 letter word lists must have file name XletterWords.txt
def importassignWordLists(word_length, reducedYN):
    
    if word_length == 5:#wordlePosAnswers is length 2315
        with open('5letterWordleAnswers.txt') as input_file:
            answersList = [line.strip() for line in input_file]
            
        with open('5letterWordleGuesses.txt') as input_file:#wordlePosGuesses is length 12972
            guessesList = [line.strip() for line in input_file]

    
    else:
        tag = "letterWords.txt"
        X = str(word_length)
        File = X+tag
        
        with open(File) as input_file:
            wordList = [line.strip() for line in input_file]
    
        ''' If using reduced lists, just use the top 12972 for guesses and top 2315 for answers (like Wordle)'''
        if (reducedYN == 1) and (len(wordList) >= 12972):
            wordsAndFreqs = topXWordInfo(wordList, 12972)
            answersList = [item[0] for item in wordsAndFreqs][0:2315]
            guessesList = [item[0] for item in wordsAndFreqs]
        
        else: 
            answersList = wordList
            guessesList = wordList
    
        print('Length of Answer List: ', len(answersList))
        print('Length of Guesses List: ', len(guessesList))
        
    return answersList, guessesList




#Returns the top numWords&freq of words from wordList based on frequency. (Which words are most common)
#A little worried about wordFrew being updated in the future and my word lists not matching up anymore...
def topXWordInfo(wordList, numWords):
    wordsWFreq = []
    
    #Get frequency for every word in the list
    for word in wordList:
        wordsWFreq.append((word, word_frequency(word, 'en')))
    
    #Sorting based on word frequency. Most common to least
    wordsWFreq.sort(key = lambda x:x[1], reverse = True)
    
    #Just want the "numWords" most common words
    topXWordsInfo = wordsWFreq[0:numWords]
    
    return topXWordsInfo

