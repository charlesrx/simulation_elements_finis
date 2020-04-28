#Le but de ce code est de vérifier la validité de la simulation numérique
#Pour cela on va comparer une solution connue du problème de déflexion avec la solution calculée numériquement

from sympy import *
init_printing(use_unicode=True, wrap_line=False)
from sympy.physics.continuum_mechanics.beam import Beam

E, I = symbols('E, I')
x,y=symbols('x,y')


#Le module d'young est E
E=1.18e11

#Le faisceau métallique à une longueur L de 20 mètres et une section de longueur 2
L=20

#Le moment quadratique I de la section S par rapport à l'axe Ox est 
I=20

#Le faisceau a une longueur de 20 mètres
beam = Beam(L, E, I)


#On applique une force de 8e4*N Newton à la barre au coin supérieur droit
#Dans notre cas N=10
N=10
beam.apply_load(-8e4*N,20,-1)
#Le terme -1 


#The fixed end imposes two boundary conditions: 1) no vertical 
#deflection and 2) no rotation. These are specified by appending 
#tuples of x values and the corresponding deflection or slope values:
beam.bc_deflection.append((0, 0))
beam.bc_slope.append((0, 0))

#These boundary conditions introduce an unknown reaction force and 
#moment which need to be applied to the beam to maintain static 
#equilibrium:

R, M = symbols('R, M')
beam.apply_load(R, 0, -1)
beam.apply_load(M, 0, -2)
beam.load


#These two variables can be solved for in terms of the applied 
#loads and the final loading can be displayed:

beam.solve_for_reaction_loads(R, M)
beam.reaction_loads


beam.plot_deflection()

exec(open('./multiNy.py').read())


xm=np.linspace(0,2*N,N+1)

ym=np.zeros(len(xm))
cpt=0
for i in xm:
	ym[cpt]=beam.deflection().subs(x,i)
	cpt+=1


plt.plot(xm,0.5*uy[int(ligne1),:]+0.5*uy[int(ligne2),:])
plt.plot(xm,ym)
plt.title('Comparaison entre la solution calculée et celle de sympy.continuum_mechanics')
plt.show()



