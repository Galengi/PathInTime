import asyncio
import datetime
import json
from spade.message import Message
from spade.agent import Agent
from actualizarWeb import WebCreator
from aiohttp import web

from spade.behaviour import FSMBehaviour
from spade.behaviour import State
from spade.behaviour import OneShotBehaviour



CONTACTE = "CONTACTE"
MENU = "MENU"
REBRE_NIVELL = "REBRE_NIVELL"
ENVIAR_MOVIMENT = "ENVIAR_MOVIMENT"
REBRE_MOVIMENT = "REBRE_MOVIMENT"
EIXIR = "EIXIR"


class BehaviourEstats(FSMBehaviour):
    async def on_start(self):
        print(f"FSM starting at initial state {self.current_state}")
        self.agent.interfaz = str(self.agent.jid)[0:-10] + "Interfaz@localhost"

    async def on_end(self):
        print(f"FSM CLIENT AGENT finished at state {self.current_state}")
        await self.agent.stop()



#USUARI
class EstatContacteUsuari(State):
    async def run(self):
        print(f"estat 1 running at {datetime.datetime.now().time()}")
        msg = Message(to=self.agent.gestor)
        msg.body = "primer contacte del client"
        print("Enviem missatge PRIMER CONTACTE, deuriem poder visualitzar MENU en uns moments")

        await self.send(msg)
        self.set_next_state(MENU)


#USUARI
class EstatMenuUsuari(State):
    async def run(self):
        print("ESPERANT NIVELL U ALTRA ACCIÓ a L'ESTAT MENU de l'USUARI")
        #RESETEJEM MOVIMENT JA QUE HI HA VEGADES QUE NO ES TANCA LA WEB, PER TANT L'USUARI REPETEIX EL MOVIMENT I AQUESTA
        #VARIABLE QUEDA EN UN VALOR QUAN NO DEURIA TINDRE'N
        self.agent.movimentNou = -5
        msg = await self.receive(500) # wait for a message for 10 seconds
        if msg:
            if str(msg.sender) != str(self.agent.jid):
                print("Reb nivell i ranking personal del gestor per poder fer el selector de nivells")
                dicNivell = json.loads(msg.body)
                self.agent.nivell = dicNivell["nivell"]
                self.agent.rankingPersonal = dicNivell["rankingPersonal"]
                dicNivell["port"] = self.agent.port

                self.agent.instanciaWeb.menuInicialBotons(msg.body)

                # if not self.agent.menuCarregat:
                #     self.agent.carregarMenu()
                mesa = Message(to=self.agent.interfaz)
                dicInfo = {"window": "MENU", "port" : self.agent.web.port}
                mesa.body = json.dumps(dicInfo)
                await self.send(mesa)

                self.set_next_state(MENU)

            else:
                #print("Hem polsat algún botó a l'ESTAT MENU de l'USUARI")
                if msg.body == "EIXIR":
                    print("Informem a l'AC per a que s'apague en cas de que es trobe activat")
                    missatge = Message(to=self.agent.controlador)
                    missatge.body = "EIXIR"
                    await self.send(missatge)

                    self.set_next_state(EIXIR)

                if msg.body == "CLASIFICACIO":
                    print("Informem a l'AI per a obtindre la CLASSIFICACIO")
                    mesa = Message(to=self.agent.interfaz)
                    dicInfo = {"window": "RANKING"}
                    mesa.body = json.dumps(dicInfo)

                    await self.send(mesa)

                    self.set_next_state(MENU)

                elif msg.body == "NIVELL":
                    print("Hem seleccionat nou NIVELL")
                    missatge = Message(to=self.agent.gestor)
                    missatge.body = str(self.agent.nivellSeleccionat)
                    self.agent.nivell = self.agent.nivellSeleccionat
                    self.agent.nivellSeleccionat = -5
                    #print("ENVIEM MISSATGE DEL NIVELL SELECCIONAT AL GESTOR")

                    await self.send(missatge)
                    self.set_next_state(REBRE_NIVELL)


#USUARI
class EstatNivellEstaticUsuari(State):
    async def run(self):
        print("Esperem missatge amb el NIVELL estàtic o no, per part del CONTROLADOR a l'estat NIVELL ESTATIC de l'USUARI")
        msg = await self.receive(timeout=100) # wait for a message for 10 seconds
        if msg:
            print("Hem rebut el nivell del CONTROLADOR a l'estat NIVELL ESTATIC de l'USUARI")
            self.agent.diccionariNivell = json.loads(msg.body)
            self.agent.controlador = str(msg.sender)
            (self.agent.dimY, self.agent.dimX) = self.agent.diccionariNivell["dimensions"]

            #HEM DE FER SEMPRE EL ESTÀTIC ACÍ, JA QUE AL SER EL CONTACTE POT O NO TINDRE EL NIVELL CARREGAT
            # JA QUE SI HA COMENÇAT PARTIDA, PERO APAGA AGENT SE LI RESETEJEN LES DADES QUE DONEM PER ESTATIQUES
            #PERO EL GESTOR CONTINUA TINGUEN LES CELES I PER TANT LI FALTARIEN LES DADES ESTATIQUES AL NIVELL
            self.agent.instanciaWeb.nivellEstaticBotons(msg.body)

            mesa = Message(to=self.agent.interfaz)
            dicInfo = {"window": "NIVELL", "size" : (self.agent.dimY, self.agent.dimX), "mode": "BOTONS"}
            mesa.body = json.dumps(dicInfo)

            await self.send(mesa)
            self.set_next_state(ENVIAR_MOVIMENT)


#USUARI
class EstatEnviarMovimentUsuari(State):
    async def run(self):
        print("Esperem MOVIMENT U ALTRA ACCIÓ en l'estat ENVIAR_MOVIMENT de l'USUARI")
        msg = await self.receive(timeout=500)  # wait for a message for 10 seconds
        missatge = Message(to=self.agent.controlador)
        if msg:
            if msg.body == "MENU":
                #MENU FA QUE S'OBRIGA UNA PESTAÑA NOVA DE SELECCIO DE MENU
                #AÇÒ POT SER ÚTIL PER SI EL JUGADOR HA TANCAT LA FINESTRA DEL MENU
                missatge.body = "MENU"
                await self.send(missatge)
                self.agent.instanciaWeb.tancarNivell()

                self.set_next_state(MENU)
                print("S'ha polsat el boto MENU")

            elif msg.body == "EIXIR":
                #EIXIR FA QUE CANVIE D'ESTAT A LMENU I QUE EL CONTROLADOR QUEDE EXPECTANT UN NIVELL
                missatge.body = "EIXIR"
                await self.send(missatge)

                self.set_next_state(EIXIR)
                print("S'ha polsat el boto EIXIR")

            elif msg.body == "REINICIAR":
                missatge.body = "REINICIAR"
                await self.send(missatge)

                self.set_next_state(REBRE_MOVIMENT)
                print("S'ha polsat el boto REINICIAR")

            elif msg.body == "MOVIMENT":
                print("Moviment seleccionat: ", self.agent.movimentNou)
                missatge.body = str(self.agent.movimentNou)
                self.agent.moviment = -5
                self.agent.movimentNou = -5
                await self.send(missatge)

                self.set_next_state(REBRE_MOVIMENT)
                print("S'ha polsat un MOVIMENT")

            elif msg.body == "NIVELL":
                print("HEM SELECCIONAT EL NOU NIVELL QUAN ESPERAVEM SELECCIONAR UN MOVIMENT")
                #PODEM FER QUE QUAN TANQUE FINESTRA CANVIE D'ESTAT?

                #ENVIEM AL GESTOR EL NIVELL SELECCIONAT
                #L'USUARI PER LA SEUA BANDA CANVIARÁ A ESTAT REBRE_NIVELL, ESPERANT EL NIVELL DEL CONTROLADOR
                missatge = Message(to=self.agent.gestor)
                missatge.body = str(self.agent.nivellSeleccionat)
                self.agent.nivellSeleccionat = -5
                await self.send(missatge)

                self.set_next_state(REBRE_NIVELL)
            else:
                self.set_next_state(ENVIAR_MOVIMENT)


#USUARI
class EstatRebreMovimentUsuari(State):
    async def run(self):
        print("Esperem confirmació del MOVIMENT del CONTROLADR al estat REBRE_MOVIMENT")

        msg = await self.receive(timeout=100)
        if msg:
            #print("Rebem missatge del CONTROLADOR al estat REBRE_MOVIMENT")
            dicNivell = json.loads(msg.body)
            print(dicNivell)

            if dicNivell["moviment"] == "COMPLET":
                print("USUARI ha rebut el nivell COMPLET")
                #self.agent.instanciaWeb.tancarNivell()

                self.set_next_state(MENU)

            elif dicNivell["moviment"] == "SI":
                print("MOVIMENT ACCEPTAT")

                self.agent.instanciaWeb.nivellDinamicBotons(msg.body)

                self.set_next_state(ENVIAR_MOVIMENT)
            else:
                print("MOVIMENT DENEGAT")
                #CREAR UNA FUNCIÓ PER A TRAURE UN POP UP DIGUENT QUE NO S'HA POGUT REALITZAR EL MOVIMENT
                self.set_next_state(ENVIAR_MOVIMENT)


        
class EstatEixir(State):
    async def run(self):
        print("Anem a apagar Agent Usuari, informem al agent Interficie ")
        mesa = Message(to=self.agent.interfaz)
        dicInfo = {"window": "EIXIR"}
        mesa.body = json.dumps(dicInfo)

        await self.send(mesa)
        print("Apaguem Agent ", str(self.agent.jid))
        #si no assignem un següent estat és com si acabara

class AgentUsuariBotons(Agent):
    gestor = "agentegestor@localhost"
    intefaz = ""
    controlador = "res"
    nivellAcabat = False
    window = "nothing"
    dimY = 0
    dimX = 0
    #url = "http://127.0.0.1:13000/level"
    nivell = 1
    ranking = {}
    rankingPersonal = 0
    diccionariNivell = {}
    moviment = -5
    movimentNou = -5
    nivellSeleccionat = -5
    eixir = "res"
    reiniciar = "res"
    menu = "res"
    clasificacio = "res"
    instanciaWeb = WebCreator()

    #menuCarregat = False

    class novaInst(OneShotBehaviour):
        async def run(self):
            print("Hem seleccionat algún botó INSTRUCCIO ACTIVADA")
            msg = Message(to=str(self.agent.jid))
            if self.agent.movimentNou != -5:
                msg.body = "MOVIMENT"

            elif self.agent.eixir != "res":
                msg.body = "EIXIR"
                self.agent.eixir = "res"

            elif self.agent.clasificacio != "res":
                msg.body = "CLASIFICACIO"
                self.agent.clasificacio = "res"

            elif self.agent.menu != "res":
                msg.body = "MENU"
                self.agent.menu = "res"

            elif self.agent.reiniciar != "res":
                msg.body = "REINICIAR"
                self.agent.reiniciar = "res"

            elif self.agent.nivellSeleccionat != -5:
                msg.body = "NIVELL"

            else:
                msg.body = "ERROR"
            print("El botó selecciona ES: ", msg.body)
            await self.send(msg)

    async def seleccioMoviment(self, request):
        data = await request.post()
        self.movimentNou = data['mov']
        self.novaInstruccio = self.novaInst()
        self.add_behaviour(self.novaInstruccio)
        await asyncio.sleep(0.1)

        raise web.HTTPFound('/level')
    
    async def seleccioNivell(self, request):
        data = await request.post()

        self.nivellSeleccionat = data['nivellSeleccionat']
        print("EL NIVELL SELECCIONA ES")
        print(self.nivellSeleccionat)
        self.novaInstruccio = self.novaInst()
        self.add_behaviour(self.novaInstruccio)

        #SI NO FEM UN SLEEP OBRI LA NOVA FINESTRA ABANS DE TINDRE LA PAGINA CARREGADA
        await asyncio.sleep(0.2)

        raise web.HTTPFound('/launcher')
        

    async def seleccioMenu(self, request):
        data = await request.post()

        self.menu = data['menu']
        self.novaInstruccio = self.novaInst()
        self.add_behaviour(self.novaInstruccio)

        await asyncio.sleep(0.5)
        raise web.HTTPFound('/launcher')

    async def seleccioClasificacio(self, request):
        data = await request.post()

        self.clasificacio = data['clasificacio']
        self.novaInstruccio = self.novaInst()
        self.add_behaviour(self.novaInstruccio)

        raise web.HTTPFound('/launcher')

    async def seleccioReiniciar(self, request):
        data = await request.post()

        self.reiniciar = data['reiniciar']
        self.novaInstruccio = self.novaInst()
        self.add_behaviour(self.novaInstruccio)

        await asyncio.sleep(0.2)
        raise web.HTTPFound('/level')

    async def seleccioEixir(self, request):
        data = await request.post()

        self.eixir = data['eixir']
        self.novaInstruccio = self.novaInst()
        self.add_behaviour(self.novaInstruccio)

    async def setup(self):
        fsm = BehaviourEstats()
        fsm.add_state(name=CONTACTE, state=EstatContacteUsuari(), initial=True)
        fsm.add_state(name=REBRE_NIVELL, state=EstatNivellEstaticUsuari())
        fsm.add_state(name=MENU, state=EstatMenuUsuari())
        fsm.add_state(name=ENVIAR_MOVIMENT, state=EstatEnviarMovimentUsuari())
        fsm.add_state(name=REBRE_MOVIMENT, state=EstatRebreMovimentUsuari())
        fsm.add_state(name=EIXIR, state=EstatEixir())


        fsm.add_transition(source=CONTACTE, dest=MENU)

        fsm.add_transition(source=MENU, dest=REBRE_NIVELL)
        fsm.add_transition(source=MENU, dest=MENU)

        fsm.add_transition(source=REBRE_NIVELL, dest=ENVIAR_MOVIMENT)

        fsm.add_transition(source=ENVIAR_MOVIMENT, dest=REBRE_MOVIMENT)
        fsm.add_transition(source=ENVIAR_MOVIMENT, dest=ENVIAR_MOVIMENT)
        fsm.add_transition(source=ENVIAR_MOVIMENT, dest=MENU)
        fsm.add_transition(source=ENVIAR_MOVIMENT, dest=REBRE_NIVELL)

        fsm.add_transition(source=REBRE_MOVIMENT, dest=ENVIAR_MOVIMENT)
        fsm.add_transition(source=REBRE_MOVIMENT, dest=MENU)
        
        fsm.add_transition(source=CONTACTE, dest=EIXIR)
        fsm.add_transition(source=MENU, dest=EIXIR)
        fsm.add_transition(source=REBRE_NIVELL, dest=EIXIR)
        fsm.add_transition(source=ENVIAR_MOVIMENT, dest=EIXIR)
        fsm.add_transition(source=REBRE_MOVIMENT, dest=EIXIR)

        self.add_behaviour(fsm)

        self.web.add_get("/launcher", lambda request: {}, "menu.html")
        self.web.add_get("/level", lambda request: {}, "pruebaLauncher.html")
        self.web.add_post("/submit", self.seleccioMoviment, None)
        self.web.add_post("/submitNivell", self.seleccioNivell, None)
        self.web.add_post("/submitEixir", self.seleccioEixir, None)
        self.web.add_post("/submitReiniciar", self.seleccioReiniciar, None)
        self.web.add_post("/submitMenu", self.seleccioMenu, None)
        self.web.add_post("/submitClasificacio", self.seleccioClasificacio, None)
        #print("Path:XXXXXXXXXXXXXXX", self.web.BaseRequest.raw_path)
        
        self.web.start()
        #print("AQUI5")
        #print("Path:XXXXXXXXXXXXXXX2", self.web.BaseRequest.raw_path)

        #app = self.web.Application()
        await super().setup()


