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

universal_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

# input("AFTER INITIALIZING PYGAME")

"""LOADING#################################################################"""

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

# print(loaded_characters)

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
    while True:
        try:

            # print(prefix)
            item=pygame.image.load(('./assets/images/bg/' + directory + '/' + prefix[0] + str(curFrame) + prefix[1] + '.png'))
            item=pygame.transform.scale(item,(450,600)).convert_alpha()
            loaded_backgrounds[directory][1].append(item) #adds item to main directory

            #updates the current frame
            curFrame+=1

        #if an error occurs, the search is complete
        except FileNotFoundError:
            curFrame=1
            break
        break #debug remove - makes there only one image

# input("LOADED BACKGROUNDS")

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

# input("LOADED BULLETS")

"""UI IMAGES---"""
class UiImages:

    #BEGIN AND END
    beginImage = pygame.image.load("./assets/images/UI/BEGIN AND END/GET READY.png")
    endImage = pygame.image.load("./assets/images/UI/BEGIN AND END/LEVEL COMPLETE.png")

    #ERRORS
    error_title = pygame.image.load("./assets/images/UI/errors/error_occurred.png")

    #LOGO FOR TITLE
    logo1 = pygame.image.load("./assets/images/UI/title/logo1.png")
    logo2 = pygame.image.load("./assets/images/UI/title/logo2.png")
    logo3 = pygame.image.load("./assets/images/UI/title/logo3.png")
    title_bg_logo = [logo1, logo2, logo3]
    del logo1, logo2, logo3

    #PAUSE GRAPHIC
    pause1=pygame.image.load('./assets/images/UI/pause/paus\'d (1).png')
    pause2=pygame.image.load('./assets/images/UI/pause/paus\'d (2).png')
    pause3=pygame.image.load('./assets/images/UI/pause/paus\'d (3).png')

    pause=[pause1,pause2,pause3]
    for _ in range(len(pause)):
        pause[_]=pygame.transform.scale(pause[_],(450,150)).convert_alpha()
    del pause1,pause2,pause3

    #PRESS SPACE
    press_space = pygame.image.load("./assets/images/UI/space.png")

    #BUTTONS
    quit_button = pygame.image.load("./assets/images/UI/quit_button.png")
    quit_button_pressed = pygame.image.load("./assets/images/UI/quit_button_pressed.png")
    QUIT = [quit_button, quit_button_pressed]
    del quit_button, quit_button_pressed

    start_button = pygame.image.load("./assets/images/UI/start_button.png")
    start_button_pressed = pygame.image.load("./assets/images/UI/start_button_pressed.png")
    START = [start_button, start_button_pressed]
    del start_button, start_button_pressed

    options_button = pygame.image.load("./assets/images/UI/options_button.png")
    options_button_pressed = pygame.image.load("./assets/images/UI/options_button_pressed.png")
    OPTIONS = [options_button, options_button_pressed]
    del options_button, options_button_pressed

    continue_button = pygame.image.load("./assets/images/UI/continue_button.png")
    continue_button_pressed = pygame.image.load("./assets/images/UI/continue_button_pressed.png")
    CONTINUE = [continue_button, continue_button_pressed]
    del continue_button,continue_button_pressed

    #LOADING
    loading = pygame.image.load("./assets/images/UI/loading/load_small.png")

    #GENERAL
    yes = pygame.image.load("./assets/images/UI/YES.png")
    yes = pygame.transform.scale(yes, (50, 25))
    no = pygame.image.load("./assets/images/UI/NO.png")
    no = pygame.transform.scale(no, (50, 25))
    on = pygame.image.load("./assets/images/UI/ON.png")
    off = pygame.image.load("./assets/images/UI/OFF.png")
    checkmark = pygame.image.load("./assets/images/UI/CHECKMARK.png")
    xmark = pygame.image.load("./assets/images/UI/X.png")
    slider = pygame.image.load("./assets/images/UI/slider.png")
    knob = pygame.image.load("./assets/images/UI/knob.png")

    #SETTINGS IMAGES
    option_bg = pygame.transform.scale(pygame.image.load("./assets/images/UI/options/bg.png"), (450, 600))
    option_30 = pygame.transform.scale(pygame.image.load("./assets/images/UI/options/FPS30.png"),(50,30))
    option_60 = pygame.transform.scale(pygame.image.load("./assets/images/UI/options/FPS60.png"),(50,30))

    #BAGKGROUNDS
    title_bg = pygame.transform.scale(pygame.image.load("./assets/images/UI/title/background.png"), (450, 600))
    error_bg = pygame.transform.scale(pygame.image.load("./assets/images/UI/errors/bg.png"), (450, 600))
    load_bg = pygame.transform.scale(pygame.image.load("./assets/images/UI/splash.png"), (450, 600))

    #CURSOR
    cursor = pygame.image.load("./assets/images/UI/LIVES/000.png")

ui=UiImages #this creates an object of the class. this is what everything refers to

# input("LOADED UI")

"""SOUNDS---"""

class Sounds:

    def __init__(self):
        ###################SOUNDS####################

        self.sounds = {}
        self.ost = {}

        self.offsetSounds = {}
        ##############################################

    ###############FUNCTIONS###############-

    def play_song(self,song_name):
        # return
        with open('./assets/settings.txt','r') as data:
            vol=eval(data.read())['OST VOL'][0]
        self.ost[str(song_name)].set_volume(vol)
        pygame.mixer.Channel(0).play(self.ost[str(song_name)],loops=-1)


    @staticmethod
    def stop_song():
        pygame.mixer.Channel(0).stop()

    def play_nonmain_song(self,song):
        # return
        #This is specifically because if you replace the music file being played, in a menu for instance, it will not remember any song played before.
        #If you pause the game, it replaces the gameplay music with the pause music, and forges all about the gameplay music.
        with open('./assets/settings.txt','r') as data:
            vol=eval(data.read())['OST VOL'][0]
        self.ost[song].set_volume(vol)
        pygame.mixer.Channel(1).play(self.ost[song],loops=-1)
        return self.ost[song]
    #songs are easily stopped on their own and do not need a stop function


    def adjust_sounds(self, volume):
        for sound in self.sounds.values():
            sound.set_volume(volume)
        self.apply_offsets()
        # death.set_volume(death.get_volume() / 2)


    @staticmethod
    def adjust_ost(volume=None):

        if volume is not None:
            pygame.mixer.music.set_volume(volume)

        else:
            with open('./assets/settings.txt','r') as data:volume=eval(data.read())['OST VOL'][0]
            pygame.mixer.music.set_volume(volume)


    def apply_offsets(self):
        pass
        # for k,v in self.offsetSounds.items():
        #
        #     volume=self.soundList[self.soundList.index(k)].get_volume()*v
        #
        #     self.soundList[self.soundList.index(k)].set_volume(volume)

sounds=Sounds();sounds.apply_offsets()#this creates an object of the class. this is what everything refers to

for sound in os.listdir("./assets/sounds/"):
    sounds.sounds[str(sound)] = pygame.mixer.Sound("./assets/sounds/" + str(sound))

# input("LOADED SOUND EFFECTS")

sounds.ost["pause.mp3"] = pygame.mixer.Sound("./assets/ost/pause.mp3")
for song in os.listdir("./assets/ost/"):
    if ".mp3" not in song:
        continue
    else:
        sounds.ost[str(song)] = pygame.mixer.Sound("./assets/ost/" + str(song))


# print(sounds.container)


"""FINISHING---"""

del x,photo, prefixList, curFrame,directory, temp, the_code, i





"""SHARED ASSETS##############################################################"""

"""APPLYING SETTINGS--------------------"""
def read_apply_settings(settings_dict=None, nonmain_song=None):

    if settings_dict is None:
        with open("assets/settings.txt", "r") as data:
            # print("settings not present | settings file read")
            settings_dict = eval(data.read())

    fullscreen = settings_dict["FULLSCREEN"][0]

    # audio adjust
    sounds.adjust_sounds(settings_dict['SOUND VOL'][0])
    sounds.adjust_ost(settings_dict['OST VOL'][0])
    if nonmain_song is not None: nonmain_song.set_volume(settings_dict['OST VOL'][0])

    # screen adjust
    if fullscreen:
        pygame.display.set_mode((450, 600), pygame.FULLSCREEN | pygame.SCALED)
    else:
        pygame.display.set_mode((450, 600), pygame.SCALED)

    return settings_dict

settings=read_apply_settings()


"""DEBUG TEXT--------------------"""
def debug_displays(sprite_class_dict, variables, time_passed, fps, level, win=None):

    #adding items to the print list
    base_text= ["-DEBUG-", "FPS:" + str(round(fps, 1)), "TIME:" + str(round(time_passed, 1)), "LEVEL:" + str(level)]

    for key, value in variables.items():
        base_text.append(str(key) + "-var:" + str(len(value)))

    base_text.append("ALL SPRITES:" + str(len(universal_group)))

    for key,value in sprite_class_dict.items():
        base_text.append(""+str(key)+":"+str(len(value)))


    #displaying the print list
    if win is None:
        print(base_text)

    else:
        for _ in range(len(base_text)):
            font = pygame.font.Font("./assets/font/Setfont-Regular.ttf", 20)
            surface = font.render(str(base_text[i]), True, "white")
            window.blit(surface, (0, ((i * 20) + 30)))
            del surface,font

    del base_text


"""LOADING--------------------"""
def long_load():
    window.blit(ui.load_bg, (0, 0))

    pygame.display.update()

long_load()

def short_load():
    window.blit(ui.loading, (0, 0))

    pygame.display.update()


"""SCORE DISPLAY--------------------"""
def display_score(score_value, coord, snap=True, shadow=True, color=(255, 255, 255), shadow_color=(0, 0, 0), size=20):

    score_font = pygame.font.Font("./assets/font/Setfont-Regular.ttf",size)

    if shadow: score_surface = score_font.render(str(score_value), True, color, shadow_color)
    else: score_surface = score_font.render(str(score_value), True, color)
    
    score_rect = score_surface.get_rect()

    if snap:score_rect.right = coord[0]
    else: score_rect.center = coord

    window.blit(score_surface, score_rect)

    del score_font,score_rect,score_surface


# input("LOADED IMPORTANT FUNCTIONS")







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


    #This is the code that will run on-frame.
    #It does not display the background, just update the current image to *be* displayed.
    def update(self):
        # print(self.photoName)

        window.fill("black")#initial screen fill in case of transparency


        #present config
        if self.config is not None:
            #scroll code
            self.curFrame += 1
            self.bgY += self.config['scrollVert']
            self.bgX += self.config['scrollHoriz']
            if self.bgY >= 600 or self.bgY <= -600: self.bgY=0
            if self.bgX >= 450 or self.bgX <= -450: self.bgX=0

            #RESETTING THE FRAME
            if self.curFrame>=len(self.dir):self.curFrame=0

        #absent config
        else:
            self.curFrame+=1 #advancing frame

            if self.curFrame >= len(self.dir): self.curFrame = 0 #resetting frame


    # Duplicating images around current background to make the background look like it is repeating
    def decoys(self):
        if self.bgY != 0:
            window.blit(self.dir[self.curFrame], (self.bgX, self.bgY - 600))
            window.blit(self.dir[self.curFrame], (self.bgX, self.bgY + 600))

        if self.bgX != 0:
            window.blit(self.dir[self.curFrame], (self.bgX + 450, self.bgY))
            window.blit(self.dir[self.curFrame], (self.bgX - 450, self.bgY))

        if self.bgY != 0 and self.bgX != 0:
            window.blit(self.dir[self.curFrame], (self.bgX + 450, self.bgY - 600))
            window.blit(self.dir[self.curFrame], (self.bgX - 450, self.bgY + 600))
            window.blit(self.dir[self.curFrame], (self.bgX + 450, self.bgY + 600))
            window.blit(self.dir[self.curFrame], (self.bgX - 450, self.bgY - 600))

        return

    #Displaying the bg is treated differently due to fps changes in gameplay
    def display_bg(self):
        window.blit(self.dir[self.curFrame],(self.bgX,self.bgY))
        if self.config is not None: self.decoys()


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
                        args={ "groups": {"universal":universal_group,"bullet":bullet_group,"enemy":enemy_group},
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
            universal_group.add(self.spawned_formation[self.spawn_list_indexes[0][0]][self.columns])
            enemy_group.add(self.spawned_formation[self.spawn_list_indexes[0][0]][self.columns])

            #instead of using the y value for some things, we use *columns*, because some blank indexes get left out
            self.columns+=1

            #deleting index 0 so the next one is in line
            self.spawn_list_indexes.pop(0)

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
        with open("levels/worldOrder.txt", "r") as data:
            self.worldOrder=eval(data.read())

        self.player = player
        self.level = 1
        self.level_in_world=1
        self.world_num = world_num
        self.world_num_looped = self.world_num - (self.world_num * (self.world_num//len(self.worldOrder)))
        self.worldData=loaded_levels
        self.world_ended=False
        self.world_file=None

        #refresh-world-data default values
        self.worldName=""
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
        self.worldName = self.worldOrder[self.world_num_looped-1]

        self.world_file = self.worldData[self.worldName].data(level=self.level)


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


        # except AttributeError: pass

    def advance_world(self):
        self.world_num+=1
        self.world_num_looped = self.world_num - ( len(self.worldOrder) * ((self.world_num-1)//len(self.worldOrder)) )

        # print(str(self.world_num),"|",str(self.world_num_looped))



"""STATES###############################################################"""

"""TITLE ASSETS--------------------"""
def title():
    # try:
    #IMAGE LOADING, FIRST AND FOREMOST
    #these are not preloaded because they are only needed like once

    run = True

    fps = 15 #TEST ENABLE
    clock = pygame.time.Clock()
    start = time.time()
    frame = 0

    index = 1

    #GETS DA SOUNDS TO PLAY
    sounds.play_song('title.mp3')

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
                exit()


            #Code that checks for if a key is pressed.
            if event.type == pygame.KEYDOWN:

                #This code checks for an enter press.
                #It will always lock out the enter button if it is being held down. It waits until enter is released to register again.
                if event.key == pygame.K_j:
                    sounds.sounds["select.mp3"].play()

                    #starting gameplay, returns a value telling main to use gameplay
                    if index == 1: sounds.stop_song(); return "start"

                    #If you picked options, it will open the options menu
                    elif index == 2: sounds.stop_song(); return "options"

                    # If you pick quit, or something else by some chance, the game will quit.
                    else:sounds.sounds["select.mp3"].play();time.sleep(0.5);run = False;exit()


                #Escape press for quitting game
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_k:
                    sounds.sounds["back.mp3"].play()
                    exit()


                #Item selection; changes index
                if event.key == pygame.K_w:
                    if index > 1: index -=1
                    sounds.sounds["scroll.mp3"].play()

                if event.key == pygame.K_s:
                    if index < 3: index +=1
                    sounds.sounds["scroll.mp3"].play()




"""OPTIONS ASSETS--------------------"""
def options():
    def render_text(text):
        font = pygame.font.Font("./assets/font/Setfont-Regular.ttf", 50)
        surface = pygame.transform.scale(font.render(str(text), True, "white"), (75, 40))

        return surface

    sounds.play_nonmain_song("pause.mp3")

    # Reads a dictionary, with the index name and the values associated with it
    settings_keys_images = {}

    # Compiling a dictionary of rendered text to be displayed for the items
    for key in settings.keys(): settings_keys_images[key] = render_text(str(key))

    # UI settings
    run = True
    index = 0

    def redraw_window():
        # filling the bg and showing the title
        window.blit(ui.option_bg, (0, 0))
        # displaying the setting names
        y = 0
        for value in settings_keys_images.values():
            window.blit(value, (50, (y * 50) + 200))
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

    clock=pygame.time.Clock()
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

                if event.key == pygame.K_k:
                    sounds.sounds["back.mp3"].play()
                    # writing the settings
                    sounds.ost["pause.mp3"].stop()
                    return "title"

                if event.key == pygame.K_s and index < (len(settings) - 1):
                    sounds.sounds["scroll.mp3"].play()
                    index += 1
                    # print(index)
                if event.key == pygame.K_w and index > 0:
                    sounds.sounds["scroll.mp3"].play()
                    index -= 1
                    # print(index)
                if event.key == pygame.K_j:
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
                    read_apply_settings(settings, sounds.ost["pause.mp3"])
                    with open("./assets/settings.txt", "w+") as data:
                        data.write(str(settings))
                #only redraws the window when a setting is changed. No FPS needed.
                redraw_window()




"""PAUSE ASSETS--------------------"""
def pause(img=None): #it takes in the UI images as an argument to lower RAM usage and prevent leakage :)
    """-----PLEASE NOTE !-----
    pause is usually run as a state within a state
    it does not return the next state to be run within, but instead a time frame for how long it was used for
    got it?
    """

    sounds.play_nonmain_song('pause.mp3')


    #sets the values
    fps=60;run=True;clock = pygame.time.Clock();index = 1
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
                if event.key == pygame.K_j:
                    sounds.sounds["select2.mp3"].play()
                    if index == 1:
                        sounds.ost["pause.mp3"].stop()
                        run = False
                    if index == 2:
                        sounds.ost["pause.mp3"].stop()
                        options()
                        sounds.play_nonmain_song('pause.mp3')
                    if index == 3:
                        sounds.ost["pause.mp3"].stop()
                        return "title"

    sounds.ost["pause.mp3"].stop()
    return time_passed




"""GAMEPLAY ASSETS--------------------"""
def play(bullet_shared=loaded_bullets["shared"],settings=None):

    # DEALING WITH SETTINGS:
    if settings is None:
        settings = read_apply_settings()


    # CREATING THE PLAYER
    player = loaded_characters["player"].Player(
        sounds=sounds,
        loaded_bullets=loaded_bullets,
        groups = {
            "universal":universal_group,
            "bullet":bullet_group,
            "enemy":enemy_group
            }
    )
    universal_group.add(player)
    player_group.add(player)


    world_num=1

    if not settings["FPS"][0]:
        loop=2
        fps=30

    else:
        loop = 1
        fps = 60 #TEST ENABLE

    run = True  # Variable that tells the game to loop
    clock = pygame.time.Clock()  # The clock is essentially just a thing that tells the computer to update the screen after a set period of time.
    # LEVEL INITIALIZATION
    level_class = Level(player=player,world_num=world_num)


    graphical=True #this is for debug purposes, where if you turn it off, the display turns off but the framerate rises heavily


    def exit_state(state_list=(enemy_group, bullet_group, player_group, universal_group)):
        for item in state_list:
            item.empty()


    def redraw_window():

        level_class.bg.display_bg()
        universal_group.draw(window) 

        # UI
        # bullet_shared.display_bullet(window, (0, 0), player.current_weapon, loaded_bullets)
        player.display_health(window, 0)
        display_score(player.score, (450, 0), window)


        # FINISHING WITH AN UPDATE STATEMENT
        if graphical:pygame.display.update()


    def update_sprites():
        universal_group.update()
        level_class.bg.update()


    # VARIABLE DEFINITIONS WHEN THE CODE BEGINS.

    switch_frames=0

    while run:
        # print(str(clock.get_fps()),str(player.score))

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
            exit_state()
            return "title"



        # inputs
        for event in pygame.event.get():

            # QUIT GAME CODE
            if event.type == pygame.QUIT:
                run = False
                exit()


            # PAUSE CODE
            if event.type == pygame.KEYDOWN:

                # pause code
                if event.key == pygame.K_i:
                    # freezes everything and opens the pause menu
                    player.reset_movement()

                    pygame.mixer.Channel(0).pause()

                    time_paused =  pause(img=level_class.bg.dir[0])

                    # If an error occurs, or any exit code is brought up, it spits you back at the title
                    if type(time_paused) != float:
                        exit_state()
                        return "title"  # Sends the character into "title state", removing every single bit of progress made.

                    pygame.mixer.Channel(0).unpause()


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



#DEBUG COMMAND EXECUTION
# exit_commands=["exit","quit","leave","abort","depart"]
# while True:
#     cmd=input("COMMAND:")
#     if cmd.lower() in exit_commands:break
#     exec(cmd)
# exit()





"MAIN LOOP###############################################################"
next_state = "title"

while True:
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
            continue

        elif next_state == "options":
            next_state = options()
            continue

        else:exit()

    elif next_state is None:
        short_load()
        exit()

    else:
        print("invalid state entry")
        exit()


