#this file will store the logic for playing the game of cluedo
#this will include the state of the board, cards, etc
#how to actually make decisions will be up to other programs
#written by Henry Chadban from 07/12/2022

import pandas #for reading csv files
import numpy as np #for storing the state of the board

#constants
tiles = ['wall','walk','kitchen','dining','lounge','hall','study','library','billards','conservatory','ballroom','start_mustard',
        'start_scarlet','start_plum','start_peacock','start_rev_green','start_white','secret_study','secret_lounge','secret_consevatory','secret_kitchen','centre']


#cludeo is played on a 25 tile wide,25 tile tall board
class Board():
    #create the board on which the game will be played
    def __init__(self,board_path):
        board_raw = pandas.read_csv(board_path,header=None) #extract raw data from the csv file
        self.board = self.board_extract(board_raw) #extract the tiles that make up the board as a numpy array
    
    #convert the raw data about the board from a csv file to a numpy array
    def board_extract(self,board_raw):
        board_size = board_raw.shape #get the dimensions of the board
        board_values = np.zeros(board_size)#the board represented as a numpy array, the numbers represent what type of tile occupies each grid-square
        for i,tile_name in enumerate(tiles): #go through all the types of tiles
            truth = board_raw==tile_name #find the tiles which are the current type of tile
            board_values = board_values + truth*i #set the tile number accordingly
        
        board_values = np.array(board_values) #convert back to a numpy array
        return board_values #provide the numeric representation of the boards tiles
            

            
