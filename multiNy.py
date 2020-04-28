#Les packages------------------------------------------------------------
from sympy import *
init_printing(use_unicode=True)
import numpy as np
from numpy.linalg import solve
import matplotlib.pyplot as plt
import xlsxwriter


#Déclaration des variables et fonctions symboliques------------------------------------------------------------
x,y,lam,mu=symbols('x,y,lam,mu')
E=1.18e11
nu=0.31
lam=E*nu/(1+nu)/(1-2*nu)
mu=E/2/(1+nu)
#Nombre d'éléments horizontaux
N=10
#Nombre d'éléments verticaux
NN=6
a=1/NN

#Les fonctions------------------------------------------------------------

g1=(1+x)*(1+y)/4
g2=(1+x)*(1-y)/4
g3=(1-x)*(1+y)/4
g4=(1-x)*(1-y)/4

def gg(ux,uy,vx,vy):
	return integrate(lam*(diff(ux,x)+diff(uy,y))*(diff(vx,x)+diff(vy,y))+mu*(diff(ux,x)*diff(vx,x)+diff(ux,x)*diff(vx,x)+diff(uy,x)*diff(vx,y)+diff(ux,y)*diff(vx,y)+diff(ux,y)*diff(vy,x)+diff(uy,x)*diff(vy,x)+diff(uy,y)*diff(vy,y)+diff(uy,y)*diff(vy,y)),(x,-1,1),(y,-1,1))


def fl(vx,vy):
	return Float(-8e4*1*vy.subs(x,1).subs(y,0))

def nl(n):
	return floor((n-1)/N)+1
	

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

#M est la matrice qui représente la partie bilinéaire de la formulation faible
M=zeros(8,8)
for m in range(1,9):
	for n in range(1,9):
		M[m-1,n-1]=gg(listeX[m-1],listeY[m-1],listeX[n-1],listeY[n-1])

#print(M)
#On convertit la matrice de valeurs symboliques vers float
M=np.array(M).astype(np.float64)



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



# l2c=np.array([[2,5,1,6,8,11,7,12],[3,4,2,5,9,10,8,11]])

#On remplit la matrice en balayant les éléments et en réarrangeant les termes de la matrice M à chaque noeud
#Les éléments ont une longueur 2/NN selon y et 2 selon x, il faut donc multiplier les termes de la matrice par 2/NN
for n in range(1,N*NN+1):
	for i in range(1,9):
		for j in range(1,9):
			K[int(l2c[n-1,i-1]-1),int(l2c[n-1,j-1]-1)]+=a*M[i-1,j-1]



#Le vecteur b représente le terme source de la forme faible
#On ajoute le terme source aux bords droits en y
b=np.zeros(2*(N+1)*(NN+1))
# for i in range(1,NN+2):
# 	b[(N+1)*(NN+1)+(N+1)*i-1]=-8e4*N/2

b[(N+1)*(NN+1)+N+1-1]=-8e4*N

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


# workbook = xlsxwriter.Workbook('arrays.xlsx')
# worksheet = workbook.add_worksheet()

# row = 0

# for col, data in enumerate(np.transpose(K)):
#     worksheet.write_column(row, col, data)

# workbook.close()	

# Il faut maintenant résoudre le système d'équations M.u=b pour obtenir le résultat
u=solve(K,b)
ux=0*x
uy=0*y

g1=(1+x)*(1+y)/4*Piecewise((1,-1<=x),(0,True))*Piecewise((1,x<=1),(0,True))*Piecewise((1,-1<=y),(0,True))*Piecewise((1,y<=1),(0,True))
g2=(1+x)*(1-y)/4*Piecewise((1,-1<=x),(0,True))*Piecewise((1,x<=1),(0,True))*Piecewise((1,-1<=y),(0,True))*Piecewise((1,y<=1),(0,True))
g3=(1-x)*(1+y)/4*Piecewise((1,-1<=x),(0,True))*Piecewise((1,x<=1),(0,True))*Piecewise((1,-1<=y),(0,True))*Piecewise((1,y<=1),(0,True))
g4=(1-x)*(1-y)/4*Piecewise((1,-1<=x),(0,True))*Piecewise((1,x<=1),(0,True))*Piecewise((1,-1<=y),(0,True))*Piecewise((1,y<=1),(0,True))

liste=[]
liste.append(g1)
liste.append(g2)
liste.append(g3)
liste.append(g4)

for n in range(1,N*NN+1):
	for i in range(1,5):
		ux+=u[int(l2c[n-1,i-1]-1)]*liste[i-1].subs(x,x-((n-1)*2+1-2*N*(nl(n)-1))).subs(y,(y-(1-a-2*a*(nl(n)-1)))/a)
		uy+=u[int(l2c[n-1,i-1+4]-1)]*liste[i-1].subs(x,x-((n-1)*2+1-2*N*(nl(n)-1))).subs(y,(y-(1-a-2*a*(nl(n)-1)))/a)



fff=lambdify([x,y],uy)
fffx=lambdify([x,y],ux)


X,Y = np.meshgrid(np.linspace(0,2*N,100),np.linspace(-1,1,10))
uxx = fffx(X,Y)
uyy = fff(X,Y)

plt.quiver(X,Y,uxx,uyy)
plt.show()

xxx=np.concatenate((np.linspace(0,2*N,100),np.ones(100)*2*N,np.linspace(2*N,0,100),np.zeros(100)))
yyy=np.concatenate((-np.ones(100),np.linspace(-1,1,100),np.ones(100),np.linspace(1,-1,100)))

plt.plot(xxx,yyy)
plt.plot(xxx+500*fffx(xxx,yyy),yyy+500*fff(xxx,yyy))
plt.gca().set_aspect('equal', adjustable='box')
plt.show()
