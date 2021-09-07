import time
from AgentGestor import AgentGestor


if __name__ == "__main__":

    xmpp_server = "localhost"

    jid_launch = "agentegestor" + "@" + xmpp_server

    passwd_launch = "admin"
    gestoragent = AgentGestor(jid_launch, passwd_launch)
    gestoragent.web.port = 14000
    gestoragent.port = gestoragent.web.port + 4000
    future = gestoragent.start(auto_register=True)
    future.result() # wait for receiver agent to be prepared.


    print("  ---> Connect to ranking in web-browser: http://localhost:", gestoragent.web.port, "/ranking")
    print("  ---> Connect to leyenda in web-browser: http://localhost:", gestoragent.web.port, "/leyenda")
    
    #import ctypes
    #ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 6 )

    while gestoragent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            gestoragent.stop()
            break
    print("Agents finished")