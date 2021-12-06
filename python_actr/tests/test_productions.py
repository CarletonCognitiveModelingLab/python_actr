import python_actr





def test_self():
    class ProdTest(python_actr.ProductionSystem):
      x=1
      def test(self='x:1'):
          self.x=2

    p=ProdTest()
    p.run()
    assert p.x == 2
    

def test_multi():
    class Prod(python_actr.ProductionSystem):
      class Module1(python_actr.Model):
         a=1
         def set(self,value):
             self.a=value
      class Module2(python_actr.Model):
         b=2
         def set(self,value):
             self.b=value
      state='swap'
      def swap(self='state:swap',Module1='a:?a',Module2='b:?b'):
          Module1.set(b)
          Module2.set(a)
          self.state=None

    p=Prod()
    p.run()
    assert p.Module1.a == '2'
    assert p.Module2.b == '1'

    
    
    
    


if __name__ == '__main__':
  unittest.main()     
