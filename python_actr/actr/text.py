import python_actr

class TextOutput(python_actr.Model):
    def write(self,text):
        print(text)
        self.log._=text
