import random
import game
import heuristics
import sys

# Author:      chrn (original by nneonneo)
# Date:        11.11.2016
# Copyright:   Algorithm from https://github.com/nneonneo/2048-ai
# Description: The logic to beat the game. Based on expectimax algorithm.

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3

def find_best_move(board, config):
    """
    find the best move for the next turn.
    """
    bestmove = -1
    UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
    move_args = [UP,DOWN,LEFT,RIGHT]
    
    result = [score_toplevel_move(i, board, 3, True, config) for i in range(len(move_args))]
    bestmove = result.index(max(result))
    
    randomchoice = [bestmove]
    for i in range(len(move_args)):
        if bestmove == i:
            continue
        if result[i] == max(result):
            randomchoice.append(i)
            
    bestmove = random.choice(randomchoice)            

    #for m in move_args:
    #    print("move: %d score: %.4f" % (m, result[m]))
    #print("move: %d score: %.4f" % (bestmove, result[bestmove]))
    return bestmove
    
def score_toplevel_move(move, board, depth, maxNode, config):
    """
    Entry Point to score the first move.
    """    
    newboard = execute_move(move, board)
    
    depth-=1
    
    if board_equals(board,newboard):
        return -10000
	# TODO:
	# Implement the Expectimax Algorithm.
	# 1.) Start the recursion until it reach a certain depth
	# 2.) When you don't reach the last depth, get all possible board states and 
	#		calculate their scores dependence of the probability this will occur. (recursively)
	# 3.) When you reach the leaf calculate the board score with your heuristic.
    elif depth <= 0:
        score = heuristics.get_score(board, newboard, config)
        return score
    elif maxNode:
        highestscore = 0
        for i in range(4):
            score = score_toplevel_move(i, newboard, depth, False, config)
            if score > highestscore:
                highestscore = score
                
        return highestscore
    # no min node because 1 player
    else: #chance node
        score = 0
        boardcount = 0
        for row in range(4):
            for col in range(4):
                if newboard[row][col] == 0:
                    newboard[row][col] = 2
                    for i in range(4):
                        score += score_toplevel_move(i, newboard, depth, True, config) * 0.9 * heuristics.check_amount_of_zeros(newboard)
                    newboard[row][col] = 4
                    for i in range(4):
                        score += score_toplevel_move(i, newboard, depth, True, config) * 0.1 * heuristics.check_amount_of_zeros(newboard)
                    newboard[row][col] = 0
                    boardcount+=2
                    
                    # open tiles in calculation
                    
        return score


def execute_move(move, board):
    """
    move and return the grid without a new random tile 
	It won't affect the state of the game in the browser.
    """

    UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3

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
