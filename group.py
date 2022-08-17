# Referencias:
# https://slixmpp.readthedocs.io/en/latest/

# Proyecto 1 Redes
# Javier Hernández
# Carnet 19202

import slixmpp

class ChatGroup(slixmpp.ClientXMPP):
    def __init__(self, jid, password, room, nick):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        self.jid = jid
        self.room = room
        self.nick = nick

        self.add_event_handler("session_start", self.start)
        self.add_event_handler("groupchat_message", self.muc_message)
        self.add_event_handler("muc::%s::got_online" % self.room,
                               self.muc_online)

    async def start(self, event):
        await self.get_roster()
        self.send_presence()

    # Unirse a un chat grupal
    
        self.plugin['xep_0045'].join_muc(self.room,
                                        self.nick,
                                        )
        message = input("Mensaje... ")
        self.send_message(mto=self.room,
                        mbody=message,
                        mtype='groupchat')

    # Envío de mensajes en grupos

    def muc_message(self, msg):
        if(str(msg['from']).split('/')[1] != self.nick):
            print(str(msg['from']).split('/')[1] + " >> " + msg['body'])
            message = input("Escribe <<volver>> si deseas regresar al menu \n Mensaje... ")
            if message == "volver":
                self.plugin['xep_0045'].leave_muc(self.room, self.nick)
                self.disconnect()
            else:
                self.send_message(mto=msg['from'].bare,
                                mbody=message,
                                mtype='groupchat')

    # Mensaje de presencia

    def muc_online(self, presence):
        if presence['muc']['nick'] != self.nick:
            self.send_message(mto=presence['from'].bare,
                              mbody="¡Hola amig@ %s!" % (presence['muc']['nick']),
                              mtype='groupchat')

            