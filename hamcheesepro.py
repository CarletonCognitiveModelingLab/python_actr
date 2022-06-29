#################### ham cheese production model ###################

# this is the simplest type of act-r model
# it uses only the production system and one buffer
# the buffer represents the focus of thought
# we call it the focus buffer but it is often called the goal buffer
# productions fire if they match the focus buffer
# each production changes the contents of focus buffer so a different production will fire on the next cycle

##import sys
##sys.path.append('/Users/robertwest/ccmsuite')
##
##import ccm

## log=ccm.log()   

from python_actr import *  

#####
# Python ACT-R requires an environment
# but in this case we will not be using anything in the environment
# so we 'pass' on putting things in there

class MyEnvironment(Model):
    pass

#####
# create an act-r agent

class MyAgent(ACTR):
    
    focus=Buffer()
    focus.set('sandwich bread')

    def bread_bottom(focus='sandwich bread'):     # if focus buffer has this chunk then....
        print("I have a piece of bread")           # print
        focus.set('sandwich cheese')              # change chunk in focus buffer

    def cheese(focus='sandwich cheese'):          # the rest of the productions are the same
        print ("I have put cheese on the bread")    # but carry out different actions
        focus.set('sandwich ham')
##
    def ham(focus='sandwich ham'):
        print ("I have put  ham on the cheese")
        focus.set('sandwich bread_top')
##
    def bread_top(focus='sandwich bread_top'):
        print ("I have put bread on the ham")
        print ("I have made a ham and cheese sandwich")
        focus.set('stop')   
##
    def stop_production(focus='stop'):
        self.stop()                        # stop the agent

tim=MyAgent()                              # name the agent
subway=MyEnvironment()                     # name the environment
subway.agent=tim                           # put the agent in the environment
log_everything(subway)                 # print out what happens in the environment

subway.run(3)                               # run the environment
##ccm.finished()                             # stop the environment
