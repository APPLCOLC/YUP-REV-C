# YUP

Yup is a shmup engine written in Python using the Pygame module.

To run YUP, just run the main.py module.
You need pygame installed in order to use it.

There will be more information on the code itself added here eventually. 
Most of the information you will need is in the code files itself as comments.


TO DO LIST
---------

-get character hats working
--hat() will be a function in shared.char that spawns a hat on top of enemy sprites
--this is currently not progammed to be moddable.

-make the levels have a universal class, known as template (2/?/23)

-fix song preloading, get rid of it (2/7/23)
--make the music loading pygame.mixer.Music.load()
--if anything has to do with pausing a song and loading it back in, save the timeframe

-RESTORE POWER UP IMAGES (2/8/23)

-fix settings being loaded all the time (2/7/23)

-preload preset font surfaces (2/7/23)
--0-9 (dun)
--world names, as a list containing all the pieces of text leading to the image (dun)
--bonus names (dun)
--ui elements ( "LEVEL COMPLETE"  "SCORE:" "WOW!" "OUCH!") (dun)
--settings stuff, as to preload it (dun)


**COMPLETE BY 1/28/23**
-Transitions from stage to stage (2/4/23)
**COMPLETE BY 1/27/23**
-new SPIKE entrance pattern

-Game over screen that tells you to screenshot your score (1/31/23)
*PSEUDOCODE - FUNCTION NAME IS game_over()*
If the player is detected dead, play a little explosion over the player for the meme.
Just like pause, playstate freezes, and starts "game over state"
Game Over State takes in a few arguments, specifically the LEVEL CLASS OF PLAYSTATE.
Using level, it:
    stops the background from scrolling, specifically slowing it down before coming to a halt. 
    kills the background when it stops moving, and simply blits the first image in the sequence.
    makes the formation fly offscreen. 
    kills the formation when it is offscreen.
When formation and background are killed, it sends down a message box stating "GAVE OVER \n SCORE \n QUOTE :"
This message box, when it hits the center of the screen, stops, and displays your score and a randomly-generated quote for a few seconds before flying offscreen.
GameOver returns None, in which playstate returns "title"

      

-give character drops (1/27/23)
-player bullet armor (1/27/23)
-player health boxes (1/27/23)
