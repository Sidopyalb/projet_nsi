# Pyxel Studio

import pyxel
from random import randint, choice

TITLE = "Donkey Kong"
WIDTH = 252
HEIGHT = 252
CASE = 12
ESPACE = 36
FRAME_REFRESH = 10
FRAME_REFRESH_CHUTE = 20
X_PEACH = 10
Y_PEACH = 8
#trous
trous = [(36, 24, ESPACE, CASE, 0)]
x_trous_pair = [18*2, 18*6, 18*10]
x_trous_impair = [30*2, 78*2]
#echelles
echelles = []
x_echelles = [randint(0, 13*2), randint(96, 98), randint(72*2, 73*2), randint(108*2, 121*2)]
#personnage
vies = 3
mario_x = 24
mario_y = 228
mario=[]
vitesse = 0
sur_echelle = False
gagne = False
x_dk =60
y_dk = 2
#tonneaux
tonneaux = []
direction = [-2, 2]
chute_t = False
#bananaaaas
bananes = []
chute_b = False
star = 0
super_bananas = []
#explosions
boom = []
#costumes
costume = 0
costume_banane = 0

pyxel.init(WIDTH, HEIGHT, title= TITLE)
pyxel.load("res.pyxres")
pyxel.play(0, 0)

def creation_trous_etages():
    for etage in range(2, 7, 2):
        for case in range(randint(1, 3)):
            trous.append((choice(x_trous_pair), 36*etage-12, ESPACE, CASE, 0))
    for etage in range(3, 7, 2):
        for case in range(randint(1, 2)):
            trous.append((choice(x_trous_impair), 36*etage-12, ESPACE, CASE, 0))
    return trous

def creation_echelles():
    for etage in range(1, 7):
        for echelle in range(randint(1, 3)):
            echelles.append((choice(x_echelles), 36*etage, CASE-2, ESPACE-10, 6))
    return echelles

#Perso
def mario_deplacement(x):
    #deplacements horizontaux
    if pyxel.btn(pyxel.KEY_RIGHT):
        if x < 240:
            x += 2
    elif pyxel.btn(pyxel.KEY_LEFT):
        if x > 0:
            x -= 2
    return x

"""def mario_sauter(y):
    global vitesse
    if pyxel.btnp(pyxel.KEY_SPACE) and pyxel.pget(mario_x, mario_y-4) != 4:
        vitesse = -10
    else : 
        vitesse = 0
    return y + vitesse"""
    
def chute():
    global mario_y, mario_x
    while not pyxel.btnp(pyxel.KEY_SPACE) and pyxel.pget(mario_x, mario_y+15) != pyxel.pget(0,242):
        mario_y += 2

def monter(x):
    global sur_echelle, mario_y
    for echelle in echelles:
        if echelle[0]<=mario_x+12 and echelle[1]<=mario_y+14 and echelle[0]+10>=mario_x and echelle[1]+26>=mario_y:
            if pyxel.btn(pyxel.KEY_UP):
                sur_echelle = True
                mario_y-= 1
            if pyxel.btn(pyxel.KEY_DOWN) and pyxel.pget(mario_x, mario_y+14) != pyxel.pget(0,242):
                mario_y+= 1
    if sur_echelle and not (echelle[0]<=mario_x+12 and echelle[1]<=mario_y+14 and echelle[0]+10>=mario_x and echelle[1]+26>=mario_y):
        mario_y -= 2*CASE-2
        sur_echelle = False

#Tonneaux
def creation_tonneaux():
    if pyxel.frame_count % 240==0:
        tonneaux.append([38*2, 5*2, choice(direction)])
    return tonneaux
    
def mouvement_tonneaux():
    for i in tonneaux:
        if i[0]== 2:
            i[2]= 2
        if i[0]==244:
            i[2] = -2
    return tonneaux
    
def chute_tonneaux():
    global tonneaux, chute_t
    for i in tonneaux:
        while pyxel.pget(i[0], i[1]+6) != pyxel.pget(0,242):
            chute_t = True
            i[1] += 2
        chute_t = False
    
def arrivee_tonneaux():
    for tonneau in tonneaux:
        if tonneau[1]== 236:
            explosions_creation (tonneau[0], tonneau[1])
            suppression_tonneau(tonneau)
    
def collision_tonneaux():
    global vies
    for tonneau in tonneaux:
        if tonneau[0]<=mario_x+12 and tonneau[1]<=mario_y+14 and tonneau[0]+8>=mario_x and tonneau[1]+8>=mario_y:
            suppression_tonneau(tonneau)
            vies -= 1
            explosions_creation(tonneau[0], tonneau[1])
        if  pyxel.pget(tonneau[0]+9, tonneau[1]+4)==15 or pyxel.pget(tonneau[0]-5, tonneau[1]+4)==15:
            explosions_creation(tonneau[0], tonneau[1])
            suppression_tonneau(tonneau)
    
def suppression_tonneau(i):
    global tonneaux
    tonneaux.remove(i)

#bananaaaas    
def creation_bananes():
    if pyxel.frame_count % randint(350, 500)==0:
        bananes.append([38*2, 5*2, choice(direction)])
    return bananes
    
def mouvement_bananes():
    for i in bananes:
        if i[0]== 2:
            i[2]= 2
        if i[0]==244:
            i[2] = -2
    return bananes
    
def chute_bananes():
    global bananes, chute_b
    for i in bananes:
        while pyxel.pget(i[0], i[1]+8) != pyxel.pget(0,242):
            chute_b = True
            i[1] += 2
        chute_b = False
    
def arrivee_bananes():
    for banane in bananes:
        if banane[1]== 232:
            suppression_banane(banane)
    
def collision_bananes():
    global star
    for banane in bananes:
        if banane[0]<=mario_x+12 and banane[1]<=mario_y+14 and banane[0]+8>=mario_x and banane[1]+8>=mario_y:
            suppression_banane(banane)
            star += 1
    
def suppression_banane(i):
    global bananes
    bananes.remove(i)
    
def explosions_creation(x, y):
    boom.append([x, y, 0])
    
def explosions_animation():
    for explosion in boom:
        explosion[2] +=1
        if explosion[2] == 12:
            boom.remove(explosion)

def stars():
    global star
    if star>0 and pyxel.btnp(pyxel.KEY_SPACE) and mario_y< 12:
        super_bananas.append([mario_x-10, mario_y+8, -2])
        star -= 1
    elif star>0 and pyxel.btnp(pyxel.KEY_SPACE) and not mario_y== 12:
        echelles.append((mario_x, mario_y-11, CASE-2, ESPACE-10, 6))
        star -= 1
        
def collision_super_banane():
    global gagne
    for banana in super_bananas:
        if banana[0]<=x_dk+28 and banana[1]<=y_dk+24 and banana[0]+8>=x_dk and banana[1]+8>=y_dk:
            gagne = True

def suppression_super_banane():
    global super_bananas
    for i in super_bananas:
        if i[0]== 2:
            super_bananas.remove(i)
    return super_bananas
    
def changement_costume():
    global costume
    if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_LEFT):
        costume = (costume + 1) % 2
        
def changement_bananes():
    global costume_banane
    costume_banane = (costume_banane + 1) % 8
    
        
def draw():
    if vies > 0 and not gagne:
        pyxel.cls(0)
        
        #Création etages
        for etage in range(8):
            for case in range(21):
                #pyxel.rect(case*12, 36*etage-10, CASE, CASE-2, 9)
                pyxel.blt(case*12, 36*etage-10, 0, 48, 0, CASE, CASE-2)
        #Creation trous dans etages
        for i in trous:
            pyxel.rect(i[0], i[1], i[2], i[3], i[4])
            
        #dessin du personnage
        #pyxel.rect(mario_x, mario_y, 12, 14, 8)
        if costume == 0:
            pyxel.blt(mario_x, mario_y, 0, 16, 0, 12, 14, 2)
        elif costume == 1:
            pyxel.blt(mario_x, mario_y, 0, 51, 31, 12, 14, 2)
        elif costume == 3:
            pyxel.blt(mario_x, mario_y, 0, 51, 31, 12, 14, 2)
        
        #creation echelles
        for i in echelles:
            #pyxel.rect(i[0], i[1], i[2], i[3], i[4])
            pyxel.blt(i[0], i[1], 0, 0, 0, 10, 26, 2)
            
        #tonneaux
        for i in tonneaux:
            pyxel.circ(i[0], i[1], 4, 15)
        
        #banananaas
        for i in bananes:
            if costume_banane== 0 or costume_banane== 1:
                pyxel.blt(i[0], i[1], 0, 32, 0, 8, 8, 2)
            if costume_banane== 2 or costume_banane== 3:
                pyxel.blt(i[0], i[1], 0, 40, 0, 8, 8, 2)
            if costume_banane== 4 or costume_banane== 5:
                pyxel.blt(i[0], i[1], 0, 32, 8, 8, 8, 2)
            if costume_banane== 6 or costume_banane== 7:
                pyxel.blt(i[0], i[1], 0, 40, 8, 8, 8, 2)
            
        for i in super_bananas:
            pyxel.blt(i[0], i[1], 0, 32, 0, 8, 8, 2)
        
        #vies
        pyxel.text(200, 8, f"VIES : {vies}", 7)
        
        #Explosions
        for explosion in boom:
            pyxel.circ(explosion[0]+4, explosion[1]+4, 2*(explosion[2]//4), 8+explosion[2]%3)  
        
        #pOUVOIR
        pyxel.text(170, 8, f"STAR : {star}", 7)
        
        #peach
        #pyxel.rect(X_PEACH, Y_PEACH, 10, 18, 14)
        pyxel.blt(X_PEACH, Y_PEACH, 0, 0, 30, 10, 18, 7)
        
        #donkey kong
        #pyxel.rect(60, 2, 28, 24, 10)
        pyxel.blt(x_dk, y_dk, 0, 19, 20, 28, 24, 13)
    
    elif gagne == True :
        pyxel.cls(6)
            #afficher mario et peach en gros qui s'en vont
        
    else:
        pyxel.cls(0)
        pyxel.text(118, 124, "GAME OVER", 7)
        #afficher mario qui tombe et donkey kong qui part avec peach
        
def update():
    global mario_x, mario_y, tonneaux, echelles, bananes
    if not sur_echelle:
        if pyxel.frame_count % FRAME_REFRESH == 0:
            chute()
        mario_x = mario_deplacement(mario_x)
        """mario_y = mario_sauter(mario_y)"""
        changement_costume()
    monter(mario_x)
    
    tonneaux = creation_tonneaux()
    tonneaux = mouvement_tonneaux()
    chute_tonneaux()
    
    bananes = creation_bananes()
    bananes = mouvement_bananes()
    chute_bananes()
    if not chute_t:
        for i in tonneaux:
            i[0]+= i[2]
            
    if not chute_b:
        for i in bananes:
            i[0]+= i[2]
        
    changement_bananes()
    collision_tonneaux()
    arrivee_tonneaux()
    collision_super_banane()
    
    collision_bananes()
    arrivee_bananes()
    
    explosions_animation()  
    stars()
    super_bananas = suppression_super_banane()
    for i in super_bananas:
            i[0]+= i[2]
    
    if pyxel.btn(pyxel.KEY_ESCAPE):
        quit()


trous = creation_trous_etages()
echelles = creation_echelles()
pyxel.run(update, draw)