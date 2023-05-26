'''Contains all the important functions used in the other filess'''
import random
import string
import math
import time
import numpy
import itertools
from mastermindCodeManager import *

'''-----------Functions to get user input--------------'''

def getGameCodeLength():
    
    codeLength = None
    while (codeLength not in range(2, 11)):
        try:
            codeLength = int(input('What length of code to break? Min 2, Max 11: '))
        except ValueError:
            print('')
    
    return codeLength


def getNumColors():
    
    numColors = None
    while (numColors not in range(2, 11)):
        try:
            numColors = int(input('How many colors to play with? Min 2, Max 11: '))
        except ValueError:
            print('')
    
    return numColors


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
    guess_code = []
    codeLength = len(posGuesses[0])
    
    while (guess_code not in posGuesses):
        guess_code = input('Guess a code: ').lower()
          
        if len(guess_code) != codeLength:
            print('That is not ', codeLength, ' letters!')
        if len(guess_code) == codeLength and (guess_code not in posGuesses):
            print('That is not a valid code')
    
    return guess_code


def getOutput(posGuesses):
    given_output = []
    max = len(posGuesses[0])
    
    posResponses = list(range(max+1))
    numW = None
    numR = None
    
    while numR not in posResponses:
        try:
            numR = int(input("How many red pegs in response? "))
            if numR not in posResponses:
                print("--Try again--")
                
        except ValueError: 
            print("--Try again--")
    
    
    while numW not in posResponses:
        try:
            numW = int(input("How many white pegs in response? "))
            if numW not in posResponses:
                print("--Try again--")
                
        except ValueError: 
            print("--Try again--")
    
    
    given_output = [numR, numW]
    
    return given_output
        

def getHelpYN():
    helpYN = None
    
    while (helpYN not in [0, 1]):
        try:
            helpYN = int(input('Will you want suggestions? Y=1  N=0: '))
            
        except ValueError:
            print('')

    return helpYN



def getAlgorithmCode():
    algorithmCode = None
    posAlgorithmCodes = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    print('Choose which Algorithm to use! ', '\n')
    print(' Algorithm 1: Random guess from remaining', '\n',
          
          'Algorithm 2: MaxParts with posAnswers', '\n',
          'Algorithm 3: MaxParts with posGuesses', '\n',
          
          'Algorithm 4: average_elim2 with posAnswers' , '\n',
          'Algorithm 5: average_elim2 with posGuesses' , '\n',
         
          'Algorithm 6: MaxEntropy with posAnswers', '\n',
          'Algorithm 7: MaxEntropy with posGuesses', '\n',
          
          'Algorithm 8: MiniMax with posAnswers', '\n',
          'Algorithm 9: MiniMax with posGuesses', '\n',
          )
    
    while algorithmCode not in posAlgorithmCodes:
        try:
            algorithmCode = int(input('Algorithm '))
        except ValueError:
            print('')
    return algorithmCode



'''Function to return suggested code'''

def suggestedCode(posGuesses, posAnswers, color_list, algorithm, num_guesses):
    suggested = ''
    codeLength = len(posAnswers[0])
    
    if algorithm == 1:
        #Random_guess
        suggested = random_guess(posAnswers)
        return suggested
    
    if num_guesses == 0:
        suggested_stats = firstSuggestedCode(codeLength, color_list, algorithm)
        print('I would pick, ', suggested_stats)
        return suggested_stats[0]
    
    if len(posAnswers) in [1, 2]:
        suggested = posAnswers[0]
        return suggested
    
    else:
        if algorithm == 2:
            suggested_stats = max_parts(posAnswers, posAnswers, color_list, 0)
        elif algorithm == 3:
            suggested_stats = max_parts(posGuesses, posAnswers, color_list, 0) 
        elif algorithm == 4:
            suggested_stats = average_elim(posAnswers, posAnswers, color_list, 0) 
        elif algorithm == 5:
            suggested_stats = average_elim(posGuesses, posAnswers, color_list, 0) 
        elif algorithm == 6: 
            suggested_stats = max_entropy(posAnswers, posAnswers, color_list, 0) 
        elif algorithm == 7:
            suggested_stats = max_entropy(posGuesses, posAnswers, color_list, 0) 
        elif algorithm == 8: 
            suggested_stats = MiniMax(posAnswers, posAnswers, color_list, 0) 
        elif algorithm == 9:
            suggested_stats = MiniMax(posGuesses, posAnswers, color_list, 0) 
        else:
            print('---Error: Invalid algorithm code---')
    
    print('I want to pick, ' , suggested_stats)  
        
    return suggested_stats[0] 





'''Core grading function'''
def outputGenerator(guessed, checked, colorList):
    
    if len(guessed) != len(checked):
        return ValueError('Error: codes must be same length')
    
    redCount = 0
    totalCount = 0
    
    for i in range(len(guessed)):
        if guessed[i] == checked[i]:
            redCount += 1
    
    for i in colorList:
        totalCount += min(guessed.count(i), checked.count(i))
    
    output = [redCount, (totalCount-redCount)]
    
    return output
    
    
'''Returns a properly filtered list of possible answer codes'''
def filter_posAnswers(guessed, output, posAnswers, colorList):
    posAnswers_updated = []
    
    for i in posAnswers:
        if output == outputGenerator(guessed, i, colorList):

            posAnswers_updated.append(i)
            
    return posAnswers_updated
     





'''Function to simulate game and return number of guesses it took'''
def simulate_game(answer_code, algorithm, posAnswers, posGuesses, colorList):   
    num_guesses = 0
    gameDone = 0
    print('The secret code is: ', answer_code)
    
    
    while gameDone == 0:
        guess_code = '' 
        
        #-----------Guess Selection Stuff ----------         
        guess_code = suggestedCode(posGuesses, posAnswers, colorList, algorithm, num_guesses)
        
        print('Our guess is: ', guess_code)
        
        #----------- End Guess Selection Stuff -----------
        num_guesses += 1


        #Now we have a valid guess. 
        if guess_code == answer_code:
            print ('You got the code!   Solved in ', num_guesses, 'guesses', '\n') 
            gameDone = 1
            break
    
        else:
            output = outputGenerator(guess_code, answer_code, colorList)

            # remove codes that are no longer possible answers
            posAnswers = filter_posAnswers(guess_code, output, posAnswers, colorList)
            print('There are now ', len(posAnswers), ' codes remaining') 
        
    
    return num_guesses



'''Input number of games, the list of possibleAnswers, and algorithm code'''
def testAlgorithm():
    #Gets the number of letters we play with and imports corresponding answer
    codeLength = getGameCodeLength()
    numColors = getNumColors()
    
    
    codeLists, color_list = genCodeAndColorList(codeLength, numColors)
    
    allAnswers = codeLists
    
    numGames = getNumRuns(allAnswers)
    algorithmCode = getAlgorithmCode()
    
    #Start the timer and we're off simulating
    start_time = time.perf_counter()
    guess_data = []

    for i in range(numGames):
        #Need to reassign our code lists for each game
        posAnswers = codeLists
        posGuesses = codeLists
        
        print('Run Number: ', i+1)
        num_guess = simulate_game(allAnswers[i], algorithmCode, posAnswers, posGuesses, color_list)
        guess_data.append(num_guess)
 
    #Stop the timer and compile and print our results
    end_time = time.perf_counter()
    run_time = end_time - start_time

    average_guess = sum(guess_data) / len(guess_data)
    
    print('It took ', str(run_time/60), ' minutes to play ', len(guess_data), ' games.', '\n')
    print('\n', 'The average number of guesses was ', average_guess)
    print('Code Length: ', codeLength, '\n',
          'Using Algorithm: ', algorithmCode, '\n')
    
    
    print('\n', numpy.histogram(guess_data, range(20)))
    
    return






'''Guess Suggestion Algorithms'''

def random_guess(list):
    guess = str(random.choice(list))
    return guess


'''What guess will give us the most number of unique responses?'''
def max_parts(posGuesses, posAnswers, color_list, printYN):
    maxParts = 0
    bestCode = ''
    locator = 0
    L = len(posAnswers)
    
    for guessed_code in posGuesses:
        distinctOutputs = []
        locator += 1
        
        for checked_code in posAnswers:
            output = outputGenerator(guessed_code, checked_code, color_list)
            
            if output not in distinctOutputs:
                distinctOutputs.append(output)
        
        partitions = len(distinctOutputs)
        
        if printYN == 1:
            print('Code No. ', locator, ' was ', guessed_code, ' Partitions: ', partitions)
        
        '''Figure out if this is a better code than previous best'''
        if partitions > maxParts:
            maxParts = partitions
            bestCode = guessed_code
        if (partitions == maxParts) and (bestCode not in posAnswers) and (guessed_code in posAnswers):
            maxParts = partitions
            bestCode = guessed_code 
           
    
    return bestCode, maxParts

'''On average, what guess leaves the smallest portion of the possible answers remaining?'''
def average_elim(posGuesses, posAnswers, color_list, printYN):
    bestElimFactor = 1
    bestCode = ''
    locator = 0
    L = len(posAnswers)
    
    for guessed_code in posGuesses:
        distinctOutputs = []
        countOfOutputs = []
        locator += 1
        
        for checked_code in posAnswers:
            output = outputGenerator(guessed_code, checked_code, color_list)
            
            if output in distinctOutputs:
                countOfOutputs[distinctOutputs.index(output)] += 1
            else: distinctOutputs.append(output), countOfOutputs.append(1)
        
        ourSum = sum(countOfOutputs) #this is also just the length of posAnswers
        
        #Consider switching to just the sum of squares to prevent rounding error by dividing
        elimFactor = (sum(i*i for i in countOfOutputs)/(ourSum*ourSum))
        
        if printYN == 1:
            print('Code No. ', locator, ' was ', guessed_code, ' ElimFactor: ', elimFactor)
        
        '''Figure out if this is a better code than previous best'''
        if elimFactor < bestElimFactor:
            bestElimFactor = elimFactor
            bestCode = guessed_code
        if (elimFactor == bestElimFactor) and (bestCode not in posAnswers) and (guessed_code in posAnswers):
            bestElimFactor = elimFactor
            bestCode = guessed_code 

            
    return bestCode, bestElimFactor



'''Another waay of analyzing the same data. What guess will cut our answers in half the most amount of times?'''
def max_entropy(posGuesses, posAnswers, color_list, printYN):
    maxExpEntropy = 0
    bestCode = ''
    locator = 0
    L = len(posAnswers)
    
    for guessed_code in posGuesses:
        distinctOutputs = []
        countOfOutputs = []
        locator += 1
        
        for checked_code in posAnswers:
            output = outputGenerator(guessed_code, checked_code, color_list)
            
            if output in distinctOutputs:
                countOfOutputs[distinctOutputs.index(output)] += 1
            else: distinctOutputs.append(output), countOfOutputs.append(1)
        
        ourSum = sum(countOfOutputs) #this is also just the length of posAnswers
        
        totalEntropy = 0
        for i in countOfOutputs:
            entropy = (i/ourSum)*math.log((ourSum/i), 2)
            totalEntropy += entropy
        
        if printYN == 1:
            print('Code No. ', locator, ' was ', guessed_code, ' Entropy: ', maxExpEntropy)
    
        '''Figure out if this is a better code than previous best'''
        if totalEntropy > maxExpEntropy:
            maxExpEntropy = totalEntropy
            bestCode = guessed_code
        if (totalEntropy == maxExpEntropy) and (bestCode not in posAnswers) and (guessed_code in posAnswers):
            maxExpEntropy = totalEntropy
            bestCode = guessed_code 

            
    return bestCode, maxExpEntropy


'Try to minimize the maximum possible words remaining after this guess'
def MiniMax(posGuesses, posAnswers, color_list, printYN):
    minimizeMe = 1000000000000
    bestCountOfOutputs = [0, 1000000000000]
    bestCode = ''
    locator = 0
    L = len(posAnswers)
    
    for guessed_code in posGuesses:
        distinctOutputs = []
        countOfOutputs = []
        locator += 1
        
        for checked_code in posAnswers:
            output = outputGenerator(guessed_code, checked_code, color_list)
            
            if output in distinctOutputs:
                countOfOutputs[distinctOutputs.index(output)] += 1
            else: distinctOutputs.append(output), countOfOutputs.append(1)        
        
        if printYN == 1:
            print('Code No. ', locator, ' was ', guessed_code, ' countOfOutputs: ', countOfOutputs)


        ###MiniMax
        maxNumberOfRemainingCodes = max(countOfOutputs)
        bestCountOfOutputsSorted = sorted(bestCountOfOutputs)
        countOfOutputsSorted = sorted(countOfOutputs)
       
        if (countOfOutputsSorted == bestCountOfOutputsSorted) and (bestCode not in posAnswers) and (guessed_code in posAnswers):
            minimizeMe = maxNumberOfRemainingCodes
            bestCountOfOutputs = countOfOutputs
            bestCode = guessed_code
        else:
            'If the worst case scenarios are equal, look at the 2nd worse scenarios, 3rd case...'
            maxDepthCompare = min(len(bestCountOfOutputs), len(countOfOutputs))

            for i in range(1, maxDepthCompare):
                'sorted(countOfOutputs)[-i] is iTh largest value in a list'
                if countOfOutputsSorted[-i] < bestCountOfOutputsSorted[-i]:
                    'print("Old best: ", sorted(bestCountOfOutputs), "  New best: ", sorted(countOfOutputs))'
                    minimizeMe = maxNumberOfRemainingCodes
                    bestCountOfOutputs = countOfOutputs
                    bestCode = guessed_code
                    break
                elif  countOfOutputsSorted[-i] > bestCountOfOutputsSorted[-i]:
                    break
        ###

    return bestCode, minimizeMe






'''Algorithm testing and stat summries'''


##All the real algorithms rely on the same data, can combine all 3 so only have to do comparisons once
##Use this for autobestFirstGuess() in mastermindTesting. Greatly reduces computation time
def comboAlgorithm(posGuesses, posAnswers, color_list, printYN):
    maxParts = 0
    bestCodeParts = ''
    
    bestElimFactor = 1
    bestCodeElim = ''
    
    maxExpEntropy = 0
    bestCodeEnt = ''
    
    minimizeMe = 1000000000000
    bestCodeMiniMax = ''
    bestCountOfOutputs = [0, 1000000000000]
    
    locator = 0
    L = len(posAnswers)
    
    
    for guessed_code in posGuesses:
        distinctOutputs = []
        countOfOutputs = []
        locator += 1
        
        for checked_code in posAnswers:
            output = outputGenerator(guessed_code, checked_code, color_list)
            
            if output in distinctOutputs:
                countOfOutputs[distinctOutputs.index(output)] += 1
            else: distinctOutputs.append(output), countOfOutputs.append(1)
        
        ourSum = sum(countOfOutputs) #this is also just the length of posAnswers
        
        ###PARTS
        
        partitions = len(distinctOutputs)
        
        if partitions > maxParts:
            maxParts = partitions
            bestCodeParts = guessed_code
        if (partitions == maxParts) and (bestCodeParts not in posAnswers) and (guessed_code in posAnswers):
            maxParts = partitions
            bestCodeParts = guessed_code
        
        
        ###
        
        ###ELIM
        elimFactor = (sum(i*i for i in countOfOutputs)/(ourSum*ourSum))
        
        if elimFactor < bestElimFactor:
            bestElimFactor = elimFactor
            bestCodeElim = guessed_code
        if (elimFactor == bestElimFactor) and (bestCodeElim not in posAnswers) and (guessed_code in posAnswers):
            bestElimFactor = elimFactor
            bestCodeElim = guessed_code
        ###
        
        
        ###ENTROPY
        totalEntropy = 0
        for i in countOfOutputs:
            entropy = (i/ourSum)*math.log((ourSum/i), 2)
            totalEntropy += entropy
            
        if totalEntropy > maxExpEntropy:
            maxExpEntropy = totalEntropy
            bestCodeEnt = guessed_code
        if (totalEntropy == maxExpEntropy) and (bestCodeEnt not in posAnswers) and (guessed_code in posAnswers):
            maxExpEntropy = totalEntropy
            bestCodeEnt = guessed_code 
        ###
        
        
        ###MiniMax
        maxNumberOfRemainingCodes = max(countOfOutputs)
        bestCountOfOutputsSorted = sorted(bestCountOfOutputs)
        countOfOutputsSorted = sorted(countOfOutputs)
       
        if (countOfOutputsSorted == bestCountOfOutputsSorted) and (bestCodeMiniMax not in posAnswers) and (guessed_code in posAnswers):
            minimizeMe = maxNumberOfRemainingCodes
            bestCountOfOutputs = countOfOutputs
            bestCodeMiniMax = guessed_code
        else:
            'If the worst case scenarios are equal, look at the 2nd worse scenarios, 3rd case...'
            maxDepthCompare = min(len(bestCountOfOutputs), len(countOfOutputs))

            for i in range(1, maxDepthCompare):
                'sorted(countOfOutputs)[-i] is iTh largest value in a list'
                if countOfOutputsSorted[-i] < bestCountOfOutputsSorted[-i]:
                    'print("Old best: ", sorted(bestCountOfOutputs), "  New best: ", sorted(countOfOutputs))'
                    minimizeMe = maxNumberOfRemainingCodes
                    bestCountOfOutputs = countOfOutputs
                    bestCodeMiniMax = guessed_code
                    break
                elif  countOfOutputsSorted[-i] > bestCountOfOutputsSorted[-i]:
                    break
        ###
        
        
        if printYN == 1:
            print('Code No. ', locator, ' was ', guessed_code, ' Partitions: ', partitions, 
                  ' ElimFactor: ', elimFactor,' Entropy: ', maxExpEntropy, ' MiniMax: ', minimizeMe)
            
            
    wholeCell = [[bestCodeParts, maxParts], [bestCodeElim, bestElimFactor], [bestCodeEnt, maxExpEntropy], [bestCodeMiniMax, minimizeMe]]
    
    return wholeCell






#Gives the quality of a guess by giving Partitions, ElimFactor, Entropy, MiniMax extra stuff.
#Can be called runprocedure() in mastermindTesting
def giveGuessDist():
    
    codeLength = getGameCodeLength()
    numColors = getNumColors()
    codeLists, color_list = genCodeAndColorList(codeLength, numColors)
    
    posAnswers = codeLists
    posGuesses = codeLists
    
    guessed_code = getGuess(posGuesses)
    
    
    distinctOutputs = []
    countOfOutputs = []
    
    for checked_code in posAnswers:
        output = outputGenerator(guessed_code, checked_code, color_list)
        
        if output in distinctOutputs:
            countOfOutputs[distinctOutputs.index(output)] += 1
        else: distinctOutputs.append(output), countOfOutputs.append(1)
    
    #res = list(map(''.join, distinctOutputs))
    res = list(distinctOutputs)
    print(res, '\n')
    print(countOfOutputs, '\n')
    
    
    partitions = len(distinctOutputs)
    
    ourSum = sum(countOfOutputs) #this is also just the length of posAnswers
    totalEntropy = 0
    for i in countOfOutputs:
        entropy = (i/ourSum)*math.log((ourSum/i), 2)
        totalEntropy += entropy
    
    elimFactor = (sum(i*i for i in countOfOutputs)/(ourSum*ourSum))
    
    miniMax = max(countOfOutputs)
    
    
    print('Word was: ', guessed_code)
    print('Partitions are ', partitions)
    print('Elim Factor is ', elimFactor)
    print('Entropy is ', totalEntropy)
    print('MiniMax worst case scenario: ', miniMax)
    
    
    return

