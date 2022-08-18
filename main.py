# Referencias:
# https://slixmpp.readthedocs.io/en/latest/
# https://xmpp.readthedocs.io/en/latest/

# Proyecto 1 Redes
# Javier Hernández
# Carnet 19202

import subprocess
from getpass import getpass
import xmpp

# Create user function
def createUser():
    print(' ')
    print('Crear un usuario: ')
    new_user = input('username@alumchat.fun:  ')
    new_password = getpass('password:  ')
    user = new_user
    password = new_password
    jid = xmpp.JID(user)
    print(jid)
    cli = xmpp.Client(jid.getDomain(), debug=[])
    cli.connect()
    if xmpp.features.register(cli, jid.getDomain(), {'username': jid.getNode(), 'password': password}):

        return True
    else:
        return False


cmd = 'python servidor.py -d -j'

menu = True
while menu is True:
    
    print("""
    *************************************************
    Hola, Bienvenido a ALUMCHAT.FUN
    *************************************************
    """)

    op = input('Que desea hacer:\n1.Iniciar sesion\n2.Registrarse\n3.Salir\n>>> ')

    if op == '1':
        user = input('Ingrese su usuario (user@alumchat.fun)\n>>>')
        p = '-p'
        password = getpass('Clave:\n>>> ')
        res = cmd+' '+user+' '+p+' '+password

        list_files = subprocess.run(res)
    elif op == '2':
        print('Registro')
        createUser()

    else:
        print('Gracias por usar el chat\n')
        menu = False