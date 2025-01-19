from maspy import * 
import random
import threading 
import time 
from string import Template

class AgentTaxi(Agent):
    def __init__(self, agt_name, cartesian_size):
        super().__init__(agt_name)
        self.add(Belief("available"))
        self.value = random.randrange(0, 10)
        self.start = (random.randrange(0, cartesian_size - 1), random.randrange(0, cartesian_size - 1))
        self.max_distance = random.randrange(0, 5)
    
    def agent_name(self):
        return self.my_name
        
    @pl(gain, Goal("pickup_client"))
    def atender_corrida(self, src):
        self.print("Se locomovendo em direção ao passageiro")
        self.send(src, tell, Belief("taxi_going"))
    
        