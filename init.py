#init

#Les packages------------------------------------------------------------
from sympy import *
init_printing(use_unicode=True)
import numpy as np
from numpy.linalg import solve
import matplotlib.pyplot as plt

#Renseigner les valeurs propres au matériau-------------------------------------------------
E=1.18e11
nu=0.31

#Paramètres de simulation-------------------------------------------------
#Nombre d'éléments horizontaux pour le calcul
N=16
#Nombre d'éléments verticaux pour le calcul
NN=6

#Longueurs horizontale et verticale de la poutre
horizontale=10
verticale=3

#Facteur d'exagération de la déformation pour le tracé final
exag=500

#--------------------------------------------------------------------------------------------------

#Faire les calculs avec ces paramètres - remarque la force appliquée à la poutre
#est définie dans ce code via le vecteur b
exec(open('./multiNy.py').read())

#Afficher les vecteurs déplacement
AfficherDeplacements()

#Afficher le déplacement du contour
AfficherContour()




