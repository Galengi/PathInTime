import time
import sys
from AgentUsuariBotons import AgentUsuariBotons
from AgentUsuariTeclat import AgentUsuariTeclat

def log(args):
    argCount = len(args)
    print("Estes son les dades facilitades", args)
    if argCount < 4:
        print("S'esperaven 4 arguments, funció, mode B/b = botons o T/t = teclat, nom d'usuari i contrasenya")
        print("O s'esperaven 5 arguments, funció, mode B/b = botons o T/t = teclat,  nom d'usuari, contrasenya i port, s'han posat MENYS de 3")
    elif argCount == 4:
        if args[1] == "B" or args[1] == "b":
            print("INICIEM EL AGENT USUARI BOTONS")
            clientagent = AgentUsuariBotons(args[2]+xmpp_server , args[3])
            #clientagentinterfaz = InterfazUsuari(args[1]+"Interfaz"+xmpp_server, "admin")
            #clientagentinterfaz.start(auto_register=True)
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
                    #clientagentinterfaz.stop()
                    break
        elif args[1] == "T" or args[1] == "t":
            print("INICIEM EL AGENT USUARI TECLAT")
            clientagent = AgentUsuariTeclat(args[2]+xmpp_server , args[3])
            #clientagentinterfaz = InterfazUsuari(args[1]+"Interfaz"+xmpp_server, "admin")
            #clientagentinterfaz.start(auto_register=True)
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
                    #clientagentinterfaz.stop()
                    break
        else:
            print("ERROR: Mode del Usuari no acceptat, escriu b/B per a mode de botons o t/T per a mode de teclat")

    elif argCount == 5:
        if args[1] == "B" or args[1] == "b":
            print("INICIEM EL AGENT USUARI BOTONS")
            clientagent = AgentUsuariBotons(args[2]+xmpp_server , args[3])
            #clientagentinterfaz = InterfazUsuari(args[1]+"Interfaz"+xmpp_server, "admin")
            #clientagentinterfaz.start(auto_register=True)
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
                    #clientagentinterfaz.stop()
                    break
        elif args[1] == "T" or args[1] == "t":
            print("INICIEM EL AGENT USUARI TECLAT")
            clientagent = AgentUsuariTeclat(args[2]+xmpp_server , args[3])
            #clientagentinterfaz = InterfazUsuari(args[1]+"Interfaz"+xmpp_server, "admin")
            #clientagentinterfaz.start(auto_register=True)
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
                    #clientagentinterfaz.stop()
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

    log(sys.argv)
    print("Agents finished")