from maspy import * 
from maspy.learning import *
from time import sleep
import random
import threading 
import time 
from string import Template
from AgentTaxi import AgentTaxi
from AgentClient import AgentClient
from Controller import Controller
from Environment import City
import re
      
# check function
def check_integer(s):
    if not isinstance(s, str):  # Garante que a entrada seja uma string
        return False
    s = s.strip()  # Remove espaços extras
    if s.isdigit() or (s.startswith('-') and s[1:].isdigit()):  
        return True
    return False
      
def instance(cartesian_size):
    taxi = AgentTaxi("Taxi", cartesian_size)
    taxi_2 = AgentTaxi("Taxi", cartesian_size)
    taxi_3 = AgentTaxi("Taxi", cartesian_size)
    taxi_4 = AgentTaxi("Taxi", cartesian_size)
    taxi_5 = AgentTaxi("Taxi", cartesian_size)
    possible_starts = {'location': [(taxi.start), (taxi_2.start), (taxi_3.start), (taxi_4.start), (taxi_5.start )]}
    client = AgentClient("Client", cartesian_size)
    city = City("Cidade", {"target": client.target, "cartesian_size": cartesian_size, "possible_starts": possible_starts})
    model = EnvModel(city)
    model.learn(qlearning)
    controller = Controller("Controller", [taxi, taxi_2, taxi_3, taxi_4, taxi_5], model, client)
    client.add(Goal("request_taxi"))
    Admin().connect_to([controller, taxi, taxi_2, taxi_3, taxi_4, client], city)

    Admin().start_system()
    Admin().full_report = True
    # Admin().stop_system()

if __name__ == "__main__":
    entrada = int(input("Digite o tamanho da matriz quadrada desejada, ex: 5 para uma matriz 5x5 : "))
    cartesian_size = entrada
    instance(cartesian_size)


# 1. Cliente solicita táxi 
# 1.1 Cliente está um local (taget) no modelo no mapa 
# 2. Controllador acha um táxi disponível
# 3. Táxi vai andar no plano cartesiano até encontrar o cliente