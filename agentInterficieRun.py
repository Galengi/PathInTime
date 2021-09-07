import time
import sys
from AgentInterficie import AgentInterficie



def log(args):
    argCount = len(args)
    if argCount != 2:
        print("S'han introduit més o menys arguments del esperats, per favor, introduix el nom del agent")
    else:
        print("Nom de l'agent facilitat: ", args[1])

        clientagentinterfaz = AgentInterficie(args[1]+xmpp_server, "admin")
        future = clientagentinterfaz.start(auto_register=True)
        future.result()  # wait for receiver agent to be prepared.

        while clientagentinterfaz.is_alive():
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                clientagentinterfaz.stop()
                break
        print("Agents finished")

    print(
        "Si no ha funcionat comprova que el servidor estiga encés, i el nom de l'usuari siga correcte")

if __name__ == "__main__":
    xmpp_server = "Interfaz@localhost"
    log(sys.argv)
    print("Agents finished")