class MyEnv(Model):
  pass
class MyAgent(ACTR):
  #production_time = 0.05
  #production_sd = 0.01
  #production_threshold = -20
  
  goal = Buffer() # Creating the goal buffer for the agent
  
  def init(): # this rule fires when the agent is instantiated.
    goal.set("helloworld") # set goal buffer to direct program flow
  def bread_bottom(goal="helloworld"): # if goal="sandwich bread" , fire rule
    print ("Hello World!")
    goal.set("stop") # set goal buffer to direct program flow
  #def stop_production(goal="stop"):
    #self.stop() # stop the agent

tim = MyAgent()
subway=MyEnv()
subway.agent=tim
log_everything(subway)
subway.run()
