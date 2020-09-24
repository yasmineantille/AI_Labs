#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author:      chrn (original by nneonneo)
# Date:        11.11.2016, updated by scik 30.08.2019
# Copyright:   https://github.com/nneonneo/2048-ai
# Description: Helps the user achieve a high score in a real game of 2048 by using a move searcher.
#              This Script initialize the AI and controls the game flow.


#from __future__ import print_function

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import threading
import os
import time
from sys import exit
#import heuristicai as ai #for task 4
import searchai as ai #for task 5

chrome_driver = os.getcwd() +"\\chromedriver.exe"
start_port = 9222

def print_board(m):
    for row in m:
        for c in row:
            print('%8d' % c, end=' ')
        print()

def _to_val(c):
    if c == 0: return 0
    return c

def to_val(m):
    return [[_to_val(c) for c in row] for row in m]

def _to_score(c):
    if c <= 1:
        return 0
    return (c-1) * (2**c)

def to_score(m):
    return [[_to_score(c) for c in row] for row in m]

def find_best_move(board, config):
    return ai.find_best_move(board, config)

def movename(move):
    return ['up', 'down', 'left', 'right'][move]

def play_game(runId, gamectrl, results, driver, config):
    moveno = 0
    start = time.time()
    while 1:
        state = gamectrl.get_status()
        if state == 'ended':
            break
        elif state == 'won':
            time.sleep(1)
            gamectrl.continue_game()

        moveno += 1
        board = gamectrl.get_board()
        move = find_best_move(board, config)
        if move < 0:
            break
        #print("#%d-%s %010.6f: Score %d, Move %d: %s" % (runId, config, time.time() - start, gamectrl.get_score(), moveno, movename(move)))
        gamectrl.execute_move(move)

    score = gamectrl.get_score()
    board = gamectrl.get_board()
    maxval = max(max(row) for row in to_val(board))
    result = "#%d-%s Game over. Final score %d; highest tile %d." % (runId, config, score, maxval)
    print(result)
    results.append("%s;%d;%d;%d;%d;" % (config, runId, score, maxval,moveno))
    driver.save_screenshot(".\\screenshots\\%d-%f.png" % (gamectrl.get_score(), time.time()))
    driver.quit()

def parse_args(argv):
    import argparse

    parser = argparse.ArgumentParser(description="Use the AI to play 2048 via browser control")
    parser.add_argument('-p', '--port', help="Port number to control on (default: 32000 for Firefox, 9222 for Chrome)", type=int)
    parser.add_argument('-b', '--browser', help="Browser you're using. Only Firefox with the Remote Control extension, and Chrome with remote debugging (default), are supported right now.", default='chrome', choices=('firefox', 'chrome'))
    parser.add_argument('-k', '--ctrlmode', help="Control mode to use. If the browser control doesn't seem to work, try changing this.", default='hybrid', choices=('keyboard', 'fast', 'hybrid'))
    parser.add_argument('-i', '--instances', help="How many instances should run simultaneous.", default=1, type=int)
    parser.add_argument('-e', '--headless', help="Run instance in headless mode", default=False, type=bool)

    return parser.parse_args(argv)

def start_chrome(port, headless):
    """
    Starts a new chrome session either headless or windowed
    
    Returns: 
        driver: Webdriver of the chrome instance
    """
    chrome_options = Options()
    
    if headless:
        chrome_options.add_argument("--headless")
        
    chrome_options.add_argument("--remote-debugging-port=%d" % port)
    chrome_options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=chrome_options, executable_path=chrome_driver, service_args=["--verbose", "--log-path=.\qc1.log"])
    
    driver.get("file:\\\\\\" + os.getcwd() + "\\2048_game\\index.html")
    
    time.sleep(0.5)
    
    return driver;

def start_game_session(args, i, results, config):
    
    if args.headless is None:
        args.headless = False
    
    if args.browser == 'firefox':
        from ffctrl import FirefoxRemoteControl
        if args.port is None:
            args.port = 32000
        ctrl = FirefoxRemoteControl(args.port)
    elif args.browser == 'chrome':
        from chromectrl import ChromeDebuggerControl
        driver = start_chrome(i, args.headless)
        if args.port is None:
            args.port = i
        ctrl = ChromeDebuggerControl(i)

    if args.ctrlmode == 'keyboard':
        from gamectrl import Keyboard2048Control
        gamectrl = Keyboard2048Control(ctrl)
    elif args.ctrlmode == 'fast':
        from gamectrl import Fast2048Control
        gamectrl = Fast2048Control(ctrl)
    elif args.ctrlmode == 'hybrid':
        from gamectrl import Hybrid2048Control
        gamectrl = Hybrid2048Control(ctrl)
        
    if args.instances is None:
        args.instance = 1

    if gamectrl.get_status() == 'ended':
        gamectrl.restart_game()

    play_game(i, gamectrl, results, driver, config)

def main(argv):
    args = parse_args(argv)
    
    configurations = ["s"] # ["b", "s", "l", "t", "m", "z", "bsltmz"]
    
    for config in configurations:
        thread_list = []
        results = []
        
        for i in range(start_port,start_port+args.instances):
            thread = threading.Thread(target=start_game_session, args=(args, i, results, config), name="Thread-%d-%s" % (i, config))
            thread_list.append(thread)
            
        for thread in thread_list:
            thread.start()
            
        for thread in thread_list:
            thread.join()
            
        print("==================================")
        f = open("results-%s.txt" % config, "a")
        for result in results:
            f.write("%s\n" % result)
        f.close()

if __name__ == '__main__':
    import sys
    exit(main(sys.argv[1:]))
