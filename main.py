"""START###############################################################"""
"""IMPORTS---------------------"""
import pygame,math,time,os, random

"""DISPLAY INITIALIZATION--------------------"""
pygame.display.set_caption("YUP")


icon =  pygame.image.load("assets/images/UI/icon.ico")
pygame.display.set_icon(icon)
WIN = pygame.display.set_mode((450,600),pygame.SCALED)

"""INITIALIZATION--------------------"""
pygame.font.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(16)

universal_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()


"""LOADING#################################################################"""

"""CHARACTERS"""
loaded_characters = {}

for item in os.listdir("./characters"):
    #removing file extension
    if ".py" in item:
        temp=""
        for i in range(len(item)):
            if i > len(item)-4:continue
            else: temp += item[i]
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

# for key,value in loaded_backgrounds.items():print(key);print(value[0]);print(value[1])

# print(dir())

"""LEVELS---"""
loaded_levels = {}

for item in os.listdir("./leveldata/"):
    #removing extension and kicking items without one
    if ".py" not in item:
        continue
    temp=""
    for i in range(len(item)):
        if i > len(item)-4:continue
        else: temp += item[i]
    item=temp

    #importing levels
    the_code = "import leveldata." + str(item) + " as " + str(item)
    exec(the_code, globals(), loaded_levels)




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

# for key,value in loaded_bullets.items(): print(key)

del x,photo, prefixList, curFrame,directory, temp, the_code



"""IMAGES##############################################################"""
class UiImages:

    #BEGIN AND END
    beginImage = pygame.image.load("./assets/images/UI/BEGIN AND END/GET READY.png")
    endImage = pygame.image.load("./assets/images/UI/BEGIN AND END/LEVEL COMPLETE.png")


    #ERRORS
    errortitle = pygame.image.load("./assets/images/UI/errors/errorOccured.png")


    #LOGO FOR TITLE
    logo1 = pygame.image.load("./assets/images/UI/TITLEMENU/logo1.png")
    logo2 = pygame.image.load("./assets/images/UI/TITLEMENU/logo2.png")
    logo3 = pygame.image.load("./assets/images/UI/TITLEMENU/logo3.png")
    titlebglogo = [logo1, logo2, logo3]
    del logo1, logo2, logo3


    #PAUSE GRAPHIC
    pause1=pygame.image.load('./assets/images/UI/pause/paus\'d (1).png')
    pause2=pygame.image.load('./assets/images/UI/pause/paus\'d (2).png')
    pause3=pygame.image.load('./assets/images/UI/pause/paus\'d (3).png')

    pause=[pause1,pause2,pause3]
    for i in range(len(pause)): pause[i]=pygame.transform.scale(pause[i],(450,150)).convert_alpha()
    del pause1,pause2,pause3


    #PRESS SPACE
    press_space = pygame.image.load("./assets/images/UI/space.png")


    #BUTTONS
    quitbutton = pygame.image.load("./assets/images/UI/quitbutton.png")
    quitbuttonpressed = pygame.image.load("./assets/images/UI/quitbuttonpressed.png")
    QUIT = [quitbutton, quitbuttonpressed]
    del quitbutton, quitbuttonpressed

    startbutton = pygame.image.load("./assets/images/UI/startbutton.png")
    startbuttonpressed = pygame.image.load("./assets/images/UI/startbuttonpressed.png")
    START = [startbutton, startbuttonpressed]
    del startbutton, startbuttonpressed

    optionsbutton = pygame.image.load("./assets/images/UI/optionsbutton.png")
    optionsbuttonpressed = pygame.image.load("./assets/images/UI/optionsbuttonpressed.png")
    OPTIONS = [optionsbutton, optionsbuttonpressed]
    del optionsbutton, optionsbuttonpressed

    continuebutton = pygame.image.load("./assets/images/UI/continuebutton.png")
    continuebuttonpressed = pygame.image.load("./assets/images/UI/continuebuttonpressed.png")
    CONTINUE = [continuebutton,continuebuttonpressed]
    del continuebutton,continuebuttonpressed


    #LOADING
    loading = pygame.image.load("./assets/images/UI/loading/loadgif (1).png")


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
    optionbg = pygame.transform.scale(pygame.image.load("./assets/images/UI/options/bg.png"),(450,600))
    option_30 = pygame.transform.scale(pygame.image.load("./assets/images/UI/options/FPS30.png"),(50,30))
    option_60 = pygame.transform.scale(pygame.image.load("./assets/images/UI/options/FPS60.png"),(50,30))

    #GAME OVER IMAGES
    continueGraphic1 = pygame.image.load("./assets/images/UI/game over/continue 1.png")
    continueGraphic2 = pygame.image.load("./assets/images/UI/game over/continue 2.png")
    continueGraphic3 = pygame.image.load("./assets/images/UI/game over/continue 3.png")
    continueGraphic4 = pygame.image.load("./assets/images/UI/game over/continue 4.png")
    continueGraphic = [continueGraphic2,continueGraphic3,continueGraphic4,continueGraphic1]
    del continueGraphic2, continueGraphic3, continueGraphic4, continueGraphic1
    gameOverGraphic = pygame.image.load("./assets/images/UI/game over/GAME OVER.png")
    scoreGraphic = pygame.image.load("./assets/images/UI/game over/SCORE.png")


    #BAGKGROUNDS
    titlebg1 = pygame.transform.scale(pygame.image.load("./assets/images/UI/TITLEMENU/background.png"),(450,600))
    erorrbg = pygame.transform.scale(pygame.image.load("./assets/images/UI/errors/bg.png"),(450,600))
    loadbg = pygame.transform.scale(pygame.image.load("./assets/images/UI/splash.png"),(450,600))


    #CURSOR
    cursor = pygame.image.load("./assets/images/UI/LIVES/000.png")
ui=UiImages #this creates an object of the class. this is what everything refers to




"""SOUNDS##############################################################"""
class Sounds:
        
    def __init__(self):
        ###################SOUNDS####################
        self.ostList=[];self.soundList=[]

        #UI NOISES
        self.denied=pygame.mixer.Sound('./assets/sounds/sfx_denied.wav');self.soundList.append(self.denied)
        self.back=pygame.mixer.Sound('./assets/sounds/sfx_back.wav');self.soundList.append(self.back)
        self.scroll=pygame.mixer.Sound('./assets/sounds/sfx_scroll.wav');self.soundList.append(self.scroll)
        self.select=pygame.mixer.Sound('./assets/sounds/sfx_select.wav');self.soundList.append(self.select)
        self.select2=pygame.mixer.Sound('./assets/sounds/sfx_select2.wav');self.soundList.append(self.select2)
        self.error=pygame.mixer.Sound('./assets/sounds/QUACK.wav');self.soundList.append(self.error)


        #ENEMY SOUNDS
        self.hit = pygame.mixer.Sound('./assets/sounds/sfx_boomsmall.wav');self.soundList.append(self.hit)
        self.bighit = pygame.mixer.Sound('./assets/sounds/sfx_boombig.wav');self.soundList.append(self.bighit)
        self.bosshit = pygame.mixer.Sound('./assets/sounds/sfx_bosshit.wav');self.soundList.append(self.bosshit)
        self.nyoom = pygame.mixer.Sound('./assets/sounds/sfx_nyoom.wav');self.soundList.append(self.nyoom)
        self.death = pygame.mixer.Sound('./assets/sounds/sfx_death.wav');self.soundList.append(self.death)
        self.ouch = pygame.mixer.Sound('./assets/sounds/sfx_ouch.wav');self.soundList.append(self.ouch)
        self.yeah = pygame.mixer.Sound('./assets/sounds/sfx_yeah.wav');self.soundList.append(self.yeah)


        #BULLET NOISES
        self.shoot_bap1 = pygame.mixer.Sound('./assets/sounds/shoot_bap.wav');self.soundList.append(self.shoot_bap1)
        self.shoot_bap2 = pygame.mixer.Sound('./assets/sounds/shoot_bap2.wav');self.soundList.append(self.shoot_bap2)
        self.shoot_bap3 = pygame.mixer.Sound('./assets/sounds/shoot_bap3.wav');self.soundList.append(self.shoot_bap3)
        self.shoot_bap4 = pygame.mixer.Sound('./assets/sounds/shoot_bap4.wav');self.soundList.append(self.shoot_bap4)
        self.shoot_realistic = pygame.mixer.Sound('./assets/sounds/shoot_realistic.wav');self.soundList.append(self.shoot_realistic)
        self.shoot_laser = pygame.mixer.Sound('./assets/sounds/shoot_laser.wav');self.soundList.append(self.shoot_laser)
        self.shoot_bee = pygame.mixer.Sound('./assets/sounds/shoot_bee.wav');self.soundList.append(self.shoot_bee)
        self.shoot_missile = pygame.mixer.Sound('./assets/sounds/shoot_missile.wav');self.soundList.append(self.shoot_missile)

        ##############################################
        
        self.offsetSounds = {self.shoot_laser:0.5,self.shoot_realistic:0.25}

    ###############FUNCTIONS###############-
    @staticmethod
    def play_song(directory):
        cursong=pygame.mixer.music.load("./assets/ost/" + directory)
        with open('./assets/settings.txt','r') as data:vol=eval(data.read())['OST VOL'][0]
        pygame.mixer.music.set_volume(vol)
        pygame.mixer.music.play(loops=10)
        return cursong


    @staticmethod
    def stop_song():
        pygame.mixer.music.stop()


    @staticmethod
    def play_nonmain_song(directory):
        #This is specifically because if you replace the music file being played, in a menu for instance, it will not remember any song played before.
        #If you pause the game, it replaces the gameplay music with the pause music, and forges all about the gameplay music.
        cursong=pygame.mixer.Sound("./assets/ost/" + directory)
        with open('./assets/settings.txt','r') as data:vol=eval(data.read())['OST VOL'][0]
        cursong.set_volume(vol)
        cursong.play()
        return cursong
    #songs are easily stopped on their own and do not need a stop function
        

    def adjust_sounds(self, volume):
        for item in self.soundList:
            item.set_volume(volume)
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

        for k,v in self.offsetSounds.items():

            soundvol=self.soundList[self.soundList.index(k)].get_volume()*v

            self.soundList[self.soundList.index(k)].set_volume(soundvol)


sounds=Sounds();sounds.apply_offsets()#this creates an object of the class. this is what everything refers to 
# print(sounds)








"""SHARED ASSETS##############################################################"""

"""APPLYING SETTINGS--------------------"""
def readapply(settings=None, nonmain_song=None):

    if settings is None:
        with open("assets/settings.txt", "r") as data:
            # print("settings not present | settings file read")
            settings = eval(data.read())

    fullscreen = settings["FULLSCREEN"][0]

    # audio adjust
    sounds.adjust_sounds(settings['SOUND VOL'][0])
    sounds.adjust_ost(settings['OST VOL'][0])
    if nonmain_song is not None: nonmain_song.set_volume(settings['OST VOL'][0])

    # screen adjust
    if fullscreen:
        pygame.display.set_mode((450, 600), pygame.FULLSCREEN | pygame.SCALED)
    else:
        pygame.display.set_mode((450, 600), pygame.SCALED)

    return settings



"""DEBUG TEXT--------------------"""
def debug_displays(sprite_class_dict,variables,time,fps,level,win=None): #-PLAYREMOVE

    #adding items to the print list 
    base_text= ["-DEBUG-", "FPS:" + str(round(fps, 1)), "TIME:" + str(round(time, 1)), "LEVEL:" + str(level)]

    for key, value in variables.items():
        base_text.append(str(key) + "-var:" + str(len(value)))

    base_text.append("ALLSPRITES:" + str(len(universal_group)))

    for key,value in sprite_class_dict.items():
        base_text.append(""+str(key)+":"+str(len(value)))


    #displaying the print list
    if win is None:
        print(base_text)

    else:
        for i in range(len(base_text)):
            font = pygame.font.Font("./assets/font/Setfont-Regular.ttf", 20)
            surface = font.render(str(base_text[i]), True, "white")
            WIN.blit(surface,(0,((i*20)+30)))
            del surface,font

    del base_text
 

"""LOADING--------------------"""
def long_load(window=WIN):
    window.blit(ui.loadbg, (0, 0))

    pygame.display.update()

def short_load(window=WIN):
    window.blit(ui.loading, (0, 0))

    pygame.display.update()


"""SCORE DISPLAY--------------------"""
def display_score(score_value, coord, window, snap=True, shadow=True, color=(0, 0, 0), shadow_color=(255, 255, 255), size=20):

    score_font = pygame.font.Font("./assets/font/Setfont-Regular.ttf",size)

    if shadow: score_surface = score_font.render(str(score_value), True, color, shadow_color)
    else: score_surface = score_font.render(str(score_value), True, color)

    score_rect = score_surface.get_rect()

    if snap:score_rect.right = coord[0]
    else: score_rect.center = coord

    window.blit(score_surface, score_rect)

    del score_font,score_rect,score_surface



"""APPLYING SOME TEMPORARY VALUES--------------------"""
long_load()
readapply()







"""IMPORTANT MODULES##############################################################"""


"""BACKGROUNDS--------------------"""
class BG:
    #takes loaded backgrounds ; draws them to screen ; (update) no longer loads backgrounds automatically
    def __init__(self, window, photo_name='null', current_frame=1, loaded=loaded_backgrounds):
        
        #beginning values
        self.WIN=window
        self.bgY,self.bgX=0,0 #scroll stuff
        self.curFrame=current_frame
        self.config=loaded[photo_name][0]
        self.dir=loaded[photo_name][1]


    #This is the code that will run on-frame.
    #It does not display the background, just update the current image to *be* displayed.
    def update(self):
        # print(self.photoName)

        self.WIN.fill("black")#initial screen fill in case of transparecy


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
            self.WIN.blit(self.dir[self.curFrame], (self.bgX, self.bgY - 600))
            self.WIN.blit(self.dir[self.curFrame], (self.bgX, self.bgY + 600))

        if self.bgX != 0:
            self.WIN.blit(self.dir[self.curFrame], (self.bgX + 450, self.bgY))
            self.WIN.blit(self.dir[self.curFrame], (self.bgX - 450, self.bgY))

        if self.bgY != 0 and self.bgX != 0:
            self.WIN.blit(self.dir[self.curFrame], (self.bgX + 450, self.bgY - 600))
            self.WIN.blit(self.dir[self.curFrame], (self.bgX - 450, self.bgY + 600))
            self.WIN.blit(self.dir[self.curFrame], (self.bgX + 450, self.bgY + 600))
            self.WIN.blit(self.dir[self.curFrame], (self.bgX - 450, self.bgY - 600))

        return

    #Displaying the bg is treated differently due to fps changes in playstate
    def display_bg(self):
        self.WIN.blit(self.dir[self.curFrame],(self.bgX,self.bgY))
        if self.config is not None: self.decoys()


    #Destroying the bg will delete all the background values and replace them with something else
    def destroy(self):
        for _ in self.dir:
            del _
        for _ in dir(self):
            del _



"""FORMATION FOR GAMEPLAY--------------------"""
class Formation:
    def __init__(self, player, available_char, level, file=None):

        # print("formation created")

        #note to self, the player class is used, not the sprite group.
        """
        FILE is the piece of code used that holds all the python data.
            the world file is a text file that holds all the setting data
            and the world data file is a python file that holds things such as intensity and formation
        FILE also holds the available characters to be used in a world
        """
        # print("formation created")
        self.pos=[0,0]

        self.finished=False

        self.dirH=['l','r']
        self.dirH=self.dirH[random.randint(0,1)] #potential [l/r]: randomized

        self.totalchar=0 #this is the highest amount of characters onscreen. it will create a ratio based off of how many characters are still alive to create a speed

        self.exitSpeed=10 #this is the speed in which the formation exits

        self.bullets=bullet_group #bullet classes

        self.file=file #the piece of code used that holds all the python data

        self.curFrame=0 #count for when to send down a formations

        self.loaded=loaded_characters
        self.available_char=available_char

        self.formation={} # gives the order of character spawns
        self.activeformation = {} # stores the actual character objects; for maintaining and position handling
        # self.formationSprites = pygame.sprite.Group()  # sprite group used for wiping all characters
        
        """OH BOY, A GLOB OF ELIF STATEMENTS!
        This is mostly due to the three forms of formation there are: random, random manual, and ordered
        Everything is commenterd out accordingly. """
        manual=len(self.file.manual_formations)>0 and self.file.manual_type!=0 #boolean value, since this will be used several times
        
        #random manual formation
        if manual and self.file.manual_type==1:
            
            #picking a random manual formation
            if random.randint(0,100) < self.file.manual_influence:
                self.formation=random.choice(self.file.manual_formations)

            #randomly generating a formation if that doesn't work
            else:
                self.formation=self.randomly_generate_formation

        #ordered manual formation
        elif manual and self.file.manual_type==2:
            
            #nonloopings
            if not self.file.manual_loop and level<=len(self.file.manual_formations):
                self.formation=self.file.manual_formations[level-1]
            #nonlooping if past manual order - RANDOM
            elif not self.file.manual_loop and level>len(self.file.manual_formations):
                self.formation=self.randomly_generate_formation()
            
            #looping
            elif self.file.manual_loop:
                
                #shedding the extra levels to figure out which manual_formations index to use
                index = level - (len(self.file.manual_formations)*((level-1)//len(self.file.manual_formations)))
                self.formation = self.formation=self.file.manual_formations[index-1]

        #random formation
        else:  self.formation=self.randomly_generate_formation()

        del manual



        howmanychar=0 #howmanychar is a counter that checks how many characters are there

        self.size=[0,len(self.formation)] # size is the offset made by how large the file is. It will always use this for positioning and bouncing.

        for i in range(len(self.formation)):
            if len(self.formation[i])>self.size[0]:
                self.size[0]=len(self.formation[i]) #calculates the width of the formation, appended to SIZE

        # print(self.size)

        self.pos = [50,75]  


        #CODE FOR SPAWNING CHARACTERS
        for i in range(len(self.formation)):
            for j in range(len(self.formation[i])):
                """adds a character to the formation, self.activeformation
                howmanychar is the key value
                it spawns the character using the text value in the formation as a key for the loaded list
                if a formation says {1:["nope"]}, the program will spawn a "nope" if it is in the available_char list"""
                try:

                    self.activeformation[howmanychar] = self.loaded[self.formation[i][j]].Char(allsprites=universal_group, bullets=bullet_group, player=player, enemies=enemy_group, formationPos=self.pos, offset=((j * self.file.char_distance_x), (i * self.file.char_distance_y)))
                    
                    universal_group.add(self.activeformation[howmanychar])
                    enemy_group.add(self.activeformation[howmanychar])
                    
                    howmanychar+=1

                except KeyError: pass


        self.totalchar=len(self.activeformation) #max character amount

        self.start=time.time() #this is the start timer. the more time passes, the faster the game goes
        self.speed=0 #speedup/slowdown code



    def update(self):
        """
        This line of code below me runs the function "formationUpdate" for every item in the formation
        This is, if not stated before, because every asset in the game is already "updated" through the pygame sprite class feature
        So this function updates the formation position in the code
        """
        for key,value in self.activeformation.items():value.formationUpdate(self.pos)


        #MOVEMENT code for updating CHARACTER POSITIONS
        self.formation_move()

        #THROWDOWN code for making CHARACTERS ATTACK
        self.throw_down()


        """
        The piece of code below this is for removing any dead items from the formation dictionary.
        This is for telling when to move on in the level, to make another formation.
        This COULD be done with a sprite class, but it is just easier and more understandable this way. 
        """
        for key, value in self.activeformation.items():
            if value.state == "dead": self.activeformation.pop(key);break
        if len(self.activeformation)==0: self.finished=True
    


    #The code for causing a character to attack
    def attack(self):
        #creates a list of character keys that are currently in idle state
        idle_list=[]

        #checks each character, if they are idle, their key gets added to the list
        for key in self.activeformation.keys():
            if self.activeformation[key].state=="idle":
                idle_list.append(key)

        #picks a random idle character's key and sets them to attack. 
        if len(idle_list)>0:self.activeformation[idle_list[random.randint(0,(len(idle_list)-1))]].state="attack";return


    #The code for changing the current formation positon
    #This is why you see all the characters move around in a pattern
    def formation_move(self):
        #change direction to left
        if self.pos[0]>=(450-(self.size[0]*self.file.char_distance_x)): 
            self.speed-=self.file.speed*0.025 ;self.dirH='l'

        #change direction to right
        elif self.pos[0]<=10: 
            self.speed+=self.file.speed*0.025;self.dirH='r'

        #determining speed if the formation is not going out of bounds
        else:
            if self.dirH=='l': self.speed = self.file.speed*-1
            elif self.dirH == 'r': self.speed = self.file.speed

        #actually moving the formation once the speed was set
        self.pos[0]+=self.speed
        self.pos[1]=math.sin(self.pos[0]/10)*10 + 100


    def throw_down(self): #shitty name, will change later

        self.curFrame+=1
        total_char_attack=0

        #counting every character that is currently attacking
        for item in self.activeformation.values():
            if item.state=="attack":total_char_attack+=1

        #checks if both the time is right and there aren't too many characters onscreen before causing a character to attack
        
        if (self.file.maxChar is None or total_char_attack<self.file.maxChar) and self.curFrame>=self.file.spawn_time:
            self.attack()
            self.curFrame=0
        else:
            pass


    def destroy(self):

        for key,value in self.activeformation.items():
            value.kill()
            # print(str(key),str(value),"DESTROYED.")
        self.activeformation={}
        #saying the formation is complete
        # self.finished=True


    def randomly_generate_formation(self):
        """RANDOMLY GENERATING A FORMATION
        there is no code within the leveldata file that actually spawns a specific formation
        therefore, it will randomly generate one here based on what the available_char list demands"""

        formation={}
        columnsize=random.randint(self.file.char_min_width,self.file.char_max_width) #columns are width
        rowsize=random.randint(self.file.char_min_height,self.file.char_max_height) #rows are height

        for i in range(rowsize): #row generation
            formation[i]=[]
            for j in range(columnsize): #column generation
                formation[i].append(random.choice(self.available_char))
        
        del rowsize,columnsize
        return formation



"""LEVEL ASSET CODE--------------------"""
class Level:
    def __init__(self, player, world_num):
        with open("./leveldata/worldOrder.txt", "r") as data:
            self.worldOrder=eval(data.read())

        self.universal_group = universal_group
        self.enemy_group = enemy_group
        self.bullet_group = bullet_group
        self.player = player
        self.level = 1
        self.level_in_world=1
        self.world_num=world_num
        self.world_num_looped = self.world_num - (self.world_num * (self.world_num//len(self.worldOrder)))
        self.worldData=loaded_levels
        self.world_ended=False
        self.world_file=None
        # print(self.world_num_looped)
        
        #refresh-world-data default values
        self.worldName=""
        self.bg=None
        self.form=None

        self.refresh_world_data()

    def refresh_world_data(self):
        #resetting values if they still exist
        self.level_in_world=1
        if self.form is not None:
            self.form.destroy();del self.form
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
        self.bg=BG(WIN, self.world_file.worldInfo['bg'])

        """fileReader will then pass off the worldData file to 'formation', as well as the current level"""
        self.form=Formation(player=self.player, 
            available_char=self.world_file.imports,
            level=self.level, 
            file=self.world_file) 

        self.world_ended=False       

    def update(self):

        try: #this is a try statement because there will be no form to check later

            self.form.update()  # updates the formation
             
            if self.form.finished:

                """This is the reset code. It deletes self.form, raises the level by 1, and then re-makes self.form"""
                self.form.destroy()
                del self.form
                
                self.level+=1
                self.level_in_world+=1
                self.world_file.update_intensities(self.level)
                
                self.form=Formation(player=self.player, 
                    available_char=self.world_file.imports,
                    level=self.level, 
                        file=self.world_file) 

                 
        except AttributeError: pass

    def advance_world(self):
        self.world_num+=1

        self.world_num_looped = self.world_num - ( len(self.worldOrder) * ((self.world_num-1)//len(self.worldOrder)) )

        # print(str(self.world_num),"|",str(self.world_num_looped))


        
"""STATES###############################################################"""

"""TITLE ASSETS--------------------"""
def title(window=WIN, sounds=sounds):
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
    def redraw_window(index,frame):

        #The main thing that plays in the title screen. The bg, the fizz effect, and the logo.
        window.blit(ui.titlebg1, (0, 0))
        window.blit(ui.titlebglogo[frame], (225 - (ui.titlebglogo[frame].get_width() / 2), 25))

        #"START," "OPTIONS," and "QUIT" only appear during the first part of the title menu
        if index == 1: window.blit(ui.START[1], (150, 275))
        else: window.blit(ui.START[0], (150, 275))

        if index == 2: window.blit(ui.OPTIONS[1], (150, 375))
        else: window.blit(ui.OPTIONS[0], (150, 375))

        if index == 3: window.blit(ui.QUIT[1], (150, 475))
        else: window.blit(ui.QUIT[0], (150, 475))

        pygame.display.update() #TEST ENABLE


    while run:

        # timer code for the yup and logo frames
        end = time.time()
        if end - start >= 0.25:
            start = time.time()
            frame += 1
            if frame > (len(ui.titlebglogo)-1): frame = 0

        #tells the clock to tick at the rate of FPS
        clock.tick(fps)
        # print(clock.get_fps()) #TEST ENABLE

        #once it sets all the current image forms, it will then redraw the window
        redraw_window(index,frame)

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
                    sounds.select.play()

                    #if you picked the first option, start, the program will set menudepth to 3 and begin the game
                    if index == 1: sounds.stop_song(); return "start"

                    #If you picked options, it will open the options menu
                    elif index == 2: sounds.stop_song(); return "options"

                    # If you pick quit, or something else by some chance, the game will quit.
                    else:sounds.select.play();time.sleep(0.5);run = False;exit()


                #Escape press for quitting game
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_k:
                    sounds.back.play()
                    exit()


                #Item selection; changes index
                if event.key == pygame.K_w:
                    if index > 1: index -=1
                    sounds.scroll.play()

                if event.key == pygame.K_s:
                    if index < 3: index +=1
                    sounds.scroll.play()




"""OPTIONS ASSETS--------------------"""
def options(window=WIN):
    def render_text(text):
        font = pygame.font.Font("./assets/font/Setfont-Regular.ttf", 50)
        surface = pygame.transform.scale(font.render(str(text), True, "white"), (75, 40))

        return surface

    settings = {}
    current_song = sounds.play_nonmain_song("pause.mp3")

    # Reads a dictionary, with the index name and the values associated with it
    with open("./assets/settings.txt", "r") as data:
        settings = eval(data.read())
    settings_keys_images = {}

    # Compiling a dictionary of rendered text to be displayed for the items
    for key in settings.keys(): settings_keys_images[key] = render_text(str(key))

    # UI settings
    run = True
    index = 0

    def redraw_window(settings=settings, settings_keys_images=settings_keys_images, index=index):
        # filling the bg and showing the title
        window.blit(ui.optionbg, (0, 0))
        # displaying the setting names
        yval = 0
        for value in settings_keys_images.values():
            window.blit(value, (50, (yval * 50) + 200))
            yval += 1
        # displaying the setting values
        yval = 0
        for value in settings.values():
            if value[1] == "onoff" and value[0]:
                window.blit(ui.yes, (150, ((yval * 50) + 200)))
            elif value[1] == "onoff" and not value[0]:
                window.blit(ui.no, (150, ((yval * 50) + 200)))
            elif value[1] == "3060" and value[0]:
                window.blit(ui.option_60, (150, ((yval * 50) + 200)))
            elif value[1] == "3060" and not value[0]:
                window.blit(ui.option_30, (150, ((yval * 50) + 200)))
            elif value[1] == "slider":
                window.blit(ui.slider, (150, ((yval * 50) + 200)))
                window.blit(ui.knob, ((130 + (value[0] * 175)), ((yval * 50) + 200)))
            yval += 1
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
                    sounds.back.play()
                    # writing the settings
                    current_song.stop()
                    return "title"

                if event.key == pygame.K_s and index < (len(settings) - 1):
                    sounds.scroll.play()
                    index += 1
                    # print(index)
                if event.key == pygame.K_w and index > 0:
                    sounds.scroll.play()
                    index -= 1
                    # print(index)
                if event.key == pygame.K_j:
                    sounds.select.play()
                    # list(settings)[index] is the key name
                    keyindex = list(settings)[index]
                    if settings[keyindex][1] == "onoff":
                        if not settings[keyindex][0]:
                            settings[keyindex][0] = True
                        elif settings[keyindex][0]:
                            settings[keyindex][0] = False
                    elif settings[list(settings)[index]][1] == "3060":
                        if not settings[keyindex][0]:
                            settings[keyindex][0] = True
                        elif settings[keyindex][0]:
                            settings[keyindex][0] = False
                    else:
                        sounds.denied.play()
                if event.key == pygame.K_a:
                    sounds.select.play()
                    # list(settings)[index] is the key name
                    keyindex = list(settings)[index]
                    if settings[keyindex][1] == "slider" and settings[keyindex][0] > 0:
                        settings[keyindex][0] -= 0.05
                        settings[keyindex][0] = round(settings[keyindex][0], 2)
                    else:
                        sounds.denied.play()
                    # print(values[index])
                if event.key == pygame.K_d:
                    sounds.select.play()
                    # list(settings)[index] is the key name
                    keyindex = list(settings)[index]

                    # HARD-CODING PART FOR MUTE CODE. ERASE IF RE-USED.
                    if keyindex == "OST VOL" or keyindex == "SOUND VOL": settings["MUTE"][0] = False

                    # applying settings
                    if settings[keyindex][1] == "slider" and settings[keyindex][0] < 1:
                        settings[keyindex][0] += 0.05
                        settings[keyindex][0] = round(settings[keyindex][0], 2)
                    else:
                        sounds.denied.play()

                if event.key == pygame.K_p:
                    readapply(settings, current_song)
                    with open("./assets/settings.txt", "w+") as data: data.write(str(settings))
                #only redraws the window when a setting is changed. No FPS needed.    
                redraw_window(index=index)          




"""PAUSE ASSETS--------------------"""
def pause(img=None): #it takes in the UI images as an argument to lower RAM usage and prevent leakage :)
    """-----PLEASE NOTE !-----
    pausestate is required to work like a unique MAIN function, seeing that it is a state within a state
    (By "state within a state", I mean that playstate runs pausestate, so pausestate is completely isolated from everything else)
    (On top of that, pausestate has to run separate states in ways that do not affect the original state (playstate), so it has to be specific with the way that it runs states, as well)
    this is why pausestate imports optionstate and runs it separately without requiring MAIN
    """

    current_song=sounds.play_nonmain_song('pause.mp3')


    #sets the values
    fps=60;run=True;clock = pygame.time.Clock();index = 1
    pause_start = time.time();graphic_start = time.time()
    graphic_frame = 1
    sounds.select2.play()

    #updates every graphic onscreen
    def display_update():
        if img is None:WIN.fill("black")
        else:WIN.blit(img,(0,0))

        WIN.blit(ui.pause[graphic_frame], ((225 - (ui.pause[graphic_frame].get_width() / 2)), 100))

        if index == 1: WIN.blit(ui.CONTINUE[1],((225-(ui.CONTINUE[1].get_width()/2)),275))
        else: WIN.blit(ui.CONTINUE[0],((225-(ui.CONTINUE[0].get_width()/2)),275))
        if index == 2: WIN.blit(ui.OPTIONS[1],((225-(ui.OPTIONS[1].get_width()/2)),375))
        else: WIN.blit(ui.OPTIONS[0],((225-(ui.OPTIONS[0].get_width()/2)),375))
        if index == 3: WIN.blit(ui.QUIT[1],((225-(ui.QUIT[1].get_width()/2)),475))
        else: WIN.blit(ui.QUIT[0],((225-(ui.QUIT[0].get_width()/2)),475))
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

        for event in pygame.event.get():

            if event == pygame.QUIT:
                sounds.stop_song()
                sounds.select2.play()
                run = False
            if event.type == pygame.KEYDOWN:

                #UI
                if event.key == pygame.K_w:
                    if index > 1: index -= 1
                    sounds.scroll.play()
                if event.key == pygame.K_s:
                    if index < 3: index += 1
                    sounds.scroll.play()
                if event.key == pygame.K_j:
                    sounds.select2.play()
                    if index == 1:
                        current_song.stop()
                        run = False
                    if index == 2:
                        current_song.stop()
                        options()
                        current_song.play()
                    if index == 3:
                        current_song.stop()
                        return "title"

    current_song.stop();del current_song
    return time_passed




"""GAMEPLAY ASSETS--------------------"""
def play(
        window=WIN,
        bullet_shared=loaded_bullets["shared"],
        settings=None
        ):

    # DEALING WITH SETTINGS:
    if settings is None:
        settings = readapply()


    # CREATING THE PLAYER AND LEVEL INSTANCE DEPENDING ON TEMPSAVE VALUES -PLAYREMOVE
    player = loaded_characters["player"].Player(enemy_group, bullet_group, universal_group, sounds, loaded_bullets)  # Defines the player
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
    levelclass = Level(player=player,world_num=world_num)  # -PLAYREMOVE


    graphical=True #this is for debug purposes, where if you turn it off, the display turns off but the framerate rises heavily


    def exit_playstate(state_list=(enemy_group, bullet_group, player_group, universal_group)):
        for item in state_list:
            item.empty()


    def redraw_window():

        levelclass.bg.display_bg()
        universal_group.draw(window)

        # UI -PLAYREMOVE
        bullet_shared.display_bullet(window, (0, 0), player.currentweapon, loaded_bullets) #-PLAYREMOVE
        player.display_health(window, (30, 0)) #-PLAYREMOVE
        display_score(player.score, (450, 0), window) #-PLAYREMOVE

        # DEBUG 
        # val=WIN if graphical else None
        # debug_displays(allsprites,
        #                {"PLAYER": playersprite, "ENEMIES": enemies, "BULLETS": bullets},
        #                {"PLAYSTATE": dir(), "PLAYER": dir(playerguy),
        #                 "FILEREADER": dir(Level), "PYGAME": dir(pygame)},
        #                (time.time() - start_time),
        #                clock.get_fps(),
        #                levelclass.level,
        #                WIN=val)
        # del val

        # FINISHING WITH AN UPDATE STATEMENT
        if graphical:pygame.display.update() 


    def update_sprites():
        universal_group.update()
        levelclass.bg.update()


    # VARIABLE DEFINITIONS WHEN THE CODE BEGINS.

    switch_frames=0

    while run:

        #DEBUG REMOVE
        switch_frames+=1
        if switch_frames>6:
            # levelclass.advance_world()
            # levelclass.refresh_world_data()
            switch_frames=0

        if graphical:clock.tick(fps)
        else:clock.tick(0)

        #FPS code: running values twice if graphical FPS is halved
        for i in range(loop):
            update_sprites()

        # graphical updates
        redraw_window()
        levelclass.update() 

        #game over initialization
        if player.playerdied: 
            exit_playstate()
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
                    # freezes everything and opens PAUSESTATE
                    player.reset_movement() 

                    pygame.mixer.music.pause()

                    time_paused =  pause(img=levelclass.bg.dir[0])

                    # If an error occurs, or any exit code is brought up, it spits you back at the title
                    if type(time_paused) != float:
                        exit_playstate(None, 1, [enemy_group, bullet_group, player_group, universal_group])
                        return "title"  # Sends the character into "titlestate", removing every single bit of progress made.

                    pygame.mixer.music.unpause()


            # PLAYER CONTROLS
            player.controls(event)

            # DEBUG CODE
            if event.type == pygame.KEYDOWN:

                #swaps the graphical setting
                if event.key==pygame.K_1:
                    if graphical:graphical=False
                    else:graphical=True
                if event.key==pygame.K_2:
                    levelclass.advance_world()
                    levelclass.refresh_world_data()



#DEBUG COMMAND EXECUTION
# exit_commands=["exit","quit","leave","abort","depart"]
# while True:
#     cmd=input("COMMAND:")
#     if cmd.lower() in exit_commands:break
#     exec(cmd)
# exit()





"MAIN LOOP###############################################################"
next_state = "title"
settings=readapply

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
            # next_state = errorstate.error(WIN, "unknown")
            next_state = options()
            continue

        else:exit()

    elif next_state is None:
        short_load(WIN)
        exit()

    else:
        print("invalid state entry")
        exit()

 
