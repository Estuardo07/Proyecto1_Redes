import socket
import slixmpp
import pickle
import sys
from getpass import getpass
from argparse import ArgumentParser
import logging
import asyncio

# Global Variables for the EchoBot class (Error Handling Python version)
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class Server(slixmpp.ClientXMPP):
    # Constructor
    def __init__(self, jid, password, recipient, message, show, status):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.recipient = recipient
        self.msg = message
        self.show = show
        self.stat = status
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)
        self.add_event_handler("chatstate_active", self.status_active)
        self.add_event_handler("chatstate_inactive", self.status_inactive)

    async def start(self, event):
        self.send_presence(self.show, self.stat)
        await self.get_roster()
        self.send_message(mto=self.recipient,
                          mbody=self.msg,
                          mtype='chat')

    # Mensajes
    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            print("From: ", msg["from"])
            print("Subject: ", msg["subject"])
            print("Message: ", msg["body"])
            message = ((str(msg["body"])))
            user = ((str(msg["from"])))
            userS = (user.split('/')[0])
            l = []
            with open("messages.txt", "a") as f:
                l.append('user: '+userS)
                l.append('message: '+message)
                f.write((str(l)+'\n'))

            result = 'Mensaje enviado exitosamente'

    # Eliinar cuenta
    def deleteAccount(self):
        resp = self.Iq()
        resp['type'] = 'set'
        resp['from'] = self.boundjid.full
        resp['register']['remove'] = True


if __name__ == '__main__':
    # Setup the command line arguments.
    parser = ArgumentParser(description=Server.__doc__)
    # Output verbosity options.
    parser.add_argument("-q", "--quiet", help="set logging to ERROR",
                        action="store_const", dest="loglevel",
                        const=logging.ERROR, default=logging.INFO)
    parser.add_argument("-d", "--debug", help="set logging to DEBUG",
                        action="store_const", dest="loglevel",
                        const=logging.DEBUG, default=logging.INFO)

    # JID and password options.
    parser.add_argument("-j", "--jid", dest="jid",
                        help="JID to use")
    parser.add_argument("-p", "--password", dest="password",
                        help="password to use")

    args = parser.parse_args()

    # Setup logging.
    logging.basicConfig(level=args.loglevel,
                        format='%(levelname)-8s %(message)s')

    if args.jid is None:
        args.jid = input("Username: ")
    if args.password is None:
        args.password = getpass("Password: ")

    xmpp = Server(args.jid, args.password)

    xmpp.register_plugin('xep_0030')  # Service Discovery
    xmpp.register_plugin('xep_0004')  # Data Forms
    xmpp.register_plugin('xep_0060')  # PubSub
    xmpp.register_plugin('xep_0199')  # XMPP Ping
    xmpp.register_plugin('xep_0100')  # XMPP Add contact
    xmpp.register_plugin('xep_0030')  # XMPP Delete account

    # Connect to the XMPP server and start processing XMPP stanzas.
    # Use sockets to send data to the server/client and receive data from the server/client.
    s = socket.socket()
    port = 12345

    s.bind(('', port))
    s.listen(5)
    c, addr = s.accept()

    while True:

        xmpp.connect()

        # Recepción de mensajes
        info = c.recv(1024)
        data = pickle.loads(info)

        loggedIn_option = data['opcion']

        print("Recibido: ", data)
        xmpp.process(timeout=20)

        # Mostrar contactos
        if(loggedIn_option == "1"):
            xmpp.process(timeout=20)
            print("\nContactos:\n")

            contacts = xmpp.client_roster

            print(contacts.keys())
            data = contacts.keys()
            resu = []

            for key in contacts.keys():
                resu.append(key)

            result = ' '.join(resu)
            c.send(result.encode())

        # Mensaje privado
        if(loggedIn_option == "2"):
            xmpp.process(timeout=30)
            to = data['to']
            msg = data['msg']
            result = 'Mensaje enviado exitosamente'

            xmpp.send_message(mto=to, mbody=msg, mtype='chat')
            xmpp.process(timeout=30)

            c.send(result.encode())

        # Agregar nuevo contacto
        elif(loggedIn_option == "3"):

            xmpp.process(timeout=20)
            to = data['to']

            xmpp.send_presence(pto=to, ptype="subscribe",
                               pstatus=None, pfrom=args.jid)

            xmpp.process(timeout=20)

        # Detalles de contacto
        if (loggedIn_option == "5"):
            contact = data['contact']
            xmpp.process(timeout=20)

            contacts = xmpp.client_roster

            if contact in contacts:
                print('Contacto existente!')
                res = []
                user = contacts[contact]

                res.append('Correo:'+contact)
                if contacts[contact]['name'] == '':
                    res.append('Nickname:'+'Sin nickname')
                else:
                    res.append('Nickname:'+contacts[contact]['name'])

                friends = contacts[contact]['subscription']
                if friends == 'both':
                    res.append('Suscripcion:'+'Amigo')
                result = ' '.join(res)

                c.send(result.encode())
            else:
                print('Contacto no existente!')
                r = 'Contacto no existente!'
                c.send(r.encode())

        # Mensaje personal
        if(loggedIn_option == "6"):
            status = data['status']
            typeStatus = ("available")

            xmpp.send_presence(pshow=typeStatus, pstatus=status)
            xmpp.process(timeout=20)
            res = 'Status actualizado'
            c.send(res.encode())

        # Cerrar sesión
        if(loggedIn_option == "7"):
            xmpp.process(timeout=20)

            xmpp.disconnect()
            xmpp.process(timeout=20)

            print("Logged Off")

            sys.exit()

        # Eliminar cuenta
        elif(loggedIn_option == "8"):
            xmpp.deleteAccount()
            print("Account deleted")

        if(loggedIn_option == "9"):
            xmpp.process()

    c.close()
