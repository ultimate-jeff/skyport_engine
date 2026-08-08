

def Button(mouse_pos_func: callable):
    """
    this is mean for the Render type classes
    
    this decorator will make it so that your function is only called if the mouse pos is over your Render's rect
    """
    def decorator(func):
        def wrapper(self, event):
            if self.rect.collidepoint(mouse_pos_func()):
                return func(self, event)
        return wrapper
    return decorator

def Toggle(attr_name: str):
    """
    this decorator is meant for Render type classes
    toggles a bool that you name from True to False and vice versa
 
    Example:
        @skyport.decorators.Toggle("is_open")
        def on_click(self, event):
            print("is_open is now", self.is_open)
    """
    def decorator(func):
        def wrapper(self, event):
            setattr(self, attr_name, not getattr(self, attr_name, False))
            return func(self, event)
        return wrapper
    return decorator

def Once(func=None):
    """
    this makes your function only callable once per instance
    """
    def decorator(func):
        fired = set()
 
        def wrapper(self, event):
            if id(self) not in fired:
                fired.add(id(self))
                return func(self, event)
        return wrapper
    if func != None and callable(func):
        return(decorator(func))
    return decorator

