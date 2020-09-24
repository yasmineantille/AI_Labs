import random
import numpy as np
import game
import sys

# Author:				chrn (original by nneonneo)
# Date:				11.11.2016
# Description:			The logic of the AI to beat the game.

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3

def find_best_move(board):
    bestmove = -1    
	
	# TODO:
	# Build a heuristic agent on your own that is much better than the random agent.
	# Your own agent don't have to beat the game.
    
    heuristicscore = 0;
    
    boardperformance = [
            [16, 15, 14, 13],
            [9, 10, 11, 12],
            [8, 7, 6, 5],
            [1, 2, 3, 4]
        ]
    
    # move RIGHT
    tempboard = game.merge_right(board)
    if board_equals(board, tempboard) == False: 
        heuristicscore_right = np.sum(tempboard * boardperformance)
        heuristicscore_right += find_neighboring_tiles(tempboard)
        heuristicscore_right += count_free_tiles(tempboard)
        #print('Heuristic score right: %f' % heuristicscore)
        if heuristicscore_right > heuristicscore:
            heuristicscore = heuristicscore_right
            bestmove = RIGHT;
    
    # move LEFT
    tempboard = game.merge_left(board)
    if board_equals(board, tempboard) == False:
        heuristicscore_left = np.sum(tempboard * boardperformance)
        heuristicscore_left += find_neighboring_tiles(tempboard)
        heuristicscore_left += count_free_tiles(tempboard)
        #print('Heuristic score left: %f' % heuristicscore)
        if heuristicscore_left > heuristicscore:
            heuristicscore = heuristicscore_left
            bestmove = LEFT;
    
    # move UP
    tempboard = game.merge_up(board)
    if board_equals(board, tempboard) == False:
        heuristicscore_up = np.sum(tempboard * boardperformance)
        heuristicscore_up += find_neighboring_tiles(tempboard)
        heuristicscore_up += count_free_tiles(tempboard)
        #print('Heuristic score up: %f' % heuristicscore)
        if heuristicscore_up > heuristicscore:
            heuristicscore = heuristicscore_up
            bestmove = UP;
        
    # move DOWN
    tempboard = game.merge_down(board)
    if board_equals(board, tempboard) == False:
        heuristicscore_down = np.sum(tempboard * boardperformance)
        heuristicscore_down += find_neighboring_tiles(tempboard)
        heuristicscore_down += count_free_tiles(tempboard)
        #print('Heuristic score down: %f' % heuristicscore)  
        if heuristicscore_down > heuristicscore:
            heuristicscore = heuristicscore_down
            bestmove = DOWN;
     
    
    
    return bestmove    

def find_neighboring_tiles(board):
    neighborscore = 0
    
    for i in range(3):
        for j in range(2):
            if i < 3:
                if board[i][j] == board[i][j+1]:
                    neighborscore = neighborscore + (board[i][j] * board[i][j+1])
                if board[i][j] == board[i+1][j]:
                    neighborscore = neighborscore + (board[i][j] * board[i+1][j])
            else:
                if board[i][j] == board[i+1][j]:
                    neighborscore = neighborscore + (board[i][j] * board[i][j+1])
    
    
    return neighborscore

def count_free_tiles(board):
    count = 0
    
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                count+=1
    
    return count*128

def find_best_move_random_agent():
    return random.choice([UP,DOWN,LEFT,RIGHT])
    
def execute_move(move, board):
    """
    move and return the grid without a new random tile 
	It won't affect the state of the game in the browser.
    """

    if move == UP:
        return game.merge_up(board)
    elif move == DOWN:
        return game.merge_down(board)
    elif move == LEFT:
        return game.merge_left(board)
    elif move == RIGHT:
        return game.merge_right(board)
    else:
        sys.exit("No valid move")
		
def board_equals(board, newboard):
    """
    Check if two boards are equal
    """
    return  (newboard == board).all()  