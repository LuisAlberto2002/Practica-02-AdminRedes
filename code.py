#Librerias Necesarias para ejecucion de NCM
import netmiko
import time
import re
from datetime import datetime
import os

#Variables
devices=[]
name=""
fecha=""
hora=""
direct=""
#Funcion que crear la carpeta de almacenamiento de las configuraciones de los routers
def create_folder(name):
        try:
            os.mkdir(f"C:/Users/vulpe/OneDrive/Escritorio/Practica02/{name}")
        except OSError:
            print(f"La carptera de almacenamiento para {name} ya existe")
        else:
            print(f"Carpeta de almacenamiento para {name} ha sido creada exitosamente")

#Funcion que crea el reporte de las configuraciones de los routers
def create_report(disp):
    net_connect=netmiko.ConnectHandler(**disp)
    net_connect.enable()
    net_connect.config_mode()
    output=net_connect.send_command("do show running-config")
    name=re.findall(r'RTR.',output)
    create_folder(name)
    fecha= datetime.now().strftime("%Y-%m-%d")
    hora=datetime.now().strftime('%H-%M-%S')
    direct=f"C:/Users/vulpe/OneDrive/Escritorio/Practica02/{name}/{name}-{fecha}-{hora}.txt"
    with open(f"{direct}","w+") as file:
       for text in output:
           file.write(text)
    net_connect.disconnect()
    print("Document Create!!")

#funcion que crea el objeto para realizar la conexion

def create_device(device_type,ip,username,password,secret,port):
    device={
    'device_type':device_type,
    'ip': ip,
    'username':username,
    'password':password,
    'secret':secret,
    'port':port
    }
    return device

#Inicio de ejcucion, se ingresan los valores de cada router, al igual que la cantidad de estos
print("** Creating network Objects...")
Quantity=int(input('Ingrese numero de dispositivos: '))
while(Quantity>0):
    print("\n\nInformacion Dispositivo\n\n")
    ip=input('Ingrese la IP del dispositivo: ')
    username=input('Ingrese el usuario: ')
    password=input('Ingrese la contrase;a: ')
    secret=input('Ingrese contrase;a de priv user: ')
    device_type="cisco_ios"
    port=22
    router=create_device(device_type,ip,username,password,secret,port)
    devices.append(router)
    Quantity=Quantity-1

#Es un ciclo que se ejecuta cada 20 seg
while(1>0):
    for disp in devices:
        try:
            create_report(disp)
        except BaseException:
            print("Coneccion fallida, intentando nueva conexion")
            device_type="cisco_ios_telnet"
            port=23
            disp['device_type']=device_type
            disp['port']=port
            create_report(disp)
            time.sleep(20)
        else:
            time.sleep(20)
