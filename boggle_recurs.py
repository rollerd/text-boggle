#Recursive boggle checker 6/16/13

import random
from copy import deepcopy

ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
            'A', 'A', 'E', 'I', 'I', 'O', 'O', 'U', 'U', 'M', 'N', 'T', 'S', 'G', 'P']

LETTERPOINTS = {'A':1,'B':5,'C':4,'D':3,'E':1,'F':5,'G':5,'H':2,'I':1,'J':7,'K':5,'L':2,'M':4,'N':1,'O':1,'P':4,'Q':10,'R':2,'S':1,'T':1,
                'U':4,'V':6,'W':5,'X':10,'Y':5,'Z':10}


'''BASIC GAME FUNCTIONS'''
def create_board(x, y):
    board = []
    for row in range(x):
        new_row = []
        for col in range(y):
            new_row.append(random.choice(ALPHABET))
        board.append(new_row)
    return board


def print_board(board):
    for row in board:
        for letter in row:
            print letter,
        print
        
        
def save_board(board):
    file = open('saved_board.txt', 'w')
    for row in board:
        for letter in row:
            file.write(letter)
        file.write('\n')
    file.close()


def get_word_list():
    file = open('words.txt', 'r')
    word_list = file.readlines()
    file.close()
    return word_list

       
def calculate_points(word):
    points = 0
    for letter in word:
        points += LETTERPOINTS[letter]
    return points


def end_game(score):
    print 'GAME OVER'
    print 'Your final score is: %s' % score
    return 0


'''GAME LOGIC'''
#Not sure if this is 100% or not... There is no 'return 0' anywhere. Seems to work though
def find_position(board, word, pos = 0):          
    for x in range(len(board)):
        for y in range(len(board[0])):
            letter_position = (x, y)
            if len(word) == 0:  #If we get to the end of the word and there are no letters left, return 1 for success
                return 1
            target = word[0]
            if board[x][y] == target and letter_position in adjacent_letters(pos, board):   #If the target is found and is adjacent to the last letter found...
#                 print letter_position,                #Uncomment this line to help trace path
                board[letter_position[0]][letter_position[1]] = '.'     #Remove the found letter from the board and replace with a '.'
                result = find_position(board, word[1:], letter_position)    #Added 'result =' so that I wouldn't get a lot of 0's returned as recursion stepped back up the chain. 
                if result:
                    return 1
                else:
                    board = board_reset()   #Refreshes the board to the beginning if word has not been found. Necessary or else the board with removed letters gets passed down the chain.


def board_reset():
    board = deepcopy(BOARD2)
    return board

#Finds all positions around the target coord and then returns them in a list, minus the target itself. To start, all positions on the board are available
def adjacent_letters(orig_pos, board):
    adjacent_positions = []
    if orig_pos == 0:
        for x in range(len(board)):
            for y in range(len(board[0])):
                adjacent_positions.append((x, y))
        return adjacent_positions
    
    for x in range(-1, 2):
        for y in range(-1, 2):
            coord = (orig_pos[0] + x, orig_pos[1] + y)
            adjacent_positions.append(coord)
    return adjacent_positions

   
'''GAME LOOP'''
def get_input():
    used_words = []
    score = 0
    word_list = get_word_list()
    global BOARD2
    board_size = raw_input("Please enter a size for the board(X x X): ")
    x, y = int(board_size), int(board_size)
    board = create_board(x, y)
#    save_board(board)    #Uncomment to save board to text file for letter frequency analysis
    BOARD2 = deepcopy(board)
    while True:
        board = board_reset()
        print_board(board)
        input1 = (raw_input('Enter the word to find (1 to end): ')).upper()
        result = find_position(board, input1)
        if input1 == '1':
            end_game(score)
            break
        if result and (input1 + '\n') in word_list and input1 not in used_words:
            print 'WORD FOUND'
            points = calculate_points(input1)
            score += points
            print 'Word score: %s' % points
            print 'Total Score: %s \n' % score
            used_words.append(input1)
        elif result and input1 in used_words:
            print 'WORD HAS ALREADY BEEN USED \n'
        else:
            print 'WORD NOT FOUND \n'
     
get_input()

#This is just a test GIT edit
