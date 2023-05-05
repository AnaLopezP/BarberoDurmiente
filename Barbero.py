import random
import time
from threading import *

num_sillas = 4
num_clientes = 8
num_ocupadas = 0

#Creo semáforos cerrados para controlar las posibles situaciones del barbero y los clientes.
barbero_ocupado = Semaphore(0)
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
        global num_ocupadas
        while True:
            if barbero.estado == False: #Está durmiendo
                cliente.acquire() 
                '''Como el barbero está durmiendo, espero hasta que entren clientes para despertarlo.
                Eso significa que se va a quedar bloqueado en esta linea hasta que en la clase clientes se despierte al barbero desbloqueando el semáforo clientes'''

            barbero_ocupado.release() #Llego a esta linea cuando el barbero no está haciendo nada (pero no está durmiendo). Desboqueo su semáforo
            cliente_espera.acquire() #Lo desbloqueo cuando esté siendo atendido (en la otra clase)

            print(f"El barbero está atendiendo al cliente\n")
            time.sleep(random.randint(1, 2))
            cliente_atendido.release() #Soltamos el semáforo cuando el cliente ha termiando de estar atendido
            print(f"El cliente ha sido atendido, se va\n")


class Cliente(Thread):
    #Los distintos estados del cliente son los semáforos de arriba. 
    #Puede estar: esperando, atendido, o no hay sillas.
    #Ponemos un tiempo para que vayan apareciendo clientes:
    time.sleep(random.uniform(0, 15))

    def _init_(self, id):
        super().__init__()
        self.id = id

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def run(self):
        global num_ocupadas
        if num_ocupadas == num_sillas:
            print("El cliente se va al no haber sillas libres")
        else: 
            if barbero.estado == False: #Si el barbero está durmiendo
                cliente.release() #Liberamos el semáforo cuando entra un cliente
                print(f"El cliente número {self.id} está siendo atendido")
                num_ocupadas += 1 #Aumentamos en 1 el numero de sillas ocupadas
                barbero.set_estado(True) #Despertamos al barbero
                barbero_ocupado.acquire() #Bloqueo el semáforo ya que le barbero está con un cliente

            else: #Es igual pero no despertamos al barbero porque ya está despierto
                num_ocupadas += 1 
                print(f"El cliente num {self.id} espera a ser atendido en una silla")
                barbero_ocupado.acquire()

            print(f"El cliente num {self.id} está siendo atendido")
            num_ocupadas -= 1 #El cliente se va, bajamos en 1 las sillas ocupadas
            cliente_espera.release()
            cliente_atendido.acquire()
            print(f"El cliente num {self.id} se va.")

            if num_ocupadas == 0:
                print("El barbero se duerme")
                barbero.set_estado(False)


#CÓDIGO PRINCIPAL
list_hilos = [] #Lista donde almaceno los hilos que voy creando
barbero = Barbero() #Creo al barbero
list_hilos.append(barbero)

#Creo a los clientes:
for i in range(1, num_clientes):
    cli = Cliente()
    cli.set_id(i)
    list_hilos.append(cli)

for i in list_hilos:
    i.start() #Hago que se ejecuten los códigos de los hilos barbero y clientes. Llamo al run

for i in list_hilos:
    i.join() #Para esperar a que termine el código anterior antes de continuar