# SYSTEME DE RECOMMANDATION
# K PLUS PROCHES VOISINS

# Ce fichier regroupe les fonctions necessaires pour implementer un système de recommandation basé sur l'approche des k plus proches voisins
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

def vect_uv(u,v):  #Calculer le vecteur UV avec les points/vecteurs u et v

    vecteur=[]
    n=len(u)

    for i in range(n):

        vecteur.append(u[i]-v[i])

    return vecteur


def liste_distances(indice_uti,matrice):
    # Calcule la distance euclidienne entre l'utilisateur passé en paramètre et les autres utilisateurs
    # matrice user x item remplie des notes
    u=matrice[indice_uti]
    n=len(matrice)
    list_dist=[]

    for i in range(n):

        if i!=indice_uti:

            vecteur=vect_uv(u,matrice[i])
            distance=norme_euc(vecteur)
            list_dist.append([distance,i])
        else:
            list_dist.append([0,indice_uti])

    return list_dist


def scinde(liste):
    # Scinde la liste en deux
    milieu=len(liste)//2
    Tg=liste[:milieu]
    Td=liste[milieu:]
    return Tg,Td

def fusion(L1,L2):
    # Fusionne deux listes selon le tri fusion
    if L1==[]:
        return L2
    if L2==[]:
        return L1
    if L1[0][0]<L2[0][0]:
        return [L1[0]]+fusion(L1[1:],L2)
    else:
        return [L2[0]]+fusion(L1,L2[1:])


def tri_fusion(liste):
    # Le tri fusion classique
    if len(liste)<=1:
        return liste
    else:
        Tg,Td=scinde(liste)
        Tg,Td=tri_fusion(Tg),tri_fusion(Td)
        return fusion(Tg,Td)


def k_plus_petits(liste,k):
    # Renvoie la liste des k plus petites valeur de la liste passée en parametre
        liste1=tri_fusion(liste)
        return liste1[0:k]


def KNN(k,indice_uti,matrice):
    # Renvoit les indices des k plus proches voisins de l'utilisateur indice_uti 
    candidats=matrice
    liste=liste_distances(indice_uti,candidats)
    resultat=k_plus_petits(liste,k)
    return resultat



def knn_prediction(indice_item,indice_uti,matrice,k=200):
    # Prédit la note pour l'item indice_item pour l'utilisateur indice_uti avec la méthode des k plus proches voisins
    liste_knn=KNN(k,indice_uti,matrice)
    n=len(liste_knn)
    note=0
    compteur=0
    for i in range(n):
        indice=liste_knn[i][1]
        if matrice[indice][indice_item]>0:
            note = note + matrice[indice][indice_item]
            compteur=compteur + 1

    if compteur ==0:
        return -1

    note=note/compteur

    return note






