# initial code to set up Python ACT-R
import python_actr
from python_actr import *
log=python_actr.log()

# define the model
class MyModel(ACTR):
    goal=Buffer()
    
    def greeting(goal='action:greet'):
        print("Hello")
        goal.clear()
        
# run the model        
model=MyModel()
python_actr.log_everything(model)
model.goal.set('action:greet')
model.run()


