# initial code to set up Python ACT-R
import python_actr
from python_actr import *
log=python_actr.log()

# define the model
class MyModel(ACTR):
    goal=Buffer()
    
    def greeting1(goal='action:greet style:casual person:?name'):
        print("Hi",name)
        goal.clear()
        
    def greeting2(goal='action:greet style:formal person:?name'):
        print("Greetings",name)
        goal.clear()
        
        
        
# run the model        
model=MyModel()
python_actr.log_everything(model)
model.goal.set('action:greet style:formal person:Terry')
model.run()


