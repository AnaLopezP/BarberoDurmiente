import random
import time
from threading import *

num_sillas = 4
num_clientes = 8
num_ocupadas = 0

#Creo semáforos cerrados para controlar las posibles situaciones del barbero y los clientes.
barbero_durmiendo = Semaphore(0)
cliente = Semaphore(0)
cliente_espera = Semaphore(0)
cliente_atendido = Semaphore(0)

class Barbero(Thread):
    def __init__(self):
        super().__init__()
        self.estado = False #Es false si está durmiendo. True si está despierto

    def get_estado(self):
        return self.estado

    def set_estado(self, estado):
        self.estado = estado 
    
    def run(self):
        pass

class Cliente(Thread):
    #Los distintos estados del cliente son los semáforos de arriba. 
    #Puede estar: esperando, atendido, o no hay sillas.
    #Ponemos un tiempo para que vayan apareciendo clientes:
    time.sleep(random.uniform(0, 15))

    def _init_(self, id):
        super().__init__()
        self.id = id