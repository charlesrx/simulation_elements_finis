from sympy import *
init_printing(use_unicode=True, wrap_line=False)

x,y=symbols('x,y')


#Données du problème ------------------------------------------
#La force P est en N :
N=10
P=8e4*N

#La longueur de la poutre est 20
L=20

#Le module d'Young :
E=1.18e11
#--------------------------------------------------------------


#Le moment quadratique I de la section S par rapport
# à l'axe Ox de la poutre est :
#I=integrate(y**2,(x,0,L),(y,-1,1))
I=10


#L'équation de la déformée est 
expr=-(3*L-x)*P*x**2/(6*E*I)

#Ce qui nous permet de calculer la déflection
de=lambdify([x],expr)

#plot(expr,(x,0,20))

#Comparaison avec la simulation numérique-------------------------
exec(open('./multiNy.py').read())
xm=np.linspace(0,20,100)

plt.plot(xm,fff(xm,np.zeros(len(xm))))
plt.plot(xm,de(xm))
plt.title('Comparaison entre la solution numérique et la déformée')
plt.show()




