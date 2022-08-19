# Referencias:
# https://slixmpp.readthedocs.io/en/latest/
# https://xmpp.readthedocs.io/en/latest/

# Proyecto 1 Redes
# Javier Hernández
# Carnet 19202

import slixmpp
from slixmpp.exceptions import IqError, IqTimeout
import xmpp
from slixmpp.xmlstream.stanzabase import ET

# Crear cuenta
def createUser(jid, password):
    print(' ')
    print('Crear un usuario: ')
    new_user = input('username@alumchat.fun:  ')
    new_password = input('password:  ')
    user = new_user
    password = new_password
    jid = xmpp.JID(user)
    cli = xmpp.Client(jid.getDomain(), debug=[])
    cli.connect()
    if xmpp.features.register(cli, jid.getDomain(), {'username': jid.getNode(), 'password': password}):
        return True
    else:
        return False

# Eliminar cuenta
class Eliminar(slixmpp.ClientXMPP):
    def __init__(self, jid, password, show, status):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.user = jid
        self.show = show
        self.stat = status
        self.add_event_handler("session_start", self.start)

    def start(self, event):
        self.send_presence(self.show, self.stat)
        self.get_roster()
        self.delete_account()        

    def delete_account(self):
        delete = self.Iq()
        delete['type'] = 'set'
        delete['from'] = self.user
        fragment = ET.fromstring("<query xmlns='jabber:iq:register'><remove/></query>")
        delete.append(fragment)

        try:
            delete.send()
            print("Tu cuenta ha sido eliminada \n")
            self.disconnect()
        except IqError as e:
            print("Algo no salio bien :(", e)
        except IqTimeout:
            print("Time out, no se puede establecer conexion. ")
        except Exception as e:
            print(e)  

# Chat grupal
class ChatGrupal(slixmpp.ClientXMPP):
    def __init__(self, jid, password, room, nick):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.jid = jid
        self.room = room
        self.nick = nick 

        self.add_event_handler("session_start", self.start)
        self.add_event_handler("groupchat_message", self.muc_message)
        self.add_event_handler("muc::%s::got_online" % self.room, self.muc_online)
    
    # Inicio
    async def start(self, event):
        await self.get_roster()
        self.send_presence()

        self.plugin['xep_0045'].join_muc(self.room, self.nick,)
        message = input("Mensaje...")
        self.send_message(mto=self.room, mbody=message,mtype='groupchat')
        
    def muc_message(self, msg):
        if(str(msg['from']).split('/')[1] != self.nick):
            print(str(msg['from']).split('/')[1] + " >> " + msg['body'])
            message = input("Escribe 'atras' si quieres volver  \n Mensaje... ")
            if message == "atras":
                self.plugin['xep_0045'].leave_muc(self.room, self.nick)
                self.disconnect()
            else:
                self.send_message(mto=msg['from'].bare,
                                mbody=message,
                                mtype='groupchat')

    #def muc_online(self, presence):
    #    if presence['muc']['nick'] != self.nick:
    #        self.send_message(mto=presence['from'].bare, mbody="¡Hola amig@ %s!" % (presence['muc']['nick']), mtype='groupchat')



class Rooster(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)

    # Inicio
    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        print('Contactos: \n')
        contactos = []
        roster = self.client_roster
        for contact in roster:
            contactos.append(contact)
        
        for contact in contactos:
            print(contact)

    # Mensaje de presencia
    def presenceRoster(self, to, body):
        message = self.Message()
        message['to'] = to
        message['type'] = 'chat'
        message['body'] = body
        try:
            message.send()
        except IqError as e:
            print("Algo salio mal", e, "\n")
        except IqTimeout:
            print("Time UP")



class AddFriend(slixmpp.ClientXMPP):
    def __init__(self, jid, password, name):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.name = name
        self.add_event_handler("session_start", self.start)

    # Inicio
    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        self.send_presence(pto=self.name, pstatus=None,
                           ptype='subscribe', pfrom=self.jid)
        self.disconnect()



class GetInfo(slixmpp.ClientXMPP):
    def __init__(self, jid, password, contact):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.contact = contact
        self.add_event_handler("session_start", self.start)

    # Inicio
    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        self.register_plugin('xep_0030')
        self.register_plugin('xep_0077')
        self.register_plugin('xep_0199')
        self.register_plugin('xep_0054')
        contactos = []
        roster = self.client_roster
        for jid in roster:
            contactos.append(jid)
        if self.contact in contactos:
            for x in range(0, 10):
                print("")
            print("El contacto ya existe")
            print("Detalles del contacto: " + self.contact)
            print(roster[self.contact])
            for x in range(0, 2):
                print("")
        else:
            print("El contacto no existe")

        self.disconnect()
