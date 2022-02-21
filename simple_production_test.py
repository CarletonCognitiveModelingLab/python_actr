from python_actr import *  


class MyEnvironment(Model):
    pass


class MyAgent(ACTR):
    
    focus=Buffer()
    focus.set('sandwich_step:bread_bottom')

    def bread_bottom(focus='sandwich_step:bread_bottom'):# if focus buffer has this chunk then....
        print("I have a piece of bread")                 # print the action
        focus.set('sandwich_step:cheese')                # change chunk in focus buffer

    def cheese(focus='sandwich_step:cheese'):            # the rest of the productions are the same
        print("I have put cheese on the bread")          # but carry out different actions
        focus.set('sandwich_step:ham')

    def ham(focus='sandwich_step:ham'):
        print("I have put  ham on the cheese")
        focus.set('sandwich_step:bread_top')

    def bread_top(focus='sandwich_step:bread_top'):
        print("I have put bread on the ham")
        print("I have made a ham and cheese sandwich")
        focus.set('sandwich_step:stop')   

tim=MyAgent()                              # name the agent
subway=MyEnvironment()                     # name the environment
subway.agent=tim                           # put the agent in the environment
log_everything(subway)
subway.run()                               # run the environment
