import netmiko
import time
import re
from datetime import datetime
import os

devices=[]
num_reportes=[]
name=""
fecha=""
hora=""
direct=""
last_report=""
def create_folder(name):
        os.mkdir(f"C:/Users/vulpe/OneDrive/Escritorio/Practica02/{name}")

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
    if(last_report==""):
        last_report=direct
        
    with open(f"{direct}","w+") as file:
       for text in output:
           file.write(text)
    net_connect.disconnect()
    print("Document Create!!")


def compare_data(file):
    print("Comparar los archivos de configuracion y si es similar, no crear archivo nuevo de configuracion. Caso contrario, crearlo")

def create_device(ip,username,password,enable):
    device={
    'device_type':"cisco_ios_telnet",
    'ip': ip,
    'username':username,
    'password':password,
    'secret':enable
    }
    
    return device

def compare_compliance():
    print("Compara las lineas de codigo por cada uno de las reglas de compliance que se deben cumplir y los guarda en el infotrme")

print("** Creating network Objects...")
Quantity=int(input('Ingrese numero de dispositivos: '))
while(Quantity>0):
    ip=input('Ingrese la IP del dispositivo: ')
    print("\n\nInformacion Dispositivo\n\n")
    username=input('Ingrese el usuario: ')
    password=input('Ingrese la contrase;a: ')
    enable=input('Ingrese contrase;a de priv user: ')
    router=create_device(ip,username,password,enable)
    devices.append(router)
    Quantity=Quantity-1

while(1>0):
    time.sleep(20)
    for disp in devices:
        create_report(disp)
