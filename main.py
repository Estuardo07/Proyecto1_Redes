# Referencias:
# https://slixmpp.readthedocs.io/en/latest/
# https://xmpp.readthedocs.io/en/latest/

# Proyecto 1 Redes
# Javier Hernández
# Carnet 19202

import asyncio
from argparse import ArgumentParser
import xmpp
import sys
from servidor import *
from cliente import *

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

if __name__ == '__main__':
    parser = ArgumentParser(description=Client.__doc__)

    parser.add_argument("-j", "--jid", dest="jid",
                        help="JID to use")
    parser.add_argument("-p", "--password", dest="password",
                        help="password to use")

    parser.add_argument("-s", "--show", dest="show",
                        help="show to use")
    parser.add_argument("-t", "--status", dest="status",
                        help="status to use")
    parser.add_argument("-r", "--register", dest="register",
                        help="Is new user")

    args = parser.parse_args()

    posible_status = {
        "1": "chat",
        "2": "away",
        "3": "dnd",
        "4": "xa",
    }

    print("""
    *************************************************
    Hola, Bienvenido a ALUMCHAT.FUN
    *************************************************
    """)
    print("Que desea hacer:\n1.Registrarse\n2.Iniciar sesion\n3.Salir\n>>> ")
    op = input("Ingresa el numero de opcion que desea: ")
    
    if op == '2':
        if args.jid is None:
            args.jid = input("Ingrese su usuario (user@alumchat.fun)\n>>>")
        if args.password is None:
            args.password = input("Clave:\n>>> ")
        args.show = '1'
        args.status = ''
        print("Inicio de sesion exitoso")
    
    if op == '1':
        if createUser(args.jid, args.password):
            print("Cuenta creada exitosamente ")
        else:
            print("Algo salio mal :( ")
    
    if op == '2':
        dentro = True 
        while dentro: 
            print("1. Mis contactos")
            print("2. Agregar contacto")
            print("3. Mostrar detalles de un contacto")
            print("4. Mensaje privado")
            print("5. Chat grupal")
            print("6. Mensaje de presencia")
            print("7. Cerrar sesion")
            print("8. Eliminar cuenta")
            op2 = input("Elige la opcion que desees: ")
            

            if op2 == '1':
                cliente = Rooster(args.jid, args.password)
                cliente.register_plugin('xep_0030')  # Service Discovery
                cliente.register_plugin('xep_0199')  # XMPP Pin
                print("Mostrando...")
                cliente.connect()
                cliente.process(forever=False)
                print("Ejecucion completa")


            if op2 == '2':
                name = input('Ingrese el nombre: ')
                cliente = AddFriend(args.jid, args.password, name)
                cliente.register_plugin('xep_0030')  # Service Discovery
                cliente.register_plugin('xep_0199')  # XMPP Ping
                cliente.register_plugin('xep_0077')  # In-Band Registration
                cliente.register_plugin('xep_0100')
                print("Agregando...")
                cliente.connect()
                cliente.process(forever=False)
                print("Ejecucion completa")

            if op2 == '3':
                contact = input('Ingrese el nombre del contacto: ')
                cliente = GetInfo(args.jid, args.password, contact)
                print("Mostrando detalles...")
                cliente.connect()
                cliente.process(forever=False)
                print("Ejecucion completa")


            if op2 == '4':
                recipient = input("¿A quien quieres mandarle un mensaje? ") 
                message = input("¿Cual es el mensaje? ")
                meg = Client(args.jid, args.password, recipient, message, posible_status[args.show], args.status)
                meg.register_plugin('xep_0030') # Service Discovery
                meg.register_plugin('xep_0199') # XMPP Ping
                print("Enviando...")
                meg.connect()
                meg.process(forever=False)
                print("Se envio el mensaje correctamente")

            if op2 == '5':
                room = input("Ingresa el nombre del grupo: ") 
                nick = input("¿Que nick quieres usar? ")
                if '@conference.alumchat.fun' in room:
                    cliente = ChatGrupal(args.jid, args.password, room, nick)
                    cliente.register_plugin('xep_0030') # Service Discovery
                    cliente.register_plugin('xep_0199') # XMPP Ping
                    cliente.register_plugin('xep_0045') # Mulit-User Chat (MUC)
                    print("Cargando...")
                    cliente.connect()
                    cliente.process(forever=False)
                    print("Ejecucion completa")
                    

            if op2 == '6':
                m_presencia = input("¿Cual es el mensaje? ")
                cliente = Rooster(args.jid, args.password, message=m_presencia)
                cliente.register_plugin('xep_0030') # Service Discovery
                cliente.register_plugin('xep_0199') # XMPP Ping
                print("Enviando...")
                cliente.connect()
                cliente.process(forever=False)
                print("Ejecucion completa")

            if op2 == '7':
                xmpp.process(timeout=20)
                xmpp.disconnect()
                xmpp.process(timeout=20)
                print("Logged Off")
                sys.exit()

            if op2 == '8':
                xmpp.deleteAccount()
                print("Account deleted")