'''Contains algorithms for generating the lists of codes and retrieving the already computed 
best first guesses'''
import random
import string
import math
import time
import numpy
import itertools
import pandas as pd
import ast


firstGuessDF = pd.read_excel('mastermindBestFirstGuess.xlsx', sheet_name='CodeLength x NumColors')



def firstSuggestedCode(codeLength, color_list, algorithm):
    #For some reason, theres a weird shift with Row numbers (numColors)
    numColors = len(color_list)
    entireCell = firstGuessDF.iloc[numColors-2][codeLength]
    #Above looks like a list but is actually stored as String, convert back now
    entireCell = ast.literal_eval(entireCell)
    
    #Cell contains 3 lists, depending on which algorithm to use
    
    if algorithm in [2,3]:
        suggested_stats = entireCell[0]
    elif algorithm in [4,5]:
        suggested_stats = entireCell[1]
    elif algorithm in [6,7]:
        suggested_stats = entireCell[2]
    elif algorithm in [8,9]:
        suggested_stats = entireCell[3]
    else: 
        return ValueError('Algorithm Code not Found')
    
    return suggested_stats



def genCodeAndColorList(codeLength, numColors):
    #Temporary, need better system
    if (numColors^codeLength > 300000): 
        return ValueError('OVERLOADED: Too big of list ')
    
    #full_color_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k']
    full_color_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k']
    
    color_list = full_color_list[0:(numColors)]
    permutations = itertools.product(color_list, repeat = codeLength)
    allCodes = list(permutations)

    allCodesStr = []
    for i in allCodes:
        X = ''.join(i)
        allCodesStr.append(X)
    
    return allCodesStr, color_list


#print(genCodeAndColorList(6, 8))

