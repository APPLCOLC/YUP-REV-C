import random
from levels import template
class data(template.data):
    
    def __init__(self, level=1):
        template.data.__init__(self, level)
        #LEVEL INFORMATION
        self.worldInfo={
            "songname":'cave.mp3',
            "uitype":'default',
            "bg":'Cave'
            }