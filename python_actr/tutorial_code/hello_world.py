from python_actr import *              ## Imports the code you need to run Python ACT-R

class MyAgent(ACTR):                   ## Each agent will be an instance of the class MyAgent,
                                       ##    which is a subclass of the class ACTR
    
    focus=Buffer()                     ## There is a memory buffer called focus
    focus.set('greeting:hello')        ## We set the focus to the task of greeting.

    def hello(focus='greeting:hello'): ## if focus buffer has this thing in it
        print("hello world!")          ## print something
        focus.set('greeting:stop')     ## change chunk in focus buffer. Required for it to stop.

tim=MyAgent()                          ## Create an instance of MyAgent called tim
tim.run()                              ## Now tim has a focus and something to do, so run tim.
