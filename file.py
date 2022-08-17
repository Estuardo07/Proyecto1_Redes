# Proyecto 1 Redes
# Javier Hernández
# Carnet 19202

import slixmpp
import base64

class File(slixmpp.ClientXMPP):
    def __init__(self, jid, password, show, status, file=False, recipient=None):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.recipient = recipient
        self.show = show
        self.stat = status
        self.file = file
        self.my_user = jid
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.receive)

    async def start(self, event):
        self.send_presence(self.show, self.stat)
        await self.get_roster()
        if self.file:
            self.send_file()
        
    # Enviar archivos

    def send_file(self):
        filename = input("¿Que archivo deseas mandar? ")
        message = ''
        with open(filename, "rb") as img_file:
            message = base64.b64encode(img_file.read()).decode('utf-8')
        
        self.send_message(mto=self.recipient, mbody=message, mtype="chat")
        print("¡Archivo enviado exitosamente!")
        self.disconnect()

    # Recibir archivos

    def receive(self, msg):
        sender = str(msg['from']).split("/")
        recipient = str(msg['to']).split("/")
        body = msg['body']
        if len(body) > 3000:
            received = body.encode('utf-8')
            received = base64.decodebytes(received)
            with open("recibido.png", "wb") as fh:
                fh.write(received)
        else:
            print(str(sender[0]) + " >> " + str(recipient[0]) +  " >> " + str(body))