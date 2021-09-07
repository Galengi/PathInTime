from spade.behaviour import FSMBehaviour
from spade.behaviour import State
import json

from spade.agent import Agent
from selenium import webdriver

CONTACTE = "CONTACTE"
EIXIR = "EIXIR"


class BehaviourEstats(FSMBehaviour):
    async def on_start(self):
        print(f"FSM starting at initial state {self.current_state}")
        print("El nom d'aquest usuari es: ", str(self.agent.jid))

    async def on_end(self):
        print(f"FSM GESTOR AGENT finished at state {self.current_state}")
        await self.agent.stop()


# GESTOR
class EstatContacte(State):
    async def run(self):
        if self.agent.eixim:
            self.set_next_state(EIXIR)
        else:
            msg = await self.receive(timeout=500)
            if msg:  # SOBRARIA EL IF MSG?
                info = json.loads(msg.body)
                print("Canvi en el les finestres: ", info)
                if self.agent.primerContacte:
                    self.agent.driver = webdriver.Firefox()
                    self.agent.port = info["port"]
                    self.agent.primerContacte = False

                if info["window"] == "MENU":
                    self.agent.driver.get("http://localhost:"+str(self.agent.port)+"/launcher")
                    self.agent.driver.set_window_size(400, 512)
                elif info["window"] == "NIVELL":
                    (height ,width) =  info["size"]
                    if info["mode"] == "BOTONS":
                        self.agent.driver.set_window_size(540, height * 32 + 620)
                    elif info["mode"] == "TECLAT":
                        self.agent.driver.set_window_size(400, 290 + height * 32)
                    self.agent.driver.get("http://localhost:"+str(self.agent.port)+"/level")
                elif info["window"] == "LEYENDA":
                    driver2 = webdriver.Firefox()
                    driver2.set_window_size(400, 400)
                    driver2.get("http://localhost:14000/leyenda")
                elif info["window"] == "RANKING":
                    driver2 = webdriver.Firefox()
                    driver2.set_window_size(600, 750)
                    driver2.get("http://localhost:14000/ranking")
                elif info["window"] == "EIXIR":
                    self.agent.eixim = True

            self.set_next_state(CONTACTE)


class EstatEixir(State):
    async def run(self):
        print("Apaguem Agent")
        self.agent.driver.close()
        # si no assignem un següent estat és com si acabara


class AgentInterficie(Agent):
    primerContacte = True
    driver = None
    port = 0
    eixim = False

    async def setup(self):

        fsm = BehaviourEstats()
        fsm.add_state(name=CONTACTE, state=EstatContacte(), initial=True)
        fsm.add_state(name=EIXIR, state=EstatEixir())

        fsm.add_transition(source=CONTACTE, dest=CONTACTE)
        fsm.add_transition(source=CONTACTE, dest=EIXIR)
        self.add_behaviour(fsm)

        await super().setup()