---
date: 2020
title: 'Modélisation par éléments finis de la déformation d''une poutre
  sous l''action d''une force'
---

Introduction
============

Le but est de calculer les petites déformations élastiques d'un matériau
isotrope sous l'action d'une force $\bar{F}$ dans un espace de dimension
2.

Pour cela on utilise l'équation d'élasticité linéaire :

$$\bar{\nabla} \cdot \bar{\bar {\sigma } }  + \bar{F} = \bar{0}
\label{elastic}$$

Avec $\bar{\bar {\sigma } }$ le tenseur des contraintes de Cauchy.

Pour utiliser cette équation dans le cadre des éléments finis il faut
dériver la formulation faible de l'équation
[\[elastic\]](#elastic){reference-type="eqref" reference="elastic"}.
Pour cela on multiplie l'équation par une fonction vectorielle test
$\bar{v}(x,y)$ et on intègre l'équation sur le domaine de la poutre
$\Omega$ qui est de longueur L et hauteur H.

$$\int_{\Omega} \bar{v} . ( \bar{\nabla} \cdot \bar{\bar {\sigma } } + \bar{F} ) d\Omega = \bar{0}
\label{forfai}$$

Comme le tenseur des contraintes est symétrique on peut utiliser
l'égalité suivante :

$$\bar{v}. \bar{\nabla} \cdot \bar{\bar {\sigma } } = \bar{\nabla}\cdot (\bar{v}.\bar{\bar {\sigma } }) - \bar{\bar {\sigma } } : \bar{\bar {\nabla } } \bar{v} 
\label{sym}$$

En combinant les équation [\[forfai\]](#forfai){reference-type="eqref"
reference="forfai"} et [\[sym\]](#sym){reference-type="eqref"
reference="sym"} on obtient :

$$\int_{\Omega} \bar{\nabla} \cdot (\bar{v}.\bar{\bar {\sigma } }) d\Omega - \int_{\Omega} \bar{\bar {\sigma } } : \bar{\bar {\nabla } } \bar{v} d\Omega = - \int_{\Omega} \bar{v}.\bar{F} d\Omega
\label{forfai2}$$

En utilisant le théorème de flux-divergence, l'égalité devient :

$$\int_{\partial\Omega} \bar{v}.\bar{\bar {\sigma } }.\bar{n} d\partial\Omega - \int_{\Omega} \bar{\bar {\sigma } } : \bar{\bar {\nabla } } \bar{v} d\Omega = - \int_{\Omega} \bar{v}.\bar{F} d\Omega
\label{forfai3}$$

En faisant l'hypothèse que les contraintes sont nulles aux bordures, le
premier terme de l'équation est nul. On a finalement :

$$\int_{\Omega} \bar{\bar {\sigma } } : \bar{\bar {\nabla } } \bar{v} d\Omega = \int_{\Omega} \bar{v}.\bar{F} d\Omega
\label{forfai4}$$

On utilise maintenant la loi de Hooke qui dans le cas d'un matériau
isotrope s'écrit :
$$\bar{\bar {\sigma} }=\lambda tr(\bar{\bar{\epsilon}}) \bar{\bar {1} } + 2 \mu \bar{\bar {\epsilon } }
\label{hook}$$

Avec $\bar{\bar{\epsilon}}$ le champ lié au vecteur déplacement
$\bar{u}$ par :

$$\bar{\bar {\epsilon } } = \frac{1}{2}(\bar{\bar {\nabla } } \bar{u} + \bar{\bar {\nabla } } \bar{u}^{T})
\label{sym2}$$

On intègre maintenant les équations
[\[hook\]](#hook){reference-type="eqref" reference="hook"} et
[\[sym2\]](#sym2){reference-type="eqref" reference="sym2"} dans
l'équation [\[forfai4\]](#forfai4){reference-type="eqref"
reference="forfai4"}, ce qui donne :

$$\int_{\Omega} \lambda (\nabla \cdot \bar{u}) (\nabla \cdot \bar{v}) + \mu \bar{\bar {\nabla } } \bar{u} : \bar{\bar {\nabla } } \bar{v} + \mu \bar{\bar {\nabla } } \bar{u}^{T} : \bar{\bar {\nabla } } \bar{v} d\Omega = \int_{\Omega} \bar{v}.\bar{F} d\Omega
\label{forfai5}$$

Que l'on peut mettre sous la forme :

$$a(\bar{u},\bar{v})=l(\bar{v})
\label{forfai6}$$

Avec a une fonction symétrique bilinéaire et l une fonction linéaire.

On utilise maintenant la famille de fonctions nodales bilinéaire
suivante pour aprroximer la solution sur un élément fini de dimension 2
sur 2:

$$\begin{aligned}
\bar{g_{1}} & = & \frac{(1+x)(1+y)}{4} \bar{x} \nonumber \\
\bar{g_{2}} & = & \frac{(1+x)(1-y)}{4} \bar{x} \nonumber \\
\bar{g_{3}} & = & \frac{(1-x)(1+y)}{4} \bar{x} \nonumber \\
\bar{g_{4}} & = & \frac{(1-x)(1-y)}{4} \bar{x} \nonumber \\
\bar{g_{5}} & = & \frac{(1+x)(1+y)}{4}\bar{y} \nonumber \\
\bar{g_{6}} & = & \frac{(1+x)(1-y)}{4}\bar{y} \nonumber \\
\bar{g_{7}} & = & \frac{(1-x)(1+y)}{4}\bar{y} \nonumber \\
\bar{g_{8}} & = & \frac{(1-x)(1-y)}{4}\bar{y} \nonumber \\\end{aligned}$$

Pour chaque fonction de cette famille la formulation faible est
vérifiée, i.e. pour tout i appartenant à {1,2 \... 8} on a l'égalité
suivante :

$$a(\bar{u_{s}},\bar{g_{i}})=l(\bar{g_{i}})
\label{proj1}$$

Avec $\bar{u_{s}}$ la fonction solution. Cette fonction peut être
approchée par une combinaison linéaire de la famille de fonctions
utilisées, on note alors la solution approximée $\bar{u_{h}}$ avec :

$$\bar{u_{h}} = \sum_{j=1}^{8} u_{j} \bar{g_{j}}
\label{proj2}$$

En combinant les équations [\[proj1\]](#proj1){reference-type="eqref"
reference="proj1"} et [\[proj2\]](#proj2){reference-type="eqref"
reference="proj2"} il vient :

$$\forall i \in \{1,2 ... , 8\},  a(\sum_{j=1}^{8} u_{j} \bar{g_{j}},\bar{g_{i}})=l(\bar{g_{i}})
\label{proj3}$$

Comme a est une fonction bilinéaire :

$$\forall i \in \{1,2 ... , 8\},  \sum_{j=1}^{8} u_{j} a(\bar{g_{j}},\bar{g_{i}})=l(\bar{g_{i}})
\label{proj4}$$

Ce système d'équation peut être résumé par le système matriciel :

$$\bar{\bar{A}}\bar{U}=\bar{b}
\label{proj5}$$

Avec $\bar{\bar{A}}$, la matrice de terme général
$(A_{i,j})= a(\bar{g_{j}},\bar{g_{i}})$, $\bar{U}$ le vecteur inconnu de
terme général $(U_{i})$ et $\bar{b}$ le vecteur de terme général
$(b_{i})=l(\bar{g_{i}})$.

Avant de résoudre le système matriciel il faut calculer les termes de la
matrice $\bar{\bar{A}}$ et du vecteur $\bar{b}$, en calculant les
intégrales correspondantes. Les 64 termes de la matrice sont calculés
rapidement à l'aide de la fonction 'integrate' du package symbolique
sympy de python.

Pour un élément fini de dimension 2a sur 2f, une fonctions nodales
bilinéaires sont les mêmes que les fonctions $g_{i}$ après changement de
variable;

en cours \...

La matrice $\bar{\bar{A}}$ est maintenant calculée pour un élément fini
de dimension 2 sur 2, pour calculer cette même matrice sur un élément de
dimension 2a sur 2f on peut utiliser le changement de variable :

en cours \...
