

from . import scheduler            
from . import logger
import random
import inspect      
import copy
#import ccm.config as config

class MethodWrapper:
  def __init__(self,obj,func,name):
      self.func=func
      self.obj=obj
      self.__name__=name
      self.begins=scheduler.Trigger(name+' begin')
      self.ends=scheduler.Trigger(name+' end')
      self.default_trigger=self.ends
  def __call__(self,*args,**keys):
      self.obj.sch.trigger(self.begins)
      val=self.func(self.obj,*args,**keys)
      self.obj.sch.trigger(self.ends)
      return val
class MethodGeneratorWrapper(MethodWrapper):
  def _generator(self,*args,**keys):
      self.obj.sch.trigger(self.begins)
      for x in self.func(self.obj,*args,**keys):
          yield x
      self.obj.sch.trigger(self.ends)
  def __call__(self,*args,**keys):
      return self.obj.sch.add(self._generator,args=args,keys=keys)
  def __str__(self):
      return '<MGW %s %s>'%(self.obj,self.__name__)    

def log_everything(model,log=None):
  if log is None: log=logger.log_proxy
  if not hasattr(model,'log'): model.run(limit=0)
  model.log=log
  for k,v in list(model.__dict__.items()):
    if k[0]!='_' and k!='parent':
      
      if isinstance(v,Model) and v.parent is model:
        log_everything(v,getattr(log,k))


class Model:
    __converted=False
    _convert_methods=True
    _auto_run_start=True
    name='top'
    


    def __init__(self,log=None,**keys):
        #print("this happens")
        #print(self,"Model A1")#sterling
        self.__init_log=log
        for k,v in list(keys.items()):
          setattr(self,k,v)

    #getitem added by sterling
    def __getitem__(self,item):
        return getattr(self,item)



    def __convert(self,parent=None,name=None):
        #print("__convert() called", self)
        #Culprit
        #if self.__converted: return
        assert self.__converted==False
        self.__converted=True    
        self.changes=scheduler.Trigger()
        
        if hasattr(self,'parent'): parent=self.parent
        
        methods={}
        objects={}
        #print(inspect.getmro(self.__class__),"MRO") #sterling
        #This MRO includes class object, whereas in 2.7, it does not
        #add[:-1], because it seems that object is always at the end.
        '''            obj.__convert(self,name)
                    print("run after")'''#(from line 132) now works.
        #BUT a later run crashes.
        for klass in inspect.getmro(self.__class__)[:-1]:
          
            #print(klass, "klass")
            if klass is not Model:
                #print(klass, "klass")
                for k,v in inspect.getmembers(klass):
                    #print(k,",",v,"k,v")
                    
                    if k[0]!='_':
                        #print(k,"just k")
                        #A problem. ismethod(v) is not returning true.
                        #Did run an exmample, and it worked fine.
                        #It is working though, because they are unbound methods, and ismethod
                        #should only return true if they are bound
                        #isfunction might work in it's place
                        #if inspect.ismethod(v):
                        if inspect.isfunction(v):
                            #print(k,v,"k,v+")
                            if k not in ['run','now','get_children'] and k not in methods and klass is not Model:
                                #print(k,v,"k,v-post")
                                methods[k]=v
                        else:
                            if inspect.isclass(v) and Model in inspect.getmro(v):
                                v=v()
                            if k not in objects:
                                objects[k]=v
        objects=copy.deepcopy(objects)
        #works up to here
        
        if parent:
            if not parent.__converted: parent.__convert()
            self.sch=parent.sch
            self.log=logger.dummy
            self.random=parent.random
            self.parent=parent
        else:
            self.sch=scheduler.Scheduler()
            if self.__init_log is True:
                self.log=logger.log()
            elif self.__init_log is None:
                self.log=logger.dummy   
            else:
                self.log=self.__init_log    
            self.random=random.Random() 
            #seed=config.getOptions().random
            #if seed is not None: self.random.seed(seed)
            
            self.parent=None   
        
        self._convert_info(objects,methods)
        #works up to here
        #print(list(objects.items()))
        for name,obj in list(objects.items()):
            #print("run before before",name,obj)
            #self.run(limit=0)#print(name,obj,"name,obj")
            if isinstance(obj,Model):
                #print(dir(obj))  
                if not obj.__converted:
                    #print(obj,"obj")
                    #print(self,"self")
                    #print("run before")
                    #self.run(limit=0)
                    
                    #self.run(limit=0)
                    obj.__convert(self,name)
                    #print("run after")
                    
                    #self.run(limit=0)
                else:
                    obj.name=name    
                try:
                  self._children[name]=obj
                except AttributeError:
                  self._children={name:obj}
            #print("run before 2",name,obj)
            #self.run(limit=0)
            #print(dir(obj))
            self.__dict__[name]=obj
            #print("run after 2",name,obj)
            #print(dir(obj))
            #self.run(limit=0)
        #check out _convert_info - see difference between 2.7 running and 3.3 running.
        #does not between here and last
        
        if self._convert_methods:    
          for name,func in list(methods.items()):
              #print("here",name,func)
              #print(dir(func))
              #if func.__func__.__code__.co_flags&0x20==0x20:
              if func.__code__.co_flags&0x20==0x20:
                  w=MethodGeneratorWrapper(self,func,name)
              else:
                  w=MethodWrapper(self,func,name)
              self.__dict__[name]=w    

        if self._auto_run_start:
            self.start()
        
        for k,v in list(self.__dict__.items()):
            if k[0]!='_' and k!='parent' and isinstance(v,Model):
                if not v.__converted:
                    v.__convert(parent=self)
                
        
    def _convert_info(self,objects,methods):
        pass    
                
    def __setattr__(self,key,value):
      if key=='parent' and value is None and getattr(self,'parent',None) is not None:
        del self.parent._children[self.name]
      self.__dict__[key]=value
      

      if isinstance(value,Model) and key[0]!='_' and key!='parent':
        self._ensure_converted()
        p=self
        ancestor=True
        while p is not None:
          if value is p: break
          p=getattr(p,'parent',None)
        else:
          if getattr(value,'parent',None) is not None:
            pass
            #if value.name in value.parent._children:
            #  del value.parent._children[value.name]
          else:  
            value.parent=self
            value.name=key
            try:
              self._children[key]=value
            except AttributeError:
              self._children={key:value}  
            if self.__converted and not value.__converted: value.__convert(name=key,parent=self)
              
      if self.__converted and key[0]!='_' and key not in ['parent','sch','changes','log','random','name']:
          m=self
          done=[]
          while m is not None:
            self.sch.trigger(m.changes,priority=-1)
            done.append(m)
            m=m.parent
            if m in done: m=None
          if self.log: setattr(self.log,key,value)
      
      if key=='log' and value is not None:
        for k,v in list(self.__dict__.items()):
          if k[0]!='_' and k not in ['parent','sch','changes','log','random','name']:
            if isinstance(v,(int,str,float,type(None))):
              setattr(value,k,v)
          
    
    
    
    def start(self):
        pass
    def run(self,limit=None,func=None):
        if not self.__converted:
            self.__convert()
        #if config.getOptions().logall: log_everything(self)
        if limit is not None: 
            self.sch.add(self.sch.stop,limit,priority=-9999999)
        if func is not None:
            self.sch.add(func)
        self.sch.run()
    def stop(self):
        if not self.__converted:
            self.__convert()
        self.sch.stop()
    def now(self):
        if not self.__converted:
            self.__convert()
        return self.sch.time
    
    def get_children(self):
        try:
          return list(self._children.values())
        except AttributeError:
          return []  
        
        
    def _get_scheduler(self):
        self._ensure_converted()
        return self.sch

    def _ensure_converted(self):
        if not self.__converted:
            self.__convert()

    def _is_converted(self):
        return self.__converted
        
                    
      
      
      
      
      
    




