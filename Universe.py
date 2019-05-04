'''
Universe Class
    __init__,
    __str__
'''

class Universe:
    
    # initialize all the parameters
    def __init__(self, name="", rewards=[], portals=[]):

        self.name = name
        self.rewards = []
        self.portals = []

        if rewards:
            self.rewards.extend(rewards)
            
        if portals:
            self.portals.extend(portals)

    # convert to string format
    def __str__(self):

        string = "Universe: {} ({} rewards and {} portals)"\
            .format(self.name, len(self.rewards), len(self.portals))

        string = string + "\nRewards:"
        if self.rewards:
            string = string + \
                "".join("\nat ({},{}) for {} points: {}" \
                        .format(*r) for r in self.rewards)
        else:
            string = string + "\nNone"
            
        string = string + "\nPortals:"
        if self.portals:
            string = string + \
                "".join("\n{}:({},{}) -> {}:({},{})"
                        .format(self.name, *p) for p in self.portals)
        else:
            string = string + "\nNone"

        return string



if __name__ == "__main__":

    Universe1 = Universe(name="EasyCS1",\
                  rewards=[[40, 60, 10, 'instant set knowledge'],
                           [100, 200, 40, 'bonus 5 points on hw'],
                           [200, 400, 30, 'instant knowledge of lists'],
                           [600, 800, 50, 'good variable name']],
                  portals=[[800, 600, 'MediumCS1', 200, 300],\
                           [100, 200, 'HardCS1', 10, 20]])
    
    print(str(Universe1))   
    