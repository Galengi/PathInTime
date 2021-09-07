import json
from creadorNivells import creadorNivells

from AgentControlador import AgentControlador
from actualizarWeb import WebCreator


from spade.behaviour import FSMBehaviour
from spade.behaviour import State


from spade.agent import Agent
from spade.message import Message


GESTIO = "GESTIO"
EIXIR = "EIXIR"


class BehaviourEstats(FSMBehaviour):
    async def on_start(self):
        print(f"FSM starting at initial state {self.current_state}")

    async def on_end(self):
        print(f"FSM GESTOR AGENT finished at state {self.current_state}")
        await self.agent.stop()

#GESTOR
class EstatContacteGestor(State):
    async def run(self):
        nivell = 0
        usuari = None
        controlador = None
        destinatari = None
        menu = True
        
        #CREEM UN NIVELL INICIAL PER A ANAR AMB 1 NIVELL D'ANTELACIO
        await self.agent.comprovarCrearNivell(1)

        #SI REB MISSATGE DE USUARI BUIT MOSTRA NIVELLS
        #SI REB MISSATGE D'USUARI EN UN NIVELL, PARLA EN CONTROLADOR EN CAS DE TINDRE'N I LI ENVIA NIVELL SELECCIONAT I USUARI AL CONTROLADOR
        #SI REB MISSATGE DE CONTROLADOR ACTUALITZA REGISTRES DEL USUARI CORRESPONENT

        msg = await self.receive(timeout=500)
        if msg: #SOBRARIA EL IF MSG?
            print("Reb missatge al GESTOR per part de: ", str(msg.sender))

            if str(msg.sender) in self.agent.diccionariControladors:
                print("Rebem missatge de controlador")
                controlador = str(msg.sender)
                dic = json.loads(msg.body)
                if "APAGAR" in dic:
                    self.agent.diccionariControladors[controlador] = "OFF"
                    print("APAGUEM AGENT")
                menu = await self.agent.actualitzarInformacioUsuari(dic)
                usuari = dic["usuari"]
                self.agent.instanciaWeb.ranking(json.dumps(self.agent.ranking))

                #dicInfo = json.loads(msg.body)
            else:
            #SI REB MISSATGE D'USUARI
                usuari = str(msg.sender)[0:-9]
                # list1 = list(str(msg.sender))
                # list2 = list1[:-9]
                # usuari = "".join(list2)
                print("rebem missatge d'usuari ", usuari)
                #USUARI REGISTRAT
                if usuari in self.agent.diccionariUsuaris:
                    print("USUARI EN LLISTA DE USUARIS")
                    #SI MISSATGE CONTÉ NIVELL MODIFIQUEM VARIABLE DE NIVELL I ACTIVEM EL SEU CONTROLADOR EN CAS DE SER NECESSARI
                    if msg.body.isnumeric():
                        nivell = int(msg.body)
                        await self.agent.comprovarCrearNivell(nivell)
                        menu = False
                        controlador = self.agent.diccionariUsuaris[usuari]["controlador"]
                        try:
                            await self.agent.activarAgentControlador(controlador)
                        except:
                            print("Agent controlador: ", controlador, "ja activat")
                        # if self.agent.diccionariControladors[controlador] == "OFF":
                        #     await self.agent.activarAgentControlador(controlador)
                #SI USUARI NO REGISTRAT EL REGISTREM
                else:
                    print("USUARI NO ESTA EN LLISTA DE USUARIS")
                    await self.agent.registrarUsuari(usuari)

            #SI NO VOL NIVELL VOL LLISTA NIVELLS DISPONIBLES
            if menu:
                print("VOLEM MENU")
                if controlador == None:
                    controlador = self.agent.diccionariUsuaris[usuari]["controlador"]
                destinatari = usuari
                messageB = {"nivell" : self.agent.diccionariUsuaris[destinatari]["nivellMax"], "rankingPersonal": self.agent.diccionariPuntuacio["total"][destinatari]}

            #SI VOL NIVELL ENVIEM AL CONTROLADOR LA INFORMACIÓ NECESSARIA
            elif nivell != 0:
                print("VOLEM NIVELL NO MENU")
                destinatari = controlador
                dicInfoNivell = {"USUARI" : self.agent.diccionariUsuaris[usuari], "NIVELL": self.agent.diccionariNivells[nivell]}
                messageB = dicInfoNivell
                #enviar nivell a controlador

            if destinatari != None:
                print("ENVIEM MISSATGE A", destinatari)
                message = Message(to=destinatari)
                message.body = json.dumps(messageB)
                print("HEM ENVIAT MISSATGE")
                await self.send(message)
            self.set_next_state(GESTIO)


       
class EstatEixir(State):
    async def run(self):
        print("Apaguem Agent")
        #si no assignem un següent estat és com si acabara


class AgentGestor(Agent):
    controladorCount = 0
    maxLvl = 0
    creadorInstance =  creadorNivells()
    instanciaWeb = WebCreator()
    
    diccionariUsuaris = {}
    diccionariControladors = {}
    ranking = {}

    diccionariPuntuacio = {}
    total = {}
    diccionariPuntuacio["total"] = total
    diccionariNivells ={}

    async def ordenarRanking(self):
        # RANKEJAR USUARIS
        dic = {}
        ordenat = sorted((value,key) for (key,value) in self.diccionariPuntuacio["total"].items())
        ordenat = sorted(ordenat, reverse = True)
        contador = 1
        for (x,y) in ordenat:
            if contador < 10:
                dic[contador] = (y,x)
            contador += 1
        self.ranking = dic

    async def comprovarCrearNivell(self,lvl):
        if lvl + 1 > self.maxLvl:
            self.maxLvl += 1
            nivellNou2 = self.creadorInstance.crearNivell(self.maxLvl)
            nivellNou = nivellNou2.copy()
            self.diccionariNivells[self.maxLvl] = nivellNou

    async def checkPuntuacio(self, nomUsuari, puntuacio, nivell):
        if nivell in self.diccionariPuntuacio[nomUsuari]:
            punt = self.diccionariPuntuacio[nomUsuari][nivell]
            if puntuacio > punt:
                self.diccionariPuntuacio[nomUsuari][nivell] = puntuacio
                self.diccionariPuntuacio["total"][nomUsuari] = self.diccionariPuntuacio["total"][nomUsuari] - punt + puntuacio
        else:
            self.diccionariPuntuacio[nomUsuari][nivell] = puntuacio
            self.diccionariPuntuacio["total"][nomUsuari] = self.diccionariPuntuacio["total"][nomUsuari] + puntuacio

    async def actualitzarInformacioUsuari(self, dicInfoActualitzada):
        #NOMÉS HI HA UN CONTROLADOR PER USUARI, AQUEST ÉS PER TANT L'ÚNIC QUE POT CANVIAR LA INFORMACIÓ DE L'USUARI, AIXÍ DONCS DONEM PER FET QUE EL DICCIONARI ÉS LEGÍTIM
        usuari = dicInfoActualitzada["usuari"]
        valor = True
        if "puntuacio" in dicInfoActualitzada:
            puntuacio = dicInfoActualitzada.pop("puntuacio")
            await self.checkPuntuacio(usuari, puntuacio, dicInfoActualitzada["nivellJugat"])
            await self.ordenarRanking()
        if "menu" in dicInfoActualitzada:
            dicInfoActualitzada.pop("menu")
        else:
            valor = False
        self.diccionariUsuaris[usuari] = dicInfoActualitzada
        return valor

    async def registrarUsuari(self, nomUsuari):
        self.controladorCount += 1
        controlador = "agentecontrolador" + str(self.controladorCount)+"@localhost"
        diccionari = {"usuari" : nomUsuari, "controlador" : controlador, "nivellMax" : 1, "nivellJugat" : 0, "celes" : None, "celesPos" : None, "periode" : 0}
        self.diccionariUsuaris[nomUsuari] = diccionari
        self.diccionariControladors[controlador] = "OFF"
        self.diccionariPuntuacio[nomUsuari] = {}
        self.diccionariPuntuacio["total"][nomUsuari] = 0

    async def activarAgentControlador(self, nomControlador):
        print("Activem Agent CONTROLADOR", nomControlador)
        self.diccionariControladors[nomControlador] = "ON"
        agentControlador = AgentControlador(nomControlador, "admin")
        await agentControlador.start(auto_register=True)
        print("Activem Agent CONTROLADOR COMPLET")



    async def setup(self):

        fsm = BehaviourEstats()
        fsm.add_state(name=GESTIO, state=EstatContacteGestor(), initial=True)
        fsm.add_state(name=EIXIR, state=EstatEixir())


        fsm.add_transition(source=GESTIO, dest=GESTIO)
        fsm.add_transition(source=GESTIO, dest=EIXIR)
        self.add_behaviour(fsm)
        
        self.web.add_get("/ranking", lambda request: {}, "ranking.html")
        self.web.add_get("/leyenda", lambda request: {}, "leyenda.html")
        
        self.web.start()
        await super().setup()