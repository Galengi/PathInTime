import random
import numpy as np

class creadorNivells:
    diccionariNivell = {}
    nivell = 0
    min = 5
    max = 10
    matriu2 = []
    matriu = []
    posFinalX = 0
    posFinalY = 0
    posIniX = 0
    posIniY = 0
    matriuGuardies = []
    dicCamiSol = {}

    matriuGuardies2 = {}
    matriuGuardiesPer0 = {}
    matriuGuardiesPer1 = {}

    matriuGuardiesNou0 = {}
    matriuGuardiesNou1 = {}


    numFiles = 0
    numCol = 0
    contadorCeles = 0
    obstaclesOrdenats = {}


    def crearNivell(self, lvl):
        self.nivell = lvl
        if lvl <=5:
            self.min = 5
            self.max = 7
            self.guards = 0.05
        elif lvl > 5 and lvl <= 10:
            self.min = 5
            self.max = 8
            self.guards = 0.07
        elif lvl > 10 and lvl <= 15:
            self.min = 6
            self.max = 10
            self.guards = 0.1
        elif lvl > 15 and lvl <= 20:
            self.min = 7
            self.max = 11
            self.guards = 0.12
        else:
            self.min = 8
            self.max = 13
            self.guards = 0.15

        # VARIABLES INICIALS
        complet = False

        # Files y Columnes aleatories
        self.numFiles = random.randint(self.min, self.max)
        self.numCol = random.randint(self.min, self.max)

        # Files y Columnes aleatories
        # self.numFiles = random.randint(self.min, self.max)
        # self.numCol = random.randint(self.min, self.max)

        # Creem matriu a partir de files i columnes
        self.matriu = [[0] * self.numCol for i in range(self.numFiles)]
        matriuNivell = [[0] * self.numCol for i in range(self.numFiles)]

        # Guardies aleatori
        self.guardies = int(self.numCol * self.numFiles * self.guards)

        # Guardies aleatori
        # self.guardies = int(self.numCol * self.numFiles * 0.1)


        # Creem la posició inicial i la final, i asignem la posició actual com a la inicial
        posActualX = int(self.numCol / 2)
        posActualY = self.numFiles - 1
        self.posIniX = posActualX
        self.posIniY = posActualY
        self.posFinalX = random.randint(0, self.numCol - 1)
        self.posFinalY = 0

        # Iniciem em la matriu la posició incial, guardem la posició final i iniciem el contador de celes a 1
        self.matriu[posActualY][posActualX] = 1
        self.matriu[self.posFinalY][self.posFinalX] = 99
        self.contadorCeles = 1
        self.dicCamiSol[self.contadorCeles] = (posActualY, posActualX)

        # Obstacles aleatori i iniciem les variables dels obstacles per a crear-los
        obstacles = int(self.numCol * self.numFiles * 0.3)
        x = 0
        canvi = False
        iteracions = 0
        
        self.matriuGuardies2 = {}
        self.matriuGuardiesPer0 = {}
        self.matriuGuardiesPer1 = {}

        self.matriuGuardiesNou0 = {}
        self.matriuGuardiesNou1 = {}

        diccionariObstacles = {}
        self.obstaclesOrdenats = {}

        # OBSTACLES
        comprovatSolucio = False
        # Per a comprovar que existeix un cami
        while not comprovatSolucio:
            # Necessitem copiar la matriu 2 vegades, matriu2 perque es modificada per la funció recorregut,
            # i la matriu 3 en cas d'obtindre solució sustituirà la matriu original i en cas contrari es resetejarà
            self.matriu2 = np.copy(self.matriu)
            self.matriu3 = np.copy(self.matriu)
            for i in range(obstacles):
                # Obtenim una posició aleatòria, si està ocupada tornem a repetir el mateix número d'obstàcle, per a que hi hajen els designats inicialment
                posXAl = random.randint(0, self.numCol - 1)
                posYAl = random.randint(0, self.numFiles - 1)
                if self.matriu2[posYAl][posXAl] == 0:
                    self.matriu2[posYAl][posXAl] = -5
                    self.matriu3[posYAl][posXAl] = -5
                else:
                    i -= 1
            # Al acabar comprovem que existeix algún camí
            if self.recorregut(posActualY - 1, posActualX) < 0 or self.recorregut(posActualY, posActualX - 1) < 0 or self.recorregut(posActualY, posActualX + 1) < 0:
                comprovatSolucio = True

        # Sustituim la matriu original per aquesta amb els obstàcles
        self.matriu = np.copy(self.matriu3)
        matriuNivell = np.copy(self.matriu3)
        contador = 1

        # Omplim el diccionari d'obstacles
        for i in range(self.numCol):
            for j in range(self.numFiles):
                if self.matriu[j][i] == -5:
                    diccionariObstacles[contador] = (j, i)
                    contador += 1

        for x in diccionariObstacles:
            obs = diccionariObstacles[x]
            self.obstaclesOrdenats[str(tuple(obs))] = 'obstacle'

        # Omplim els diccionariNivell en les variables corresponents
        self.diccionariNivell["dimensions"] = (self.numFiles, self.numCol)
        self.diccionariNivell["posInicial"] = (self.posIniY, self.posIniX)
        self.diccionariNivell["posFinal"] = (self.posFinalY, self.posFinalX)
        #self.diccionariNivell["obstacles"] = diccionariObstacles
        self.diccionariNivell["obstaclesOrdenats"] = self.obstaclesOrdenats

        # CAMI SOLUCIO
        while not complet:
            if iteracions >= 100:
                #print("ALGO HA PASSAT")
                complet = True
                return self.crearNivell(self.nivell)
            dir = random.randint(0, 3)
            if dir == 0:
                try:
                    if self.matriu[posActualY][posActualX + 1] == 0 or self.matriu[posActualY][posActualX + 1] == 99:
                        self.matriu2 = np.copy(self.matriu)
                        if self.recorregut(posActualY, posActualX + 1) < 0:
                            canvi = True
                            posActualX = posActualX + 1
                except IndexError:
                    print("error")
            elif dir == 1:
                try:
                    if posActualX != 0:
                        if self.matriu[posActualY][posActualX - 1] == 0 or self.matriu[posActualY][posActualX - 1] == 99:
                            self.matriu2 = np.copy(self.matriu)
                            if self.recorregut(posActualY, posActualX - 1) < 0:
                                canvi = True
                                posActualX = posActualX - 1
                except IndexError:
                    print("error")
            elif dir == 2:
                try:
                    if self.matriu[posActualY + 1][posActualX] == 0 or self.matriu[posActualY + 1][posActualX] == 99:
                        self.matriu2 = np.copy(self.matriu)
                        if self.recorregut(posActualY + 1, posActualX) < 0:
                            canvi = True
                            posActualY = posActualY + 1
                except IndexError:
                    print("error")
            else:
                try:
                    if posActualY != 0:
                        if self.matriu[posActualY - 1][posActualX] == 0 or self.matriu[posActualY - 1][posActualX] == 99:
                            self.matriu2 = np.copy(self.matriu)
                            if self.recorregut(posActualY - 1, posActualX) < 0:
                                canvi = True
                                posActualY = posActualY - 1
                except IndexError:
                    print("error")

            iteracions += 1

            if canvi:
                self.contadorCeles += 1
                self.matriu[posActualY][posActualX] = self.contadorCeles
                self.dicCamiSol[self.contadorCeles] = (posActualY, posActualX)
                canvi = False

            if posActualX == self.posFinalX and posActualY == self.posFinalY:
                complet = True

        # Creem un matriu de 3 dimensions, el primer valor l'utlitlzem per a la posició del guardia la 2na per la direcció que esta mirant al anar, i la 3ra per a la direcció on esta mirant al tornar
        complet = False
        self.diccionariNivell["solucio"] = self.contadorCeles + 1
        self.dicCamiSol[self.contadorCeles + 1] = (-5, -5)
        self.dicCamiSol[self.contadorCeles + 2] = (-5, -5)
        self.matriuGuardies = [[[(0, 0)] * self.contadorCeles for i in range(self.guardies)] for j in range(2)]

        print("el diccionari del cami es: ", self.dicCamiSol)
        print("EL CAMI SOLUCIO ES EN: ", self.diccionariNivell["solucio"])
        print("la matriu es", self.matriu)


        iteracions = 0
        numGuardia = 0
        completTot = False

        #Resetejem els diccionaris dels guardies
        self.matriuGuardiesPer0 = {}
        self.matriuGuardiesPer1 = {}

        self.matriuGuardiesPer0[1] = {}
        self.matriuGuardiesPer1[1] = {}

        #print("ENTREM A LA CREACIO DELS GUARDIES")

        while not completTot:
            #print("AFEGINT GUARDIES...")
            if iteracions >= 10:
                print("No ha pogut posar tots els guardies")
                print("TORNEM A CRIDAR AL ALGORISME")
                completTot = True
                return self.crearNivell(self.nivell)

            if self.crearCamiGuardia(numGuardia) == True:
                numGuardia += 1
                #print("LA MATRIU FINAL, ABANS DE FER EL UPDATE ", self.matriuGuardiesPer0)
                for key in range(self.contadorCeles):
                    key += 1
                    self.matriuGuardiesPer0[key].update(self.matriuGuardiesNou0[key])
                    self.matriuGuardiesPer1[key].update(self.matriuGuardiesNou1[key])
                #print("LA MATRIU FINAL, INCREMENTEM LA POSICIO d'1 GUARDIA ", self.matriuGuardiesPer0)
            else:
                iteracions += 1

            if numGuardia >= self.guardies:
                #print("Done")
                completTot = True

        self.matriuGuardies2[0] = {}
        self.matriuGuardies2[1] = {}

        #print("MATRIUGUARDIES2       ", self.matriuGuardies2)
        #print("matriuGuardiesPer0       ", self.matriuGuardiesPer0)
        #print("matriuGuardiesPer1       ", self.matriuGuardiesPer1)

        for x in range(self.contadorCeles):
            x += 1
            self.matriuGuardies2[0][x] = {}
            self.matriuGuardies2[1][x] = {}
            for key,value in self.matriuGuardiesPer0[x].items():
                keyString = str(key)
                self.matriuGuardies2[0][x][keyString] = value
            for key,value in self.matriuGuardiesPer1[x].items():
                keyString = str(key)
                self.matriuGuardies2[1][x][keyString] = value


        #self.matriuGuardies2[0] = self.matriuGuardiesPer0
        #self.matriuGuardies2[1] = self.matriuGuardiesPer1

        self.diccionariNivell["nivell"] = self.nivell
        self.diccionariNivell["guardies"] = self.matriuGuardies2
        #print("MATRIU CAMI SOLUCIO", self.dicCamiSol)
        #print("MATRIU GUARDIES", self.matriuGuardies2)

        return self.diccionariNivell

    def recorregut(self, posY, posX):
        try:
            if self.matriu2[posY][posX] == 0:
                self.matriu2[posY][posX] = -1
                # es returna 1 + una crida recursiva en totes direccions, en l'if anterior eliminem els casos en que estan ocupats
                # la posicioActual que ha inicat la crida esta ocupat, per tant no poden entrar en conflicte les dos cridades
                if posY == 0 and posX == 0:
                    return 1 + self.recorregut(posY + 1, posX) + self.recorregut(posY , posX + 1)
                elif posX == 0:
                    return 1 + self.recorregut(posY + 1, posX) + self.recorregut(posY - 1, posX) + self.recorregut(posY , posX + 1)
                elif posY == 0:
                    return 1 + self.recorregut(posY + 1, posX) + self.recorregut(posY , posX + 1) + self.recorregut(posY, posX - 1)
                else:
                    return 1 + self.recorregut(posY + 1, posX) + self.recorregut(posY - 1, posX) + self.recorregut(posY , posX + 1) + self.recorregut(posY, posX - 1)
            #si no cumplix les condicions suma 0
            elif self.matriu2[posY][posX] == 99:
                return -2000
            else:
                return 0
        except IndexError:
            return 0

    def crearCamiGuardia(self, numGuardia):
        #print("ENTREM A CREAR GUARDIA")
        moviment = 1
        ocupat = False
        comprovat = False
        completGuardia = False
        canvi = False
        mal = False
        gir = False
        iteracionsGuardia = 0
        self.matriuGuardiesNou0 = {}
        self.matriuGuardiesNou1 = {}
        self.matriuGuardiesNou0[moviment] = {}
        self.matriuGuardiesNou1[moviment] = {}

        while not comprovat:
            #Obtenim una posició aleatòria
            posX = random.randint(0, self.numCol - 1)
            posY = random.randint(0, self.numFiles - 1)
            #Comprovem que la posició no es trobe en la posició del jugador
            if posX != self.posIniX or posY != self.posIniY:
                #Comprovem que la posició no es trobe en la posició d'algún obstacle
                if str((posY, posX)) not in self.obstaclesOrdenats:
                    #Comprovem que la posició no es trobe en la posició d'algún guàrdia
                    if (posY, posX) not in self.matriuGuardiesPer0[moviment]:
                        dir = random.randint(0, 3)
                        posYMira = posY
                        posXMira = posX
                        if dir == 0:
                            direccioAnterior = 0
                            posYMira = posY + 1
                            if self.dicCamiSol[1] != (posYMira, posXMira):
                                comprovat = True
                                self.matriuGuardiesNou0[moviment][(posY, posX)] = (numGuardia, 0)
                                self.matriuGuardiesNou1[moviment][(posY + 1, posX)] = numGuardia
                        elif dir == 1:
                            direccioAnterior = 1
                            posYMira = posY - 1
                            if self.dicCamiSol[1] != (posYMira, posXMira):
                                comprovat = True
                                self.matriuGuardiesNou0[moviment][(posY, posX)] = (numGuardia, 1)
                                self.matriuGuardiesNou1[moviment][(posY - 1, posX)] = numGuardia
                        elif dir == 2:
                            direccioAnterior = 2
                            posXMira = posX + 1
                            if self.dicCamiSol[1] != (posYMira, posXMira):
                                comprovat = True
                                self.matriuGuardiesNou0[moviment][(posY, posX)] = (numGuardia, 2)
                                self.matriuGuardiesNou1[moviment][(posY, posX + 1)] = numGuardia
                        else:
                            direccioAnterior = 3
                            posXMira = posX - 1
                            if self.dicCamiSol[1] != (posYMira, posXMira):
                                comprovat = True
                                self.matriuGuardiesNou0[moviment][(posY, posX)] = (numGuardia, 3)
                                self.matriuGuardiesNou1[moviment][(posY, posX - 1)] = numGuardia
                        #print("POSICIO INICIAL DEL JUGADOR ", self.dicCamiSol[1])
                        #print("POSICIO INICIAL DEL GUARDIA ESTA OK? ", (posYMira, posXMira))
                        
        moviment += 1

        #print("PRIMERAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA POSICIÓ DE LA MATRIU DELS GUARDIES", self.matriuGuardiesNou0)

        while not completGuardia:
            if moviment not in self.matriuGuardiesPer0:
                self.matriuGuardiesPer0[moviment] = {}
            if moviment not in self.matriuGuardiesPer1:
                self.matriuGuardiesPer1[moviment] = {}
            if moviment + 1 not in self.matriuGuardiesPer0:
                self.matriuGuardiesPer0[moviment + 1] = {}
            if moviment + 1 not in self.matriuGuardiesPer1:
                self.matriuGuardiesPer1[moviment + 1] = {}


            if iteracionsGuardia >= 10:
                print("ALGO HA PASSAT EN ELS GUARDIES")
                mal = True
                completGuardia = True

            #print(moviment)
            dir = random.randint(0, 2)
            ocupat = True
            # #print("volem fer un " , dir)
            # #print(gir)
            if dir == 0 or gir:  # recte
                # baix
                if direccioAnterior == 0:
                    #print("NOVA POSICIO A LA QUE VOLEM MOUREN'S1111111111111111", posY + 1, posX)
                    # #print("movem baix")
                    if not gir:  # si gir = true, significa que acaba de girar, i per tant, s'han fet les comprovacions necessaries per a que es moga en la direcció designada
                        if posY + 1 < self.numFiles:
                            try:
                                #print("EL VALOR DE LA MATRIU EN DITA POSICIO", self.matriu[posY + 1][posX], "EL VALOR DEL MOVIMENT QUE VOLEM EFECTUAR ES: ", moviment)
                                if self.dicCamiSol[moviment] != (posY + 1, posX) and self.dicCamiSol[moviment] != (posY + 2, posX):
                                    if (posY + 1, posX) not in self.matriuGuardiesPer0[moviment] and str((posY + 1, posX)) not in self.obstaclesOrdenats:
                                        ocupat = False
                            except IndexError:
                                print("error")
                    else:
                        ocupat = False
                    if not ocupat:
                        canvi = True
                        gir = False
                        direccioAnterior = 0
                        posY += 1
                        posYMira = posY + 1
                        posXMira = posX
                        iteracionsGuardia = 0

                    # dalt
                elif direccioAnterior == 1:
                    #print("NOVA POSICIO A LA QUE VOLEM MOUREN'S222222222222222", posY - 1, posX)
                    # #print("movem dalt")
                    if not gir:
                        if posY - 1 >= 0:
                            try:
                                #print("EL VALOR DE LA MATRIU EN DITA POSICIO", self.matriu[posY - 1][posX])
                                if self.dicCamiSol[moviment] != (posY - 1, posX) and self.dicCamiSol[moviment] != (posY - 2, posX):
                                    if (posY - 1, posX) not in self.matriuGuardiesPer0[moviment] and str((posY - 1, posX)) not in self.obstaclesOrdenats:
                                        ocupat = False
                            except IndexError:
                                print("error")
                    else:
                        ocupat = False
                    if not ocupat:
                        canvi = True
                        gir = False
                        direccioAnterior = 1
                        posY -= 1
                        posYMira = posY - 1
                        posXMira = posX
                        iteracionsGuardia = 0

                    # dreta
                elif direccioAnterior == 2:
                    #print("NOVA POSICIO A LA QUE VOLEM MOUREN'S3333333333333333333333", posY, posX + 1)
                    # #print("movem dreta")
                    if not gir:
                        if posX + 1 < self.numCol:
                            try:
                                #print("EL VALOR DE LA MATRIU EN DITA POSICIO", self.matriu[posY][posX + 1])
                                # if self.matriu[posY][posX + 1] != moviment and self.matriu[posY][posX + 1] != -5 and self.matriu[posY][posX + 2] != moviment:
                                if self.dicCamiSol[moviment] != (posY, posX + 1) and self.dicCamiSol[moviment] != (posY, posX + 2):
                                    if (posY, posX + 1) not in self.matriuGuardiesPer0[moviment] and str((posY, posX + 1)) not in self.obstaclesOrdenats:
                                        ocupat = False
                            except IndexError:
                                print("error")
                    else:
                        ocupat = False
                    if not ocupat:
                        canvi = True
                        gir = False
                        direccioAnterior = 2
                        posX += 1
                        posXMira = posX + 1
                        posYMira = posY
                        iteracionsGuardia = 0

                    # esquerra
                else:
                    #print("NOVA POSICIO A LA QUE VOLEM MOUREN'S4444444444444444444444", posY, posX - 1)
                    # #print("movem esquerra")
                    if not gir:
                        if posX - 1 >= 0:
                            try:
                                #print("EL VALOR DE LA MATRIU EN DITA POSICIO", self.matriu[posY][posX - 1])
                                if self.dicCamiSol[moviment] != (posY, posX - 1) and self.dicCamiSol[moviment] != (posY, posX - 2):
                                    if (posY, posX - 1) not in self.matriuGuardiesPer0[moviment] and str((posY, posX - 1)) not in self.obstaclesOrdenats:
                                        ocupat = False
                            except IndexError:
                                print("error")
                    else:
                        ocupat = False
                    if not ocupat:
                        canvi = True
                        gir = False
                        direccioAnterior = 3
                        posX -= 1
                        posXMira = posX - 1
                        posYMira = posY
                        iteracionsGuardia = 0

            elif dir == 1:  # moures a la esquerra/dalt
                # #print("provem a girar esquerra/dalt")
                #print("POSICIO ACTUAL      555555555555555555555555", posY, posX)
                if self.dicCamiSol[moviment] != (posY, posX) and (posY, posX) not in self.matriuGuardiesPer0[moviment]:
                    # baix/dalt va cap a esquerra
                    if direccioAnterior == 0 or direccioAnterior == 1:
                        if posX - 1 >= 0:
                            #print("NOVA POSICIO A LA QUE VOLEM MOUREN'S ESQUERRA 66666666666666666666666", posY, posX - 1)
                            try:
                                #print("EL VALOR DE LA MATRIU EN DITA POSICIO actual", self.matriu[posY][posX])
                                #print("EL VALOR DE LA MATRIU EN DITA POSICIO nou", self.matriu[posY][posX - 1])
                                #print("EL VALOR DE LA MATRIU EN DITA POSICIO nou2", self.matriu[posY][posX - 2])
                                # comprovem la posicio on mira, si hi ha obstacle, si en el seguent instant podra moure's ahi i si en el següent instant podrà mirar en la mateixa direcció
                                if self.dicCamiSol[moviment] != (posY, posX - 1) and self.dicCamiSol[moviment + 1] != (posY, posX - 1) and self.dicCamiSol[moviment + 1] != (posY, posX - 2):
                                    if (posY, posX - 1) not in self.matriuGuardiesPer0[moviment + 1] and str((posY, posX - 1)) not in self.obstaclesOrdenats:
                                        ocupat = False
                                # comprovem que no hi hajen guardies en la poscio que anem a repetir i en la futura
                            except IndexError:
                                print("error")
                        if not ocupat:
                            gir = True
                            canvi = True
                            direccioAnterior = 3
                            posYMira = posY
                            posXMira = posX - 1
                            iteracionsGuardia = 0

                    # esquerra/dreta va cap a dalt
                    else:
                        #print("NOVA POSICIO A LA QUE VOLEM MOUREN'S ESQUERRA 7777777777777777777777", posY - 1, posX)
                        if posY - 1 >= 0:
                            try:
                                #print("EL VALOR DE LA MATRIU EN DITA POSICIO actual", self.matriu[posY][posX])
                                #print("EL VALOR DE LA MATRIU EN DITA POSICIO nou", self.matriu[posY - 1][posX])
                                #print("EL VALOR DE LA MATRIU EN DITA POSICIO nou2", self.matriu[posY - 2][posX])
                                if self.dicCamiSol[moviment] != (posY - 1, posX) and self.dicCamiSol[moviment + 1] != (posY - 1, posX) and self.dicCamiSol[moviment + 1] != (posY - 2, posX):
                                    if (posY - 1, posX) not in self.matriuGuardiesPer0[moviment + 1] and str((posY - 1, posX)) not in self.obstaclesOrdenats:
                                        ocupat = False
                            except IndexError:
                                print("error")
                        if not ocupat:
                            gir = True
                            canvi = True
                            direccioAnterior = 1
                            posYMira = posY - 1
                            posXMira = posX
                            iteracionsGuardia = 0

            else:  # moures a la dreta/baix
                # #print("provem a girar dreta/baix")
                #print("POSICIO ACTUAL      8888888888888888888888", posY, posX)
                if self.dicCamiSol[moviment] != (posY, posX) and (posY, posX) not in self.matriuGuardiesPer0[moviment]:
                    # baix/dalt va cap a la dreta
                    if direccioAnterior == 0 or direccioAnterior == 1:
                        #print("NOVA POSICIO A LA QUE VOLEM MOUREN'S9999999999999999999999999999", posY, posX + 1)
                        if posX + 1 < self.numCol:
                            try:
                                # comprovem la posicio on mira, si hi ha obstacle si en el seguent instant podra moure's ahi i si en el següent instant podrà mirar en la mateixa direcció
                                if self.dicCamiSol[moviment] != (posY, posX + 1) and self.dicCamiSol[moviment + 1] != (posY, posX + 1) and self.dicCamiSol[moviment + 1] != (posY, posX + 2):
                                    if (posY, posX + 1) not in self.matriuGuardiesPer0[moviment + 1] and str((posY, posX + 1)) not in self.obstaclesOrdenats:
                                        ocupat = False
                            except IndexError:
                                print("error")
                        if not ocupat:
                            gir = True
                            canvi = True
                            direccioAnterior = 2
                            posYMira = posY
                            posXMira = posX + 1
                            iteracionsGuardia = 0

                    # esquerra/dreta va cap a baix
                    else:
                        #print("NOVA POSICIO A LA QUE VOLEM MOUREN'S BAIXAR 1111111111111100000000000000000", posY + 1, posX)
                        if posY + 1 < self.numFiles:
                            try:
                                #print("EL VALOR DE LA MATRIU EN DITA POSICIO actual", self.matriu[posY][posX])
                                #print("EL VALOR DE LA MATRIU EN DITA POSICIO nou", self.matriu[posY + 1][posX])
                                #print("EL VALOR DE LA MATRIU EN DITA POSICIO nou2", self.matriu[posY + 2][posX])
                                if self.dicCamiSol[moviment] != (posY + 1, posX) and self.dicCamiSol[moviment + 1] != (posY + 1, posX) and self.dicCamiSol[moviment + 1] != (posY + 2, posX):
                                    if (posY + 1, posX) not in self.matriuGuardiesPer0[moviment + 1] and str((posY + 1, posX)) not in self.obstaclesOrdenats:
                                        ocupat = False
                            except IndexError:
                                print("error")
                        if not ocupat:
                            gir = True
                            canvi = True
                            direccioAnterior = 0
                            posYMira = posY + 1
                            posXMira = posX
                            iteracionsGuardia = 0

            iteracionsGuardia += 1
            if moviment == self.contadorCeles and posY == self.posFinalY and posX == self.posFinalX:
                mal= True
                completGuardia = True

            if canvi:
                #print("LAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA POSICIO ELEGIDA FINALMENT ES  ", posY, posX)
                #print("POSICIONS EN TEORIA, SENSE MODIFICAR: ", self.matriuGuardiesPer0)
                #print("POSICIONS NOVES", self.matriuGuardiesNou0)
                #print("EL MOVIMENT EEEEES:  ", moviment, "POSICIOO", posY, posX)
                #print("ESTOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO EEES EL CAMI SOLUCIO EN EL MOVIMENT QUE ESTEM FENT, OSIGA, EL MATEIX VALOR DE MOVIMENT POSAEM EN LA MATRIU I ES EL VALOR D'ESTA", self.dicCamiSol[moviment])
                self.matriuGuardiesNou0[moviment] = {}
                self.matriuGuardiesNou1[moviment] = {}
                self.matriuGuardiesNou0[moviment][(posY, posX)] = (numGuardia, direccioAnterior)
                self.matriuGuardiesNou1[moviment][(posYMira, posXMira)] = numGuardia
                #print("EN LA MATRIU DELS GUARDIES, MOVIMENT I POSICIÓ ASIGNADAAAAAAA, ", self.matriuGuardiesNou0[moviment][(posY, posX)])
                moviment += 1
                canvi = False
                #print("POSICIONS EN TEORIA, SENSE MODIFICAR: ", self.matriuGuardiesPer0)
                #print("POSICIONS NOVES", self.matriuGuardiesNou0)

            if moviment > self.contadorCeles + 1:
                completGuardia = True

        if mal:
            print("EL GUARDIA HA PETAT I PER TANT HEM DE RESETEJAR TOT EL GUARDIA")
            #print("LA MATRIU QUE ESTEM COPIANT I NO HEM DE PASSAR ", self.matriuGuardiesNou0)
            #print("LA MATRIU FINAL, DEU QUEDAR-SE COM ES ESTA ARA, EN UN PRINCIPI ", self.matriuGuardiesPer0)
            return False
        else:
            return True

