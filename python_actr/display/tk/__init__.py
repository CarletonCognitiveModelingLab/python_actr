from .default import DefaultRenderer

def render(obj,canvas):
    if not hasattr(obj,'_display'):
        obj._display=DefaultRenderer(obj,canvas)    
    obj._display.render(canvas)
    for c in obj.get_children():
        render(c,canvas)
        
