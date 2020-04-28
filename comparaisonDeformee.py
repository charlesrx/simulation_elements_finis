x,y=symbols('x,y')


#Données du problème ------------------------------------------
#La force P est en N :
P=8e4*N

#La longueur de la poutre est 20
L=2*N
#--------------------------------------------------------------


#Le moment quadratique I :
I=13.333

#L'équation de la déformée est 
expr=-(3*L-x)*P*x**2/(6*E*I)

#Ce qui nous permet de calculer la déflection
de=lambdify([x],expr)

#plot(expr,(x,0,20))

#Comparaison avec la simulation numérique-------------------------
#exec(open('./multiNy.py').read())
xm=np.linspace(0,2*N,N+1)

if int(NN/2)==NN/2:
	ligne1=NN/2+1
	ligne2=NN/2+1
else:
	ligne1=int(NN/2)
	ligne2=int(NN/2)+1


plt.plot(xm,0.5*uy[int(ligne1),:]+0.5*uy[int(ligne2),:])
plt.plot(xm,de(xm))
plt.title('Comparaison entre la solution numérique et la déformée')
plt.show()






