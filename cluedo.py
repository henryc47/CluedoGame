#this file will store the logic for playing the game of cluedo
#this will include the state of the board, cards, etc
#how to actually make decisions will be up to other programs
#written by Henry Chadban from 07/12/2022

import pandas #for reading csv files
import numpy as np #for storing the state of the board
import pygame
import pygame.locals
import sys
import random
import os

#constants
#list of all static objects
tiles = ['wall','walk','kitchen','dining_room','lounge','hall','study','library','billards','conservatory','ballroom','start_mustard',
'start_scarlet','start_plum','start_peacock','start_rev_green','start_white','secret_study','secret_lounge','secret_conservatory','secret_kitchen',
'centre']
#list of all players
players = ['mustard','scarlet','plum','peacock','rev_green','white']

#load the static sprites we are using in this game
class StaticSprites():
    def __init__(self):
        self.walk = pygame.image.load("cluedo_images/walk.png")
        self.centre = pygame.image.load("cluedo_images/centre.png")
        self.wall = pygame.image.load("cluedo_images/wall.png")
        self.space = pygame.image.load("cluedo_images/space.png")
        self.secret = pygame.image.load("cluedo_images/secret.png")

#load the sprites of the players
class PlayerBoardSprites():
    def __init__(self):
        self.mustard = pygame.image.load("cluedo_images/mustard.png").convert_alpha()
        self.scarlet = pygame.image.load("cluedo_images/scarlet.png").convert_alpha()
        self.peacock = pygame.image.load("cluedo_images/peacock.png").convert_alpha()
        self.rev_green = pygame.image.load("cluedo_images/rev_green.png").convert_alpha()
        self.plum = pygame.image.load("cluedo_images/plum.png").convert_alpha()
        self.white = pygame.image.load("cluedo_images/white.png").convert_alpha()

class PlayerDisplaySprites():
    def __init__(self):
        #for display in the info screens, these will be 67 by 67
        self.mustard = pygame.transform(pygame.image.load("cluedo_images/mustard.png").convert_alpha(),(67,67))
        self.scarlet = pygame.transform(pygame.image.load("cluedo_images/scarlet.png").convert_alpha(),(67,67))
        self.peacock = pygame.transform(pygame.image.load("cluedo_images/peacock.png").convert_alpha(),(67,67))
        self.rev_green = pygame.transform(pygame.image.load("cluedo_images/rev_green.png").convert_alpha(),(67,67))
        self.plum = pygame.transform(pygame.image.load("cluedo_images/plum.png").convert_alpha(),(67,67))
        self.white = pygame.transform(pygame.image.load("cluedo_images/white.png").convert_alpha(),(67,67))

#sprites of the cards
class CardSprites():
    def __init__(self):
        #these will be 67 by 67
        self.question = pygame.image.load("cluedo_images/question.png") #unknown card
        #player cards
        self.mustard = pygame.transform(pygame.image.load("cluedo_images/mustard.png").convert_alpha(),(67,67))
        self.scarlet = pygame.transform(pygame.image.load("cluedo_images/scarlet.png").convert_alpha(),(67,67))
        self.peacock = pygame.transform(pygame.image.load("cluedo_images/peacock.png").convert_alpha(),(67,67))
        self.rev_green = pygame.transform(pygame.image.load("cluedo_images/rev_green.png").convert_alpha(),(67,67))
        self.plum = pygame.transform(pygame.image.load("cluedo_images/plum.png").convert_alpha(),(67,67))
        self.white = pygame.transform(pygame.image.load("cluedo_images/white.png").convert_alpha(),(67,67))
        #room cards
        self.billards = pygame.image.load("cluedo_images/question.png")
        self.conservatory = pygame.image.load("cluedo_images/question.png")
        self.ballroom = pygame.image.load("cluedo_images/question.png")
        self.kitchen = pygame.image.load("cluedo_images/question.png")
        self.lounge = pygame.image.load("cluedo_images/question.png")
        self.study = pygame.image.load("cluedo_images/question.png")
        self.hall = pygame.image.load("cluedo_images/question.png")
        self.dining_room = pygame.image.load("cluedo_images/question.png")
        self.library = pygame.image.load("cluedo_images/question.png")
        #weapon cards
        self.spanner = pygame.image.load("cluedo_images/question.png")
        self.rope = pygame.image.load("cluedo_images/question.png")
        self.dagger = pygame.image.load("cluedo_images/question.png")
        self.lead_piping = pygame.image.load("cluedo_images/question.png")
        self.candlestick = pygame.image.load("cluedo_images/question.png")
        

#cludeo is played on a 27 tile wide,25 tile tall board
class Board():
    #create the board on which the game will be played
    def __init__(self,board_values,board_width,board_height,tile_size,debug):
        self.name = 'board' #name of the object, for debugging purposes
        self.board_values = board_values #numbers what type of static object each position holds
        self.board_width = board_width
        self.board_height = board_height
        self.tile_size = tile_size
        self.board_pixel_width = self.tile_size*self.board_width #determine the default width in pixels of the board
        self.board_pixel_height = self.tile_size*self.board_height #determine the default height in pixels of the board
        self.debug = debug
        self.create_players_at_start()
        self.setup_rendering()
        self.render_board()
    
    #create the objects involved in rendering the board, and render the static background
    def setup_rendering(self):
        self.board_surface = pygame.Surface((self.board_pixel_width,self.board_pixel_height)) #create a surface of the correct size
        self.static_sprites = StaticSprites() #load the static sprites used in the game
        self.dynamic_sprites = PlayerBoardSprites() #load the dynamic sprites used in the game
        self.render_background() #create the background
        
    #render the current board        
    def render_board(self):
        self.board_surface.blit(self.static_board_surface,(0,0)) #render the background onto the main surface
        self.render_players() #render the players onto the background

    #render the background of the board
    def render_background(self):
        self.static_board_surface = pygame.Surface((self.board_pixel_width,self.board_pixel_height)) #create a surface of the correct size to be the background
        self.render_static_tiles() #render the tiles on the board
        self.render_room_text() #render the text on the board

    #render the text displayed on the rooms
    def render_room_text(self):
        font = pygame.font.SysFont(None,24)
        black = pygame.Color(0,0,0)
        #generate text for each room
        billards_room_text = font.render('Billiards Room',True,black)
        kitchen_text = font.render('Kitchen',True,black)
        lounge_text = font.render('Lounge',True,black)
        library_text = font.render('Library',True,black)
        hall_text = font.render('Hall',True,black)
        study_text = font.render('Study',True,black)
        ballroom_text = font.render('Ballroom',True,black)
        dining_room_text = font.render('Dining Room',True,black)
        conservatory_text = font.render('Conservatory',True,black)
        #now let's render each text at the centre of the respective room
        self.render_at_centre(billards_room_text,black,'billards')
        self.render_at_centre(kitchen_text,black,'kitchen')
        self.render_at_centre(lounge_text,black,'lounge')
        self.render_at_centre(library_text,black,'library')
        self.render_at_centre(hall_text,black,'hall')
        self.render_at_centre(study_text,black,'study')
        self.render_at_centre(ballroom_text,black,'ballroom')
        self.render_at_centre(dining_room_text,black,'dining_room')
        self.render_at_centre(conservatory_text,black,'conservatory')



    #render text at the centre of a room, by which we mean the midpoint between the extremes
    def render_at_centre(self,text,colour,room_name):
        centre_x,centre_y = self.find_room_centre(room_name)
        if self.debug==True:
            print('room = ',room_name,' centre x = ',centre_x,' centre y = ',centre_y)
        text_width = text.get_width()
        text_height = text.get_height()
        offset_x = int(text_width/2)
        offset_y = int(text_height/2)
        self.static_board_surface.blit(text,(centre_x-offset_x,centre_y-offset_y))
        

    #find the pixel coordinates at the centre of a room
    def find_room_centre(self,room_name):    
        min_x = self.board_width
        min_y = self.board_height
        max_x = -1
        max_y = -1
        scan_x = 0
        scan_y = 0
        #go through all the tiles in the board
        for row in self.board_values:
            scan_x = 0
            for tile_value in row: 
                tile_text = tiles[tile_value] #find the text of the tile
                if tile_text==room_name: #we are looking at a tile of the desired room
                    #check if new minima/maxima found
                    if scan_x<min_x: #if new minimum
                        min_x = scan_x #store new minimum
                    if scan_y<min_y:
                        min_y = scan_y
                    if scan_x>max_x: #if new maxima
                        max_x = scan_x #store new maxima
                    if scan_y>max_y: 
                        max_y = scan_y
                else:
                    pass
                scan_x = scan_x + 1 #move onto the next tile in the row

            scan_y = scan_y + 1 #move onto the next row

        if max_x==-1: #if no maxima (and therefore minima) found
            #return -1 as pixel position to indicate error
            centre_x = -1
            centre_y = -1    
        else:
            #calculate the central pixel of the room
            centre_x = ((min_x+max_x+1)/2)*self.tile_size
            centre_y = ((min_y+max_y+1)/2)*self.tile_size

        return centre_x,centre_y

    #render the static tiles that make up the board
    def render_static_tiles(self):
        x = 0 #position of current tile in the board along the x-axis
        y = 0 #position of current tile in the board along the y-axis
        
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

    #render the player characters on top of the static board
    def render_players(self):
        #loop through the player map to find which player is in which tile
        x = 0
        y = 0
        for row in self.player_map:
            x = 0 #reset x position after each row
            for player_text in row:
                x_position = x*self.tile_size
                y_position = y*self.tile_size
                x = x+1 #update the column, this is earlier due to potential use of continue later
                #get the relevant image for each player
                if player_text=='mustard':
                    image = self.dynamic_sprites.mustard
                elif player_text=='scarlet':
                    image = self.dynamic_sprites.scarlet
                elif player_text=='plum':
                    image = self.dynamic_sprites.plum
                elif player_text=='peacock':
                    image = self.dynamic_sprites.peacock
                elif player_text=='rev_green':
                    image = self.dynamic_sprites.rev_green
                elif player_text=='white':
                    image = self.dynamic_sprites.white
                else:
                    continue #we do not need to render an image
                self.board_surface.blit(image,(x_position,y_position))
                
            y = y+1 #update the row

    #create the map of players at their starting positions
    def create_players_at_start(self):
        self.player_map = []
        for row in self.board_values:
            new_row = []
            for tile in row:
                tile_text = tiles[tile] #get the text of the tile
                if tile_text=='start_mustard':
                    player='mustard'
                elif tile_text=='start_scarlet':
                    player='scarlet'
                elif tile_text=='start_plum':
                    player='plum'
                elif tile_text=='start_peacock':
                    player='peacock'
                elif tile_text=='start_rev_green':
                    player='rev_green'
                elif tile_text=='start_white':
                    player='white'
                else:
                    player=' ' #placeholder
                new_row.append(player)
            self.player_map.append(new_row)
                
    def mouse_down(self,x,y,debug):
        tile_x,tile_y = self.pixel_position_to_tile(x,y) #determine the position of the clicked on tile
        if debug==True:
            print('tile x = ',tile_x,' tile y =',tile_y)
        tile_type = self.extract_tile_type(tile_x,tile_y) #determine the type of tile we clicked on
        if debug==True:
            print('this is a ',tile_type,' tile')
        
    
    #convert pixel position on the board to tile position
    def pixel_position_to_tile(self,x,y):
        tile_position_x = int(x/self.tile_size)
        tile_position_y = int(y/self.tile_size)
        return tile_position_x,tile_position_y

    #provide the type of tile at a particular position
    def extract_tile_type(self,tile_x,tile_y):
        tile_value = self.board_values[tile_y,tile_x]
        tile_type = tiles[tile_value]
        return tile_type


#controls the logic for the displayed player
class OwnPlayer():
    def __init__(self,debug):
        self.debug = debug #are we in debug mode

#controls the state of cards in the game
class CardController():
    #create the list of cards and decide on the murder cards
    def __init__(self):
        self.room_cards : list[str] = ["billards","kitchen","lounge","library","hall","study","ballroom","dining_room","conservatory"]
        self.weapon_cards : list[str] = ["spanner","rope","dagger","lead_piping","candlestick"]
        self.player_cards : list[str] = ["mustard","scarlet","peacock","rev_green","plum","white"]
        self.calculate_murder_cards()
        self.players : list[str] = ['mustard','scarlet','peacock','rev_green','plum','white'] #list of all valid players
        self.num_players : int = len(self.players)


    def calculate_murder_cards(self):
        #how many cards of each type
        num_room_cards : int = len(self.room_cards)
        num_weapon_cards : int = len(self.weapon_cards)
        num_player_cards : int = len(self.player_cards)
        #get the murder card index for each room
        room_card_num : int = random.randint(0,num_room_cards-1)
        weapon_card_num : int = random.randint(0,num_weapon_cards-1)
        player_card_num : int = random.randint(0,num_player_cards-1)
        #extract each murder card and remove it from the list of free cards
        self.murder_room : str = self.room_cards[room_card_num]
        del self.room_cards[room_card_num]
        self.murder_weapon : str = self.weapon_cards[weapon_card_num]
        del self.weapon_cards[weapon_card_num]
        self.murder_player : str = self.player_cards[player_card_num]
        del self.player_cards[player_card_num]
        self.all_cards_left : list[str] = self.room_cards + self.weapon_cards + self.player_cards

    def assign_cards_to_players(self,player_list : list[str]):
        #note player list is in order
        #lists to store which cards players own
        self.player_cards : list[list[str]] = [[],[],[],[],[],[]]
        #is each player playing
        self.player_playing : list[bool] = [False,False,False,False,False,False]
        num_playing :int = 0
        for player in player_list:
            num_playing = num_playing + 1
            valid_player : bool = False
            for i in range(self.num_players):
                if self.players[i]==player:
                    self.player_playing[i] = True
                    valid_player = True
                    break
                else:
                    continue
            if valid_player==False:
                print("WARNING: INVALID PLAYER ",player," DETECTED")
                #invalid players cannot play no matter what
                num_playing = num_playing - 1 #so reverse increment of number of players
        
        #now it is time to distribute the cards
        num_cards_left : int = len(self.all_cards_left)
        player_to_deal : int = 0 #which player are we dealing at
        while(num_cards_left>0): #while there are cards left to be dealed
            card_dealt : bool = False #has a card been dealt yet
            loops : int = 0
            while card_dealt==False: #if there are no valid players this may get trapped in an infinite loop
                if self.player_playing[player_to_deal]==True:
                    card_dealt = True
                else:
                    player_to_deal = player_to_deal + 1
                    if player_to_deal==6:
                        loops = loops + 1
                        player_to_deal = 0
                    if loops>=2:
                        print("INFINITE LOOP DETECTED DURING DEALING")
            new_card_index : int = random.randint(0,num_cards_left-1) #extract random card from the remaining cards
            new_card : str = self.all_cards_left[new_card_index]
            del self.all_cards_left[new_card_index] #remove the card from the pile
            self.player_cards[player_to_deal].append(new_card) #add it to the list of cards each player has
            player_to_deal = player_to_deal + 1 #next player to deal
            if player_to_deal==6: #reset player counter once we reach the max number of players
                player_to_deal = 0
            num_cards_left = num_cards_left-1 #we have 1 less card on the pile now it has been dealt


#controls the overall flow of the game logic
class GameMaster():
    def __init__(self,board_path='board.csv'):
        self.debug = True #change to false once we have finished development
        board_values,board_size =  self.extract_board_data(board_path,tiles)
        board_height = board_size[0] #height of the board in tiles, should be 26
        board_width = board_size[1] #width of the board in tiles, should be 27
        self.tile_size = 32 #number of pixels in a tile
        self.board_height_pixels = board_height*self.tile_size #height of the playing board in pixels, should be 832
        self.board_width_pixels = board_height*self.tile_size #width of the playing board in pixels, should be 864
        self.other_player_width_pixels = 172 #width of the left sidebar, where players and their cards are displayed
        self.self_player_width_pixels = 172 #width of the right sidebar, where your own cards and controls are displayed
        self.screen_default_width = self.board_width_pixels + self.other_player_width_pixels + self.self_player_width_pixels #total width, pixels,s of the screen
        self.screen_default_height = self.board_height_pixels #total height, pixels, of the screen
        self.display = pygame.display.set_mode((self.screen_default_width,self.screen_default_height),pygame.RESIZABLE) #create the display on which the screen is projected
        self.display_resized_flag = False #the display has not yet been resized
        self.display_width = self.screen_default_width #display width
        self.display_height = self.screen_default_height #display height
        self.screen =  pygame.Surface((self.screen_default_width,self.screen_default_height)) #screen object on which UI elements are project
        #create the board object
        self.board : Board = Board(board_values,board_height,board_width,self.tile_size,self.debug) #create the board object
        self.card_controller : CardController = CardController()
        active_players : list[str] = ['mustard','scarlet','peacock','plum','white'] #currently active players 
        self.card_controller.assign_cards_to_players(active_players) #assign cards to players 
        

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
        self.screen.blit(self.board.board_surface,(self.other_player_width_pixels,0)) #project the board onto the screen
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
        #if player clicks on the playing board
        if screen_x>=self.other_player_width_pixels and screen_x<self.other_player_width_pixels+self.board_width_pixels:
            if self.debug==True:
                print('clicked on board')
            #calculate the click position with top left of the board being zero zero
            object_x = screen_x-self.other_player_width_pixels
            object_y = screen_y
            object_clicked = self.board #we clicked on the board
        #if player clicks on info about other players
        elif screen_x<self.other_player_width_pixels:
            if self.debug==True:
                print('clicked on other players region')
            object_x = screen_x
            object_y = screen_y
            object_clicked = 0 #self.other_players_region #will be zero till implementation
        #if player clicks on info about themsleves
        elif screen_x>=self.other_player_width_pixels+self.board_width_pixels:
            if self.debug==True:
                print('clicked on own region')
            object_x = screen_x-(self.other_player_width_pixels+self.board_width_pixels)
            object_y = screen_y
            object_clicked = 0 #self.other_players_region #will be zero till implementation
        #player clicked in a undefined region
        else:
            object_x = -1
            object_y = -1
            object_clicked = -1

        return object_x,object_y,object_clicked

    #handler for the mouse down event
    def mouse_down(self,event):
        screen_x,screen_y = self.screen_mouse_position(event.pos[0],event.pos[1]) #find the position of the mouse down event on the screen
        object_x,object_y,object_clicked = self.return_object_at_position(screen_x,screen_y)
        #if the user clicked an invalid object, do nothing
        if object_clicked == -1:
            if self.debug==True:
                print('invalid region clicked on')
        #if the user clicked an object not yet defined, do nothing
        elif object_clicked == 0:
            if self.debug==True:
                print('undeveloped region clicked on')
        else:
            if self.debug==True:
                print('clicked on the ',object_clicked.name,' object')
            object_clicked.mouse_down(object_x,object_y,self.debug) #all objects on the screen need to have mouse down methods to allow for clicking

    
        
def main():
    pygame.init()  # initialize pygame
    clock = pygame.time.Clock() #create a clock to set the frame-rate
    pygame.display.set_caption('Cluedo') #display the game title in the window
    #board = Board("board.csv") #create the board
    #print(board.board_static)
    gm = GameMaster()
    printed : bool = False #debug
    while True:
        clock.tick(60)
        #bg = pygame.image.load("rock.jpeg")
        gm.display_render()
        #x, y = pygame.mouse.get_pos() #get pixel position of mouse
        for event in pygame.event.get():
            gm.event_handle(event)
        pygame.display.update()
        #testing
        if gm.debug==True:
            if printed==False:
                print("all cards left ",gm.card_controller.all_cards_left)
                ['mustard','scarlet','peacock','rev_green','plum','white'] #list of all valid players
                print("mustard cards ",gm.card_controller.player_cards[0])
                print("mustard playing ",gm.card_controller.player_playing[0])
                print("scarlet cards ",gm.card_controller.player_cards[1])
                print("scarlet playing ",gm.card_controller.player_playing[1])
                print("peacock cards ",gm.card_controller.player_cards[2])
                print("peacock playing ",gm.card_controller.player_playing[2])
                print("rev_green cards ",gm.card_controller.player_cards[3])
                print("rev_green playing ",gm.card_controller.player_playing[3])
                print("plum cards ",gm.card_controller.player_cards[4])
                print("plum playing ",gm.card_controller.player_playing[4])
                print("white cards ",gm.card_controller.player_cards[5])
                print("white playing ",gm.card_controller.player_playing[5])
                printed = True
            else:
                pass
            
            


if __name__ == '__main__':
    main()