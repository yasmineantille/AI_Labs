# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 10:42:31 2020

@author: antilyas, bertaben
"""

import numpy as np

def get_score(board, nextboard, config):
    """
    Calculates the overall score for the specific move
    
    Returns: 
        score (int): overall score achieved with heuristics
    """
    score = 0
    if board_equals(board, nextboard) == False: 
        if "b" in config:
            score += check_board_performance_border(nextboard)*10
        if "s" in config:
            score += check_board_performance_snake(nextboard)*100
        if "l" in config:
            score += check_largest_number(nextboard)*25
        if "t" in config:
            score += find_neighboring_tiles(nextboard)*10
        if "z" in config:
            score += check_amount_of_zeros(nextboard)*25
        if "m" in config:
            score += check_amount_of_merges(board, nextboard)*40
            
    return score

def find_neighboring_tiles(board):
    neighborscore = 0
    
    for i in range(4):
        for j in range(3):
            if i < 3:
                if board[i][j] == board[i][j+1]:
                    neighborscore += (board[i][j] * board[i][j+1])
                if board[i][j] == board[i+1][j]:
                    neighborscore += (board[i][j] * board[i+1][j])
            else:
                if board[i][j] == board[i][j+1]:
                    neighborscore += (board[i][j] * board[i][j+1])
    
    
    return neighborscore

# config: t
def check_matching_tiles(nextboard):
    """
    Checks all cells of the game board for matching numbers next to each other 
    or under each other
    
    Parameters: 
        nextboard (board): new board to check for matching tiles
    
    Returns:
        score (int): score for amount of matching tiles
    """
    
    score = 0
    for row in nextboard: 
        score += check_next_to(row)
    # send columns as rows to check for matching numbers
    i = 0
    while i < 4:
        score += check_next_to(nextboard[:,i])
        i += 1
    return score

def check_next_to(row): 
    """
    Checks if 2 values next to each other in a row are equal

    Parameters:
        row: array of 4 values

    Returns:
        matches (int): returns amount of matches found (max 2 matches per row)

    """
    row = row[row != 0]
    prevelement = -1
    matches = 0 
    
    i = 0
    while i < len(row):
        val = row[i]
        if val == prevelement:
            matches += 1
            i += 1
        if (i < len(row)): 
            prevelement = row[i]
        i += 1
    
    return matches

# config z
def check_amount_of_zeros(board): 
    """
    Checks for zeroes in board

    Parameters:
        board: simulated game board after move

    Returns:
        zeros (int): amount of zeroes found on board

    """
    zeros = np.count_nonzero(board==0)
    return zeros

# config l
def check_largest_number(board):
    return np.max(board)

# config m
def check_amount_of_merges(board, nextboard):
    """
    Checks how many merges are possible with the chosen move

    Parameters: 
        board : the original game board before moving
    nextboard : the simulated board after using a move

    Returns:
        merges (int): amount of possible merges

    """
    merges = 0
    if (check_amount_of_zeros(nextboard) > check_amount_of_zeros(board)):
        merges = check_amount_of_zeros(nextboard) - check_amount_of_zeros(board)
    return merges

# config s
def check_board_performance_snake(board):
    """
    Checks score of evaluated board performance. 
    Values are scored as they should appear in the game snake
    so row for row the values get lower graded
    
    Parameters: 
        board: simulated game board
        
    Returns: 
        score (int): calculated performance
    """
    score = 0    
    # boardperformance as snake 
    boardperformance = [
            [1024, 512, 256, 128],
            [8, 16, 32, 64],
            [4, 2, 1, 0],
            [0, 0, 0, 0]
        ]
    
    # boardperformance = [
    #         [1024, 512, 256, 128],
    #         [8, 16, 32, 64],
    #         [4, 2, 2, 2],
    #         [2, 2, 2, 2]
    #     ]
        
    score += np.sum(board * boardperformance)
    return score

# config b
def check_board_performance_border(board):
    """
    Checks score of evaluated board performance. 
    Higher values in corners give higher performance value
    
    Parameters: 
        board: simulated game board
        
    Returns: 
        score (int): calculated performance
    """
    score = 0
    boardperformance = [
            [20, 10, 10, 20],
            [10, 5, 5, 10],
            [10, 5, 5, 10],
            [20, 10, 10, 20]
        ]

    score += np.sum(board * boardperformance)
    return score

def board_equals(board, newboard):
    """
    Check if two boards are equal
    """
    return  (newboard == board).all()  