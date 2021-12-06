from .default import DefaultRenderer

def render(obj,screen):
    try:
        obj._display.render(screen)
    except AttributeError:
        obj._display=DefaultRenderer(obj,screen)
    for c in obj.get_children():
        render(c,screen)
        
