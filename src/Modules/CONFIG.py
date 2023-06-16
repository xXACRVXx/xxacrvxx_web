import os
import platform
import psutil
from dotenv import load_dotenv

load_dotenv("config.env") # carga las variables de entorno desde el archivo .env

SECRECT = os.getenv("SECRET_KEY")



MY_OS = platform.system()
SYSTEM_PATH = os.getcwd()
if MY_OS == "Windows":
    DOWLOAD_PATH = "\Downloads"
else:
    DOWLOAD_PATH = "/Downloads"


RUTE = f"{SYSTEM_PATH}{DOWLOAD_PATH}"




disk_usage = psutil.disk_usage(SYSTEM_PATH)
disk_space = disk_usage.free / 1024**2
if disk_space >= 1024:
    the_space = round(disk_space / 1024, 2)
    Free_Space = f"{the_space}GB"
else:
    the_space = round(disk_space, 2)
    Free_Space = f"{the_space}MB"




def SPACE_FILE(uss,archive):  
    if MY_OS == "Windows":
        the_file=os.path.getsize((rf'{RUTE}\{uss}\{archive}'))
        f_space = the_file / 1024**2
        if f_space >= 1024:
            the_space_file = round(f_space / 1024, 2)
            return f"{the_space_file}GB"
        else:
            the_space_file = round(f_space, 2)
            return f"{the_space_file}MB"
    else:
        the_file=os.path.getsize((rf'{RUTE}/{uss}/{archive}'))
        f_space = the_file / 1024**2
        if the_file / 1024**1 <= 1024:
            the_space_file = round(the_file / 1024**1, 2)
            return f"{the_space_file}KB"
        elif f_space >= 1024:
            the_space_file = round(f_space / 1024, 2)
            return f"{the_space_file}GB"
        else:
            the_space_file = round(f_space, 2)
            return f"{the_space_file}MB"






if __name__ == "__main__":
    print(f"SISTEMA OPERATIVO: {MY_OS}")
    print(f"RUTA DEL PATH DEL SERVIDOR: {RUTE}")
    print(f"ESPACIO DISPONIBLE  {Free_Space}")
