from maspy import *
from maspy.learning import *
from time import sleep
import random
from Report import Report

class City(Environment):
    def __init__(self, env_name=None, args=None):
        super().__init__(env_name)
        
        self.target = args['target']
        self.max_row = args['cartesian_size'] - 1
        self.max_col = args['cartesian_size'] - 1
        self.bad_ways = self.setBadWays(self.max_col+1)
        self.create(Percept("location", (self.max_row+1,self.max_col+1), cartesian))
        self.possible_starts = args['possible_starts']
        self.report = Report()
        

        self.create(Percept('reward', 0))
        self.create(Percept('dist', 0))
        self.create(Percept('reach', 'Não'))
        print(f"Initial percept created: {self.get(Percept('location', (Any,Any)))}")
    
    def move_transition(self, state: dict, direction: str):
        location = state["location"]

        location =self.moviment(location, direction)
            
        state["location"] = location

        if location == self.target:
            reward = 5
            terminated = True
        elif location in self.bad_ways:
            reward = -3
            terminated = False
        else:
            reward = -1
            terminated = False
        return state, reward, terminated

    @action(listed, ["up","down","left","right"], move_transition)
    def move(self, agt, direction: str):
        percept = self.get(Percept("location", (Any,Any)))
        print(f"Partindo de : {percept.args}")
        print(f"{agt} se moveu para: {direction}")
        # self.print(self.possible_starts)
    

        reward_percept = self.get(Percept('reward', Any))
        dist_percept = self.get(Percept('dist', Any))
        reach_percept = self.get(Percept('reach', Any))
        
        assert isinstance(percept, Percept)
        assert isinstance(reward_percept, Percept)
        assert isinstance(dist_percept, Percept)
        assert isinstance(reach_percept, Percept)
        
        new_location = self.moviment(percept.args, direction)
        
        self.change(percept, new_location)
        print(f"Chegando em: {percept.args}")
    
        reward = reward_percept.args
        dist = dist_percept.args
        reach = reach_percept.args

        if new_location == self.target:
            reward = reward_percept.args + 100
            dist = dist_percept.args + 1
            self.change(reward_percept, reward)
            self.change(dist_percept, dist)
            self.print(f"{agt} reached the target")
            self.change(reach_percept, 'Sim')
            self.add_row(agt)
            Admin().stop_all_agents()
        elif new_location in self.bad_ways:
            self.print("bad way")
            reward = reward_percept.args - 10
            dist = dist_percept.args + 2
        else:
            reward = reward_percept.args - 10
            dist = dist_percept.args + 1
        self.change(reward_percept, reward)
        self.change(dist_percept, dist)

        sleep(3)
    
    def moviment(self, location, direction):
        if direction == "up" and location[0] > 0:
            location = (location[0]-1, location[1])
        elif direction == "down" and location[0] < self.max_row:
            location = (location[0]+1, location[1])
        elif direction == "left" and location[1] > 0:
            location = (location[0], location[1]-1)
        elif direction == "right" and location[1] < self.max_col:
            location = (location[0], location[1]+1)
        return location
    
    #auxiliar
    def setBadWays (self, cols):
        bad_ways = []
        for col in range(round((cols**2)/2)):
            bad_way = (random.randrange(0,cols - 1), random.randrange(0,cols - 1))
            if (bad_way != self.target or bad_way):
                bad_ways.append(bad_way)
        print(f'Rua congestionadas ${bad_ways}')
        return bad_ways
    
    
    def check_reached(self, src, agt):
        reward_percept = self.get(Percept('reward', Any))
        reward = reward_percept.args
        dist_percept = self.get(Percept('dist', Any))
        dist = dist_percept.args
        reach_percept = self.get(Percept('reach', Any))
        reach = reach_percept.args
        self.report.add_row(self.max_col+1, agt, reward_percept.args, dist_percept.args, reach)
        self.change(reward_percept, 0)
        self.change(dist_percept, 0)
        self.change(reach_percept, 'Não')
        return dist 
    
    def add_row(self, agt):
        reward_percept = self.get(Percept('reward', Any))
        reward = reward_percept.args
        dist_percept = self.get(Percept('dist', Any))
        dist = dist_percept.args
        reach_percept = self.get(Percept('reach', Any))
        reach = reach_percept.args
        self.report.add_row(self.max_col+1, agt, reward_percept.args, dist_percept.args, reach)

    def set_start(self, src, start):
        location = self.get(Percept('location', (Any, Any)))

        self.change(location, start)
        