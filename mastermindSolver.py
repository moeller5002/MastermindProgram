'''Single function to help solve a game of Mastermind. Can be called in runProcedure() in mastermindmastermindMainFile'''
import random
import string
import math
from mastermindCodeManager import *
from mastermindMainFunctions import *


def mastermindComputerPlus():
    print('Lets crack the Mastermind!')
    
    #Gets the number of letters we play with and imports corresponding code lists
    codeLength = getGameCodeLength()
    numColors = getNumColors()
    codeLists, color_list = genCodeAndColorList(codeLength, numColors)
    
    posAnswers = codeLists
    posGuesses = codeLists
    
    algorithmCode = getAlgorithmCode()
    

    num_guesses = 0
    
    for i in range(10):
    
        '''-----------Suggested Guess Stuff ----------'''
        
        suggested_code = suggestedCode(posGuesses, posAnswers, color_list, algorithmCode, num_guesses)
        print('The recommended code is ', suggested_code, '\n')   
        
        '''----------- End Suggested Guess Stuff -----------'''
    
        '''Gets a valid guess'''
        print('Guess No. ', num_guesses + 1)
        guess_code = getGuess(posGuesses)     
        num_guesses += 1
    
        '''Gets the response'''
        given_output = getOutput(posGuesses)
    
        posAnswers = filter_posAnswers(guess_code, given_output, posAnswers, color_list)
    
        print(posAnswers)
        print('There are now ', len(posAnswers), ' codes remaining')        
        
        if len(posAnswers) in [0, 1]:
            return


