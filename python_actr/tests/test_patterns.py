
from python_actr.pattern import Pattern,PatternException

class Obj:
  def __init__(self,**keys):
    for k,v in list(keys.items()):
      self.__dict__[k]=v
      
def makePattern(text):
  return Pattern(dict(self=text))
      

def test_exact():
    obj={'self':Obj(a=1,b=2,c=3)}
    p=Pattern(dict(self='a:1 b:2 c:3'))
    assert p.match(obj) == {}
    obj['self'].c=2
    assert p.match(obj) == None
    assert Pattern(dict(self='a:1 a:2')).match(obj) == None
    assert p.match({'self':None}) == None
    assert Pattern(dict(self=None)).match({'self':None}) == {}
    
    
def test_notexact():
    obj={'self':Obj(a=1,b=2,c=3)}
    p=makePattern('a:!2 b:2')
    assert p.match(obj) == {}
    obj['self'].a=2
    assert p.match(obj) == None
    
def test_vars():
    obj={'self':Obj(a=1,b=2,c=1)}
    
    assert makePattern('a:?x').match(obj) == {'x':'1'}
    assert makePattern('a:?x c:?x').match(obj) == {'x':'1'}
    assert makePattern('a:?x b:?x').match(obj) == None
    assert makePattern('a:?x b:?y').match(obj) == {'x':'1','y':'2'}
    assert makePattern('a:?x b:!?x').match(obj) == {'x':'1'}
    assert makePattern('a:?x c:!?x').match(obj) == None
    
def test_unnamed_slot():
    obj={'self':[1,2,1]}

    assert makePattern('?x').match(obj) == {'x':'1'}
    assert makePattern('?x ? ?x').match(obj) == {'x':'1'}
    assert makePattern('?x ?x').match(obj) == None
    assert makePattern('?x ?y').match(obj) == {'x':'1','y':'2'}
    assert makePattern('?x !?x').match(obj) == {'x':'1'}
    assert makePattern('?x ? !?x').match(obj) == None
        
    assert makePattern('?x 1:?y').match(obj) == {'x':'1','y':'2'}
    assert makePattern('?x 2:?x').match(obj) == {'x':'1'}
    assert PatternException,makePattern == ('a:1 2')
  
    
def test_str():
    obj={'self':dict(a=True,b=False,c=None)}
    
    assert makePattern('a:True').match(obj) == {}
    assert makePattern('b:False').match(obj) == {}
    assert makePattern('c:None').match(obj) == {}
    
    assert makePattern('a:False').match(obj) == None
    assert makePattern('b:None').match(obj) == None
    assert makePattern('c:False').match(obj) == None
    
def test_group():
    obj={'a':dict(a=1,b=None),'c':dict(d=2,e=1)}
    
    assert Pattern(dict(c='d:2 e:1')).match(obj) == {}
    assert Pattern(dict(a='a:?x',c='d:2 e:?x')).match(obj) == {'x':'1'}
    assert Pattern(dict(a='b:!?x',c='d:!?x e:?x')).match(obj) == {'x':'1'}
    assert Pattern(dict(a='a:!?x b:!?x',c='d:!?x e:?x')).match(obj) == None
  
def test_lambda():
    obj={'self':Obj(a=1,b=2,c=1)}

    assert makePattern(lambda x,b: x.a+x.b+x.c==4).match(obj) == {}
    assert makePattern(lambda x,b: x.a+x.b+x.c==3).match(obj) == None      
    assert makePattern(['a:?z',lambda x,b: x.a+x.b+x.c-int(b['z'])==3]).match(obj) == {'z':'1'}
    assert makePattern(['a:?z',lambda x,b: x.a+x.b+x.c+int(b['z'])==3]).match(obj) == None