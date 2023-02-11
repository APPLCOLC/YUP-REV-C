"""START###############################################################"""
# input("START")
"""IMPORTS---------------------"""
import pygame,math,time,os,random

"""DISPLAY INITIALIZATION--------------------"""
pygame.display.set_caption("YUP")

icon =  pygame.image.load("assets/images/UI/icon.ico")
pygame.display.set_icon(icon)
window = pygame.display.set_mode((450, 600), pygame.SCALED)

"""INITIALIZATION--------------------"""
pygame.font.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(16)

groups = {
    "universal":pygame.sprite.Group(),
    "player":pygame.sprite.GroupSingle(),
    "bullet":pygame.sprite.Group(),
    "enemy":pygame.sprite.Group(),
    "priority":pygame.sprite.Group(), #the priority group ; gets shown over the others graphically 
}

clock = pygame.time.Clock()

continue_song = False #universal value for title screen, ignore 
# input("AFTER INITIALIZING PYGAME")






"""LOADING#################################################################"""
"""SETTINGS"""
with open("assets/settings.txt", "r") as data: settings = eval(data.read())

"""UI IMAGES---"""
class UiImages:

    #BEGIN AND END
    beginImage = pygame.image.load("./assets/images/UI/BEGIN AND END/GET READY.png").convert_alpha()
    endImage = pygame.image.load("./assets/images/UI/BEGIN AND END/LEVEL COMPLETE.png").convert_alpha()

    #ERRORS
    error_title = pygame.image.load("./assets/images/UI/errors/error_occurred.png").convert_alpha()

    #LOGO FOR TITLE
    title_bg_logo = [
        pygame.image.load("./assets/images/UI/title/logo1.png").convert_alpha(), 
        pygame.image.load("./assets/images/UI/title/logo2.png").convert_alpha(), 
        pygame.image.load("./assets/images/UI/title/logo3.png").convert_alpha()]

    #PAUSE GRAPHIC
    pause = [ 
        pygame.transform.scale(pygame.image.load('./assets/images/UI/pause/paus\'d (1).png'),(450,150)).convert_alpha(),
        pygame.transform.scale(pygame.image.load('./assets/images/UI/pause/paus\'d (2).png'),(450,150)).convert_alpha(),
        pygame.transform.scale(pygame.image.load('./assets/images/UI/pause/paus\'d (3).png'),(450,150)).convert_alpha(),
    ]

    #PRESS SPACE
    press_space = pygame.image.load("./assets/images/UI/space.png").convert_alpha()

    #BUTTONS
    quit_button = pygame.image.load("./assets/images/UI/quit_button.png").convert_alpha()
    quit_button_pressed = pygame.image.load("./assets/images/UI/quit_button_pressed.png").convert_alpha()
    QUIT = [quit_button, quit_button_pressed]
    del quit_button, quit_button_pressed

    start_button = pygame.image.load("./assets/images/UI/start_button.png").convert_alpha()
    start_button_pressed = pygame.image.load("./assets/images/UI/start_button_pressed.png").convert_alpha()
    START = [start_button, start_button_pressed]
    del start_button, start_button_pressed

    options_button = pygame.image.load("./assets/images/UI/options_button.png").convert_alpha()
    options_button_pressed = pygame.image.load("./assets/images/UI/options_button_pressed.png").convert_alpha()
    OPTIONS = [options_button, options_button_pressed]
    del options_button, options_button_pressed

    continue_button = pygame.image.load("./assets/images/UI/continue_button.png").convert_alpha()
    continue_button_pressed = pygame.image.load("./assets/images/UI/continue_button_pressed.png").convert_alpha()
    CONTINUE = [continue_button, continue_button_pressed]
    del continue_button,continue_button_pressed

    #LOADING
    loading = pygame.image.load("./assets/images/UI/loading/load_small.png")

    #GENERAL
    yes = pygame.transform.scale(pygame.image.load("./assets/images/UI/YES.png"), (50, 25)).convert_alpha()
    no = pygame.transform.scale(pygame.image.load("./assets/images/UI/NO.png"), (50, 25)).convert_alpha()
    on = pygame.image.load("./assets/images/UI/ON.png").convert_alpha()
    off = pygame.image.load("./assets/images/UI/OFF.png").convert_alpha()
    checkmark = pygame.image.load("./assets/images/UI/CHECKMARK.png").convert_alpha()
    xmark = pygame.image.load("./assets/images/UI/X.png").convert_alpha()
    slider = pygame.image.load("./assets/images/UI/slider.png").convert_alpha()
    knob = pygame.image.load("./assets/images/UI/knob.png").convert_alpha()

    #SETTINGS IMAGES
    option_bg = pygame.transform.scale(pygame.image.load("./assets/images/UI/options/bg.png"), (450, 600)).convert_alpha()
    option_30 = pygame.transform.scale(pygame.image.load("./assets/images/UI/options/FPS30.png"),(50,30)).convert_alpha()
    option_60 = pygame.transform.scale(pygame.image.load("./assets/images/UI/options/FPS60.png"),(50,30)).convert_alpha()

    #BAGKGROUNDS
    title_bg = pygame.transform.scale(pygame.image.load("./assets/images/UI/title/background.png"), (450, 600)).convert_alpha()
    error_bg = pygame.transform.scale(pygame.image.load("./assets/images/UI/errors/bg.png"), (450, 600)).convert_alpha()
    load_bg = pygame.transform.scale(pygame.image.load("./assets/images/UI/splash.png"), (450, 600)).convert_alpha()

    #CURSOR
    cursor = pygame.image.load("./assets/images/UI/LIVES/000.png").convert_alpha()

    #GAME OVER
    game_over_sign = pygame.image.load("./assets/images/UI/GAME OVER.png").convert_alpha()

ui=UiImages #this creates an object of the class. this is what everything refers to

#"long loading" before it is defined, just so you aren't sitting there looking at nothing
window.blit(ui.load_bg, (0, 0))
pygame.display.update()

"""CHARACTERS"""
loaded_characters = {}

for item in os.listdir("./characters"):
    #removing file extension
    if ".py" in item:
        temp=""
        for _ in range(len(item)):
            if _ > len(item)-4:continue
            else: temp += item[_]
        item=temp
    #importing characters
    the_code = "import characters." + str(item) + " as " + str(item)
    exec(the_code, globals(), loaded_characters)

from characters import shared

"""BACKGROUNDS---"""
loaded_backgrounds = {}

for directory in os.listdir("./assets/images/bg/"):
    # print(directory)
    # removing non-directories
    if "." in directory: continue  # breaking if there is a file extension, as it should only be detecting folders
    #removing empty directories
    if len(os.listdir("./assets/images/bg/"+directory))<=0: continue




    """PREFIX LOADING---"""
    # discovering the prefixes used for the directory
    # list of potential prefixes
    prefix=[]
    prefixList = [('', ''), ('(', ')'), ('frame (', ')'), ('frame', ''), ('frame ', ''), ('Frame (', ')'),
                  ('Frame', ''), ('Frame ', '')]
    photo=None
    x = 0

    # iterating through every prefix to see which one will properly load a background ; if one is properly loaded, that is the set prefix
    for item in prefixList:
        #attempting a prefix
        try:
            photo = pygame.image.load(('./assets/images/bg/' + directory + '/' + prefixList[x][0] + '1' + prefixList[x][1] + '.png'))
            prefix = prefixList[x]
            break
        #changing prefix to retry
        except FileNotFoundError:
            photo=None
            x += 1
        #if no prefixes work
        if x >= len(prefixList):
            photo=None
            break

    # print(prefix)

    """ADDING EACH FOLDER AS LOADED_BG INDEX"""
    # loading each folder
    loaded_backgrounds[str(directory)] = [None, []]  # index 0 is config file, index 1 contains the imported images

    """ADDING CONFIG"""
    try:
        with open(('./assets/images/bg/' + directory + '/config.txt'),"r") as data:
            loaded_backgrounds[directory][0]=eval(data.read())

    except FileNotFoundError:
        loaded_backgrounds[directory][0]=None

    """ADDING LOADED FRAMES TO LOADED_BACKGROUNDS"""
    #assembling a list of images using the prefixes given before
    #the frame it uses for searching goes up by 1 every iteration9?
    #when a file is not found, that means the list search is complete and the program continues
    curFrame=1

    #this is what configures the resizing of the images
    #there is an optional configuration key called "resize" that will resize the item
    #this is the resize option done so it doesn't need to be re-checked each frame
    if (loaded_backgrounds[directory][0] == None) or ("resize" not in loaded_backgrounds[directory][0]) or (loaded_backgrounds[directory][0]["resize"] == 3):
        resize = 3 #defaulting to resize both
    else:
        resize = loaded_backgrounds[directory][0]["resize"] #picking resizing option

    while True:
        try:

            # print(prefix)
            item=pygame.image.load(('./assets/images/bg/' + directory + '/' + prefix[0] + str(curFrame) + prefix[1] + '.png'))

            # print(str(directory),str(resize))
            if resize == 0 :
                scale = (item.get_width(),item.get_height())
            elif resize == 1: #scaling vertically based off what needs to be scaled horizontally to fit the screen
                multiplier = 450 / item.get_width()
                scale = ( item.get_width() * multiplier, item.get_height() * multiplier )
                del multiplier
            elif resize == 2: #scaling horizontally based off what needs to be scaled vertically to fit the screen
                multiplier = 600 / item.get_height()
                scale = ( item.get_width() * multiplier, item.get_height() * multiplier )
                del multiplier
            else: #3 or onward resizing to fit screen
                scale = (450,600)
            


            item=pygame.transform.scale(item,scale).convert_alpha()

            loaded_backgrounds[directory][1].append(item) #adds image to main directory

            #updates the current frame
            curFrame+=1

        #if an error occurs, the search is complete
        except FileNotFoundError:
            curFrame=1
            break
        break #debug remove - makes there only one image



"""LEVELS---"""
loaded_levels = {}

for item in os.listdir("levels/"):

    #removing extension and kicking items without one
    if ".py" not in item:
        continue
    temp=""
    for _ in range(len(item)):
        if _ > len(item)-4:continue
        else: temp += item[_]
    item=temp

    #importing levels
    the_code = "import levels." + str(item) + " as " + str(item)
    exec(the_code, globals(), loaded_levels)

# input("LOADED LEVELS")

"""BULLETS---"""
loaded_bullets = {}

for item in os.listdir("./bullets/"):
    #removing extension and kicking items without one
    if ".py" not in item:
        continue
    temp=""
    for i in range(len(item)):
        if i > len(item)-4:continue
        else: temp += item[i]
    item=temp


    #importing bullets
    the_code = "import bullets." + str(item) + " as " + str(item)
    exec(the_code, globals(), loaded_bullets)

# providing the SHARED CHARACTER LIBRARY with the bullet images
shared.BulletItem.loaded_bullets = loaded_bullets


"""SOUNDS---"""

class Sounds:

    def __init__(self):
        ###################SOUNDS####################

        self.sounds = {}
        self.ost = {}

        self.offsetSounds = {}
        ##############################################

    ###############FUNCTIONS###############-

    def play_song(self,song,pos=0.0):
        pygame.mixer.music.set_volume(settings["OST VOL"][0])
        pygame.mixer.music.load("./assets/ost/"+song)
        pygame.mixer.music.play(loops=-1,start=pos/1000)

    @staticmethod
    def stop_song():
        pygame.mixer.music.stop()

    def adjust_sounds(self):
        for sound in self.sounds.values():
            sound.set_volume(settings["SOUND VOL"][0])
        # death.set_volume(death.get_volume() / 2)

    def adjust_ost(self):
        pygame.mixer.music.set_volume(settings["OST VOL"][0])

    def apply_offsets(self):
        # for k,v in self.offsetSounds.items():
        #
        #     volume=self.soundList[self.soundList.index(k)].get_volume()*v
        #
        #     self.soundList[self.soundList.index(k)].set_volume(volume)
        return

sounds=Sounds();sounds.apply_offsets()#this creates an object of the class. this is what everything refers to

for sound in os.listdir("./assets/sounds/"):
    sounds.sounds[str(sound)] = pygame.mixer.Sound("./assets/sounds/" + str(sound))






"""FONTS---"""
loaded_text = {}
#0-9
for _ in range(10):
    loaded_text[_] = ( pygame.font.Font("./assets/font/Terminus.ttf",20).render(str(_),True,"white","black") )
#world names
with open("./levels/worldOrder.txt") as world_order:
    world_order = eval(world_order.read())
for _ in world_order:
    loaded_text[_] = ( pygame.font.Font("./assets/font/Terminus.ttf",20).render( str(_.upper()),True,"white","black" )) 
#ouch, wow, bonus, score, level complete
ui_names = ["WOW!","OUCH!","BONUSES:","YOU SCORED:","SCORE:","COMBO!","NO MISS!", "WARPING TO", "YOU DID GREAT!", "YOU SUCK!","YOU'RE WINNER!", "STAGE COMPLETE!"]
for _ in ui_names:
    loaded_text[_] = ( pygame.font.Font("./assets/font/Terminus.ttf",20).render( str(_),True,"white","black" )) 
#settings text, since it's always designed on startu
for _ in settings.keys(): 
    loaded_text[_] = pygame.transform.scale(
        pygame.font.Font(
            "./assets/font/Setfont-Regular.ttf", 50
            ).render(str(_), True, "white"), 
        (75, 40)
        )

#VISUAL EFFECT TEXT
class Text(pygame.sprite.Sprite):
    possible_patterns = [ "static", "linear", "sine", "squared", "static sine" ]
    screen_rect = pygame.Rect(0,0,450,600)
    def __init__( self,
        text :str = "WOW!",
        pattern :str = "static", #pattern, random.choice( [ "static", "linear", "sine", "squared" ] )
        duration:str = -1, #how many frames the item should last for. -1 equals infinity 
        size:int = None, #resizable ; if None, no resize
        font:str = "./assets/font/Terminus.ttf", #the font ; could also be SetFont
        fg:str = "white", #foreground color
        bg:str = "black", #background color
        pos:tuple = (0,0), #where item is placed, or the vertex of the function
        vertex:tuple = (0,0), #used for sine and squared
        modifier:int = 1, #slope, sine vertical stretch, etc
        modifier2:int = 1, #sine horizontal stretch, idk what else
        speed:int = 1, #self explanatory - vertical movement
        ):

        pygame.sprite.Sprite.__init__(self)

        #FIXING PATTERN
        
        self.pattern = "static" if pattern not in Text.possible_patterns or pattern == "static" else pattern

        #IMAGE REGISTRATION
        if text in loaded_text.keys():
            #if the image is loaded
            self.image = loaded_text[text]
        else:
            #if the image is not loaded
            # print("TEXT NOT PRESENT, ADDING...")
            loaded_text[text] = pygame.font.Font(font,20).render(str(text),True,fg,bg)
            self.image = loaded_text[text]

        #resizing image
        if size is not None:
            self.image = pygame.transform.scale(self.image,((size//2)*len(text),size))
        self.rect = self.image.get_rect()
        
        #positioning image
        self.rect.center = pos

        #turning around if wrong way
        if (pos[0] < 0 and speed < 0) or (pos[0] > 450 and speed > 0):
            speed *= -1
    

        #making class items
        self.pos,self.vertex = pos,vertex
        self.modifier,self.modifier2 = modifier,modifier2
        self.speed = speed
        
        #counting up
        self.counter = 0 if duration >= 0 else -2
        self.duration = duration
            
    def update(self):
        self.counter += 1
        if (self.counter >= 60 and not self.on_screen()) or ( (self.duration != -1) and (self.counter >= self.duration) ):
            # print("ded")
            self.kill()
        
        #no movement
        if self.pattern == "static":
            return
        #sine in-place
        elif self.pattern == "static sine":
            # print(self.counter)
            self.rect.center = (
                self.rect.center[0],
                #based off counter since this one doesn't move the x position
                (self.modifier * math.sin((self.modifier2*(self.counter)) + self.vertex[0])) + self.vertex[1]
            )
        #sine moving
        elif self.pattern == "sine":
            self.rect.center = (
                self.rect.center[0]+self.speed,
                #based off x position since this one moves the x position
                (self.modifier * math.sin((self.modifier2*(self.rect.center[0])) + self.vertex[0])) + self.vertex[1]
            )
        elif self.pattern == "slope":
            pass
        else: self.kill()

    def on_screen(self):
        return self.rect.colliderect(Text.screen_rect)
        
        





"""FINISHING---"""

del x,photo, prefixList, curFrame,directory, temp, the_code, i,world_order
# print(dir())





"""SHARED ASSETS##############################################################"""

"""APPLYING SETTINGS--------------------"""
def apply_settings():

    fullscreen = settings["FULLSCREEN"][0]

    # audio adjust
    sounds.adjust_sounds()
    sounds.adjust_ost()
    pygame.mixer.Channel(0).set_volume(settings['OST VOL'][0])
    pygame.mixer.Channel(1).set_volume(settings['OST VOL'][0])

    # screen adjust
    if fullscreen:
        pygame.display.set_mode((450, 600), pygame.FULLSCREEN | pygame.SCALED)
    else:
        pygame.display.set_mode((450, 600), pygame.SCALED)
apply_settings()


"""LOADING--------------------"""
def long_load():
    window.blit(ui.load_bg, (0, 0))
    pygame.display.update()

def short_load():
    window.blit(ui.loading, (0, 0))

    pygame.display.update()


"""TEXT DISPLAY--------------------"""
def draw_text(score_value, coord, snap=True, shadow=True, color=(255, 255, 255), shadow_color=(0, 0, 0), size=20, snap_direction = "r"):

    score_font = pygame.font.Font("./assets/font/terminus.ttf",size)

    if shadow: score_surface = score_font.render(str(score_value), True, color, shadow_color)
    else: score_surface = score_font.render(str(score_value), True, color)
    
    score_rect = score_surface.get_rect()

    if snap and snap_direction == 'r':score_rect.right = coord[0] ; score_rect.y = coord[1]
    elif snap and snap_direction == 'l':score_rect.left = coord[0] ; score_rect.y = coord[1]
    else: score_rect.center = coord

    window.blit(score_surface, score_rect)

    del score_font,score_rect,score_surface

#specifically displaying the score
def draw_score(score, snap="right",x=0,y=0):
    score=str(score)
    if snap == 'right':
        for i in range(len(score)):
            window.blit(
                loaded_text[
                    int(score[i])
                    ], 
                    (((len(score)-(i+1)) * -11+(x-11)), y) 
                )
    
    del score,snap,i





"""IMPORTANT MODULES##############################################################"""


"""BACKGROUNDS--------------------"""
class BG:
    #takes loaded backgrounds ; draws them to screen ; (update) no longer loads backgrounds automatically
    def __init__(self, photo_name='null', current_frame=1, loaded=loaded_backgrounds):

        #beginning values
        self.bgY,self.bgX=0,0 #scroll stuff
        self.curFrame = current_frame
        self.photo_name = photo_name
        self.config=loaded[photo_name][0]
        self.dir=loaded[photo_name][1]

        #default self.config 
        self.config = {
            "speed":1, 
            "reverse":False,
            "flip_vert":False,
            "flip_horiz":False,
            "opacity":255, #defaults at 255
            "scrollVert":0, #for off, select 0
            "scrollHoriz":0, #for off, select 0
            "interpolate":True, #transitions first and last frames to loop better
            } if self.config == None else self.config 



    #This is the code that will run on-frame.
    #It does not display the background, just update the current image to *be* displayed.
    def update(self, scroll_values : tuple = None):
        window.fill("black")#initial screen fill in case of transparency

        #scroll code - advancing frame turnary operator
        self.curFrame = self.curFrame +1  if self.curFrame+1<len(self.dir) else 0
        if scroll_values is None:
            self.bgY += self.config['scrollVert']
            self.bgX += self.config['scrollHoriz']
        else:
            self.bgY += scroll_values[1]
            self.bgX += scroll_values[0]
        if self.bgY >= self.dir[self.curFrame].get_height() or self.bgY <= (self.dir[self.curFrame].get_height()*-1): self.bgY=0
        if self.bgX >= self.dir[self.curFrame].get_width() or self.bgX <= (self.dir[self.curFrame].get_width()*-1): self.bgX=0

        


    # Duplicating images around current background to make the background look like it is repeating
    def decoys(self):
        if self.bgY != 0:
            window.blit(self.dir[self.curFrame], (self.bgX, self.bgY - self.dir[self.curFrame].get_height()))
            window.blit(self.dir[self.curFrame], (self.bgX, self.bgY + self.dir[self.curFrame].get_height()))

        if self.bgX != 0:
            window.blit(self.dir[self.curFrame], (self.bgX + self.dir[self.curFrame].get_width(), self.bgY))
            window.blit(self.dir[self.curFrame], (self.bgX - self.dir[self.curFrame].get_width(), self.bgY))

        if self.bgY != 0 and self.bgX != 0:
            window.blit(self.dir[self.curFrame], (self.bgX + self.dir[self.curFrame].get_width(), self.dir[self.curFrame].get_height() - 600))
            window.blit(self.dir[self.curFrame], (self.bgX - self.dir[self.curFrame].get_width(), self.dir[self.curFrame].get_height() + 600))
            window.blit(self.dir[self.curFrame], (self.bgX + self.dir[self.curFrame].get_width(), self.dir[self.curFrame].get_height() + 600))
            window.blit(self.dir[self.curFrame], (self.bgX - self.dir[self.curFrame].get_width(), self.dir[self.curFrame].get_height() - 600))

        return

    #Displaying the bg is treated differently due to fps changes in gameplay
    def display_bg(self):
        window.blit(self.dir[self.curFrame],(self.bgX,self.bgY))
        self.decoys()


    #Destroying the bg will delete all the background values and replace them with something else
    def destroy(self):
        for _ in self.dir:
            del _
        for _ in dir(self):
            del _


"""FORMATION FOR GAMEPLAY--------------------"""
class Formation:
    def __init__(
            self,
            player,
            level, #levels in world
            file=None,
            total_level=1): #total level takes worlds into account

    # print("==============NEW FORMATION")

        #DEFINITIONS
        self.state="start" #level's state; "start","idle", and "complete"
        self.file=file #level's python file
        self.player=player #the player object
        self.level = level #current level number ; for intensities

        self.pos=[0,100] #position lol
        self.direction = random.choice(['l','r']) #direction, either 'l' or 'r'
        self.speed=0 #speed the formation moves in idle
        self.current_frame = 0 #calculating when to throw a character down, or when to spawn a character

        self.total_characters = 0 #total amount of characters
        self.spawn_list = {} #spawnlist
        self.spawned_formation = [] #spawned characters
        available_char = self.file.imports #characters that can be randomly generated

        #calculating characters to use
        self.used_char = [available_char[0]]
        if len(available_char) >= 2:
            chunk = self.file.level_length / (len(available_char)-1)
        
            for _ in range( int(level // chunk) ):
                if len(self.used_char) < len(available_char):
                    self.used_char.append(available_char[_+1])

        self.formation_size = [0,0] #size of the formation


        self.spawn_list=self.generate_spawn_list()


        #FORMATION SIZE
        # SPAWN*LIST* SIZE
        self.formation_size[1] = len(self.spawn_list)  # vertical size is figured out
        for row in self.spawn_list:
            if len(self.spawn_list[row]) > self.formation_size[0]:  # horizontal size is the longest row
                self.formation_size[0] = len(self.spawn_list[row])

        #CENTERING FORMATION BASED ON SIZE
        self.pos[0] = 225-(self.formation_size[0]*self.file.char_distance_x/2)

        #formation spawn code
        self.spawn_list_indexes=[]
        self.columns=0 #instead of using the y value for some things, we use *columns*, because some blank indexes get left out
        self.current_row=0 #this is so we know when to reset columns
        #this will append every index in the formation spawn list so the start state can add them in order without any complex loops
        for i in range(len(self.spawn_list)):
            self.spawned_formation.append([])
            for j in range(len(self.spawn_list[i])):
                self.spawn_list_indexes.append((i, j))

        #potential item spawn
        self.items_to_spawn = {}
        """puts an item in a character if the timing is right and the player has no shield"""
        if (self.player.bullet == "default") and (self.level%self.file.drop_health == 0):
            self.items_to_spawn[random.choice(self.spawn_list_indexes)] = ("health",None)
        """puts a bullet in a character if random chance"""
        if random.randint(0,100) < self.file.drop_bullet:
            self.items_to_spawn[random.choice(self.spawn_list_indexes)] = ("bullet",random.choice(self.file.bullets))
            # print("CONDITION MET")


    def update(self):
        #self-explanatory
        if self.state == "idle": self.idle()
        elif self.state == "start": self.start()
        elif self.state == "exit": self.exit()

        # self.update_size()
        self.update_character_formation_pos()
        if self.state != "start": self.remove_dead()


    def idle(self):
        #actually moving
        self.formation_move()
        #attacking based on time
        self.calculate_attack_time()

    def start(self):
        #moving formation
        self.formation_move()

        #checking if time has passed
        self.current_frame += 1

        if self.current_frame >= 20: #DEBUG - CHANGE TO 6
            
            # index = random.randint(0,len(self.spawn_))
            
            #resetting timer
            self.current_frame = 0

            #breaking out of start state to prevent error
            if len(self.spawn_list_indexes) <= 0:
                self.state = 'idle'
                return

            #resetting columns
            if self.spawn_list_indexes[0][0] != self.current_row:
                self.current_row = self.spawn_list_indexes[0][0]
                self.columns = 0


            #spawning a character
            try:
                #adds a character to the formation
                self.spawned_formation[self.spawn_list_indexes[0][0]].append(
                    loaded_characters[self.spawn_list[self.spawn_list_indexes[0][0]][self.spawn_list_indexes[0][1]]].Char(
                        args={ "groups": groups,
                               "player": self.player,
                               "formation_position": self.pos,
                               "offset":((self.spawn_list_indexes[0][1] * self.file.char_distance_x),(self.spawn_list_indexes[0][0] * self.file.char_distance_y)),
                               "level":self.level
                            }))
                """INDEX REFERENCE
                items_to_spawn: KEY, (row,column) ; VALUE, (item_type,item_name)
                spawned_formation: [FIRST BRACKET], LIST OF ROWS ; [SECOND BRACKET], CHARACTERS IN ROW
                """
                # print(self.spawned_formation)
                for key,value in self.items_to_spawn.items():
                    if key[0] <= (len(self.spawned_formation)-1):
                        # print("ROW CONDITION MET |",str(key),"|",str(self.spawned_formation))
                        if key[1] <= len(self.spawned_formation[key[0]])-1:
                            self.spawned_formation[key[0]][key[1]].container = value
                            # print("ITEM ADDED")
                            self.items_to_spawn.pop(key) ; break
                        else:
                            # print("COLUMN CONDITION NOT MET |", str(key) , str(self.spawned_formation[key[0]]))
                            pass

            #ignoring emtpy enemy spaces -
            except KeyError:
                self.spawn_list_indexes.pop(0)
                return

            #adding to group
            groups["universal"].add(self.spawned_formation[self.spawn_list_indexes[0][0]][self.columns])
            groups["enemy"].add(self.spawned_formation[self.spawn_list_indexes[0][0]][self.columns])

            #instead of using the y value for some things, we use *columns*, because some blank indexes get left out
            self.columns+=1

            #deleting index 0 so the next one is in line
            self.spawn_list_indexes.pop(0)

    def exit(self):
        self.current_frame += 1

        if self.current_frame >= 6:
            self.current_frame = 0
            groups["universal"].add(shared.dieBoom(self.spawned_formation[0][0].rect.center, (50, 50)))
            self.spawned_formation[0][0].state = "dead"
            self.spawned_formation[0][0].kill()



    def calculate_attack_time(self):
        #calculating when to make a character attack

        self.current_frame += 1
        total_attack_enemies = 0

        #calcuating the amount of enemies attacking
        for i in range(len(self.spawned_formation)):
            for j in range(len(self.spawned_formation[i])):
                if self.spawned_formation[i][j].state == "attack":
                    total_attack_enemies += 1

        #checking if the right amount of enemies are attacking and if enough time has passed
        if (self.file.maxChar is None or total_attack_enemies < self.file.maxChar) and (self.current_frame >= self.file.spawn_time):
            self.attack()
            self.current_frame = 0

    def attack(self):
        #current characters in idle
        idle_list = []

        #checks characters and adds ones in idle to idle_list
        for i in range(len(self.spawned_formation)):
            for j in range(len(self.spawned_formation[i])):
                if self.spawned_formation[i][j].state == "idle":
                    idle_list.append((i,j))

        #picking a random character to make attack
        if len(idle_list) > 0:
            chosen_list = random.choice(idle_list); del idle_list
            self.spawned_formation[chosen_list[0]][chosen_list[1]].state = "attack"
            return

    def update_character_formation_pos(self):
        #updating the characters on what the formation position is
        for i in range(len(self.spawned_formation)):
            for j in range(len(self.spawned_formation[i])):
                self.spawned_formation[i][j].formationUpdate(self.pos)

    def formation_move(self):
        #updating the movement

        #changing the direction from right to left
        if self.pos[0]>=(500-(self.formation_size[0]*self.file.char_distance_x)):
            self.speed-=self.file.speed*0.025
            self.direction='l'
        #changing the direction from left to right
        elif self.pos[0]<=10:
            self.speed+=self.file.speed*0.025
            self.direction='r'
        #speeding up if no direction change
        else:
            if self.direction=='l': self.speed = self.file.speed*-1
            elif self.direction == 'r': self.speed = self.file.speed
        #updating positions based on speed
        self.pos[0]+=self.speed
        self.pos[1]=(math.sin(self.pos[0]/10)*10 + 100)

    def random_spawn_list(self):
        #randomly generates characters and puts them in a formation
        formation = {}

        #column size based on current level
        column_size = int(
                self.file.char_min_width + #minimum value
                ((self.level / self.file.level_length)* #percent
                 (self.file.char_max_width - self.file.char_min_width)) #amount of variation
        )
        row_size = int(
                self.file.char_min_height +  # minimum value
                ((self.level / self.file.level_length) *  # percent
                 (self.file.char_max_height - self.file.char_min_height))  # amount of variation
        )

        # print(str(self.level) + "|" + str(self.file.level_length) + "|" + str(column_size) + "|" + str(row_size))


        for i in range(row_size): #row generation
            formation[i]=[]
            for j in range(column_size): #column generation
                formation[i].append(random.choice(self.used_char))
        return formation

    def generate_spawn_list(self):
        spawn_list={}
        #SPAWNLIST
        manual=len(self.file.manual_formations)>0 and self.file.manual_type!=0 #boolean value, figures out if formation is manual
        # manual spawn list
        if manual:
            #random manual formation
            if self.file.manual_type==1:
                #picks a random manual_formation a certain percent of the time, randomly generates one the other percent
                if random.randint(0,100) < self.file.manual_influence: #chance picks a manual formation
                    spawn_list=random.choice(self.file.manual_formations)
                else: #chance picks elsewise
                    spawn_list = self.random_spawn_list()
            #ordered manual formation
            elif self.file.manual_type==2:
                #nonlooping
                if not self.file.manual_loop:
                    #if level is within the length of the formations
                    if self.level <= len(self.file.manual_formations):
                        spawn_list = self.file.manual_formations[self.level-1] #level -1 because it doesn't start at 0
                    #if level has surpassed length of the formations
                    else:
                        spawn_list = self.random_spawn_list()
                #looping
                else:
                    #shedding the looped numbers off of levels
                    index = self.level - (len(self.file.manual_formations)*((self.level-1)//len(self.file.manual_formations)))
                    #setting formation
                    spawn_list = self.file.manual_formations[index-1]
        #random spawn list
        else:
            spawn_list = self.random_spawn_list()

        return spawn_list

    def update_size(self):
        #UPDATING SIZE BASED OFF SPAWN
        self.formation_size[1] = len(self.spawned_formation)  # vertical size is figured out
        for row in self.spawned_formation:
            if len(row) > self.formation_size[0]:  # horizontal size is the longest row
                self.formation_size[0] = len(row)

    def remove_dead(self):
        #deleting dead characters
        for row in range(len(self.spawned_formation)):
            for column in range(len(self.spawned_formation[row])):
                if self.spawned_formation[row][column].state == "dead":
                    self.spawned_formation[row].pop(column)
                break

        #deleting empty rows
        for row in range(len(self.spawned_formation)):
            if len(self.spawned_formation[row])==0:
                self.spawned_formation.pop(row)
                break

        #changing state to "complete" if there are no rows
        if len(self.spawned_formation) == 0:
            self.state = "complete"

    def destroy(self):
        #deletes all characters
        for i in range(len(self.spawned_formation)):
            for j in range(len(self.spawned_formation[i])):
                self.spawned_formation[i][j].kill()

        #empties
        self.spawned_formation = []
        self.state = "complete"


"""LEVEL ASSET CODE--------------------"""
class Level:
    def __init__(self, player, world_num):
        with open("levels/worldOrder.txt", "r") as _:
            self.worldOrder=eval(_.read())

        self.player = player
        self.level = 1
        self.level_in_world=1
        self.world_num = world_num
        self.world_num_looped = self.world_num - (self.world_num * (self.world_num//len(self.worldOrder)))
        self.worldData=loaded_levels
        self.world_ended=False
        self.world_file=None

        #refresh-world-data default values
        self.world_name=""
        self.bg = None
        self.form = None

        self.refresh_world_data()

    def refresh_world_data(self):
        #resetting values if they still exist
        self.level_in_world=1
        if self.form is not None:
            self.form.destroy()
            self.form=None

        if self.bg is not None:
            self.bg.destroy();del self.bg
            self.bg=None


        #looks at the list of worlds and figures out the world name based off the index of world_num
        self.world_name = self.worldOrder[self.world_num_looped-1]

        self.world_file = self.worldData[self.world_name].data(level=self.level)


        #loading the music
        sounds.play_song(str(self.world_file.worldInfo['songname']))

        #loading the background
        self.bg=BG(self.world_file.worldInfo['bg'])

        """fileReader will then pass off the worldData file to 'formation', as well as the current level"""
        if self.form is None:
            self.form=Formation(player = self.player,
                level=self.level,
                file=self.world_file)
        else:
            self.form.__init__(player = self.player,
                level=self.level,
                file=self.world_file)

        self.world_ended=False

        # print("NEW WORLD ||",str(self.level),str(self.level_in_world))


    def update(self):

        # try: #this is a try statement because there will be no form to check later

        self.form.update()  # updates the formation

        if self.form.state == "complete":
            
            """This is the reset code. It deletes self.form, raises the level by 1, and then re-makes self.form"""
            self.form.destroy()

            self.level+=1
            self.level_in_world+=1
            self.world_file.update_intensities(self.level)

            self.form.__init__(player=self.player,
                level=self.level,
                file=self.world_file)
                
            # print(str(self.level),str(self.level_in_world))


    def advance_world(self):
        self.world_num+=1
        self.world_num_looped = self.world_num - ( len(self.worldOrder) * ((self.world_num-1)//len(self.worldOrder)) )





"""STATES###############################################################"""

"""TITLE ASSETS--------------------"""
def title():
    # try:
    #IMAGE LOADING, FIRST AND FOREMOST
    #these are not preloaded because they are only needed like once

    run = True

    fps = 15 #TEST ENABLE
    start = time.time()
    frame = 0

    index = 1

    if not continue_song: sounds.play_song('title.mp3')

    #REDRAW_WINDOW IS ONLY FOR GRAPHICS. NO SOUND EFFECTS OR SPRITES.
    #redraw_window will show and hide sprites depending on what menu you're in and what index you have selected
    def redraw_window():

        #The main thing that plays in the title screen. The bg, the fizz effect, and the logo.
        window.blit(ui.title_bg, (0, 0))
        window.blit(ui.title_bg_logo[frame], (225 - (ui.title_bg_logo[frame].get_width() / 2), 25))

        #"START," "OPTIONS," and "QUIT" only appear during the first part of the title menu
        if index == 1:
            window.blit(ui.START[1], (150, 275))
        else:
            window.blit(ui.START[0], (150, 275))

        if index == 2:
            window.blit(ui.OPTIONS[1], (150, 375))
        else:
            window.blit(ui.OPTIONS[0], (150, 375))

        if index == 3:
            window.blit(ui.QUIT[1], (150, 475))
        else:
            window.blit(ui.QUIT[0], (150, 475))

        pygame.display.update() #TEST ENABLE


    while run:

        # timer code for the yup and logo frames
        end = time.time()
        if end - start >= 0.25:
            start = time.time()
            frame += 1
            if frame > (len(ui.title_bg_logo) - 1): frame = 0

        #tells the clock to tick at the rate of FPS
        clock.tick(fps)
        # print(clock.get_fps()) #TEST ENABLE

        #once it sets all the current image forms, it will then redraw the window
        redraw_window()

        for event in pygame.event.get():

            #Code to end the game if conditions are met.
            if event == pygame.QUIT:
                run = False


            #Code that checks for if a key is pressed.
            if event.type == pygame.KEYDOWN:

                #This code checks for an enter press.
                #It will always lock out the enter button if it is being held down. It waits until enter is released to register again.
                if event.key == pygame.K_j or event.key == pygame.K_SPACE:
                    sounds.sounds["select.mp3"].play()

                    #starting gameplay, returns a value telling main to use gameplay
                    if index == 1: sounds.stop_song(); return "start"

                    #If you picked options, it will open the options menu
                    elif index == 2: return "options"

                    # If you pick quit, or something else by some chance, the game will quit.
                    else:sounds.sounds["select.mp3"].play();time.sleep(0.5);run = False


                #Escape press for quitting games
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_k:
                    sounds.sounds["back.mp3"].play()


                #Item selection; changes index
                if event.key == pygame.K_w:
                    if index > 1: index -=1
                    sounds.sounds["scroll.mp3"].play()

                if event.key == pygame.K_s:
                    if index < 3: index +=1
                    sounds.sounds["scroll.mp3"].play()


"""OPTIONS ASSETS--------------------"""
def options():

    # UI settings
    run = True
    index = 0

    #QUICK NOTE -- options has no music, as it plays whatever was playing previously

    def redraw_window():
        # filling the bg and showing the title
        window.blit(ui.option_bg, (0, 0))
        # displaying the setting names
        y = 0
        for key in settings.keys():
            window.blit(loaded_text[key], (50, (y * 50) + 200))
            y += 1
        # displaying the setting values
        y = 0
        for value in settings.values():
            if value[1] == "onoff" and value[0]:
                window.blit(ui.yes, (150, ((y * 50) + 200)))
            elif value[1] == "onoff" and not value[0]:
                window.blit(ui.no, (150, ((y * 50) + 200)))
            elif value[1] == "3060" and value[0]:
                window.blit(ui.option_60, (150, ((y * 50) + 200)))
            elif value[1] == "3060" and not value[0]:
                window.blit(ui.option_30, (150, ((y * 50) + 200)))
            elif value[1] == "slider":
                window.blit(ui.slider, (150, ((y * 50) + 200)))
                window.blit(ui.knob, ((130 + (value[0] * 175)), ((y * 50) + 200)))
            y += 1
        # displaying the cursor
        window.blit(ui.cursor, (0, ((index * 50) + 200)))
        # self-explanatory: updating the display
        pygame.display.update() #TEST ENABLE
    redraw_window()

    fps=15

    while run:
        clock.tick(fps) #TEST ENABLE
        # print(clock.get_fps()) #TEST ENABLE

        # HARD-CODING PART FOR MUTE CODE. ERASE IF RE-USED.
        if settings["MUTE"][0]:
            settings["OST VOL"][0] = 0.0
            settings["SOUND VOL"][0] = 0.0

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_k or event.key == pygame.K_ESCAPE:
                    sounds.sounds["back.mp3"].play()
                    # writing the settings
                    return "title"

                if event.key == pygame.K_s and index < (len(settings) - 1):
                    sounds.sounds["scroll.mp3"].play()
                    index += 1
                    # print(index)
                if event.key == pygame.K_w and index > 0:
                    sounds.sounds["scroll.mp3"].play()
                    index -= 1
                    # print(index)
                if event.key == pygame.K_j or event.key == pygame.K_SPACE:
                    sounds.sounds["select.mp3"].play()
                    # list(settings)[index] is the key name
                    key_index = list(settings)[index]
                    if settings[key_index][1] == "onoff":
                        if not settings[key_index][0]:
                            settings[key_index][0] = True
                        elif settings[key_index][0]:
                            settings[key_index][0] = False
                    elif settings[list(settings)[index]][1] == "3060":
                        if not settings[key_index][0]:
                            settings[key_index][0] = True
                        elif settings[key_index][0]:
                            settings[key_index][0] = False
                    else:
                        sounds.sounds["denied.mp3"].play()
                if event.key == pygame.K_a:
                    sounds.sounds["select.mp3"].play()
                    # list(settings)[index] is the key name
                    key_index = list(settings)[index]
                    if settings[key_index][1] == "slider" and settings[key_index][0] > 0:
                        settings[key_index][0] -= 0.05
                        settings[key_index][0] = round(settings[key_index][0], 2)
                    else:
                        sounds.sounds["denied.mp3"].play()
                    # print(values[index])
                if event.key == pygame.K_d:
                    sounds.sounds["select.mp3"].play()
                    # list(settings)[index] is the key name
                    key_index = list(settings)[index]

                    # HARD-CODING PART FOR MUTE CODE. ERASE IF RE-USED.
                    if key_index == "OST VOL" or key_index == "SOUND VOL": settings["MUTE"][0] = False

                    # applying settings
                    if settings[key_index][1] == "slider" and settings[key_index][0] < 1:
                        settings[key_index][0] += 0.05
                        settings[key_index][0] = round(settings[key_index][0], 2)
                    else:
                        sounds.sounds["denied.mp3"].play()

                if event.key == pygame.K_p:
                    apply_settings()
                #only redraws the window when a setting is changed. No FPS needed.
                redraw_window()


"""PAUSE ASSETS--------------------"""
def pause(img=None): #it takes in the UI images as an argument to lower RAM usage and prevent leakage :)
    """-----PLEASE NOTE !-----
    pause is usually run as a state within a state
    it does not return the next state to be run within, but instead a time frame for how long it was used for
    got it?
    """

    sounds.play_song('meowchill.mp3')


    #sets the values
    fps=60;run=True;index = 1
    pause_start = time.time();graphic_start = time.time()
    graphic_frame = 1
    sounds.sounds["select2.mp3"].play()

    #updates every graphic onscreen
    def display_update():
        if img is None:window.fill("black")
        else:window.blit(img, (0, 0))

        window.blit(ui.pause[graphic_frame], ((225 - (ui.pause[graphic_frame].get_width() / 2)), 100))

        if index == 1: window.blit(ui.CONTINUE[1], ((225 - (ui.CONTINUE[1].get_width() / 2)), 275))
        else: window.blit(ui.CONTINUE[0], ((225 - (ui.CONTINUE[0].get_width() / 2)), 275))
        if index == 2: window.blit(ui.OPTIONS[1], ((225 - (ui.OPTIONS[1].get_width() / 2)), 375))
        else: window.blit(ui.OPTIONS[0], ((225 - (ui.OPTIONS[0].get_width() / 2)), 375))
        if index == 3: window.blit(ui.QUIT[1], ((225 - (ui.QUIT[1].get_width() / 2)), 475))
        else: window.blit(ui.QUIT[0], ((225 - (ui.QUIT[0].get_width() / 2)), 475))
        pygame.display.update()

    time_passed=0
    while run:
        #sets time values and raises graphic frames according to them
        end = time.time()
        time_passed = end-pause_start
        graphic_time = end-graphic_start
        if graphic_time >= 0.25 and graphic_frame < 2: graphic_frame += 1;graphic_start=time.time()
        elif graphic_time >= 0.25  and graphic_frame >= 2: graphic_frame = 1; graphic_start = time.time()
        else: pass

        display_update()
        clock.tick(fps)

        #taking input
        for event in pygame.event.get():

            if event == pygame.QUIT:
                sounds.stop_song()
                sounds.sounds["select2.mp3"].play()
                run = False
            if event.type == pygame.KEYDOWN:

                #UI
                if event.key == pygame.K_w:
                    if index > 1: index -= 1
                    sounds.sounds["scroll.mp3"].play()
                if event.key == pygame.K_s:
                    if index < 3: index += 1
                    sounds.sounds["scroll.mp3"].play()
                if event.key == pygame.K_j or event.key == pygame.K_SPACE:
                    sounds.sounds["select2.mp3"].play()
                    if index == 1:
                        sounds.stop_song()
                        run = False
                    if index == 2:
                        options()
                    if index == 3:
                        sounds.stop_song()
                        return "title"

    sounds.stop_song()
    return time_passed



"""GAME OVER----------------------"""
def game_over(level_class : Level = None, score : int = 0):
    run = True
    fps = 60

    quote = random.choice([
        "sheesh","you suck","BURN DOWN THE MCDONALD","nop\ne","is your monitor on","i don't know what to put on the screen","get better","greasy grove","ahhhhhhhhhhhhhh","computer aids cheese","i love men",
        "POOPENFARTEN ","FORT NITE gntals","this is a sentence","ink sacs","grummy bear","shloppy", "TOOTH PASTE !" , "JOHNNY BALLSICKLE", "DO NOT THROW BANANAS AT GOATS" , "I AM THE MASTER ABLEIST",
        "COMMUNISM", "CAPITALISM", "ANARCHISM", "CLOROX SUCKS", "KRUEGER CLICKER", "WHERE IS MY WIFE?", "PROMORTOIJNNSOFKJAAS:LFAJFEO:DFKJIHADFH" , "?????", "EDGY WOLF TEEN MEETS BAND KID",
        "TOXIC MASCULINITY", "SQUID", "THE LOBOTOMY IS CONFIRMED", "TODAY IS THE LAST DAY", "I AM BALDING    ?",   "   W E D N E S D A Y   ",
        "THAT'S WHAT I'M SAYING", "WHAT THE DOG DOIN", "HELP", "I LOVE THE CCP", "SAVE THE TURTLES", "SAVE THE TREES", "I HATE EARTH DAY", "     WHEN", "when", " FORT     NIGHT   "
    ]).upper()
    quote_index = 0
    built_quote = ""

    """THERE ARE TWO STATES: slowdown and results
    slowdown will slow both the background and formation down, eventually throwing the formation offscreen
    results simply displays the score over a cute little game over image"""
    state = "slowdown"
    """the results state is a number that pretty much goes [sign animation, score display, quote display, wait, fly down]"""
    state_results = 0


    """it fetches the background image in order to remove the bulk of BG"""
    bg_image_1 = level_class.bg.dir[0]
    """it also fetches the scroll values as to not modify the original config file"""
    scroll_values = [level_class.bg.config['scrollHoriz'],level_class.bg.config['scrollVert']]

    """Stopping the music."""
    sounds.stop_song()
    """Killing the formation"""
    level_class.form.state = "exit"

    """game over image positioning"""
    game_over_image_x = 0
    """pause stops the game over thing from progressing"""
    center = 225-(ui.game_over_sign.get_width()/2)

    """for state 1 - this is a counter to give the score more personality"""
    score_counter = 0

    """frame counter that is used for checking how long each result_state should be in"""
    timer = 0

    while run:
        clock.tick(fps)

        if state == "slowdown":

            """THE BACKGROUND SLOWDOWN
            this still uses the background class, and it begins to slow down the scroll speed of the background if there is any
            when the background speed hits 0.01 or less, or if there is no config, it kills the background, and sets the state to "results" """
            if level_class.bg.config is not None and (scroll_values[1]>0.1 or scroll_values[0]>0.1):
                """when the background and formation are still alive and well"""
                scroll_values[0] *= 0.95
                scroll_values[1]*=0.95
                level_class.bg.update(scroll_values = scroll_values)
                level_class.bg.display_bg()
                """updating the formation, including deleting the characters"""
                level_class.form.update()

            elif level_class.bg.config is None or (scroll_values[1]<=0.1 or scroll_values[0]<=0.1):
                """it will just kill the bg if there is no config present, meaning there is no scroll"""
                level_class.bg.destroy()
                level_class.form.destroy()
                del level_class.form, level_class.bg
                for _ in groups.values():
                    _.empty()
                state = "results"
        
        elif state == "results":
            # print(state_results)
            """THE ACTUAL RESULTS CODE
            this is based on the state, either 0,1,2, or 3.
            the state of 0 is kind of unneeded since pause_x exists but whatever"""

            """unrelated updates that play in several instances"""
            if state_results == 0 and game_over_image_x == 200:
                state_results = 1

            if state_results == 0 or state_results == 3:
                """beginning and end code"""
                game_over_image_x += 1


            elif state_results == 1:
                """updating score - graphical score is displayed elsewhere"""
                score_counter = score_counter + int(round( ((score-score_counter)/50) , 0 )) if abs(score_counter - score) > 50 else score

                """exits if condition is met and timer is over"""
                if abs(score_counter - score) < 50:
                    score_counter = score
                    timer = 0
                    state_results = 2

            elif state_results == 2:
                """updating timer"""
                timer += 1
                """displaying funny quote"""
                if timer >= 3 and built_quote != quote:
                    # print("building onto quote")
                    built_quote += quote[quote_index]
                    quote_index += 1
                    timer = 0
                elif timer >= 300:
                    timer = 0
                    state_results = 3


            window.blit(bg_image_1,(0, 0))
            window.blit(ui.game_over_sign,(center, 0.05*((game_over_image_x-200)**2) ))



        #handling EXITING
        for event in pygame.event.get():
            if event == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        """RETURNING THE CODE
        game_over_image_x is used as its the counter that is used at the beginning and end"""
        if game_over_image_x > 300: return

        """DRAWING ITEMS
        the universal group draws all the sprites at the end
        if it did it before, the background would go over it"""
        groups["universal"].update()
        groups["universal"].draw(window)
        """this draws the score and the quote"""
        if state_results == 1 or state_results == 2:
            draw_text(score_counter, coord = (125,150), snap_direction='l', size = 35)
        if state_results == 2:
            draw_text(built_quote, coord = (125,200), snap_direction = 'l', size = 25)
        pygame.display.update()



"""LEVEL COMPLETE"""
def level_complete(level_class : Level = None, player : loaded_characters["player"].Player = None):

    #startup info
    FPS = 60
    run = True

    """SOUND EDITING
    this is specifically stopping channel 1 as this should not play outside of main"""
    sounds.play_song("Detention.mp3")

    """BG SPEED STARTUP
    this will make the speeds speed up and slow down depending on things
    during the speedup, it applies the little speed effect 1000 times
    during the slowdown, it slows it down by 0.95 until it hits the desired speed of the next bg"""
    state = "speedup"
    scroll_values = [level_class.bg.config['scrollHoriz'],level_class.bg.config['scrollVert']]
    speedups_applied = 0
    """default scroll value"""
    if scroll_values[0] == 0 and scroll_values[1] == 0:
        scroll_values = [1,0]


    """TEXT VISUALS
    During this transition, there is a cute little thing with text scrolling by for just a tinge of nice visual effect
    This will dictate the list of random text you get, or specifically if it says "YOU DID GREAT" or "YOU SUCK!" """
    inspirational_list = ["WOW!","YOU'RE WINNER!"]
    if player.health > 1: inspirational_list.append("YOU DID GREAT!")
    else: inspirational_list.append("YOU SUCK!")
    """The world name has an error where, if you look past the range of the worlds, an error is raised
    this will prevent that."""
    next_world_number = 0 if level_class.world_num_looped > (len(level_class.worldOrder)-1) else level_class.world_num_looped
   
    
    level_class.form.state = "dead" #fuly stops the playstate
    level_class.form.destroy() #kills everything in playstate

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                # print(speedups_applied)
                pass
            player.controls(event)


        """SPEEDING UP THE BACKGROUND"""
        if state == 'speedup' and speedups_applied < 256:
            speedups_applied+=1 
            """applying background change"""
            scroll_values = [scroll_values[0]*1.025,scroll_values[1]*1.025] if scroll_values[0] < 100 and scroll_values[1] < 100 else scroll_values
        
            #TEXT EFFECT
            if speedups_applied % 5 == 0:
                size,speed = random.randint(20,30),random.randint(5,7)
                text = Text(
                    pos=(random.choice([-150,600]),0), 
                    vertex=(0,random.randint(0,600) ),
                    modifier = random.uniform(0.1,20), 
                    modifier2 = random.uniform(0.005,0.05),
                    pattern="sine", 
                    speed=random.choice([-1*speed,speed]), 
                    text=random.choice(inspirational_list), 
                    size = size)
                groups["universal"].add(text)
                # print(len(universal_group))
            
            #"WORLD COMPLETE! text"
            if speedups_applied == 1: 
                text = Text(pos=(225,0), vertex=( 0 , 50 ),modifier = 3, modifier2 = 0.75, size = 40,duration = 384,
                    pattern="static sine", speed=1, text="STAGE COMPLETE!", )
                groups["universal"].add(text);groups["priority"].add(text)
            #2
            if speedups_applied == 64: 
                text = Text(pos=(225,0), vertex=( 0 , 100 ),modifier = 3, modifier2 = 1,size = 40,duration = (380-64),
                    pattern="static sine", speed=1, text="WARPING TO", )
                groups["universal"].add(text);groups["priority"].add(text)
            #3
            if speedups_applied == 112: 
                text = Text(pos=(225,0), vertex=( 0 , 150 ),modifier = 5, modifier2 = 2, size = 40,duration = (376-112),
                    pattern="static sine", speed=1, text=str(level_class.worldOrder[next_world_number]))
                groups["universal"].add(text);groups["priority"].add(text)
            #4
            if speedups_applied == 208: 
                text = Text(pos=(225,0), vertex=( 0 , 200 ),modifier = 3, modifier2 = 0.75, size = 40,duration = (372-208),
                    pattern="static sine", speed=1, text="BONUSES:")
                groups["universal"].add(text);groups["priority"].add(text)




        #FINISHING SPEEDUP
        elif state == 'speedup' and speedups_applied >= 256:
            state = 'slowdown'
            level_class.advance_world()
            level_class.refresh_world_data()
        # SLOWDOWN
        elif state == 'slowdown' and (
            abs(scroll_values[0] - level_class.bg.config["scrollHoriz"]) > 1 or abs(scroll_values[1] - level_class.bg.config["scrollVert"]) > 1):

            scroll_values = [
                scroll_values[0]*0.95,
                scroll_values[1]*0.95
            ]
        #RECENTERING THE BACKGROUND
        elif state == "slowdown" and ( abs(level_class.bg.bgX) > 10 or abs(level_class.bg.bgY) > 10 ):
            
            #RECENTERING BG
            if level_class.bg.bgX < -10:
                level_class.bg.bgX += 5
            elif level_class.bg.bgX > 10:
                level_class.bg.bgX -= 5
            if level_class.bg.bgY < -10 or level_class.bg.bgY > 10:
                level_class.bg.bgY += 5

        else: 
            level_class.bg.bgX = level_class.bg.bgY = 0
            # print(level_class.bg.bgX)
            # print(level_class.bg.bgY)
            # print("COMPLETE")
            run = False

        
        """ALL UPDATES"""
        groups["universal"].update()
        level_class.bg.update(scroll_values = scroll_values)
        level_class.bg.display_bg()
        groups["universal"].draw(window)
        groups["priority"].draw(window) #priority graphical
        pygame.display.update()


"""GAMEPLAY ASSETS--------------------"""
def play(bullet_shared=loaded_bullets["shared"]):

    # CREATING THE PLAYER
    player = loaded_characters["player"].Player(
        sounds=sounds,
        loaded_bullets=loaded_bullets,
        groups = groups
    )
    groups["universal"].add(player)
    groups["player"].add(player)


    world_num=1

    if not settings["FPS"][0]:
        loop=2
        fps=30

    else:
        loop = 1
        fps = 60 #TEST ENABLE

    run = True  # Variable that tells the game to loop

    # LEVEL INITIALIZATION
    level_class = Level(player=player,world_num=world_num)


    graphical=True #this is for debug purposes, where if you turn it off, the display turns off but the framerate rises heavily
    time_pos = 0 #positioning for songs

    def exit_state():
        for _ in groups.values():
            _.empty()


    def redraw_window():

        level_class.bg.display_bg()
        groups["universal"].draw(window) 

        # UI
        # bullet_shared.display_bullet(window, (0, 0), player.current_weapon, loaded_bullets)
        player.display_health(window, 0)
        # draw_text(player.score, (450, 0), window)
        draw_score(player.score,x=450)


        # FINISHING WITH AN UPDATE STATEMENT
        if graphical:pygame.display.update()


    def update_sprites():
        groups["universal"].update()
        level_class.bg.update()


    # VARIABLE DEFINITIONS WHEN THE CODE BEGINS.

    switch_frames=0

    while run:

        #DEBUG REMOVE
        switch_frames+=1
        if switch_frames>60:
            # level_class.advance_world()
            # level_class.refresh_world_data()
            switch_frames=0

        if graphical:clock.tick(fps)
        else:clock.tick(0)

        #FPS code: running values twice if graphical FPS is halved
        for _ in range(loop):
            update_sprites()

        # graphical updates
        redraw_window()
        level_class.update()

        #game over initialization
        if player.state == "dead":
            game_over(level_class=level_class, score=player.score)
            exit_state()
            return "title"
      
        #finishing the level
        if level_class.level_in_world > level_class.world_file.level_length:
            level_complete(level_class,player)
            time_pos = 0

        # inputs
        for event in pygame.event.get():

            # QUIT GAME CODE
            if event.type == pygame.QUIT:
                run = False


            # PAUSE CODE
            if event.type == pygame.KEYDOWN:

                # pause code
                if event.key == pygame.K_i or event.key == pygame.K_ESCAPE:
                    # freezes everything and opens the pause menu
                    player.reset_movement()

                    #fetching the time from the song being played, as the music will stop
                    time_pos += pygame.mixer.music.get_pos()
                    result =  pause(img=level_class.bg.dir[0])
                    sounds.play_song(str(level_class.world_file.worldInfo['songname']),pos=time_pos)

                    # If an error occurs, or any exit code is brought up, it spits you back at the title
                    if type(result) != float:
                        exit_state()
                        return "title"  # Sends the character into "title state", removing every single bit of progress made.


            # PLAYER CONTROLS
            player.controls(event)

            # DEBUG CODE
            if event.type == pygame.KEYDOWN:

                #swaps the graphical setting
                if event.key==pygame.K_1:
                    if graphical:graphical=False
                    else:graphical=True
                if event.key==pygame.K_2:
                    level_class.advance_world()
                    level_class.refresh_world_data()
                if event.key == pygame.K_3:
                    level_complete(level_class,player)






"MAIN LOOP###############################################################"
next_state = "title"
run = True
while run:
    #ADJUSTS THE VOLUME EVERY SINGLE TIME A STATE CHANGES
    short_load()

    if type(next_state) == str:
        if next_state == "start":
            long_load()
            next_state = play()
            # shortLoad()
            continue

        elif next_state == "title":
            next_state = title()
            continue_song = False #resetting title state song restart
            continue

        elif next_state == "options":
            next_state = options()
            continue_song = True #tells title state not to restart song
            continue
        
        else:
            run = False

    elif next_state is None:
        run = False

    else:
        run = False

with open("./assets/settings.txt", "w") as data:
    data.write(str(settings))

exit()