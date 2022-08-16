# Javier Hernández
# Carnet 19202

import xmpp2
import slixmpp
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream.stanzabase import ET

# Registrar cuenta

def registro(usuario, password):
    jid = xmpp2.JID(usuario)
    cli = xmpp2.Client(jid.getDomain(), debug=[])
    cli.connect()
    if xmpp2.features.register(cli, jid.getDomain(), {'username': jid.getNode(), 'password': password}):
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
            print("Tu cuenta en ALUMCHAT v.20.21 ha sido elimada permanentemente\n")
            self.disconnect()
        except IqError as e:
            print("Un error inesperado ha ocurrido", e)
        except IqTimeout:
            print("ERROR 500: El server no esta respondiendo")
        except Exception as e:
            print(e)  