# SYSTEME DE RECOMMANDATION
# CORRELATION DE PEARSON

# Ce fichier regroupe les fonctions necessaires pour implementer un système de recommandation basé sur l'approche de la corrélation de Pearson
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


def moyenne_vect(u): #Calcule la moyenne des composantes d'un vecteur

    moyenne=0
    compteur=0

    for i in u:

        if i>0:  #On fait la moyenne sur les composantes non nulles

            compteur = compteur + 1

            moyenne= moyenne + i

    moyenne = moyenne / compteur

    return moyenne



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


def retrancher_vect(u,valeur):  #retranche une valeur a toutes les composante d'un vecteur

    n=len(u)

    for i in range(n):

        u[i]= u[i] - valeur

    return u

def correlation_pearson(k,matrice):
        #k est l'indice de l'utilisateur
        #matrice utilisateurs (lignes) x items (colonnes)
        #cette fonction renvoie la liste des corrélations de pearson de l'utilisateur k avec tous les autres utilisateurs

        utilisateur=matrice[k]

        moyenne_uti=moyenne_vect(utilisateur)

        liste_corr=[]

        n=len(matrice)  #nombre d'utilisateurs

        for i in range(n):  #parcourt les utilisateurs

            if i!=k:  #on saute l'utilisateur k

                moyenne_aux=moyenne_vect(matrice[i])  #moyenne des composantes de l'utilisateur i

                u1,v1=composantes_communes(utilisateur,matrice[i])  #vecteurs avec seulement composantes en commun

                u1,v1=retrancher_vect(u1,moyenne_uti),retrancher_vect(v1,moyenne_aux)  #vecteurs avec moyenne retranchée

                normeu1=norme_euc(u1)

                normev1=norme_euc(v1)

                if normeu1!=0 and normev1!=0:  

                    produit_scal=p_s_can(u1,v1)

                    pearson = produit_scal/(normeu1*normev1)

                    liste_corr.append(pearson)

                else:

                    liste_corr.append('NaN')  #les utilisateurs n'ont pas notés de films en commun

            elif i==k:

                liste_corr.append('NaN')  #pour garder les bons indices


        return liste_corr


def pearson_note(item,k,matrice):  # Prediction de la note a l'aide de pearson

    #k indice utilisateur
    #item indice de l'item
    #matrice utilisateurs (lignes) x items (colonne)

    liste_corr=correlation_pearson(k,matrice)

    moyenne_k=moyenne_vect(matrice[k])

    n=len(liste_corr)

    note = 0
    somme_corr = 0 #somme pour la moyenne pondérée

    for i in range(n):

        if liste_corr[i]==('NaN'): #on prend que si les utilisateurs sont corrélés

            note=note

        elif matrice[i][item]>0: #on prend que les notes positives

            moyenne_aux=moyenne_vect(matrice[i])

            somme_corr = somme_corr + abs(liste_corr[i])

            note = note + liste_corr[i] * (matrice[i][item] - moyenne_aux)

    if somme_corr==0:  #si tous les utilisateurs en commun ( admettant une similitude pearson ) n'ont pas noté le film (donc somme sim = 0)

        return -1

    note = note/somme_corr + moyenne_k

    return note







