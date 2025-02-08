from maspy import *
from maspy.learning import *
from time import sleep
import random
import threading 
import time 
from string import Template

class Controller(Agent):
    def __init__(self, agt_name, taxis, model, client):
        super().__init__(agt_name)
        self.taxis = taxis
        self.taxi = None
        self.client = client
        self.model = model
          
    @pl(gain, Belief("client_request_taxi"))
    def search_available(self, src):
        available_taxis = []
            
        for taxi in self.taxis:
            if (taxi.has(Belief("available"))):
                self.print(Template('Valor da corrida do ${name} : ${value}').substitute(name=taxi.my_name, value=taxi.value))
                available_taxis.append(taxi)

        if available_taxis:
            nearest_taxi = min(available_taxis, key=lambda taxi: taxi.value)

            self.taxi = nearest_taxi
            self.taxi.rm(Belief("available"))
            self.send(self.taxi.my_name, achieve, Goal("pickup_client"))

            self.print(Template('${nome} escolhido').substitute(nome=self.taxi.my_name))
            self.print(f'Táxi iniciando em: {self.taxi.start_pos}')
            
        else:
            self.send(self.client.my_name, tell, Belief("no_taxi"))
            
    @pl(gain, Belief("taxi_going"))
    def find_way(self, src): 
        self.print("Adicionando politica")
        cartesian_size = 4
        # self.city.possible_starts = {'location': [self.taxi.start]}
        self.set_start(self.taxi.start_pos)
        self.taxi.add_policy(self.model)
        self.taxi.auto_action = True
        # sleep(5)
        # reward = self.check_reached()
        # self.print(f'Distância: {reward}')
        # if (reward > self.taxi.max_distance):
        #     self.taxi._strategies.pop()
        #     self.taxi.disconnect_from("Cidade")
        #     self.model.learn(qlearning)
        #     self.print(f'Distância máxima aceita pelo Táxi: {self.taxi.max_distance}')
        #     self.print(f'Buscando outro táxi')
        #     self.add(Belief("client_request_taxi"))
        # else:
        #     self.print("Finish")
        #     Admin().stop_all_agents()
        
        # [(0, 0), (1, 0), (2, 2), (2, 0), (1, 2), (0, 1), (2, 0), (2, 0)]

    @pl(gain, Goal("show_reward"))
    def show_reward(self, src):
       percept = self.get(Belief('reward', source='Cidade'))

class AgentTaxi(Agent):
    def __init__(self, agt_name, cartesian_size):
        super().__init__(agt_name)
        self.add(Belief("available"))
        self.value = random.randrange(0, 10)
        self.start_pos = (random.randrange(0, cartesian_size - 1), random.randrange(0, cartesian_size - 1))
        self.max_distance = random.randrange(0, 5)
    
    def agent_name(self):
        return self.my_name
        
    @pl(gain, Goal("pickup_client"))
    def atender_corrida(self, src):
        self.print("Se locomovendo em direção ao passageiro")
        self.send(src, tell, Belief("taxi_going"))
    

class AgentClient(Agent):
    def __init__(self, agt_name, cartesian_size):
        super().__init__(agt_name)
        self.target = (random.randrange(0, cartesian_size - 1), random.randrange(0, cartesian_size - 1))
              
    @pl(gain, Goal("request_taxi"))
    def solicitar_taxi(self, src):
        self.print(Template('Cliente na posição ${nome}').substitute(nome=self.target))
        self.send("Controller", tell, Belief("client_request_taxi"))

class City(Environment):
    def __init__(self, env_name=None, args=None):
        super().__init__(env_name)
        
        self.target = args['target']
        self.max_row = args['cartesian_size'] - 1
        self.max_col = args['cartesian_size'] - 1
        self.bad_ways = self.setBadWays(self.max_col+1)
        
        print(f"Bad ways: {self.bad_ways}")
        
        for x in range(self.max_row + 1):
            print('|',end="")
            for y in range(self.max_col + 1):
                if (x,y) == self.target:
                    print('C|',end="")
                elif (x,y) in self.bad_ways:
                    print('X|',end="")
                else:
                    print('-|',end="")
            print('')
        
        self.create(Percept("location", (self.max_row+1,self.max_col+1), cartesian))
        
        self.possible_starts = args['possible_starts']

        self.create(Percept('reward', 0))
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
        print(f"Current location before move: {self.get(Percept('location', (Any,Any)))}")
        self.print(self.possible_starts)

        self.print(f"{agt} is Moving {direction}")
        
        percept = self.get(Percept("location", (Any,Any)))

        reward_percept = self.get(Percept('reward', Any))
        
        assert isinstance(percept, Percept)
        assert isinstance(reward_percept, Percept)
        
        new_location = self.moviment(percept.args, direction)
        
        self.change(percept, new_location)
        self.print_percepts
    
        reward = reward_percept.args

        if new_location == self.target:
            reward = reward_percept.args + 1
            self.print(f"{agt} reached the target")
            # Admin().stop_all_agents()
        elif new_location in self.bad_ways:
            self.print("bad way")
            reward = reward_percept.args + 5
        else:
            reward = reward_percept.args + 1
        self.change(reward_percept, reward)

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
    
    
    def check_reached(self, src):
        reward_percept = self.get(Percept('reward', Any))
        reward = reward_percept.args
        self.change(reward_percept, 0)
        return reward 

    def set_start(self, src, start):
        location = self.get(Percept('location', (Any, Any)))

        self.change(location, start)

def instance(cartesian_size):
    taxi = AgentTaxi("Taxi", cartesian_size)
    #taxi_2 = AgentTaxi("Taxi", cartesian_size)
    #taxi_3 = AgentTaxi("Taxi", cartesian_size)
    #taxi_4 = AgentTaxi("Taxi", cartesian_size)
    #taxi_5 = AgentTaxi("Taxi", cartesian_size)
    possible_starts = {'location': [(taxi.start_pos)]}#, (taxi_2.start), (taxi_3.start), (taxi_4.start), (taxi_5.start )]}
    client = AgentClient("Client", cartesian_size)
    city = City("Cidade", {"target": client.target, "cartesian_size": cartesian_size, "possible_starts": possible_starts})
    model = EnvModel(city)
    #for i,j in model.P.items():
    #    print(f'{i}: {j}')
    model.learn(qlearning)
    controller = Controller("Controller", [taxi], model, client)#, taxi_2, taxi_3, taxi_4, taxi_5], model, client)
    client.add(Goal("request_taxi"))
    Admin().connect_to([controller, taxi, client], city)#, taxi_2, taxi_3, taxi_4, client], city)

    Admin().start_system()
    # Admin().stop_system()

if __name__ == "__main__":
    cartesian_size = 6
    instance(cartesian_size)