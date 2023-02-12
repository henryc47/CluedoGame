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
    def __init__(self,board_values,board_width,board_height,tile_size):
        self.board_values = board_values
        self.board_width = board_width
        self.board_height = board_height
        self.tile_size = tile_size
        self.board_pixel_width = self.tile_size*self.board_width
        self.board_pixel_height = self.tile_size*self.board_height
        self.static_sprites = StaticSprites() #load the static sprites used in the game
        self.dynamic_sprites = DynamicSprites() #load the dynamic sprites used in the game
        self.render_board()
    
            
    def render_board(self):
        self.render_static_tiles()

    def render_static_tiles(self):
        start_x = 0 #where does the board display start, x pixels
        start_y = 0 #where does the static section start, y pixels
        x = 0 #position of current tile in the board along the x-axis
        y = 0 #position of current tile in the board along the y-axis
        self.static_board_surface = pygame.Surface((self.board_pixel_width,self.board_pixel_height)) #create a surface of the correct size
        #self.static_board_surface.set_colourkey((0,0,0)) #background is black
        for row in self.board_values:
            x = 0 #reset x position each row
            for tile in row:
                x_position = x*self.tile_size
                y_position = y*self.tile_size
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
class GameMaster():
    def __init__(self,board_path='board.csv',tile_list=tiles):
        board_values,board_size =  self.extract_board_data(board_path,tiles)
        board_height = board_size[0] #height of the board in tiles
        board_width = board_size[1] #width of the board in tiles
        self.tile_size = 32 #number of pixels in a tile
        self.board_height_pixels = board_height*self.tile_size #height of the playing board in pixels
        self.board_width_pixels = board_height*self.tile_size #width of the playing board in pixels
        self.other_player_width_pixels = 258 #width of the left sidebar, where players and their cards are displayed
        self.self_player_width_pixels = 258 #width of the right sidebar, where your own cards and controls are displayed
        self.screen_default_width = self.board_width_pixels + self.other_player_width_pixels + self.self_player_width_pixels #total width, pixels,s of the screen
        self.screen_default_height = self.board_height_pixels #total height, pixels, of the screen
        self.display = pygame.display.set_mode((self.screen_default_width,self.screen_default_height),pygame.RESIZABLE) #create the display on which the screen is projected
        self.display_resized_flag = False #the display has not yet been resized
        self.display_width = self.screen_default_width #display width
        self.display_height = self.screen_default_height #display height
        self.screen =  pygame.Surface((self.screen_default_width,self.screen_default_height)) #screen object on which UI elements are project
        #create the board object
        self.board = Board(board_values,board_height,board_width,self.tile_size) #create the board object           

    #handle events generated by the game
    def event_handle(self,event):
        #quit the game
        if event.type == pygame.QUIT:
                sys.exit() #quit the game
        #resize the screen
        elif event.type == pygame.VIDEORESIZE:
                new_size = event.dict['size']
                self.display_resize(new_size)
        #handle the user clicking down on the mouse
        elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_down(event)

    #resize the screen
    def display_resize(self,new_size):
        self.display_resized_flag = True #indicate the display has been resized
        self.new_size = new_size #store the new size of the display
        self.display_width = new_size[0] #update display width
        self.display_height = new_size[1] #update display height

    def screen_mouse_position(self,x,y):
        #convert mouse position between display coordinates and screen coordinates
        screen_x = x*(self.screen_default_width/self.display_width) #position on the screen
        screen_y = y*(self.screen_default_height/self.display_height) #position on the screen
        return screen_x,screen_y


    #display the contents of the screen on the display
    def display_render(self):
        #project UI elements on the screen
        self.screen.blit(self.board.static_board_surface,(self.other_player_width_pixels,0)) #project the board onto the screen
        #project the screen onto the final display accounting for dynamic resizing
        if self.display_resized_flag==False:
            self.display.blit(self.screen, (0, 0))
        elif self.display_resized_flag==True:
            self.display.blit(pygame.transform.scale(self.screen,self.new_size),(0,0))

    #extract info about the board
    def extract_board_data(self,board_path,tiles):
        board_raw = pandas.read_csv(board_path,header=None) #extract raw data from the csv file
        board_size = board_raw.shape #get the dimensions of the board
        board_values = np.zeros(board_size)#the board represented as a numpy array, the numbers represent what type of tile occupies each grid-square
        for i,tile_name in enumerate(tiles): #go through all the types of tiles
            truth = board_raw==tile_name #find the tiles which are the current type of tile
            board_values = board_values + truth*i #set the tile number accordingly

        board_values = np.array(board_values,dtype=int) #convert back to a numpy array of ints
        return board_values,board_size #provide the numeric representation of the boards tiles

    #return the object at the referenced position on the screen
    def return_object_at_position(self,screen_x,screen_y):
        pass
        #handler for the board object


    #handler for the mouse down event
    def mouse_down(self,event):
        screen_x,screen_y = self.screen_mouse_position(event.pos[0],event.pos[1]) #find the position of the mouse down event on the screen
        self.return_object_at_position(screen_x,screen_y)

    
        
def main():
    pygame.init()  # initialize pygame
    clock = pygame.time.Clock() #create a clock to set the frame-rate
    pygame.display.set_caption('Cluedo') #display the game title in the window
    #board = Board("board.csv") #create the board
    #print(board.board_static)
    gm = GameMaster()
    while True:
        clock.tick(60)
        #bg = pygame.image.load("rock.jpeg")
        gm.display_render()
        #x, y = pygame.mouse.get_pos() #get pixel position of mouse
        for event in pygame.event.get():
            gm.event_handle(event)


        pygame.display.update()

if __name__ == '__main__':
    main()