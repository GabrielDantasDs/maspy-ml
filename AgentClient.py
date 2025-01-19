from maspy import * 
import random
import threading 
import time 
from string import Template

class AgentClient(Agent):
    def __init__(self, agt_name, cartesian_size):
        super().__init__(agt_name)
        self.target = (random.randrange(0, cartesian_size - 1), random.randrange(0, cartesian_size - 1))
              
    @pl(gain, Goal("request_taxi"))
    def solicitar_taxi(self, src):
        self.print(Template('Cliente na posição ${nome}').substitute(nome=self.target))
        self.send("Controller", tell, Belief("client_request_taxi"))