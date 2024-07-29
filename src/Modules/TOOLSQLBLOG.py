import sqlite3
import jwt
import datetime
import cryptocode
import time
import random
import os


######### LOGGER ###########
import logging
try:
    import LOGGER
except:
    pass

log = logging.getLogger("BLOGDB")

############################


########## EDIT ############

DB_FOLDER = "Databases"

DB_NAME = "blogdb.db"

############################

SYSTEM_PATH = os.getcwd()

PATH = os.path.join(SYSTEM_PATH, DB_FOLDER)

PARENT_DIR = os.path.dirname(SYSTEM_PATH)

if os.path.exists(PATH) and os.path.isdir(PATH):
    DB_PATH = os.path.join(PATH, DB_NAME)
else:
    PARENT_PATH = os.path.join(PARENT_DIR, DB_FOLDER)
    if os.path.exists(PARENT_PATH) and os.path.isdir(PARENT_PATH):
        DB_PATH = os.path.join(PARENT_PATH, DB_NAME)
    else:
        os.makedirs(PATH, exist_ok=True)
        DB_PATH = os.path.join(PATH, DB_NAME)


######### connection and cursor #########
con = sqlite3.connect(DB_PATH, check_same_thread=False)

cur = con.cursor()


def recon():
    global con
    global cur
    con = sqlite3.connect(DB_PATH, check_same_thread=False)
    cur = con.cursor()
##########################################


def CONNECTION_TEST():
    global con
    global cur
    "CONNECTION_TEST: This function is used to test the connection to the database"
    try:
        con_test = sqlite3.connect(DB_PATH)
        cur_test = con_test.cursor()
        cur_test.execute('SELECT * FROM USERDB')
        con_test.close()
        log.info("CONNECTION_TEST: OK (sqlite3) ")
        return f'\nCONECTADO CORRECTAMENTE A SQLite3\n'
    except Exception as e:
        ERROR = f"ERROR AL CONECTARSE A SQLite3:\n{e}"
        if ERROR.__contains__("Unknown database"):
            try:
                CREATE_TABLE()
                log.info("CONNECTION_TEST: OK (sqlite3)")
                return f'\nCONECTADO A SQLite3 + TABLA DE DATOS CREADAS'
            except Exception as e:
                ERROR = f"ERROR AL CONECTARSE A SQLite3:\n{e}"
                log.error(f'[CONNECTION_TEST] [ERROR 1] {ERROR}')
                return ERROR
        else:
            try:
                CREATE_TABLE()
                con = sqlite3.connect(DB_PATH, check_same_thread=False)
                cur = con.cursor()
                log.info("CONNECTION_TEST: OK (sqlite3)")
                return f'\nCONECTADO CORRECTAMENTE A SQLite3\n'
            except Exception as e:
                ERROR = f"ERROR AL CONECTARSE A SQLite3:\n{e}"
                log.error(f'[CONNECTION_TEST] [ERROR 2] {ERROR}')
                return ERROR


def CREATE_TABLE():
    """
    CREATE_TABLE()
    this function is used to create a table in the database.

    return: message with the table created.

    Example:
    CREATE_TABLE()

    return: 'TABLA DE DATOS CREADA'
    """
    
    EXECREATE = 'CREATE TABLE BLOGDB (ID INTEGER PRIMARY KEY AUTOINCREMENT, TITLE TEXT, CONTENT TEXT, C_BY TEXT, TAGS TEXT, PERMISSION TEXT, EXTRA TEXT, TIME TEXT)'
    try:
        recon()    
        cur.execute(EXECREATE)
        con.close()
        log.info(f"[CREATE_TABLE:] [OK]")
        return f'TABLA DE DATOS CREADA'
    except Exception as e:

        ERROR = f"ERROR AL CREAR LA TABLA:\n{e}"
        if ERROR.__contains__("Unknown database"):
            try:
                recon()
                cur.execute(f'CREATE DATABASE {DB_NAME}')
                cur.execute(EXECREATE)
                con.close()
                log.info(f"[CREATE_TABLE:] [OK]")
                CONNECTION_TEST()
                return f'TABLA DE DATOS CREADA'
            except Exception as e:
                ERROR = f"ERROR AL CREAR LA TABLA:\n{e}"
                log.error(f"[CREATE_TABLE:] [ERROR] {ERROR}")
                return ERROR
        else:
            log.error(f"[CREATE_TABLE:] [ERROR2] {ERROR}")
            return ERROR


def INSERT_BL(TITLE='', CONTENT='', C_BY=''):
    try:
        comp1 = SEARCH_BL('TITLE', TITLE)
        if comp1 == None:
            TIME = datetime.datetime.now()
            recon()
            cur.execute(
                f'INSERT INTO BLOGDB (TITLE, CONTENT, C_BY, TIME)  VALUES ("{TITLE}", "{CONTENT}", "{C_BY}", "{TIME}")')
            con.commit()
            con.close
            log.info(
                f"[INSERT_DB:] [OK] (Title: {TITLE}, Content: {CONTENT}, Create_by: {C_BY})")
            return f'ENTRADA {TITLE} CREADA CORRECTAMENTE'

        else:
            log.debug(
                f"[INSERT_DB:] [ERROR] TITLE EXIST (Title: {TITLE}, Content: {CONTENT}, Create_by: {C_BY})")
            return f'EL TITULO {TITLE} YA EXISTE'
    except Exception as e:
        ERROR = f"ERROR AL INCERTAR EN LA TABLA:\n{e}"
        log.error(
            f"[INSERT_DB:] [ERROR] [{ERROR}] (Title: {TITLE}, Content: {CONTENT}, Create_by: {C_BY})")
        return ERROR


def ALL_BL():

    try:
        lista = []
        recon()
        for row in cur.execute('SELECT * FROM BLOGDB'):
            ALL = row
            lista.append(ALL)
        con.close
        log.debug(f"[ALL_BLOGS:] [OK]")
        return lista
    except Exception as e:
        ERROR = f"ERROR AL BUSCAR TODO EN LA TABLA:\n{e}"
        log.error(f"[ALL_BLOGS:] [ERROR] [{ERROR}]")
        return ERROR

def SEARCH_BL(TYPE='TITLE', DATA_SEARCH=''):
    try:
        recon()
        TIPOS = ["ID", "TITLE", "CONTENT", "C_BY", "TAGS", "PERMISSION", "EXTRA"]
        if TYPE in TIPOS:
            search_sql = f'SELECT * FROM BLOGDB WHERE {TYPE}="{DATA_SEARCH}"'
            cur.execute(search_sql)
            resp = None
            for rew in cur.fetchall():
                log.debug(
                    f"[SEARCH_DB:] [OK] (type: {TYPE}, data: {DATA_SEARCH})")
                resp = rew
            con.close()
            return resp
            

        elif TYPE == 'TIME':
            lista = []
            cur.execute('SELECT * FROM BLOGDB')
            for row in cur.fetchall():
                ALL = row
                if ALL[8].__contains__(DATA_SEARCH):
                    lista.append(ALL)
            con.close
            log.debug(f"[SEARCH_DB:] [OK] (type: {TYPE}, data: {DATA_SEARCH})")
            return lista
        else:
            log.debug(
                f"[SEARCH_DB:] [None] (type: {TYPE}, data: {DATA_SEARCH})")
            return None
    except Exception as e:
        ERROR = f"ERROR AL BUSCAR EN LA TABLA:\n{e}"
        log.error(
            f"[SEARCH_DB:] [ERROR] [{ERROR}] (type: {TYPE}, data: {DATA_SEARCH})")
        return ERROR



def DELETEBL(B_ID):
    """
    DELETE(US_EM)
    US_EM: The user email or user name.

    return: True or False.

    Example:
    DELETE('user')

    return: True
    """

    try:
        if SEARCH_BL('ID', B_ID) != None:
            recon()
            cur.execute(f'DELETE FROM BLOGDB WHERE ID="{B_ID}"')
            con.commit()
            con.close()
            log.info(f'[DELETEBL:] [OK] (ID: {B_ID})')
            return 'EL CORREO SE HA BORRADO'
        else:
            log.debug(f'[DELETEBL:] [None] (ID: {B_ID})')
            return 'EL CORREO NO EXISTE '
    except Exception as e:
        ERROR = f'ERROR AL BORRAR:\n{e}'
        log.error(f'[DELETEBL:] [ERROR] (ERROR={ERROR})')
        return ERROR


def EDITBL(TYPE='TITLE', B_ID='', NEWD=''):

    try:
        if not SEARCH_BL('ID', B_ID) == None:
            TIPOS = ["ID", "TITLE", "CONTENT", "C_BY", "TAGS", "PERMISSION", "EXTRA", "TIME"]
            if TYPE in TIPOS:
                recon()
                cur.execute(
                    f'UPDATE BLOGDB SET {TYPE}="{NEWD}" WHERE ID="{B_ID}"')
                con.commit()
                con.close()
                log.info(
                    f'[EDITARBL:] [OK] (type: {TYPE}, id: {B_ID}, data: {NEWD})')
                return 'EDITADO'
            else:
                log.debug(
                    f'[EDITARBL:] [None] (type: {TYPE}, id: {B_ID}, data: {NEWD})')
                return 'COMPRUEBE QUE DESEA EDITAR'
        else:
            log.debug(
                f'[EDITARBL:] [None] No Exist (type: {TYPE}, id: {B_ID}, data: {NEWD})')
            return f'EL POST {B_ID} NO EXISTE'

    except Exception as e:
        ERROR = f'ERROR AL EDITAR\n{e}'
        log.error(f'[EDITARBL:] [ERROR] (ERROR={ERROR})')
        return ERROR


def COMMANDSQL(text):
    try:
        lista = []
        recon()
        for row in cur.execute(text):
            ALL = row
            lista.append(ALL)
        con.close
        log.debug(f"[COMMANDSQL:] [{text}] [OK]")
        return lista
    except Exception as e:
        ERROR = f"ERROR AL EJECUTAR:\n{e}"
        log.error(f"[COMMANDSQL:] [ERROR] [{ERROR}]")
        return ERROR


if __name__ == '__main__':

    print(CONNECTION_TEST())
    existe = os.path.isfile(DB_PATH)
    if existe == True:
        print("RUTA =", DB_PATH)
    else:
        print(f"ERROR: LA RUTA ={DB_PATH} NO EXISTE")

    while True:
        entrada = str(input('\nEscribe aqui: '))

        if entrada.startswith('crearTabla'):
            respuesta = CREATE_TABLE()
            print(respuesta)
        
        if entrada == "sql":
            texto = input("Comando: ")
            resp = COMMANDSQL(texto)
            print(resp)
        
        if entrada == 'insert':
            valor1 = input('TITULO: ')
            valor2 = input('CONTENIDO: ')
            valor3 = input('ID CREADOR: ')
            respuesta = INSERT_BL(valor1, valor2, valor3)
            print(respuesta)

        if entrada == 'ls':
            respuesta = ALL_BL()
            print(respuesta)

        if entrada == 'buscar':
            valor1 = input('TIPO DE BUSQUEDA: ')
            valor2 = input('DATO A BUSCAR: ')
            respuesta = SEARCH_BL(valor1, valor2)
            print(respuesta)


        if entrada == 'borrar':
            valor1 = input('ESCRIBA PARA BORRAR: ')
            respuesta = DELETEBL(valor1)

            print(respuesta)

        if entrada == 'editar':
            valor1 = input('TIPO: ')
            valor2 = input('USUARIO: ')
            valor3 = input('INFO NEW: ')
            respuesta = EDITBL(valor1, valor2, valor3)
            print(respuesta)


        if entrada == 'help':

            respuesta = """
            Help:
            crearTabla Crea una Tabla
            insert Inserta un usuario
            ls Lista todos los usuarios
            buscar Busca un usuario
            encriptar Encripta un texto
            desencriptar Desencripta un texto
            validar Valida un usuario
            borrar Borra un usuario
            editar Edita un usuario
            conv valida un codigo de confirmacion de correo
            """

            print(respuesta)
