import python_actr
import unittest

class SubSubModel(python_actr.Model):
  def start(self):
    self.value=0
    yield self.random.random()
    self.value+=1


class SubModel(python_actr.Model):
  def start(self):
    self.value=0
    yield self.random.random()
    self.value+=1
  subsub1=SubSubModel()
  subsub2=SubSubModel()

class BaseModel(python_actr.Model):
  def start(self):
    self.value=0
    yield 1
    self.value+=1
  
  sub1=SubModel()
  sub2=SubModel()

class ModuleA(python_actr.Model):
  def __init__(self,other):
    self.other=other
  def start(self):
    yield 0.5
    self.other.a='a'
    yield 0.5
    self.other.store(1)

class ModuleB(python_actr.Model):
  def store(self,value):
    self.value=value

class Joined(python_actr.Model):
  b=ModuleB()
  a=ModuleA(b)
 

class TestNested(unittest.TestCase):
  def test_nested(self):
    m=BaseModel()
#    python_actr.log_everything(m)
    m.run()
    self.assertEqual(m.value,1)
    self.assertEqual(m.sub1.value,1)
    self.assertEqual(m.sub2.value,1)
    self.assertEqual(m.sub1.subsub1.value,1)
    self.assertEqual(m.sub2.subsub1.value,1)
  
  def test_joined(self):
    m=Joined()  
#    python_actr.log_everything(m)
    m.run()
    self.assertEqual(m.b.a,'a')
    self.assertEqual(m.b.value,1)



if __name__ == '__main__':
    unittest.main()    

