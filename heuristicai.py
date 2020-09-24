import random
import game
import sys
import heuristics

# Author:				chrn (original by nneonneo)
# Date:				11.11.2016
# Description:			The logic of the AI to beat the game.

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3

def find_best_move(board, config):
    bestmove = -1 
	# TODO:
	# Build a heuristic agent on your own that is much better than the random agent.
	# Your own agent don't have to beat the game.
    bestmove = find_best_move_personal_agent(board, config)
    return bestmove


def find_best_move_personal_agent(board, config):
    bestmove = -1
    bestscore = -1
    
    # Try move UP
    upboard = game.merge_up(board)
    upscore = heuristics.get_score(board, upboard, config)
    if upscore > bestscore:
        bestscore = upscore
        bestmove = UP
    
    # Try move DOWN
    downboard = game.merge_down(board)
    downscore = heuristics.get_score(board, downboard, config)
    if downscore > bestscore:
        bestscore = downscore
        bestmove = DOWN
       
    # Try move RIGHT
    rightboard = game.merge_right(board)
    rightscore = heuristics.get_score(board, rightboard, config)
    if rightscore > bestscore:
        bestscore = rightscore
        bestmove = RIGHT
    
    # Try move LEFT
    leftboard = game.merge_down(board)
    leftscore = heuristics.get_score(board, leftboard, config)
    if leftscore > bestscore:
        bestscore = leftscore
        bestmove = LEFT
        
    # if moves achieve same score randomly choose one
    result = [upscore, downscore, leftscore, rightscore]
    randomchoice = [bestmove]
    for i in range(4):
        if bestmove == i:
            continue
        if result[i] == max(result):
            randomchoice.append(i)
            
    bestmove = random.choice(randomchoice)  
                    
    return bestmove

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