#this file will store the logic for playing the game of cluedo
#this will include the state of the board, cards, etc
#how to actually make decisions will be up to other programs
#written by Henry Chadban from 07/12/2022

import pandas #for reading csv files
import numpy as np #for storing the state of the board
import pygame
import pygame.locals
import sys
import os

#constants
tiles = ['wall','walk','kitchen','dining_room','lounge','hall','study','library','billards','conservatory','ballroom','start_mustard',
'start_scarlet','start_plum','start_peacock','start_rev_green','start_white','secret_study','secret_lounge','secret_conservatory','secret_kitchen',
'centre']

#load the static sprites we are using in this game
class StaticSprites():
    def __init__(self):
        self.walk = pygame.image.load("cluedo_images/walk.png")
        self.centre = pygame.image.load("cluedo_images/centre.png")
        self.wall = pygame.image.load("cluedo_images/wall.png")
        self.space = pygame.image.load("cluedo_images/space.png")
        self.secret = pygame.image.load("cluedo_images/secret.png")

#load the dynamic sprites we are using in this game
class DynamicSprites():
    def __init__(self):
        self.mustard = pygame.image.load("cluedo_images/mustard.png")
        self.scarlet = pygame.image.load("cluedo_images/scarlet.png")
        self.peacock = pygame.image.load("cluedo_images/peacock.png")
        self.rev_green = pygame.image.load("cluedo_images/rev_green.png")
        self.plum = pygame.image.load("cluedo_images/plum.png")
        self.peacock = pygame.image.load("cluedo_images/peacock.png")


#cludeo is played on a 27 tile wide,25 tile tall board
class Board():
    #create the board on which the game will be played
    def __init__(self,board_path):
        board_raw = pandas.read_csv(board_path,header=None) #extract raw data from the csv file
        self.board_static,board_size = self.board_extract(board_raw) #extract the tiles that make up the board as a numpy array
        self.tile_width = 32 #constant, x size
        self.tile_height = 32 #constant, y size
        self.board_width = board_size[1]
        self.board_height = board_size[0]
        print('board width = ',self.board_width,' board_height = ',self.board_height)
        self.board_pixel_width = self.tile_width*self.board_width
        self.board_pixel_height = self.tile_height*self.board_height
        self.static_sprites = StaticSprites() #load the static sprites used in the game
        self.dynamic_sprites = DynamicSprites() #load the dynamic sprites used in the game
        self.render_board()
    
    #convert the raw data about the board from a csv file to a numpy array
    def board_extract(self,board_raw):
        board_size = board_raw.shape #get the dimensions of the board
        board_values = np.zeros(board_size)#the board represented as a numpy array, the numbers represent what type of tile occupies each grid-square
        for i,tile_name in enumerate(tiles): #go through all the types of tiles
            truth = board_raw==tile_name #find the tiles which are the current type of tile
            board_values = board_values + truth*i #set the tile number accordingly
        
        board_values = np.array(board_values) #convert back to a numpy array
        return board_values,board_size #provide the numeric representation of the boards tiles
            
    def render_board(self):
        self.render_static_tiles()

    def render_static_tiles(self):
        start_x = 0 #where does the board display start, x pixels
        start_y = 0 #where does the static section start, y pixels
        x = 0 #position of current tile in the board along the x-axis
        y = 0 #position of current tile in the board along the y-axis
        self.static_board_surface = pygame.Surface((self.board_pixel_width,self.board_pixel_height)) #create a surface of the correct size
        #self.static_board_surface.set_colourkey((0,0,0)) #background is black
        for row in self.board_static:
            x = 0 #reset x position each row
            for tile in row:
                x_position = x*self.tile_width
                y_position = y*self.tile_height
                tile_text = tiles[int(tile)] #get the text of the tile
                #select image based on what type of tile we are using
                if tile_text=='wall':
                    image = self.static_sprites.wall
                elif tile_text=='walk' or tile_text=='start_mustard' or tile_text=='start_scarlet' or tile_text=='start_plum' or tile_text=='start_peacock' or tile_text=='start_rev_green' or tile_text=='start_white':
                    image = self.static_sprites.walk
                elif tile_text=='centre':
                    image = self.static_sprites.centre
                elif tile_text=='secret_study' or tile_text=='secret_lounge' or tile_text=='secret_conservatory' or tile_text=='secret_kitchen':
                    image = self.static_sprites.secret
                else:
                    image = self.static_sprites.space
                #render the image in the correct position
                #rect = image.get_rect() #extract the rect object from the image
                #
                self.static_board_surface.blit(image,(x_position,y_position))
                x = x+1

            y = y+1 #moving down to the next row

    def print_position_attribute(x,y):
        pass

#controls the overall flow of the game logic
def GameMaster():
    def __init__(self,board_path='board.csv',tile_list=tiles):
       board_values,board_size =  self.extract_board_data(board_path,tiles)
        


    #extract info about the board
    def extract_board_data(board_path,tiles):
        board_raw = pandas.read_csv(board_path,header=None) #extract raw data from the csv file
        board_size = board_raw.shape #get the dimensions of the board
        board_values = np.zeros(board_size)#the board represented as a numpy array, the numbers represent what type of tile occupies each grid-square
        for i,tile_name in enumerate(tiles): #go through all the types of tiles
            truth = board_raw==tile_name #find the tiles which are the current type of tile
            board_values = board_values + truth*i #set the tile number accordingly

        board_values = np.array(board_values,dtype=int) #convert back to a numpy array of ints
        return board_values,board_size #provide the numeric representation of the boards tiles


        
def main():
    pygame.init()  # initialize pygame
    resized_flag = False
    clock = pygame.time.Clock() #create a clock to set the frame-rate
    screen = pygame.display.set_mode((864,832),pygame.RESIZABLE)
    pygame.mouse.set_visible(1)
    pygame.display.set_caption('Cluedo') #display the game title in the window
    board = Board("board.csv") #create the board
    print(board.board_static)
    while True:
        clock.tick(60)
        #bg = pygame.image.load("rock.jpeg")
        display = board.static_board_surface
        if resized_flag==False:
            screen.blit(display, (0, 0))
        elif resized_flag==True:
            screen.blit(pygame.transform.scale(display,resized),(0,0))
        x, y = pygame.mouse.get_pos() #get pixel position of mouse
        print("x = ",x," y = ",y) #display pixel position of mouse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                resized_flag = True
                resized = event.dict['size']
        pygame.display.update()

if __name__ == '__main__':
    main()