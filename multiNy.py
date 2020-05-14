


#Déclaration des variables et fonctions symboliques------------------------------------------------------------
x,y,lam,mu=symbols('x,y,lam,mu')

lam=E*nu/(1+nu)/(1-2*nu)
mu=E/2/(1+nu)

h=H/NN/2
l=L/N/2


#Les fonctions------------------------------------------------------------

g1=(1+x)*(1+y)/4
g2=(1+x)*(1-y)/4
g3=(1-x)*(1+y)/4
g4=(1-x)*(1-y)/4

def gg(ux,uy,vx,vy):
	return integrate(lam*(diff(ux,x)+diff(uy,y))*(diff(vx,x)\
		+diff(vy,y))+mu*(diff(ux,x)*diff(vx,x)+diff(ux,x)*diff(vx,x)\
		+diff(uy,x)*diff(vx,y)+diff(ux,y)*diff(vx,y)+diff(ux,y)*diff(vy,x)\
		+diff(uy,x)*diff(vy,x)+diff(uy,y)*diff(vy,y)+diff(uy,y)*diff(vy,y))\
		,(x,-1,1),(y,-1,1))


def nl(n):
	return floor((n-1)/N)+1

def AfficherDeplacements():
	#Faire le tracé du champ de déplacements
	plt.quiver(X,Y,ux,uy)
	plt.title('déplacements au sein de la poutre')
	plt.show()

def AfficherContour():
	plt.plot(xx,yy)
	plt.plot(xx+exag*uxx,yy+exag*uyy)
	plt.gca().set_aspect('equal', adjustable='box')
	plt.title('Déformation de la poutre exagérée par un facteur :'+ str(exag) )
	plt.show()


#Le code------------------------------------------------------------

#On forme une base de 8 fonctions qui ont des coordonnées en x et y.
listeX=[]
listeX.append(g1)
listeX.append(g2)
listeX.append(g3)
listeX.append(g4)
listeX.append(Integer(0))
listeX.append(Integer(0))
listeX.append(Integer(0))
listeX.append(Integer(0))


listeY=[]
listeY.append(Integer(0))
listeY.append(Integer(0))
listeY.append(Integer(0))
listeY.append(Integer(0))
listeY.append(g1)
listeY.append(g2)
listeY.append(g3)
listeY.append(g4)

#A est la matrice qui représente la partie bilinéaire de la formulation faible
A=zeros(8,8)
for m in range(1,9):
	for n in range(1,9):
		A[m-1,n-1]=gg(listeX[m-1],listeY[m-1],listeX[n-1],listeY[n-1])

#print(A)
#On convertit la matrice de valeurs symboliques vers float
A=np.array(A).astype(np.float64)


#On a (N+1)*(NN+1) points il faut donc une matrice globale de 2*(N+1)*(NN+1) lignes, idem pour b
K=np.zeros((2*(N+1)*(NN+1),2*(N+1)*(NN+1)))


#On créée une matrice locale vers globale
l2c=np.zeros((N*NN,8))
#Pour cela on balaye les éléments et on associe les valeurs
#Pour chaque élément on balaye les coins pour x et y
for n in range(1,N*NN+1):
	l2c[n-1,1-1]=n+nl(n)
	l2c[n-1,2-1]=n+N+nl(n+N)
	l2c[n-1,3-1]=n+nl(n)-1
	l2c[n-1,4-1]=n+N+nl(n+N)-1
#on numérote ensuite les coins y des éléments
	l2c[n-1,5-1]=n+nl(n)+(N+1)*(NN+1)
	l2c[n-1,6-1]=n+N+nl(n+N)+(N+1)*(NN+1)
	l2c[n-1,7-1]=n+nl(n)-1+(N+1)*(NN+1)
	l2c[n-1,8-1]=n+N+nl(n+N)-1+(N+1)*(NN+1)


#On remplit la matrice en balayant les éléments et en réarrangeant les termes de la matrice A à chaque noeud
#Il faut aussi prendre en compte le fait que les intégrales sont calculés sur des éléments finis de largeur et hauteur 2, après changement de variable il faut multiplier par les termes h et l.
for n in range(1,N*NN+1):
	for i in range(1,9):
		for j in range(1,9):
			K[int(l2c[n-1,i-1]-1),\
			int(l2c[n-1,j-1]-1)]+=h*l*A[i-1,j-1]



#Le vecteur b représente le terme source de la forme faible
b=np.zeros(2*(N+1)*(NN+1))

#On ajoute le terme source aux bords droits en y
# for i in range(1,NN+2):
# 	b[(N+1)*(NN+1)+(N+1)*i-1]=-8e4*N/2

#On ajoute une force verticale de 4e4*horizontal Newton vers le bas au coin supérieur droit.
b[(N+1)*(NN+1)+N+1-1]=-4e4*L

#On veut maintenant imposer des conditions de dirichlet au côté gauche
#Comme les conditions imposée au bord sont nulles il n'y a pas besoin de retrancher les termes dans les autres lignes
#Supprimer les valeurs des lignes correspondants aux points gauches

for i in range(1,NN+2):
	#pour x
	K[1+(i-1)*(N+1)-1,:]=np.zeros(2*(N+1)*(NN+1))
	K[1+(i-1)*(N+1)-1,1+(i-1)*(N+1)-1]=1
	#pour y
	K[(N+1)*(NN+1)+1+(i-1)*(N+1)-1,:]=np.zeros(2*(N+1)*(NN+1))
	K[(N+1)*(NN+1)+1+(i-1)*(N+1)-1,(N+1)*(NN+1)+1+(i-1)*(N+1)-1]=1



# Il faut maintenant résoudre le système d'équations A.u=b pour obtenir le résultat
u=solve(K,b)

#Préparer les données pour les tracés
ux=np.reshape(u[0:(N+1)*(NN+1)],(NN+1,N+1))
uy=np.reshape(u[(N+1)*(NN+1):],(NN+1,N+1))
X,Y=np.meshgrid(np.linspace(0,L,N+1),np.linspace(H/2,-H/2,NN+1))

#Préparer les données pour faire le tracé de l'ancien et du nouveau profil
xx=np.empty(0)
yy=np.empty(0)
uxx=np.empty(0)
uyy=np.empty(0)

for i in range(0,N+1):
	xx=np.append(xx,X[0,i])
	yy=np.append(yy,Y[0,i])
	uxx=np.append(uxx,ux[0,i])
	uyy=np.append(uyy,uy[0,i])

for i in range(0,NN+1):
	xx=np.append(xx,X[i,N])
	yy=np.append(yy,Y[i,N])
	uxx=np.append(uxx,ux[i,N])
	uyy=np.append(uyy,uy[i,N])

for i in range(N,-1,-1):
	xx=np.append(xx,X[NN,i])
	yy=np.append(yy,Y[NN,i])
	uxx=np.append(uxx,ux[NN,i])
	uyy=np.append(uyy,uy[NN,i])

for i in range(NN,-1,-1):
	xx=np.append(xx,X[i,0])
	yy=np.append(yy,Y[i,0])
	uxx=np.append(uxx,ux[i,0])
	uyy=np.append(uyy,uy[i,0])





