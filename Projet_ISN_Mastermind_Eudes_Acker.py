## BIBLIOTHEQUES

from random import *
from time import *
from copy import *
from math import *
from tkinter import *
from tkinter.messagebox import *


## FONCTIONS COMMUNES AUX DEUX ALGORITHMES

def toutes_les_combinaisons_possibles(liste_jetons,nbre_trous):# on crée une liste de tous les combinaisons possibles pour un nombre de couleurs et de trous 
    liste_copie=deepcopy(liste_jetons) # on copie en dur
    for i in range(len(liste_copie)): # on parcourt la liste des couleurs
        liste_copie[i]=str(liste_copie[i])
        # on transforme en caractère pour pouvoir concatener
    L_=deepcopy(liste_copie) # on copie la liste 
    while len(L_[0])<nbre_trous:
    # tant que les éléments n'ont pas la longueur voulue
        L_2=[]
        for base in L_: # on prend un element de L_
            for elt in liste_copie:
                L_2.append(base+elt)
                # on lui ajoute un elt de la liste des pions
                
        L_=list(L_2) # on transfère L_2 dans L_
        
    for k in range(len(L_)):
        L=[]
        for i in range(len(L_[k])):
            L.append(int(L_[k][i])) # on retransforme chaque élément en entier
        L_[k]=list(L)
        
    return L_

def BP(prop,code): # calcule le nombre de pions bien placés
    bien_place=0         # on initialise à 0
    for i in range(len(code)):
        if code[i]==prop[i]: # on regarde 'pion' à 'pion'
            bien_place+=1 # on incrémente le nombre de 'bons pions' si ils sont identiques
            prop[i]='p_ut' # on remplace les nombres pour ne pas les compter deux fois.
            code[i]='c_ut'
            
    return (bien_place)
   
def MP(prop,code): # calcule le nombre de pions mal placés
    mal_place=0         # on initialise à 0
    for i in range(len(prop)):
        for j in range(len(code)): # on explore les deux listes à la recherche de pions identiques
            if prop[i]==code[j]: 
                mal_place+=1
                prop[i]='p_ut' # idem
                code[j]='c_ut'                
    return (mal_place)

def score(prop,code):
    prop_1=deepcopy(prop) # on utilise des copies en dur pour ne pas dénaturer les listes de départ
    code_1=deepcopy(code)    

    return [BP(prop_1,code_1),MP(prop_1,code_1)] # on renvoie le score sous la forme [1,0]
    
def maxi(liste): # donne le maximum d'une liste
    M=liste[0]
    for elt in liste: 
        if elt>=M:
            M=elt
    return M
    

def choix_min(liste):  # permet de trouver le critère mini et le premier élément de la liste qui à ce poids (dans le cas de Knuth, le critère est le poids max, dans Irving, la taille espérée)
    mini=liste[0][1] # on choisit comme minimum arbitraire le critère de la première possibilité
    for elt in liste:
        if elt[1]<=mini: # si l'élément rencontré a un poids plus petit ca devient le minimum
            mini=elt[1] # critère minimum de la liste des propositions
                
    test=False # on definit un test faux
    while test==False: # tant que ce test est faux :
        for elt in liste: # on teste le critère de l'élément  
            if elt[1]==mini: # premier élément qui a le critère minimum
                test=True # on en a un, on arrête de chercher
                return elt[0] # on retourne la combinaison, qui va servir de proprosition

def choix_max(liste):
    max=liste[0][1] # on choisit comme maximum arbitraire le critère de la premiere possibilite
    for elt in liste:
        if elt[1]>=max:
            max=elt[1] # critère minimum de la liste des propositions
                
    test=False # on definit un test faux
    while test==False: # tant que ce test est faux :
        for elt in liste: # on teste le critère de l'élément  
            if elt[1]==max: # premier élément qui a le critère maximum
                test=True # on en a un, on arrête de chercher
                return elt[0] # on retourne la combinaison, qui va servir de proprosition
    
def new_cand(S_red,PROP,SCORE): # on définit une nouvelle liste de candidats en fonction de la proposition de critère mininmum retenue:
    S_n=[]
    for candidat in S_red:
        if score(candidat,PROP)==SCORE: # on crée une liste contenant toutes les combinaisons qui obtiennent face à la proposition le même score que la proposition face au code
            S_n.append(candidat)    
    return S_n


def depouiller(liste): # depouille une liste de données brutes
    MAXI=maxi(liste)
    L_=[[i,0] for i in range(1,MAXI+1)] # on crée une liste des nombres de scores possibles avec 0 comme effectif
    
    for i in range(len(liste)): # on parcourt la liste 
        for j in range(1,MAXI+1): # on parcourt le nombre de coups
            if liste[i]==j: # si il est rencontré
                L_[j-1][1]+=1 # on incrémente son effectif de 1                
    return (L_)
    
def moyenne(liste): # calcule la somme des éléments d'une liste et sa moyenne 
    total=0 # on initialise à 0
    for elt in liste:  # on parcourt la liste 
        total+=elt # on ajoute chaque élément rencontré
    return total/float(len(liste))  # on divise par le total

def liste_score(S_red):
    scores=[]
    for proposition in S:
        SC=[] # liste des scores possibles
        EF=[] # les effectifs respectifs
        for candidat in S_red: # on teste les éléments  
            score_=score(proposition,candidat) # on calcule le score
            if score_ in SC: # si le score existe deja 
                EF[SC.index(score_)]+=1 # on augmente son effectif de 1            
            else:
                SC.append(score_) # sinon on le crée avec un effectif 1
                EF.append(1)
        scores.append([proposition,EF])
    return scores

## KNUTH

def worst_case(S_red): # fonction d'evaluation de poids de Knuth
    global S
    liste_poids=[]  # on initialise la liste de poids 
    for elt in liste_score(S_red): # on parcourt la liste des propositions et de leurs scores
        liste_poids.append([elt[0],maxi(elt[1])]) # on crée une liste de chaque candidat et du poids (en gardant le maximum)
    return liste_poids

def knuth(): # marche pour toutes les configurations
    S_red=deepcopy(S) # on copie S
    coups=0 # on intialise le nombre de coups à 0
    SCORE=[0,0] # le score à "0"
    while len(S_red)!=1 and SCORE!=[nbr_trous,0]: # tant que l'on a pas le bon résultat
        coups+=1 # on incrémente d'un coup
        liste_poids=worst_case(S_red)# on calcule la liste des propositions et de leur poids 
        PROP=choix_min(liste_poids)  # on choisit la proposition ayant le poids mininmum (la première atteinte en cas d'égalité)
        print (PROP) # on affiche la proposition choisie
        SCORE=score(PROP,code_secret) # on calcule son score
        S_red=new_cand(S_red,PROP,SCORE) # on détermine la nouvelle liste de candidats
    coups+=1
    if len(S_red)==1:
        print (S_red[0])        
    print ('nombre de coups : ',coups)
        
    
def knuth_2(): # pour jouer plus vite en 6 couleurs/4 trous
    K=[] # on crée un liste de coups vide
    for code in S: # on teste sur toutes les combinaisons possibles
        code_secret=code 
        print('code secret : ',code_secret)
        S_red=deepcopy(S) # on crée un S_red "égal" à S
        coups=1 # on initialise le nombre de coups
        PROP=[0,0,1,1] # on force la première proposition
        print (PROP) # on l'affiche 
        SCORE=score(PROP,code_secret) # on calcule son score
        S_red=new_cand(S_red,PROP,SCORE) # on réduit la liste des candidats
        
        while len(S_red)!=1 and SCORE!=[nbr_trous,0]:
            coups+=1 # on incrémente le nombre de coups
            liste_poids=worst_case(S_red) # on calcule la liste des propositions et de leur poids 
            PROP=choix_min(liste_poids) # on choisit la proposition ayant le poids mininmum (la première atteinte en cas d'égalité) 
            print (PROP) # on l'affiche 
            SCORE=score(PROP,code_secret)  # on calcule son score
            S_red=new_cand(S_red,PROP,SCORE) # on détermine la liste réduite des candidats        
        coups+=1
        if len(S_red)==1:
            print (S_red[0])
            
        print ('nombre de coups : ',coups) # on affiche le nombre de coups
        K.append(coups) # on l'ajoute à la liste 
        
    M_K=moyenne(K)  # on calcule la moyenne des coups
    K=depouiller(K) # on dépouille la liste des coups
    return K,M_K # pour créer le fichier de statistiques

##IRVING

def exp_size(S_red):
    global S
    liste_poids=[] # on crée un liste vide 
    for elt in liste_score(S_red):
        poids=0.0 # on initialise le poids à 0
        for effectif in elt[1]: # on parcourt les scores
            poids+=effectif**2 # on ajoute le carré du score
        poids=poids/(nbr_couleurs**nbr_trous) # on divise par le cardinal de S
        liste_poids.append([elt[0],poids]) # on crée une liste de chaque candidat et du poids ainsi calculé
    return liste_poids

    
def irving(): # même fonction que Knuth
    S_red=deepcopy(S)
    coups=0
    SCORE=[0,0]
    while len(S_red)!=1 and SCORE!=[nbr_trous,0]:
        coups+=1
        liste_poids=exp_size(S_red) # on calcule le poids différemment 
        PROP=choix_min(liste_poids)    
        print (PROP)
        SCORE=score(PROP,code_secret)            
        S_red=new_cand(S_red,PROP,SCORE)    
    coups+=1
    if len(S_red)==1:
        print (S_red[0])        
    print ('nombre de coups : ',coups)        
    
def irving_2(): # même fonction que Knuth_2
    I=[]
    for code in S:
        code_secret=code
        print('code secret : ',code_secret)
        S_red=deepcopy(S)
        coups=1
        PROP=[0,0,1,2] # la proposition forcée est différente
        print (PROP)
        SCORE=score(PROP,code_secret)
        S_red=new_cand(S_red,PROP,SCORE)
        
        while len(S_red)!=1 and SCORE!=[nbr_trous,0]:
            coups+=1
            liste_poids=exp_size(S_red) # on calcule le poids
            PROP=choix_min(liste_poids)    
            print (PROP)
            SCORE=score(PROP,code_secret)            
            S_red=new_cand(S_red,PROP,SCORE)
        
        coups+=1
        if len(S_red)==1:
            print (S_red[0])
            
        print ('nombre de coups : ',coups)
        I.append(coups)
        
    M_I=moyenne(I)    
    I=depouiller(I)
    return I,M_I


## jeu joueur

def epeler_nombre(nbr): # permet de transformer l'entrée du joueur en liste d'entiers
    liste=[]
    for digit in nbr:
        liste.append(int(digit)) # on ajoute chaque "lettre" dans la liste, transformée en entier
    return liste
    
def joueur():
    global J
    print ('Les couleurs disponibles sont : ',J)
    coups=1 # on initialise les coups à 1
    gagne=False
    while coups<=12:  # tant qu'il reste des coups à jouer
        print ('coup : ',coups) # on affiche le coup joué
        prop=str(input("choix?  : ")) # on demande le choix du joueur
        #prop='1231' # prop figée pour gagner du temps en debug
        prop=epeler_nombre(prop) # on transforme l'entrée en liste d'entiers
        print (prop) # on affiche le choix du joueur sous forme de liste
        score_joueur=score(code_secret,prop) # on calcule le score du joueur
        print (score_joueur) # on l'affiche
        if score_joueur==[nbr_trous,0]: # si il a la bonne combinaison
            print('GAGNE') # on affiche 'GAGNE'
            gagne=True
            coups=13 # on met coups à 13 pour arreter la boucle
        else: 
            coups+=1 # on avance d'un cran
    if gagne==False:      
        print ('PERDU') # si il n'y a plus d'essai on affiche 'PERDU'
        print ('code secret : ',code_secret) # et on affiche la solution


## QUASI HUMAIN

def eval(SCORE):
    return (SCORE[0]+0.5*SCORE[1])/float(nbr_trous)
    # on évalue un score pour pouvoir comparer deux propositions
    # [0,0] donne donc 0
    # le code secret obtient 1 quel que soit le nombre de trous
    
def consistant(CAND,LISTE,code_secret): # sert à savoir si un candidat est consistant avec les jeux précédents 
    somme=0 
    for PROP in LISTE : # on teste toutes les propositions déja jouées
        SCORE=score(PROP,code_secret) # on calcule leur score face au code
        SCORE_=score(CAND,PROP) # le score du candidat face à la proposition
        d=abs(SCORE[0]-SCORE_[0])+abs(SCORE[1]-SCORE_[1]) # on calcule les distances
        somme+=d # on somme : si la somme est nulle c'est consistant
    return somme
        
        
def cand(PROP,SCORE,couleurs,L,code_secret): 
# fonction qui permet le calcul du nouveau candidat
    E_PROP=eval(SCORE) # on calcule l'évaluation de la proposition qui va permettre de construire le candidat
    if E_PROP!=0.0: # si elle est non nulle
        test=True
        while test==True: # tant que le candidat n'est pas optimal
            CAND=['x' for c in range(nbr_trous)] # un candidat vierge
            places_libres=[a for a in range(nbr_trous)] # places libres dans le candidat
            places_libres_prop=[b for b in range(nbr_trous)] # places libres dans la proposition
            # ETAPE 1
            for i in range(SCORE[0]): # on répète autant de fois que de jetons rouges
                pos=choice(places_libres) # on choisit une place au hasard
                CAND[pos]=PROP[pos] # on garde ce pion
                places_libres.remove(pos) # on l'enlève des places libres
                places_libres_prop.remove(pos)
                
            # ETAPE 2
            for j in range(SCORE[1]): # on répète autant de fois que jetons blancs
                pos_d=choice(places_libres_prop) # on choisit une place au hasard dans la proposition
                pos_a=choice(places_libres) # on choisit une place au hasard dans le candidat
                CAND[pos_a]=PROP[pos_d]  # on positionne le pion
                places_libres_prop.remove(pos_d) # on l'enlève des places libres
                places_libres.remove(pos_a)
            # ETAPE 3
            for k in places_libres: # pour les places libres éventuelles
                CAND[k]=choice(couleurs) # on remplace par une couleur choisie au hasard
            if consistant(CAND,L,code_secret)==0: # si le candidat est consistant face aux propositions précédentes
                test=False # on arrête de chercher
    else: # si la proposition a obtenu un score de [0,0]
        for elt in PROP:
            if elt in couleurs:
                couleurs.remove(elt) # on enlève ces couleurs des couleurs possibles (car elles ne sont pas dans le code secret)
        CAND=[choice(couleurs) for i in range(nbr_trous)] # on crée un candidat au hasard
    return CAND,couleurs
    
        


def quasi_humain():
    couleurs=list(J) # on copie la liste des couleurs
    coups=1 # on initialise le nombre de coups joués
    PROP=choice(S) # on fait une première proposition au hasard
    SCORE=score(PROP,code_secret) # on calcule son score
    L=[PROP] # on l'ajoute à la liste des coups déja joués
    continuer=True # tant qu'on a pas le bon code
    if eval(SCORE)==1.0: 
        continuer=False # si on a le code dès le premier coup on s'arrête
    print (PROP) 
    BEST_PROP=PROP # la "meilleur proposition" est initialisée
    BEST_SCORE=SCORE # le "meilleur score" aussi
        
    while continuer==True:  # tant qu'on a pas trouvé le code 
        coups+=1
        test_1=True
        while test_1==True: # pour être sur de ne pas rejouer une combinaison déja jouée
            PROP=cand(BEST_PROP,BEST_SCORE,couleurs,L,code_secret)[0] # on calcule un nouveau candidat
            couleurs=cand(BEST_PROP,BEST_SCORE,couleurs,L,code_secret)[1] # on met à jour les couleurs dispos
            SCORE=score(PROP,code_secret) # on calcule son score        
            if PROP not in L: # si elle n'est pas dans la liste des combinaisons jouées
                test_1=False # on arrête de chercher
        L.append(PROP) # on ajoute la proposition dans la liste des combinaisons jouées
        print (PROP)
        if eval(SCORE)==1.0: # si son score est le meilleur         
            continuer=False # on arrête de chercher
        if eval(SCORE)==0: # si le score est [0,0]
            for elt in PROP:
                if elt in couleurs:
                    couleurs.remove(elt) # on enleve ces couleurs des couleurs possibles (car elles ne sont pas dans le code_secret)
        if eval(SCORE)>eval(BEST_SCORE): # si le score de la proposition est meilleur que le "meilleur score"
            BEST_PROP=list(PROP) # la proposition devient la "meilleure proposition"
            BEST_SCORE=list(SCORE) # son score le "meilleur score"
    print ('nombre de coups : ',coups)
    return (coups)

def quasi_humain_2():
    HC=[] # on initialise le nombre de coups
    for code in S: # on teste toutes les combinaisons possibles
        couleurs=list(J)
        code_secret=code
        print('code secret : ',code_secret)        
        PROP=choice(S)
        SCORE=score(PROP,code_secret)
        L=[PROP]
        continuer=True
        if eval(SCORE)==1.0:
            continuer=False
        print (PROP)
        BEST_PROP=PROP
        BEST_SCORE=SCORE
        coups=1
        
        while continuer==True:    
            coups+=1
            test_1=True
            while test_1==True:
                PROP=cand(BEST_PROP,BEST_SCORE,couleurs,L,code_secret)[0]
                couleurs=cand(BEST_PROP,BEST_SCORE,couleurs,L,code_secret)[1]
                SCORE=score(PROP,code_secret)
            
                if PROP not in L:
                    test_1=False
            L.append(PROP)
            print (PROP)
            if eval(SCORE)==1.0:            
                continuer=False
            if eval(SCORE)==0:
                for elt in PROP:
                    if elt in couleurs:
                        couleurs.remove(elt)
            if eval(SCORE)>eval(BEST_SCORE):
                BEST_PROP=list(PROP)
                BEST_SCORE=list(SCORE)
        print ('nombre de coups : ',coups)
        HC.append(coups)
    M_HC=moyenne(HC)
    HC=depouiller(HC)
    return HC,M_HC


## SHAPIRO
def shapiro():
    S_red=deepcopy(S) # on copie S
    coups=0 # on intialise le nombre de coups à 0
    SCORE=[0,0] # le score à "0"
    while len(S_red)!=1 and SCORE!=[nbr_trous,0]: # tant que l'on a pas le bon résultat
        coups+=1 # on incrémente d'un coup
        PROP=S_red[0]  # on choisit la proposition ayant le poids mininmum (la première atteinte en cas d'égalité)
        print (PROP) # on affiche la proposition choisie
        SCORE=score(PROP,code_secret) # on calcule son score
        S_red=new_cand(S_red,PROP,SCORE) # on détermine la nouvelle liste de candidats
    coups+=1
    if len(S_red)==1:
        print (S_red[0])        
    print (coups)

def shapiro_2():
    Sh=[] # on crée un liste de coups vide
    for code in S: # on teste sur toutes les combinaisons possibles
        code_secret=code 
        print('code secret',code_secret)
        S_red=deepcopy(S) # on crée un S_red "égal" à S
        coups=1 # on initialise le nombre de coups
        PROP=S_red[0] # on force la première proposition
        print (PROP) # on l'affiche 
        SCORE=score(PROP,code_secret) # on calcule son score
        S_red=new_cand(S_red,PROP,SCORE) # on réduit la liste des candidats
        
        while len(S_red)!=1 and SCORE!=[nbr_trous,0]:
            coups+=1 # on incrémente le nombre de coups
            PROP=S_red[0] # on choisit la proposition ayant le poids mininmum (la première atteinte en cas d'égalité) 
            print (PROP) # on l'affiche 
            SCORE=score(PROP,code_secret)  # on calcule son score
            S_red=new_cand(S_red,PROP,SCORE) # on détermine la liste réduite des candidats        
        coups+=1
        if len(S_red)==1:
            print (S_red[0])
            
            print ('nombre de coups : ',coups) # on affiche le nombre de coups
        Sh.append(coups) # on l'ajoute à la liste 
        
    M_Sh=moyenne(Sh)  # on calcule la moyenne des coups
    Sh=depouiller(Sh) # on dépouille la liste des coups
    return Sh,M_Sh # pour créer le fichier de statistiques
    

## ENTROPIE
def poids(S_red):   # on  calcule les scores possibles d'une possibilite de S par 
                    # rapport aux candidats potentiels et on renvoie l'entropie 
                    #de chaque candidat
    liste=[]
    entropie_m=0.0
    E_=0
    for elt_ in S_red:
        Sc=[] # liste des scores possibles
        Ef=[] # les effectifs respectifs
        for elt in S_red: # on teste les elements  
            score_=score(elt,elt_) #on calcule le score
            if score_ in Sc: #si le score existe deja 
                Ef[Sc.index(score_)]+=1 #on augmente son effectif de 1            
            else:
                Sc.append(score_) #sinon on le crée avec un effectif 0
                Ef.append(1)
        E_=0
        for elt__ in Sc:
            p_i=(float(Ef[Sc.index(elt__)])/float(nbr_couleurs**nbr_trous))
            if p_i: 
                E_+=((p_i)*log2(p_i)) # on calcule l'entropie en bit/Shannon
        entropie_m=-(E_) # on inverse l'accumulateur pour trouver la valeur positive
        liste.append([elt_,entropie_m]) # on rajoute la proposition et son 
                                        # entropie à la liste 
    return liste



def entropie():
    S_red=deepcopy(S) # on copie S
    coups=0 # on intialise le nombre de coups à 0
    SCORE=[0,0] # le score à "0"
    while len(S_red)!=1 and SCORE!=[nbr_trous,0]: # tant que l'on a pas le bon résultat
        coups+=1 # on incrémente d'un coup
        PROP=choix_max(poids(S_red))  # on choisit la proposition ayant l'entropie maximum (la première atteinte en cas d'égalité)
        print (PROP) # on affiche la proposition choisie
        SCORE=score(PROP,code_secret) # on calcule son score
        S_red=new_cand(S_red,PROP,SCORE) # on détermine la nouvelle liste de candidats
    coups+=1
    if len(S_red)==1:
        print (S_red[0])        
        print ('nombre de coups : ',coups)
    
    
def entropie_2():    
    E=[]
    for code in S: # on teste sur toutes les combinaisons possibles
        code_secret=code 
        print('code secret :',code_secret)
        S_red=deepcopy(S) # on crée un S_red "égal" à S
        coups=1 # on initialise le nombre de coups
        PROP=[0,1,2,3] # on force la première proposition
        print (PROP) # on l'affiche 
        SCORE=score(PROP,code_secret) # on calcule son score
        S_red=new_cand(S_red,PROP,SCORE) # on réduit la liste des candidats
        
        while len(S_red)!=1 and SCORE!=[nbr_trous,0]:
            coups+=1 # on incrémente le nombre de coups
            PROP=choix_max(poids(S_red)) # on choisit la proposition ayant l'entropie maximum (la première atteinte en cas d'égalité) 
            print (PROP) # on l'affiche 
            SCORE=score(PROP,code_secret)  # on calcule son score
            S_red=new_cand(S_red,PROP,SCORE) # on détermine la liste réduite des candidats        
        coups+=1
        if len(S_red)==1:
            print (S_red[0])
            
            print ('nombre de coups : ',coups) # on affiche le nombre de coups
        E.append(coups) # on l'ajoute à la liste 
        
    M_E=moyenne(E)  # on calcule la moyenne des coups
    E=depouiller(E) # on dépouille la liste des coups
    return E,M_E # pour créer le fichier de statistiques




## JEU GRAPHIQUE

def grille(nbr_couleurs,nbr_trous): # plateau de jeu
    for i in range(12):  # les 12 lignes
        for j in range(nbr_trous):
            canevas.create_oval(100+j*100-15,20+i*40-15,100+j*100+15,20+i*40+15,fill='grey') # places pions de jeu 
            canevas.create_oval(600+j*50-5,20+i*40-5,600+j*50+5,20+i*40+5,fill='grey') # places jetons score

    for i in range(nbr_couleurs): # pions de couleurs cliquables 
        canevas.create_oval(100*(i+1)-20,550-20,100*(i+1)+20,550+20,fill=Couleurs[i]) 
        
        
def placement(x,y,tours,coups,liste): # place un pion de la couleur séléctionnée au bon endroit
    for i in range(nbr_couleurs):
        if 100*(i+1)-20<x<100*(i+1)+20 and 550-20<y<550+20: # choix de la couelur
            canevas.create_oval(100+coups*100-15,500-tours*40-15,100+coups*100+15,500-tours*40+15,fill=Couleurs[i]) # place le pion
            liste.append(couleurs[i]) # on ajoute la couleur jouée à la liste de jeu 
            return 1 # si c'est une couleur qui a été cliquée, c'est un 'bon clic'
                
def jeton(SCORE,tours): # pour placer les jetons en fonction du score
    for i in range(SCORE[0]):
        canevas.create_oval(600+i*50-10,500-tours*40-10,600+i*50+10,500-tours*40+10,fill='red') # les rouges

    for j in range(SCORE[0],SCORE[0]+SCORE[1]):
        canevas.create_oval(600+j*50-10,500-tours*40-10,600+j*50+10,500-tours*40+10,fill='white') # les blancs
 
 
def verif(nbr_trous,code_secret):
    global tours,coups,liste
    if coups==nbr_trous: # si le nombre de coups joués dans le tour est égal au nombre de trous
        Sc=score(liste,code_secret) # on calcule le score
        jeton(Sc,tours) # on place les jetons rouges/blancs
        if Sc==[nbr_trous,0]: # si le score est le maximum possible
            showinfo('RESULTAT','GAGNE') # on ouvre une fenêtre GAGNE
        else:    
            tours+=1 # sinon on avance d'un tour
            coups=0 # on remet les coups à 0
            liste=[] # et la liste de coups joués aussi
    if tours==13:
        showinfo('RESULTAT','PERDU') # si on a épuisé le nombre de tours 
        perdu(code_secret,nbr_trous) # on affiche une fenetre PERDU et une fenetre contenant le code secret
        
def perdu(code_secret,nbr_trous): # pour afficher le code secret
    fenetre_2=Tk() 
    fenetre_2.title('CODE SECRET') # nomme la fenetre

    canevas_2=Canvas(fenetre_2, width=(nbr_trous)*50,height=40,bg='white') # on cree un canevas
    canevas_2.pack(padx=10,pady=10) # on place le canevas dans la fenetre (marges)

    for i in range(nbr_trous):
        canevas_2.create_oval(20+i*50-15,5,20+i*50+15,35,fill=Couleurs[code_secret[i]]) # place les pions
    fenetre_2.mainloop()

        
def clic(evenement):# on clique sur les couleurs
    global choix,nbr_couleurs,nbr_trous,tours,coups,liste
    X=evenement.x # position horizontale du clic
    Y=evenement.y # position verticale du clic
    # la suite permet de ne compter un coup joué que si l'on clique sur une couleur
    bon_clic=placement(X,Y,tours,coups,liste) # on place (eventuellement) le pion
    if bon_clic==1: # si on a bien cliqué sur une couleur 
        coups+=1 # on avance d'un coup
    verif(nbr_trous,code_secret) # on verifie l'etat du jeu 

## PROGRAMME PRINCIPAL

print ('1 : mode automatique en 6 couleurs/ 4 trous')
print ('2 : mode semi-automatique qui permet choisir sa configuration de jeu')
print ('3 : mode automatique qui execute tous les algorithmes automatiques et génère un fichier de statistiques')
choix_mode=int(input('? : '))


if choix_mode==1:
    nbr_couleurs=6 #choix du nombre de couleurs figé pour essais sur 6/4
    nbr_trous=4 # choix du nombre de trous figé pour essais  sur 6/4
    J=[i for i in range(nbr_couleurs)] #liste des jetons en fonction du nombre de couleurs
    S=toutes_les_combinaisons_possibles(J,nbr_trous) #on etablit la liste des combinaisons possibles en fonction du nbr de couleur et du nbr de trous 
        
    print ('QUEL ALGORITHME : ')
    print ('1 : KNUTH')
    print ('2 : IRVING')
    print ('3 : QUASI-HUMAIN')    
    print ('4 : SHAPIRO')
    print ('5 : ENTROPY')
    choix_algo=int(input('Choix ? : '))
    if choix_algo==1:
        k=knuth_2()
        print (k[1])
    elif choix_algo==2:   
        i=irving_2()
        print(i[1])        
    elif choix_algo==3:
        q=quasi_humain_2()
        print(q[1])        
    elif choix_algo==4:
        s=shapiro_2()
        print(s[1])
    elif choix_algo==5:
        e=entropie_2()    
        print(e[1])       
    else:
        print('Au revoir!')
        
elif choix_mode==2:
    continu=True
    while continu==True: 
        nbr_couleurs=int(input('Nombre de jetons différents ? : ')) # demande le nombre de pions
        nbr_trous=int(input('Nombre de trous ? : ')) # demande le nombre de trous
        J=[i for i in range(nbr_couleurs)] # liste des pions en fonction du nombre de couleurs
        S=toutes_les_combinaisons_possibles(J,nbr_trous) # on etablit la liste des combinaisons possibles en fonction du nbr de couleur et du nbr de trous 
        code_secret=[choice(J) for i in range(nbr_trous)]     # choix du code secret par l'ordi
        print ('QUEL ALGORITHME : ')
        print ('0 : JOUEUR HUMAIN CONSOLE')    
        print ('1 : KNUTH')
        print ('2 : IRVING')
        print ('3 : QUASI-HUMAIN')        
        print ('4 : SHAPIRO')
        print ('5 : ENTROPY')
        print ('6 : JEU HUMAIN GRAPHIQUE (8x5 maxi)')
        choix_algo=int(input('Choix ? : '))
        
        if choix_algo !=0 and choix_algo!=6:
            print('code secret : ',code_secret) # si le jeu est automatique on affiche le code
        if choix_algo==0:
            joueur()
        if choix_algo==1:
            knuth()
        elif choix_algo==2:   
            irving()
        elif choix_algo==3:
            quasi_humain()
        elif choix_algo==4:
            shapiro()
        elif choix_algo==5:
            entropie()                
        elif choix_algo==6 and nbr_couleurs<=8 and nbr_trous<=5: 
                fenetre=Tk() # on ouvre une fenêtre
                fenetre.title('FENETRE DE JEU') # on nomme la fenêtre                                        
                largeur = 900
                hauteur = 600            
                tours=1 # on initialise le nombre de tours 
                coups=0 # le nombre de coups
                liste=[] # la liste des coups joués
                couleurs=deepcopy(J) # on copie les couleurs 
                Couleurs=['red','green','blue','cyan','yellow','magenta','black','white'] # on crée une liste de couleurs compréhensible par Tkinter
                canevas=Canvas(fenetre, width=largeur,height=hauteur,bg='white') # on crée un canevas
                canevas.pack(padx=10,pady=10) # on place le canevas dans la fenetre (marges)
                grille(nbr_couleurs,nbr_trous) # on place la grille                 
                canevas.bind('<Button-1>',clic) # gestion du clic
                fenetre.mainloop() # boucle principale
        else:
            print('Au revoir!')
        choix_continu=input('Continuez ? (o/n): ')
        if choix_continu=='o':  # pour rejouer
            continu==True
        else:
            continu=False
            print ('au revoir')


elif choix_mode==3:    
    nbr_couleurs=6 # choix du nombre de couleurs figé
    nbr_trous=4 # choix du nombre de trous figé
    J=[i for i in range(nbr_couleurs)] # liste des jetons en fonction du nombre de couleurs
    S=toutes_les_combinaisons_possibles(J,nbr_trous) # on établit la liste des combinaisons possibles en fonction du nbr de couleur et du nbr de trous 
    #S=[[1,2,3,4],[5,2,0,1],[3,2,2,1],[0,0,1,1]] # pour tester sur un petit nombre de combinaisons
    f = open('statistiques.txt','w') # on ouvre un fichier txt qui va contenir les statistiques
    k=knuth_2() # renvoie la liste dépouillée du nombre de coups k[0] et la moyenne k[1]
    f.write('Knuth : '+'\n')   
    f.write(str(k[0])+'\n') # on écrit la liste dépouillée dans le fichier 
    f.write(str(k[1])+'\n') # la moyenne 
    i=irving_2()
    f.write('Irving : '+'\n')        
    f.write(str(i[0])+'\n') 
    f.write(str(i[1])+'\n')       
    q=quasi_humain_2()
    f.write('Quasi-humain : '+'\n')        
    f.write(str(q[0])+'\n') 
    f.write(str(q[1])+'\n')       
    s=shapiro_2()
    f.write('Shapiro : '+'\n')        
    f.write(str(s[0])+'\n') 
    f.write(str(s[1])+'\n')       
    e=entropie_2()
    f.write('Entropie : '+'\n')            
    f.write(str(e[0])+'\n') 
    f.write(str(e[1])+'\n')       
    f.close()

    
input() # pour garder la fenêtre ouverte
