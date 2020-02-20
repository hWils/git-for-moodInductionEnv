# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 17:57:35 2019

@author: Psychology User


# Need to alter so can choose between a pracice trial with no recording to file and a lesser amount of trials. 
4# Potentially this could be a separate file.

Additional functionality required: To record the vividness ratings after each image. For now can just get these to save to a list.

"""
1
from datetime import datetime

from PIL import Image
import glob
from psychopy import visual, event, core, monitors
import random
import csv
import numpy as np



displayFrameRate = 59
participantNumber = 3
distanceFromMonitor = 60
beginningInstructions = "This is the practice experiment. \n \n Please ask throughout if you have questions. \n  \n As soon as you press a key, the experiment will immediately commence and your first visual stimuli will appear on the screen."
task = 'scary'
saveDataList = []
num_blocks = 1



# setup the monitor, to establish distance of ppt from monitor so can do visual angles rather than size
mon = monitors.Monitor('DellXPS', width = 35)#fetch the most recent calib for this monitor
mon.setDistance(distanceFromMonitor)#further away than normal?
mon.setSizePix((1920, 1080))


# define the window on which presentation will occur - size is chosen as error message suggested it should be that size
win = visual.Window(size =[1920,1080],
      monitor = mon,
      color =[-1,-1,-1], # background is black
      fullscr = True)   #remember to uncomment this!!

# load up all the images from the stimuli folder
image_list = []
for filename in glob.glob('fixationPaint/*.png'): #assuming gif
    image_list.append(filename)

#declaring presentation stimuli
img =visual.ImageStim(
    win=win,
    image="fixationPaint/blueSquare.png", #arbitary stand in stimuli
    units="deg",
    size = 0.05
)
#declaring visual noise
mask1 =visual.ImageStim(
    win=win,
    image="noiseAndBlank/noise1.png",
        units="norm"
   # units="pix"
)
#declaring visual noise
mask2 =visual.ImageStim(
    win=win,
    image="noiseAndBlank/noise2.png",
    units="norm"
  #  units="pix"
)
#declaring visual noise
mask3 =visual.ImageStim(
    win=win,
    image="noiseAndBlank/noise3.png",
    units="norm"
  #  units="pix"
)
# declaring black blank screen
blankBlack = visual.ImageStim(
    win=win,
    image="noiseAndBlank/blankBlack.png",
    units="norm"
   # units="pix"
)

instructions = visual.TextStim(
            win=win,
    wrapWidth=None,
    text = beginningInstructions,
    units = 'norm',
    pos=[0.5, 0.0],
    height=0.08, 
    )


breakInstructions = "Break press key when ready \n to move on"
finishInstructions = "Thank you for completing the experiment, \n please notify the experimenter \n that you have finished"
vividnessInstructions = "How vividly did you imagine the previous image? From 0 - 5 (5 being extremely vivid, and 0 being no imagery at all)"


def seconds(seconds):
    frames = seconds * displayFrameRate
    return frames


#enables termination of experirment by key-press - Esc to quit, and F to exit fullscreen
def get_keypress():
    keys = event.getKeys()
    if keys and keys[0] == 'escape':
        win.close()
        core.quit()
    if keys and keys[0] == 'f':
        win.fullscr = False
        
# draws the instructions, then stays on this screen till user keyboard input.
def beginExperiment():
    instructions.draw()
    win.flip()
    event.waitKeys()    

def breakWait():  # screen changes to begin next block when ppt presses key
    instructions.text = breakInstructions
    instructions.draw()
    win.flip()
    event.waitKeys()
    
# finishing text, press escape to close the window and end the experiment
def finishExperiment():
    instructions.text = finishInstructions
    instructions.autoDraw = True
    instructions.draw()
    win.flip()
    while True:
        keys = event.getKeys()
        print(keys)
        if keys:
            if keys[0] == 'escape':
                win.close()
                core.quit()
                
###############################################################################
 #displays instructions and waits for correct key press before saving response to a dictionary      
def vividnessRating(image):
    global saveDataArray
    instructions.text = vividnessInstructions
    instructions.draw()
    win.flip()
    keys = event.waitKeys()
    intKey = int(keys[0])
    stimulusName = image.image
    return stimulusName, intKey
                
# this method handles the basic trial: presents image, followed by visual mask, then black screen for imagination task, then mask again
def TrialFunction(presentationImage):
    for frameN in range(seconds(9)):   # For exactly 200 frames
        escapeKey = get_keypress() 
        
        # IMAGE
        if seconds(0) <= frameN < seconds(0.3):  # Present stim for a different subset
            mask1.size = (2,2)
            mask1.draw()
        if seconds(0.3) <= frameN < seconds(0.6):  # Present stim for a different subset
            mask2.size = (2,2)
            mask2.draw()
        if seconds(0.6) <= frameN < seconds(1.0):  # Present stim for a different subset
            mask3.size = (2,2)
            mask3.draw()
  
  
        # IMAGE
        if seconds(1) <= frameN < seconds(3):  # Present fixation for a subset of frames
            presentationImage.units = 'deg'
            presentationImage.size = 18
           # presentationImage.size = (1000,1000)
            presentationImage.draw()
            
        # MASKS
        if seconds(3) <= frameN < seconds(3.3):  # MASK    
            mask1.size = (2,2)
            mask1.draw()
        if seconds(3.3) <= frameN < seconds(3.6):  # MASK    
            mask2.size = (2,2)
            mask2.draw()
        if seconds(3.6) <= frameN < seconds(4):  # MASK    
            mask3.size = (2,2)
            mask3.draw()
            
       # BLANK      
        if seconds(4) <= frameN < seconds(9):  # Present stim for a different subset   5 seconds
            blankBlack.draw()
        win.flip() # changes what is displayed on the screen
  


        
# this method runs through all the picture stimuli, by first randomising list - then adds a break onto the end
def blockFunction():
    random.shuffle(image_list)
   # image_list = image_list[0:9]
    print(image_list)
    for filename in image_list:
        img =visual.ImageStim(
        win=win,
        image=filename,
        units="deg"
      )
        TrialFunction(img)
        stimulusName, intKey = vividnessRating(img)
    # then break
    breakWait()
    
  # includes all blocks plus beginning and finishing instructions, plus saving eye data after each block.
def mainExperiment():
   # while movieStim.status != visual.FINISHED:     
   #     movieStim.draw()  #downloaded avbin 10 to make this work, put avbin.dll files into spyder
  #      win.flip()
    # the below assigns name to csv file based on ppt number, and writes the heading lines to the columns

    global block
    block = 1
    beginExperiment()
    for i in range(0, num_blocks):
        print("in method")
        blockFunction()
        block +=1  ##### 
#    finishInstructions()
        
mainExperiment()


