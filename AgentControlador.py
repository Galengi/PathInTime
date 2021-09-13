import json
import operator
from spade.behaviour import FSMBehaviour
from spade.behaviour import State
from spade.agent import Agent
from spade.message import Message


TRANSFERENCIA_NIVELL = "TRANSFERENCIA_NIVELL"
COMPROVAR_MOVIMENT = "COMPROVAR_MOVIMENT"
EIXIR = "EIXIR"


class BehaviourEstats(FSMBehaviour):
    async def on_start(self):
        print(f"CONTROLADOR ", str(self.agent.jid) ,"FSM starting at initial state {self.current_state}")

    async def on_end(self):
        print(f"FSM CONTROLADOR AGENT finished at state {self.current_state}")
        await self.agent.stop()



#CONTROLADOR
class EstatMenuControlador(State):
    async def run(self):
        msg = await self.receive(timeout=500)
        if msg: #SOBRARIA EL IF MSG?
            if msg.sender == self.agent.usuari or str(msg.sender)[0:-9] == self.agent.usuari:
                print("Rebem missatge de l'usuari al estat MENU del CONTROLADOR", str(msg.sender))
                if msg.body == "EIXIR":
                    dicInfoUsuari = await self.agent.empaquetarUsuariN()
                    dicInfoUsuari["APAGAT"] = "OFF"
                    message = Message(to=self.agent.agentGestor)
                    message.body = json.dumps(dicInfoUsuari)
                    await self.send(message)

                    self.set_next_state(EIXIR)

            diccionariInfo = json.loads(msg.body)
            #COMENÇEM REBENT INFO DEL GESTOR, PER TANT CARREGUEM LES VARIABLES QUE ENS ARRIBEN EN CAS DE QUE AQUEST AGENT
            # S'ACABE D'ACTIVAR, JA QUE SI JA ESTAVA DESACTIVAT ELS VALORS S'HAURAN RESETEJAT
            if self.agent.usuari == None:
                await self.agent.carregarVariables(diccionariInfo["USUARI"])
            #CARREGUEM EL NIVELL
            if self.agent.nivell != diccionariInfo["NIVELL"]["nivell"]:
                await self.agent.carregarNivell(diccionariInfo["NIVELL"])

            #ENVIEM A USUARI NIVELL EN PERIODE CORRESPONENT
            if self.agent.nivell != self.agent.nivellJugat:
                await self.agent.netejarRegistres()

            #ENVIEM EL DICCIONARI REBUT PERO NOMÉS EL PERIODE ADEQÜAT, SI AQUEST ÉS DIFERENT D'1 SIGNIFICA QUE EL NIVELL JA HA SIGUT COMENÇAT I PER TANT TAN NECESSITA LA SEQÜENCIA DE CELES
            dicNivellContacte = self.agent.dicNivell.copy()
            guardiesEmpaquetats = {}
            guardiesEmpaquetats = await self.agent.empaquetarGuardies(guardiesEmpaquetats, self.agent.periode)
            dicNivellContacte["guardies"] = guardiesEmpaquetats

            #SI EL PERIODE ES DIFERENT D'1 TAMBÉ HI HA QUE POSAR CELES
            if self.agent.periode != 1:
                dicNivellContacte["periode"] = self.agent.periode
                dicNivellContacte["celes"] = self.agent.celes
                dicNivellContacte["celesPos"] = self.agent.celesPos

            #ENVIEM DICCIONARI
            #print("ENVIEM DICCIONARI A USUARI")
            message = Message(to=self.agent.usuari)
            message.body = json.dumps(dicNivellContacte)
            await self.send(message)

            self.set_next_state(COMPROVAR_MOVIMENT)


#CONTROLADOR
class EstatMovimentControlador(State):
    async def run(self):

        print("ESTAT COMPROVAR MOVIMENT al CONTROLADOR")
        msg = await self.receive(timeout=500)
        if msg:
            #print("Rebem missatge al estat COMPROVAR MOVIMENT")
            dicNivellUsuari = {}
            retrocedeix = False
            potFerMoviment = True
            destinatari = self.agent.usuari
            yActual = None
            xActual = None
            printPos = None


            if str(msg.sender) == self.agent.agentGestor or str(msg.sender) == self.agent.agentGestor2:
                print("Rebem missatge del GESTOR esperant un MOVIMENT")
                #SI ENS PARLA EL GESTOR EN ESTE ESTAT ÉS PERQUE L'USUARI HA ACCEDIT AL MENU DE FORMA ERRONEA I HA SELECCIONAT UN NIVELL,
                #PER TANT ENS ENVIEM AQUEST MISSATGE A L'ESTAT CORRECTE I ACTUEM COM SI RES
                destinatari = str(self.agent.jid)

            elif msg.body == "MENU":
                dicInfoUsuari = await self.agent.empaquetarUsuariN()
                dicInfoUsuari["menu"] = "si"
                destinatari = self.agent.agentGestor

            elif msg.body == "REINICIAR":
                await self.agent.netejarRegistres()
                dicNivellUsuari = {}
                guardiesEmpaquetats = {}
                guardiesEmpaquetats = await self.agent.empaquetarGuardies(guardiesEmpaquetats, self.agent.periode)
                dicNivellUsuari["guardies"] = guardiesEmpaquetats
                dicNivellUsuari["moviment"] = "SI"
                dicNivellUsuari["periode"] = self.agent.periode
                dicNivellUsuari["celes"] = self.agent.celes
                dicNivellUsuari["celesPos"] = self.agent.celesPos


            elif msg.body == "EIXIR":
                print("Enviem informació de apagat a l'AG")
                dicInfoUsuari = await self.agent.empaquetarUsuariN()
                dicInfoUsuari["APAGAT"] = "OFF"
                destinatari = self.agent.agentGestor

            else:
                if msg.body == "ARRIBA":
                    pos = (-1,0)
                elif msg.body == "ABAJO":
                    pos = (1,0)
                elif msg.body == "IZQUIERDA":
                    pos = (0,-1)
                elif msg.body == "DERECHA":
                    pos = (0,1)
                else:
                    print("ERROR, hem rebut: ", msg.body, "en l'estat COMPROVAR MOVIMENT")
                    print("ERROR, aquest missatge ha sigut envia per: ", msg.sender)

                #print("COMPROVEM UN MOVIMENT", pos)

                #OBTENIM LA POSICIO A LA QUE VOLEM MOURE'NS, COM LA LLISTA COMENÇA EN 0 I EL PERIODE EN 1, LA ULTIMA POSICIO ES EN PERIODE -1
                #celes_list = list(self.agent.celes)
                #ultimaPosicio = celes_list[self.agent.periode-1]

                #OBTENIM ELS DIGITS DE LA TUPLA, JA QUE ES DE TIPUS STRING I TENIM QUE SEPARAR COMES I PARENTESIS
                #ultPos = [int(word) for word in tuple(ultimaPosicio) if word.isdigit()]
                ultPos = self.agent.celesPos[str(self.agent.periode)]

                #print("ULTIMA POS", ultPos)


                (yActual,xActual) = tuple(map(operator.add, ultPos, pos))

                #(yActual,xActual) = tuple(map(operator.add, tuple(ultPos), pos))
                #print("POSICIO DE Y", yActual, "POSICIO DE X", xActual)

                    
                ###### COMPROVEM SI IX DEL TAULER
                if yActual < 0 or xActual < 0 or yActual > self.agent.dimY - 1 or xActual > self.agent.dimX - 1:
                    print("FORA DELS LLIMITS")
                    potFerMoviment = False

                #SI PER ALGUN MOTIU NO POT FER MOVIMENT ENS AHORREM DIVERSES COMPROVACIONS
                if potFerMoviment:
                    #print("NO ESTA FORA DELS LLIMITS")
        
                    ####### COMPROVEM SI RETROCEDEIX

                    #OBTENIM PENULTIMA POSICIO DEL JUGADOR DE LA MATEIXA FORMA QUE HEM OBTÉS LA ÚLTIMA PERO REDUINT UNA POSICIÓ MÉS, AQUESTA POT NO EXISTIR, PER TANT HA D'HAVER UN PERIODE 2 COM A MÍNIM, TENINT EN COMPTE QUE COMENÇEM EN PERIODE 1
                    if self.agent.periode >= 2:
                        penUltPos = self.agent.celesPos[str(self.agent.periode - 1)]
                        #penultimaPosicio = tuple(celes_list[self.agent.periode-2])
                        #penUltPos = [int(word) for word in tuple(penultimaPosicio) if word.isdigit()]
                    else:
                        penUltPos= (-5, -5)

                    if (yActual,xActual) == tuple(penUltPos) and potFerMoviment:
                        print("HEM CALCULAT QUE RETROCEDEIX")
                        self.agent.celes.pop(str(ultPos))
                        self.agent.celesPos.pop(str(self.agent.periode))
                        periodeProvisional = self.agent.periode - 1
                        retrocedeix = True
                ####### SABEM QUE NO RETROCEDEIX

                    # COMPROVEM SI OBSTRUIX UN OBSTACLE
                    elif str((yActual,xActual)) in self.agent.obstaclesOrdenats:
                        print("ENS HEM TROBAT EN UN OBSTACLE")
                        potFerMoviment = False
                    # COMPROVEM SI OBSTRUIX EL RASTRE
                    elif str((yActual,xActual)) in self.agent.celes:
                        print("ENS HEM TROBAT EN UN RASTRE")
                        potFerMoviment = False
                    # COMPROVEM SI HI HA GUARDIA O MIRA
                    else:
                        #print("COMPROVEM SI SUPERA LA QUANTITAT DE MOVIMENTS")
                        periodeProvisional = self.agent.periode + 1
                        if periodeProvisional >= self.agent.solucio:
                            print("S'HA ACABAT LA CANTITAT DE MOVIMENTS QUE POT FER")
                            potFerMoviment = False
                        else:
                            guardiesDic = {}
                            guardiesDic[0] = self.agent.guardies["0"][str(periodeProvisional)]
                            guardiesDic[1] = self.agent.guardies["1"][str(periodeProvisional)]

                            posActual = str((yActual,xActual))
                            if posActual in guardiesDic[0]:
                                print("ENS HEM TROBAT EN UN GUARDIA")
                                potFerMoviment = False
                            elif posActual in guardiesDic[1]:
                                print("ENS HEM TROBAT EN UN GUARDIA VISIO")
                                potFerMoviment = False



                    # SI RES ENS HA IMPEDIT FER EL MOVIMENT
                    if potFerMoviment:
                        print("PODEM REALITZAR MOVIMENT")
                        self.agent.periode = periodeProvisional
                        # COMPROVEM SI EL NIVELL ESTA COMPLET
                        if retrocedeix:
                            dicNivellUsuari["moviment"] = "SI"
                            dicNivellUsuari["periode"] = self.agent.periode
                            dicNivellUsuari["celes"] = self.agent.celes
                            dicNivellUsuari["celesPos"] = self.agent.celesPos
                            guardiesEmpaquetats = {}
                            guardiesEmpaquetats = await self.agent.empaquetarGuardies(guardiesEmpaquetats, self.agent.periode)
                            dicNivellUsuari["guardies"]= guardiesEmpaquetats
                        elif str((yActual,xActual)) == str(tuple(self.agent.posFinal)):
                            print("NIVELL COMPLET")
                            # SI LA CASSELLA USUARI ESTA EN LA CASSELLA FINAL, CANVIEM REGISTRES I MOVEM AL ESTAT CONTACTE GESTOR
                            dicNivellUsuari["moviment"] = "COMPLET"
                            destinatari = self.agent.agentGestor

                            #OBTENIM PUNTUACIO
                            puntuacio = 20 -(self.agent.periode - self.agent.solucio)

                            #REINICIEM LES DADES DEL USUARI
                            await self.agent.netejarRegistres()

                            #SI EL NIVELL QUE ACABEM DE COMPLETAR ÉS EL MAXIM AUGMENTEM EN 1 EL MAXIM
                            if self.agent.nivellMax == self.agent.nivellJugat:
                                self.agent.nivellMax += 1
                            dicInfoUsuari = await self.agent.empaquetarUsuari(puntuacio)
                            dicInfoUsuari["menu"] = "si"

                            #print("ENVIEM UN MISSATGE AL USUARI PER A INFORMAR-LI QUE HA COMPLETAT EL NIVELL")
                            messageUsuari = Message(to=self.agent.usuari)
                            messageUsuari.body = json.dumps(dicNivellUsuari)
                            await self.send(messageUsuari)


                        # SI EL NIVELL NO ESTA COMPLET REALITZEM EL MOVIMENT
                        else:
                            #PRIMER LES VARIABLES QUE PASSEM AL CLIENT
                            guardiesEmpaquetats = {}
                            guardiesEmpaquetats = await self.agent.empaquetarGuardies(guardiesEmpaquetats, periodeProvisional)
                            dicNivellUsuari["guardies"] = guardiesEmpaquetats
                            dicNivellUsuari["moviment"] = "SI"
                            dicNivellUsuari["periode"] = self.agent.periode
                            self.agent.celes[str((yActual,xActual))] = self.agent.periode
                            self.agent.celesPos[str(self.agent.periode)] = (yActual,xActual)
                            dicNivellUsuari["celesPos"] = self.agent.celesPos
                            dicNivellUsuari["celes"] = self.agent.celes
                    else:
                        print("NO hem pogut realitzar el MOVIMENT solicitat")
                        dicNivellUsuari["moviment"] = "NO"
                else:
                    print("NO hem pogut realitzar el MOVIMENT solicitat")
                    dicNivellUsuari["moviment"] = "NO"

                            
            #SI ENVIEM MISSATGE AL USUARI ES PER INFORMAR DEL MOVIMENT QUE VOL REALTIZAR
            #SI ENVIEM MISSATGE AL GESTOR ES PERQUE EM TORNAT AL MENU
            #SI ENVIEM MISSATGE AL CONTROLADO ES PERQUE AQUEST ESTA ACTUANT COM A GESTOR

            message = Message(to=destinatari)

            if destinatari == self.agent.usuari:
                message.body = json.dumps(dicNivellUsuari)
                await self.send(message)

                self.set_next_state(COMPROVAR_MOVIMENT)
            elif destinatari == self.agent.agentGestor or destinatari == self.agent.agentGestor2:
                print("Enviem NIVELL COMPLET a l'agent GESTOR per a que ACTUALITZE REGISTRES")
                message.body = json.dumps(dicInfoUsuari)
                await self.send(message)

                if msg.body == "EIXIR":
                    self.set_next_state(EIXIR)
                else:
                    self.set_next_state(TRANSFERENCIA_NIVELL)
            elif destinatari == str(self.agent.jid):
                print("Ens reenviem aquest missatge i canviem a estat TRANSFERENCIA_NIVELL")
                message.body = msg.body
                await self.send(message)

                self.set_next_state(TRANSFERENCIA_NIVELL)
            else:
                print("ERROR, VOLEM ENVIAR MISSATGE A ALGÚ QUE NO ES GESTOR, USUARI O NOSALTRES EN ESTAT COMPROVAR MOVIMENT")

       
class EstatEixir(State):
    async def run(self):
        print("Apaguem Agent CONTROLADOR", str(self.agent.jid))
        #si no assignem un següent estat és com si acabara


class AgentControlador(Agent):
    agentGestor = "agentegestor@localhost"
    agentGestor2 = "agentegestor@127.0.0.1"
    contador = 0

    usuari = None
    nivellMax = 0
    nivellJugat = 0
    celes = {}
    celesPos = {}
    periode = 0
    dicNivell = {}

    nivell = 0
    dimensions = None
    posInicial = None
    posFinal = None
    solucio = 0
    obstaclesOrdenats = None
    guardies = None


    async def carregarVariables(self, dicInfoUsuari):
        self.usuari = dicInfoUsuari["usuari"]
        self.nivellMax = dicInfoUsuari["nivellMax"]
        self.nivellJugat = dicInfoUsuari["nivellJugat"]
        self.celes = dicInfoUsuari["celes"]
        self.celesPos = dicInfoUsuari["celesPos"]
        self.periode = dicInfoUsuari["periode"]

    async def carregarNivell(self, dicInfoNivell):
        self.dicNivell = dicInfoNivell.copy()
        self.nivell = dicInfoNivell["nivell"]
        (self.dimY, self.dimX) = dicInfoNivell["dimensions"]
        self.posInicial = dicInfoNivell["posInicial"]
        self.posFinal = dicInfoNivell["posFinal"]
        self.solucio = dicInfoNivell["solucio"]
        self.obstaclesOrdenats = dicInfoNivell["obstaclesOrdenats"]
        self.guardies = dicInfoNivell["guardies"]

        #PER A OBSTACLES DESCOMENTAR OBSTACLES ORDENATS EN CREADOR DE NIVELLS


    async def netejarRegistres(self):
        self.nivellJugat = self.nivell
        self.periode = 1
        (x,y) = self.posInicial
        self.celes = {str((x,y)) : 1}
        self.celesPos = {'1' : (x,y)}

    async def empaquetarGuardies(self, guardiesPeriode, per):
        guardiesPeriode[0] = self.guardies["0"][str(per)]
        guardiesPeriode[1] = self.guardies["1"][str(per)]

        return guardiesPeriode

    async def empaquetarUsuariN(self):
        dicInfoUsuari = {"usuari" : self.usuari, "controlador" : str(self.jid), "nivellMax" : self.nivellMax, "nivellJugat" : self.nivellJugat, "celes" : self.celes, "celesPos" : self.celesPos, "periode" : self.periode}
        print("Guardem els dades de l'agent USUARI en un diccionari per a enviar-li'l a l'agent GESTOR")
        return dicInfoUsuari

    async def empaquetarUsuari(self, puntuacio):
        dicInfoUsuari = {"usuari" : self.usuari, "controlador" : str(self.jid), "nivellMax" : self.nivellMax, "nivellJugat" : self.nivellJugat, "celes" : self.celes, "celesPos" : self.celesPos, "periode" : self.periode, "puntuacio" : puntuacio}
        print("Hem COMPLETAT NIVELL, Guardem els dades de l'agent USUARI nés la PUNTUACIO en un diccionari per a enviar-li'l a l'agent GESTOR")
        return dicInfoUsuari
    


    async def setup(self):

        fsm = BehaviourEstats()
        fsm.add_state(name=TRANSFERENCIA_NIVELL, state=EstatMenuControlador(), initial=True)
        fsm.add_state(name=COMPROVAR_MOVIMENT, state=EstatMovimentControlador())
        fsm.add_state(name=EIXIR, state=EstatEixir())

        fsm.add_transition(source=TRANSFERENCIA_NIVELL, dest=COMPROVAR_MOVIMENT)
        fsm.add_transition(source=COMPROVAR_MOVIMENT, dest=COMPROVAR_MOVIMENT)
        fsm.add_transition(source=COMPROVAR_MOVIMENT, dest=TRANSFERENCIA_NIVELL)

        fsm.add_transition(source=TRANSFERENCIA_NIVELL, dest=EIXIR)
        fsm.add_transition(source=COMPROVAR_MOVIMENT, dest=EIXIR)
        self.add_behaviour(fsm)

        await super().setup()
