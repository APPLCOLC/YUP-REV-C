# YUP

Yup is a shmup engine written in Python using the Pygame module.

To run YUP, just run the main.py module.
You need pygame installed in order to use it.

There will be more information on the code itself added here eventually. 
Most of the information you will need is in the code files itself as comments.


TO DO LIST
----------
**COMPLETE BY 1/28/23**
-Transitions from stage to stage, and bonuses

**COMPLETE BY 1/27/23**
-new SPIKE entrance pattern

-Game over screen that tells you to screenshot your score
*PSEUDOCODE*
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
