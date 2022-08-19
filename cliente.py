

import slixmpp

# Mensajes
class Client(slixmpp.ClientXMPP):    
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

# Envío y recepción de mensajes
    async def message(self, msg):
        if msg['type'] in ('chat'):
            sender = str(msg['from']).split("/")
            recipient = str(msg['to']).split("/")
            body = msg['body']
            print(str(sender[0]) + " >> " + str(recipient[0]) +  " >> " + str(body))
            self.change_status(self.recipient, 'composing')
            message = input("Escribe 'atras' si quieres volver al menu \n Mensaje... ")
            self.change_status(self.recipient, 'paused')
            if message == "atras":
                self.change_status(self.recipient, 'gone')
                self.disconnect()
            else:
                self.send_message(mto=self.recipient,
                                mbody=message, mtype='chat')
