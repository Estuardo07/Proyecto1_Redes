# Referencias:
# https://slixmpp.readthedocs.io/en/latest/

# Proyecto 1 Redes
# Javier Hernández
# Carnet 19202

import slixmpp

# Chat privado

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
        self.add_event_handler("chatstate_composing", self.status_composing)
        self.add_event_handler("chatstate_paused", self.status_paused)
        self.add_event_handler("chatstate_gone", self.status_gone)

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
            message = input("Escribe <<volver>> si deseas regresar al menu \n Mensaje... ")
            self.change_status(self.recipient, 'paused')
            if message == "volver":
                self.change_status(self.recipient, 'gone')
                self.disconnect()
            else:
                self.send_message(mto=self.recipient,
                                mbody=message, mtype='chat')

    # Notificaciones

    def change_status(self, to, status):
        msg = self.make_message(
            mto=to,
            mfrom=self.boundjid.bare,
            mtype='chat'
        )
        msg['chat_state'] = status
        msg.send()

    # Notificaciones de usuarios activos

    def status_active(self, chatstate):
        print(str(chatstate['from']).split("/")[0] + " esta activo.")

    # Notificaciones de usuarios inactivos

    def status_inactive(self, chatstate):
        print(str(chatstate['from']).split("/")[0] + " esta inactivo.")

    # Notificaciones de usuarios que estan escribiendo en el chat

    def status_composing(self, chatstate):
        print(str(chatstate['from']).split("/")[0] + " esta escribiendo...")

    # Notificaciones de usuarios que han dejado de escribir en el chat

    def status_paused(self, chatstate):
        print(str(chatstate['from']).split("/")[0] + " ha dejado de escribir.")

    # Notificaciones de usuarios que han dejado el chat

    def status_gone(self, chatstate):
        print(str(chatstate['from']).split("/")[0] + " se ha ido a hacer algo mas.")
