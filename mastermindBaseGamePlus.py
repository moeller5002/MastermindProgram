'''Single function to play a game of Mastermind. Can be called in runProcedure() in mastermindMainFile'''
import random
import string
import math
from mastermindCodeManager import *
from mastermindMainFunctions import *



def letsPlayGame():
    print('Lets play some Mastermind!')
    
    #Gets the codeLength and number of colors and generates corresponding codeLists
    codeLength = getGameCodeLength()
    numColors = getNumColors()
    codeLists, color_list = genCodeAndColorList(codeLength, numColors)
    
    posAnswers = codeLists
    posGuesses = codeLists

    getHelp = getHelpYN()
    
    if getHelp == 1:
        algorithmCode = getAlgorithmCode()
    
    
    print('Playing with ', codeLength, 'pegs. With ', color_list, '. Suggestions: ', getHelp)
    
    #Generates Secret Word
    answer_code = random.choice(posAnswers).lower()
    
    print('The secret word is: ', answer_code)
    print('There are', len(posAnswers)-1, 'words to eliminate!')
    
    
    #Game actually starts
    num_guesses = 0
    
    for i in range(10):
        
        '''-----------Suggested Guess Stuff ----------'''
        ##Needs work
        if getHelp == 1:
            suggested_code = suggestedCode(posGuesses, posAnswers, color_list, algorithmCode, num_guesses)
            print('The recommended code is ', suggested_code)   
        
        '''----------- End Suggested Guess Stuff -----------'''
        
        #Gets a valid guess
        print('Guess No. ', num_guesses + 1)
        guess_code = getGuess(posGuesses)              
        num_guesses += 1
    
        #Now we have a valid guess.   
        if guess_code == answer_code: #If its correct: Game is done; Break out.
            print ('\n\n', 'It took you ', num_guesses, 'guesses', '\n',
                   'You got the code!!! -------------------------------------------------\n\n\n')
            return
        
        else: #If not correct: Print the output and optionally provide help
            output = outputGenerator(guess_code, answer_code, color_list)
            print('Output is:', output, '\n\n')
    
            # Remove codes that are no longer possible
            posAnswers = filter_posAnswers(guess_code, output, posAnswers, color_list)
            
            if getHelp == 1:
                print(posAnswers)
                print('There are now ', len(posAnswers), ' codes remaining')        
              
    
    if guess_code != answer_code and num_guesses == 10:
        print('\n', 'The correct code was ', answer_code, '.  Better luck next time!', '\n\n\n')
        
    return
