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
