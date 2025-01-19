from maspy import * 
import random
import threading 
import time 
from string import Template
from time import sleep

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
            self.print(f'Táxi iniciando em: {self.taxi.start}')
            
        else:
            self.send(self.client.my_name, tell, Belief("no_taxi"))
            
    @pl(gain, Belief("taxi_going"))
    def find_way(self, src): 
        self.print("Adicionando politica")
        cartesian_size = 4
        self.model.set_state(self.taxi.start)
        self.taxi.add_policy(self.model)
        sleep(5)
        reward = self.check_reached()
        self.print(f'Distância: {reward}')
        if (reward > self.taxi.max_distance):
            self.taxi._strategies.pop()
            self.taxi.disconnect_from("Cidade")
            self.model.reset_percepts()
            self.print(f'Distância máxima aceita pelo Táxi: {self.taxi.max_distance}')
            self.print(f'Buscando outro táxi')
            self.add(Belief("client_request_taxi"))
        else:
            self.print("Finish")
            Admin().stop_all_agents()

    @pl(gain, Goal("show_reward"))
    def show_reward(self, src):
       percept = self.get(Belief('reward', source='Cidade'))