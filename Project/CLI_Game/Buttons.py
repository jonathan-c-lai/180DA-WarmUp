# for holding the class that should represent button object
# there should be another class that should have the game logic where buttons are created

class Buttons:
    difficulty = 1

    # existing buttons will be key'd with their location and then value will be the 
    # key press that it should be
    existing_buttons = dict()
    
    def __init__(self):
        self.existing_buttons = dict()

    def spawn_button(self):
        self.existing_buttons

    # returns whether a button exists at a certain location
    def __button_exists(self, location):
        if location in self.existing_buttons:
            return True
        else:
            return False