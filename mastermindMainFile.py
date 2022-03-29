'''Main place to run all the functions'''
import random
import string
import math
from mastermindCodeManager import *
from mastermindMainFunctions import *
from mastermindBaseGamePlus import *
from mastermindSolver import *


def runProcedure():
    choice = []
    validChoice = [1,2,3,4,0]
    
    while choice != 0:
        
        print('\n\n\n', 'Please choose what you would like to do...  ', '\n',
          '1: Play a game of Mastermind', '\n',
          '2: Solve a game of Mastermind (Cheat)','\n',
          '3: Test an algorithm','\n',
          '4: Check quality of a guess', '\n',
          '0: Exit to console')
        
        while (choice not in validChoice):
            try:
                choice = int(input('What would you like to do?  '))
            
            except ValueError:
                print('Invalid input')
                
        if choice == 1:
            letsPlayGame()
        elif choice == 2:
            mastermindComputerPlus()
        elif choice == 3:
            testAlgorithm()
        elif choice == 4:
            giveGuessDist()            
        elif choice == 0:
            return
        
        choice = []
        
        
runProcedure()






#Computes best first guess & its performance for each algorithm based on codeLength and numColors. An entire cell in the excel table    
def autobestFirstGuess():
    codeLength = getGameCodeLength()
    numColors = getNumColors()
    
    
    codeLists, color_list = genCodeAndColorList(codeLength, numColors)
    
    posAnswers = codeLists
    posGuesses = codeLists
    
    start_time = time.perf_counter()
    
    
    X = comboAlgorithm(posGuesses, posAnswers, color_list, 1)
    
    end_time = time.perf_counter()
    run_time = end_time - start_time
    
    print('\n', 'CodeLength: ', codeLength, ' NumColors: ', numColors)
    print('Best Guess According to... MaxParts, AverageElim, MaxEntropy', '\n', X, '\n')
    print('It took ', str(run_time/60), ' minutes to compute ', '\n')
    
    
    
    return X
    
#autobestFirstGuess()



