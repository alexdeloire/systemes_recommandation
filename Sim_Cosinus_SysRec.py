#  SYSTEME DE RECOMMANDATION
#  SIMILITUDE COSINUS

# Ce fichier regroupe les fonctions necessaires pour implementer un système de recommandation basé sur l'approche de la similitude cosinus
# Pour les détails mathématiques, veuillez regarder le pdf de présentation

import math

def p_s_can(u,v):

    #produit scalaire canonique de R^n
    #u et v sont deux vecteurs de R^n
    n=len(u)
    resultat=0

    for i in range(n):

        resultat = resultat + u[i]*v[i]

    return resultat


def norme_euc(u):  #Norme Euclidienne

    return math.sqrt(p_s_can(u,u))


def composantes_communes(u,v):
    # Calcule les vecteurs u1 et v1 qui sont les vecteurs avec les composantes qui sont communes au vecteurs u et v

    u1=[]
    v1=[]
    n=len(u)

    for i in range(n):

        if u[i]!=0 and v[i]!=0:

            u1.append(u[i])
            v1.append(v[i])

    return u1,v1


def max_liste_et_indice(liste):

    #renvoie max et indice du max d'une liste

    max=liste[0]
    indice=0

    for i in range(len(liste)):

        if liste[i]>=m:

            max=liste[i]
            k=i

    return k,max


def calcul_liste_sim_cos(k,matrice):

    #nous allons calculer la liste des similitudes de tous les utilisateurs avec l'utilisateur k ie [cos(théta1),cos(théta2),...]

    #k est l'indice de l'utilisateur ie la ligne de la matrice

    #matrice est la matrice utilisateur(lignes) x items(colonnes) remplie des notes

    utilisateur=matrice[k]  #vecteur de l'utilisateur

    n=len(matrice) #nbre utilisateurs
    liste_sim=[]  #la ou on stocke les similitudes


    for i in range(n):

        if i!=k:   #On traite tous les utilisateurs différents de celui passé en argument

            u1,v1=composantes_communes(utilisateur,matrice[i])

            norme_v1=norme_euc(v1)

            norme_utilisateur=norme_euc(u1)

            if norme_v1!=0 and norme_utilisateur!=0:


                sim=(p_s_can(u1,v1))/(norme_utilisateur*norme_v1)   

                liste_sim.append(sim)

            else:

                liste_sim.append('NaN')  #les utilisateurs n'ont pas noté de films en commun

        else:

            liste_sim.append('NaN')  #on rajoute ca pour garder les bons indices dans la liste

    return liste_sim

#On peut maintenant trouver l'utilisateur le plus similaire en gout

def utilisateur_plus_proche(liste_sim):
    return max_liste_et_indice(liste_sim)

#Nous pouvons également prédire la note que l'utilisateur donnerai à l'article

def prediction_note(item_indice,uti_indice,matrice):

    #matrice : utilisateur (lignes) x items (colonnes)

    liste_sim = calcul_liste_sim_cos(uti_indice,matrice)
    #print(liste_sim[0:20])
    n=len(liste_sim)

    note=0

    somme_sim = 0 #on ajoute la valeur absolue des similitudes pour faire une moyenne pondérée

    for i in range(n):

        if liste_sim[i]==('NaN'):

            note = note  #utilisateurs non corréllés

        elif matrice[i][item_indice]>0:  #Nous prenons que les notes strictement positives

            somme_sim = somme_sim + abs(liste_sim[i])

            note = note + liste_sim[i] * matrice[i][item_indice]

    if somme_sim==0:  #si tous les utilisateurs en commun ( admettant une similitude cos ) n'ont pas noté le film (donc somme sim = 0)

        return -1

    note = note/somme_sim  #On normalise

    return note

