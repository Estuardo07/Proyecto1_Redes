import socket
import pickle
import sys
import filecmp
import shutil


s = socket.socket()


# Menú de Funcionalidades
def userMenu():
    print("1. Mis contactos")
    print("2. Mensaje privado")
    print("3. Agregar contacto")
    print("4. Chat grupal")
    print("5. Mostrar detalles de un contacto")
    print("6. Cambiar estado")
    print("7. Cerrar Sesion")
    print("8. Eliminar Cuenta")


s = socket.socket()
port = 12345

s.connect(('127.0.0.1', port))

# Envío y recepción de mensajes
while True:
    original = './messages.txt'
    copy = './messages_copy.txt'
    result = filecmp.cmp(original, copy)

    if result == True:
        userMenu()
        loggedIn_option = input("\nElige una opcion: ")
        
        # Mostrar contactos
        if loggedIn_option == '1':
            data = pickle.dumps({'opcion': '1'})

            s.send(data)
            print('\n')
            print("Lista de usuarios:", s.recv(1024).decode(), '\n')
        
        # Mensaje privado
        if loggedIn_option == '2':
            to = input('¿A quien desea enviarle un mensaje?:\n')
            msg = input('Mensaje (exit)>>> ')

            data = pickle.dumps({'opcion': '2', 'to': to, 'msg': msg})
            s.send(data)
        
        # Agregar nuevo contacto
        if loggedIn_option == '3':
            to = input('¿A quien deseas agregar?:\n')
            data = pickle.dumps({'opcion': '3', 'to': to})
            s.send(data)

            print("Usuario agregado!\n")
        
        # Detalles del contato
        if loggedIn_option == '5':
            contact = input('¿Cual contacto deseas ver?:\n')
            data = pickle.dumps({'opcion': '5', 'contact': contact})
            s.send(data)
            print("\nDatos del contacto:\n", s.recv(1024).decode(), '\n')

        # Cambiar estado
        if loggedIn_option == '6':
            status = input('¿Cual es el estado?:\n')
            data = pickle.dumps({'opcion': '6', 'status': status})
            s.send(data)
            print(s.recv(1024).decode(), '\n')

        # Cerrar sesión
        if loggedIn_option == '7':
            data = pickle.dumps({'opcion': '7'})

            try:
                s.send(data)

            except:
                print('Se ha cerrado sesion\n')
                sys.exit()

        # Eliminar cuenta
        if loggedIn_option == '8':
            data = pickle.dumps({'opcion': '8'})
            try:
                s.send(data)

            except:
                print('Se ha eliminado la cuenta\n')
                sys.exit()

        if loggedIn_option == '9':
            data = pickle.dumps({'opcion': '9'})

            text = input('Escribe el mensaje que deseas enviar:\n')
            s.send(data)
            while text != 'exit':

                text = input('Escribe el mensaje que deseas enviar:\n')
    if result == False:

        f = open(original, 'r')
        d = open(copy, 'w')

        data = f.readlines()

        print('Ha ingresado un nuevo mensaje:\n')
        print(data[-1])
        shutil.copyfile(original, copy)
