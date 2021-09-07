import time
import sys
from agentUsuariBotons import AgentUsuariBotons
from agentUsuariTeclat import AgentUsuariTeclat
from InterfazUsuari import InterfazUsuari


def log(args):
    argCount = len(args)
    print("ESTES SON LES DADES FACILITADES!!!!!!!!!!!!!!!!!!!!!!!1", args)
    if argCount < 4:
        print("S'esperaven 4 arguments, funció, mode B/b = botons o T/t = teclat, nom d'usuari i contrasenya")
        print("O s'esperaven 5 arguments, funció, mode B/b = botons o T/t = teclat,  nom d'usuari, contrasenya i port, s'han posat MENYS de 3")
    elif argCount == 4:
        if args[1] == "B" or args[1] == "b":
            print("INICIEM EL AGENT USUARI BOTONS")
            print("INICIEM EL AGENT USUARI BOTONS")
            print("INICIEM EL AGENT USUARI BOTONS")
            clientagentinterfaz = InterfazUsuari(args[2]+xmpp_interfaz_server, "admin")
            futureIn = clientagentinterfaz.start(auto_register=True)
            futureIn.result()  # wait for receiver agent to be prepared.
            time.sleep(3)

            clientagent = AgentUsuariBotons(args[2]+xmpp_server , args[3])
            clientagent.web.port = 13000

            print("  ---> Connect to launcher in web-browser: http://localhost:", clientagent.web.port, "/launcher")
            clientagent.port = clientagent.web.port + 4000
            future = clientagent.start(auto_register=True)
            future.result()


            while clientagent.is_alive():
                try:
                    time.sleep(1)
                except KeyboardInterrupt:
                    clientagent.stop()
                    clientagentinterfaz.stop()
                    break
        elif args[1] == "T" or args[1] == "t":
            print("INICIEM EL AGENT USUARI TECLAT")
            print("INICIEM EL AGENT USUARI TECLAT")
            print("INICIEM EL AGENT USUARI TECLAT")
            clientagentinterfaz = InterfazUsuari(args[2]+xmpp_interfaz_server, "admin")
            futureIn = clientagentinterfaz.start(auto_register=True)
            futureIn.result()  # wait for receiver agent to be prepared.
            time.sleep(3)


            clientagent = AgentUsuariTeclat(args[2]+xmpp_server , args[3])
            clientagent.web.port = 13000

            print("  ---> Connect to launcher in web-browser: http://localhost:", clientagent.web.port, "/launcher")
            clientagent.port = clientagent.web.port + 4000
            future = clientagent.start(auto_register=True)
            future.result()


            while clientagent.is_alive():
                try:
                    time.sleep(1)
                except KeyboardInterrupt:
                    clientagent.stop()
                    clientagentinterfaz.stop()
                    break
        else:
            print("ERROR: Mode del Usuari no acceptat, escriu b/B per a mode de botons o t/T per a mode de teclat")

    elif argCount == 5:
        if args[1] == "B" or args[1] == "b":
            print("INICIEM EL AGENT USUARI BOTONS")
            print("INICIEM EL AGENT USUARI BOTONS")
            print("INICIEM EL AGENT USUARI BOTONS")
            clientagentinterfaz = InterfazUsuari(args[2]+xmpp_interfaz_server, "admin")
            futureIn = clientagentinterfaz.start(auto_register=True)
            futureIn.result()  # wait for receiver agent to be prepared.
            time.sleep(3)


            clientagent = AgentUsuariBotons(args[2]+xmpp_server , args[3])
            clientagent.web.port = int(args[4])

            print("  ---> Connect to launcher in web-browser: http://localhost:", clientagent.web.port, "/launcher")
            clientagent.port = clientagent.web.port + 4000
            future = clientagent.start(auto_register=True)
            future.result()


            while clientagent.is_alive():
                try:
                    time.sleep(1)
                except KeyboardInterrupt:
                    clientagent.stop()
                    clientagentinterfaz.stop()
                    break
        elif args[1] == "T" or args[1] == "t":
            print("INICIEM EL AGENT USUARI TECLAT")
            print("INICIEM EL AGENT USUARI TECLAT")
            print("INICIEM EL AGENT USUARI TECLAT")
            clientagentinterfaz = InterfazUsuari(args[2]+xmpp_interfaz_server, "admin")
            futureIn = clientagentinterfaz.start(auto_register=True)
            futureIn.result()  # wait for receiver agent to be prepared.
            time.sleep(3)


            clientagent = AgentUsuariTeclat(args[2]+xmpp_server , args[3])
            clientagent.web.port = int(args[4])

            print("  ---> Connect to launcher in web-browser: http://localhost:", clientagent.web.port, "/launcher")
            clientagent.port = clientagent.web.port + 4000
            future = clientagent.start(auto_register=True)
            future.result()


            while clientagent.is_alive():
                try:
                    time.sleep(1)
                except KeyboardInterrupt:
                    clientagent.stop()
                    clientagentinterfaz.stop()
                    break
        else:
            print("ERROR: Mode del Usuari no acceptat, escriu b/B per a mode de botons o t/T per a mode de teclat")


        while clientagent.is_alive():
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                clientagent.stop()
                #clientagentinterfaz.stop()
                break
    else:
        print("S'esperaven 3 arguments, funció, nom d'usuari i contrasenya")
        print("O s'esperaven 4 arguments, funció, nom d'usuari, contrasenya i port, s'han posat MÉS de 4")
    print("Si no ha funcionat comprova que el servidor estiga encés, la contrasenya siga correcta o l'usuari o port no es trobe en ús")



if __name__ == "__main__":

    xmpp_server = "@localhost"
    xmpp_interfaz_server = "@localhost"

    log(sys.argv)
    print("Agents finished")