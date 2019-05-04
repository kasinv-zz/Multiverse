'''
Person Class
    __init__,
    __str__
'''

class Person:

    # initialize all parameters
    def __init__(self, name="", radius=0, home_universe=None,
                 x=0, y=0, dx=0, dy=0, current_universe=None, rewards=[]):

        self.rewards = []
        
        self.name = name
        self.radius = radius
        self.home_universe = home_universe
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

        if current_universe is None:
            self.current_universe = home_universe
        else:
            self.current_universe = current_universe           

        if rewards:
            self.rewards.extend(rewards)
    
    # convert to string format
    def __str__(self):

        num_rewards = len(self.rewards)

        points = 0
        
        if num_rewards > 0:
            for rp in self.rewards:
                points += rp[2]
                
        string = "{} of {} in universe {}\n{}at ({:0.1f},{:0.1f}) "
        
        string = string\
            + "speed ({:0.1f},{:0.1f}) with {:0d} rewards and {:0d} points"
        
        string = string.format(self.name, str(self.home_universe),\
                str(self.current_universe), "\t".expandtabs(4), self.x,\
                self.y, self.dx, self.dy, num_rewards, points)

        return string



if __name__ == "__main__":

    P1 = Person("Engineer", 15, "MediumCS1", 20, 30, 4, 5,\
            rewards=[[40, 60, 10, 'instant set knowledge'],
                           [100, 200, 40, 'bonus 5 points on hw'],
                           [200, 400, 30, 'instant knowledge of lists'],
                           [600, 800, 50, 'good variable name']])
    

    P2 = Person("Scientist", 15, "HardCS1", 20, 30, 4, 5,\
            rewards=[[100, 200, 40, 'bonus 5 points on hw'],
                           [600, 800, 50, 'good variable name']])    
    print(P1)
    print()
    print(P2)