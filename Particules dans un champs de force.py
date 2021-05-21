"""
groupe:Baltimor
       Peltier
       Delaforge
       Peltier
"""
#Les bibliotheques importees
import numpy as np
from math import atan,cos,sin
import PIL.Image as pili
import matplotlib.pyplot as plt


#fonction:"passer de coordonnee matricielle à coordonnee planaire

def convertisseur_matrice(Matrice,position):
    n=len(Matrice)
    #on definit le centre du plan
    O=[(n//2),(n//2)]
    
    #coordonnee sur l'axe des absisses
    x=0
    if position[1]>O[0]:
        while position[1]!=O[0]:
            position[1]=position[1]-1
            x=x+1
            
    elif position[1]<O[0]:
        while position[1]!=O[0]:
            position[1]=position[1]+1
            x=x+1
        x=x*(-1)
        
    #coordonnee sur l'axe des ordonnees       
    y=0
    if position[0]>O[1]:
        while position[0]!=O[1]:
            position[0]=position[0]-1
            y=y+1
            
    elif position[0]<O[1]:
        while position[0]!=O[1]:
            position[0]=position[0]+1
            y=y+1
           
        y=y*(-1)    
        
    return(x,y)

#Definition du champs de force

def matrice_des_champs(C,n):
    M=np.zeros((n+1,n+1,2))
    for i in range(0,n//2):
        for j in range(0,n//2):
            x,y=convertisseur_matrice(M,[i,j])#le champs dans les 4 cadrants
            R=(x**2+y**2)**0.5
            alpha=atan(y/x)
            
            M[i][j][0]=(C/(R**2))*cos(alpha)
            M[i][j][1]=(C/(R**2))*sin(alpha)
            
            M[n-i][j][0]=M[i][j][0]
            M[n-i][j][1]=-M[i][j][1]
            
            M[i][n-j][0]=-M[i][j][0]
            M[i][n-j][1]=-M[i][j][1]
            
            M[n-i][n-j][0]=-M[i][j][0]
            M[n-i][n-j][1]=-M[i][j][1]
    
    for j in range(n//2):#le champs sur les axes du plan
        x,y=convertisseur_matrice(M,[i,0])
        
        M[n//2][j][0]=C/x
        M[n//2][n-j][0]=-C/x
         
    for i in range(50):
        x,y=convertisseur_matrice(M,[0,j])
        
        M[i][n//2][1]=C/x
        M[n-i][n//2][1]=-C/x
    return(M)

#Coordonnees des position et vitesse

def vitesse(ax,ay,dt,Vo):#on integre
    Vx=ax*dt+Vo[0]
    Vy=ay*dt+Vo[1]
    V=[Vx,Vy]
    return(V)
    
def position(vx,vy,dt,Po):
    Px=int(vx*dt+Po[0])
    Py=int(vy*dt+Po[1])
    P=[Px,Py]
    return(P)

#liste de temps avec un pas de P qui vaut dt
#NB: Pour l'application numerique dt=1

def liste_temps(duree,dt):
    T=[]
    while duree>0:
        T.append(duree)
        duree=duree-dt  
    T.append(0)
    return(T[-1::-1])

#on reuni l'ensemble des programmes pour creer la liste de position

def modele(C,n,X,Y,Vx,Vy,duree,dt):
    L=[[X,Y]] #liste de position 
    Vitesse=[[Vx,Vy]]
    M=matrice_des_champs(C,n)
    T=liste_temps(duree,dt)
    
    P=[X,Y]
    V=[Vx,Vy]
    A=[M[X][Y][0],M[X][Y][1]]
    
    for i in range(len(T)):
        if -n<=P[0]<=n and -n<=P[1]<=n:#si la particule sort du plan le programme s'arrete
            
            A=[M[P[0]][P[1]][0],M[P[0]][P[1]][1]]
         
            V=vitesse(A[0],A[1],dt,V)
         
            P=position(V[0],V[1],dt,P)
        
            L.append(P)
            Vitesse.append(V)
        else:
            return L
    return L

#Afficher les resultats
"""dans un plan"""

def plan(C,n,x,y,Vx,Vy,duree,dt):
    P=modele(C,n,x,y,Vx,Vy,duree,dt)

    X=[]
    Y=[]
    for i in range(len(P)):
        X.append(P[i][0])
        Y.append(P[i][1])
        
    X=np.array(X)
    Y=np.array(Y)
  
    plt.plot(X,Y)
    plt.show()

"""dans une image"""

def image(C,n,x,y,Vx,Vy,duree,dt):#Point blanc sur un fond noir
    P=modele(C,n,x,y,Vx,Vy,duree,dt)
    M=np.zeros((n+1,n+1,3),dtype='uint8')
    M[n//2][n//2]=[255,255,0]#Point jaune au centre
    
    for i in range(len(P)):
        if -n<=P[i][0]<=n and -n<=P[i][1]<=n:#si il y a un point hors de l'image il n'est pas pris en compte
             M[P[i][0]][P[i][1]]=255
        else:
             I=pili.fromarray(M)
             return I.show()
         
    
    I=pili.fromarray(M)
    
    return I.show()


"""FIN DU PROGRAMME"""



