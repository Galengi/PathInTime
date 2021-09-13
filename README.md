# PathInTime
TFG de Àngel Giner Vidal

Instal·lacions necessàries
Per a iniciar el videojoc necessitem fer algunes instal·lacions prèvies, així com seguir unordre en la execució de fitxers. Aquests donen algunes coses per defecte:
El nom del servidor local és localhost.

•-Els fitxers amb les classes ’webCreator’ i ’creadorNivells’ es troben a la mateixacarpeta que la classe de l’agent Gestor.

•-El fitxer amb la classe ’WebCreator’ es troba en la mateixa carpeta que la classe del’agent Usuari.

•-El driver corresponent, Geckodriver per a Mozilla Firefox, ha sigut afegit al PATH abans d’executar l’agent Interfície.
(PER A AFEGIR A LA RUTA LA PROPIA CARPETA) export PATH=$PATH:$PWD

•-El driver corresponent, té permisos d'execució.
(PER A DONAR-LI PERMISOS D'EXECUCIÓ AL geckodriver) sudo chmod +x geckodriver

•-Si els agents no estan registrats el servidor ha de tindre elregistre en bandaactivat

Tenint en compte el punts inicials,  també cal instal·lar a l’entorn on s’executen elsagents les següents biblioteques:
spade == 3.2.0
selenium == 3.141.0
numpy == 1.21.1
Aquest últim procés pot ser obviat amb l’execució del fitxer, ’instalarBiblioteques.py’. 
El qual com el nom indica, instal·la les biblioteques anteriorment mencionades. 
No obstant hem d’informar que utilitzar un script per instal·lar paquets no és aconsellable segonsPython Packaging Authority (PyPA) degut a que pip no és un fil segur i està intencionalment dissenyat per a llançar-se com un únic procés.  
El que pot provocar resultatsinesperats.

Inici del projecte
Una vegada complit aquests requisits, s’ha d’activar el servidor al qual volem connectar-nos. 
I finalment, llançar l’agent Interfície i l’agent Gestor indiferentment de l’ordre peròsempre deixant l’agent Usuari al final.
Hem de fer-ho seguint aquest ordre ja que en cas de llançar-lo abans que l’AG, aquest norebrà comunicació de l’AU i aquest últim es quedarà esperant el nivell per a dissenyar el menú.  
En cas d’encendre’l abans que l’AI, no s’obrirà la finestra inicial per a poder seleccionar nivell.  
No obstant podrem accedir des de qualsevol navegador si sabem la URL corresponent.
Pel que fa l’AUi l’AI requereixen una sèrie d’arguments. 
En el cas de l’AI tan sols necessita elnom del seu AU. 
Per a aquest últim requereix més entrades:  un indicador per saber quin és elmodea utilitzar, teclat = t o Tibotons = bo B, el nom d’agent que volem validar, la seua respectiva contrasenya, i en cas de ser necessari, un port.  
El port ens resulta necessari en el nostre cas ja que el projecte l’hem executat a un servidor local i per tant necessitàvem diferenciar entre agents.
