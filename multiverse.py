import json
import math
from Person import *
from Universe import *

'''
SPerson Class
    __init__
    getRewardPoints()
    CheckWithinRadius(x,y)
    CalcSpeed()
    CrashWith(p2)
'''
class SPerson(Person):
    
    def __init__(self, name="", radius=0, home_universe=None,
                 x=0, y=0, dx=0, dy=0, current_universe=None,
                 rewards=[], stopped=False, reward_universe=[]):

        super().__init__(name, radius, home_universe,
                         x, y, dx, dy, current_universe,
                         rewards)
        
        self.stopped = stopped
        self.reward_universe = []
        
        if reward_universe:
            self.reward_universe = reward_universe
     
    """ 
    p.getRewardPoints()
    method to get points and rewards for a person
    returns tuple of (# of rewards, sum(points))
    used to evaluate winner(s) during simulation 
    """
    def getRewardPoints(self):
        return (len(self.rewards), sum(x[2] for x in self.rewards))
     
    """ 
    p.CheckWithinRadius(x,y)
    method to check if point x, y is within person's radius
    check distance between person and (x,y) with radius
    returns True or False (if within radius or not)
    """
    def CheckWithinRadius(self, x, y):
        return (math.sqrt((self.x-x)**2 + (self.y-y)**2) <= self.radius)
    
    
    """
    CalculateSpeed of person (crash)
    method to calculate speed, based on the reward load
    depending on whether or not there is a crash
    returns None
    """
    def CalcSpeed(self, crash):
         
        if not crash:
            n = len(self.rewards)
            self.dx = self.dx - (n%2)* (n/6)*self.dx
            self.dy = self.dy - ((n+1)%2)* (n/6)*self.dy
            return None
        else:
            n = len(self.rewards)
            self.dx = -(self.dx + (n%2) * (n/6)*self.dx)
            self.dy = -(self.dy + ((n+1)%2)* (n/6)*self.dy)
            return None            
     
    """
    p.CrashWith(self, p2)
    method to check if person will crash with p2
    returns true if crashing else false
    """
    def CrashWith(self, p2):
        
        d = math.sqrt((self.x-p2.x)**2 + (self.y-p2.y)**2)
        
        return (self.current_universe == p2.current_universe and
                d <= (self.radius + p2.radius))
    
        
"""
move all the persons

for all the persons, check eligible rewards to be picked up
check if person has reached limits, stop moving after reward collection

for all the persons, check crash scenario
check if person has reached limits, stop moving after crash scenario

for all the persons, check if portal cross-over
check if person has reached limits, after portal cross-over
"""    
def simulate(U, P, s):
    for p in P:
        for u in U:
            if u.name == p.current_universe:
                move(p, s)
                check_loc_speed(p, s)
                break
            
    for p in P:
        for u in U:
            if u.name == p.current_universe:
                check_reward(u, p, s)
                check_loc_speed(p, s)
                break
            
    for p in P:
        idx = P.index(p)
        for u in U:
            if u.name == p.current_universe:
                check_crash(u, p, P[idx+1:], U, s)
                check_loc_speed(p, s)
                break
            
    for p in P:
        for u in U:
            if u.name == p.current_universe:
                check_portal(u, p, s)
                check_loc_speed(p, s)
                break
            
    return None


"""
check if a person is within bounds and good speed
input:  person object

output: if within bounds and good speed
        set person.stopped = false (can move)
        return true,
        else
        set person.stopped = true (cannot move)
        if stopping for first time (current .stopped = false)
            write out message
        return false
"""
def check_loc_speed(in_p, s):
    if in_p.x < 1000 and in_p.x > 0 and in_p.y < 1000 and in_p.y > 0\
       and abs(float(in_p.dx)) >= 10 and abs(float(in_p.dy)) >= 10:
        
        in_p.stopped = False
        return True
    
    else:
        if not in_p.stopped:
            
            if s == 0:
                sim = s
            else:
                sim = s+1
                     
            print("{} stopped at simulation step {} at location ({:0.1f},{:0.1f})"\
                  .format(in_p.name, sim, in_p.x, in_p.y))
            print()
            in_p.stopped = True

        return False

"""
if person is in good location and speed
update the x,y of location

input:  person object
output: none
"""
def move(in_p, s):

    if check_loc_speed(in_p, s):
        in_p.x += float(in_p.dx)
        in_p.y += float(in_p.dy)
        
    return None

"""
checks rewards in the universe
if the person is in the vicinity of the reward
pick it up
add the reward to the person, and
remove it from the universe reward list

input:  universe, person, simulation counter
output: none
"""
def check_reward(in_u, in_p, s):
    for r in in_u.rewards:
        rx = r[0]
        ry = r[1]
        rn = r[3]
        
        if in_p.CheckWithinRadius(rx, ry) and not in_p.stopped:
            in_p.rewards.append(r)
            in_p.reward_universe.append(in_u.name)
            in_u.rewards.remove(r)
            in_p.CalcSpeed(0)
            print("{} picked up \"{}\" at simulation step {}"\
                  .format(in_p.name, rn, s + 1))
            print(in_p)
            print()

    return None

"""
adjust reward speed
remove the first reward in the person's reward list
add the reward back to the home universe of the person
change the person speed (dx, dy), based on new reward list

input:  universe, person
output: none
"""
def adj_reward_speed(in_p, U):
    
    if in_p.rewards:
        
        pr = in_p.rewards[0]
        ru = in_p.reward_universe[0]
        
        for ux in U:
            if ux.name == ru:
                ux.rewards.append(pr)
                in_p.rewards.remove(pr)
                in_p.reward_universe.remove(ru)
                in_p.CalcSpeed(1)
                
                print("{} dropped \"{}\", reward returned to {} at ({},{})"\
                      .format(in_p.name, pr[3], ru, pr[0], pr[1]))                
                
                break
        
    return None

"""
checks if two persons are impending crash
if distance between the person is < (sum of radii)
return back the reward to the universe
remove the reward from the person

update the speed based on the current rewards for both persons

input: universe, person, list of persons, simulation counter
output: none
"""
def check_crash(in_u, p1, Pn, U, s):
    
    for p2 in Pn:
    
        if p1.CrashWith(p2) and p1.current_universe == p2.current_universe\
        and not p1.stopped and not p2.stopped:
            
            print("{} and {} crashed at simulation step {} in universe {}"\
                  .format(p1.name, p2.name, s + 1, p1.current_universe))
            
            adj_reward_speed(p1, U)
            adj_reward_speed(p2, U)
            
            print(p1)
            print(p2)
            print()
            break

"""
checks if person is crossing over to another portal
if crossing over, for the person -
update the current_universe
set its coordinates to that of the new portal

input:  universe, person, simulation counter
output: none
"""
def check_portal(in_u, in_p, s):
    temp_val = False
    for t in in_u.portals:
        
        tx = t[0]
        ty = t[1]
        tn = t[2]
        
        newx = t[3]
        newy = t[4]
        
        if in_p.CheckWithinRadius(tx, ty) and not in_p.stopped:
            
            in_p.current_universe = tn
            in_p.x = newx
            in_p.y = newy
            
            print("{} passed through a portal at simulation step {}"\
                  .format(in_p.name, s+1))
            print(in_p)
            print()
            return True
    return temp_val
  

"""
write out the results
get the max(rewards + points) of all people

looping through all persons -
if their (rewards + points) = max value
write the person detail as a winner
also write out the rewards held by the winning person(s)
"""      
def showresults(P):
    
    max_pr = max(sum(p.getRewardPoints()) for p in P)
    
    print("Winners:")
    for p in P:
        if sum(p.getRewardPoints()) == max_pr:
            print(p)
            print("Rewards:")
            for r in p.rewards:
                print("\t".expandtabs(4) + r[3])
            print()
            

if __name__ == "__main__":

    # read input file name from user
    infile = input("Input file => ")
    print(infile)
    
    # initialize list of universe and people
    data = json.loads(open(infile).read())
    U = []
    P = []

    # for every json dictionary record
    for u in data:

        # append the universe name, rewards, and portals ro the Universe class
        uname = u['universe_name']
        urewards = u['rewards']
        uportals = u['portals']
        U.append(Universe(uname, urewards, uportals))


        # append every individual's info to the super person class
        for p in u['individuals']:
        
            P.append(SPerson(name=p[0], radius=p[1], home_universe=uname,
                             x=p[2], y=p[3], dx=p[4], dy=p[5]))


    # print all universes
    print("All universes")
    print(40*"-")
    for u in U:
        print(u)
        print()
     
    # print all individuals                 
    print("All individuals")
    print(40*"-")
    for p in P:
        print(p)
    print()
   
    # start simulation
    print("Start simulation")
    print(40*"-")   
    for i in range(100):
        simulate(U, P, i)
        
        numstopped = sum(p.stopped for p in P)
        if numstopped == len(P):
            break
     
    # print final results after going through all simulations    
    print()
    print(40*"-") 
    print("Simulation stopped at step {}".format(i+1))
    if (len(P) - numstopped) == 0:
        print("{} individuals still moving".format(len(P) - numstopped))
    else:
        moving_person = []
        for p in P:
            if not p.stopped:
                moving_person.append(p.name)

        print("{} individuals still moving: {}".format((len(P) - numstopped),\
                                                    ", ".join(moving_person)))
    showresults(P)