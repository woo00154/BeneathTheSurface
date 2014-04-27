class InputHandler:
    
    def __init__(self):
        self.button_list = {}
    
    def add_button(self,button):
        self.button_list.setdefault(button,False)
