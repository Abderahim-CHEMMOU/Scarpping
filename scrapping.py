
import requests
from bs4 import BeautifulSoup

adresse= "https://iceandfire.fandom.com/wiki/Petyr_Baelish"
# pour récupérer le fichier html
fichier_html=requests.get(adresse)

soup = BeautifulSoup(fichier_html.text, 'html.parser')

# Projet
# Quest1

# verifie si une chaine contient :
def filtre(s):
    for c in s:
        if(c == ":"):
            return False
    return True
    
def liste_liens(page):
    
    adresse = "https://iceandfire.fandom.com/wiki/" + page

    response=requests.get(adresse)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find('div', {'id': 'mw-content-text'}).find_all('a')
    hrefs=[]
    for link in links:
        if filtre(link.get('href')):
            href = link.get('href')
            if(href.startswith('/wiki/')):
                hrefs.append(href[6:])
    return hrefs

doc = {'Petyr_Baelish':liste_liens("Petyr_Baelish")}

def svg_dico(doc, file_name):
    with open(file_name, 'a') as f:
        for key , value in doc.items():
            f.write(f"{key}: {value}\n")

# svg_dico(doc, 'essaye_rahim.txt')

def chg_dico(file_name):
    diction= {}
    with open(file_name, 'r') as f:
        for line in f:
            # récupérer la cle et la valeur 
            cle, valeur = line.split(': ')
            # strip pour supprimer les \n
            # eval pour convertir la chaine de caractere en une liste
            diction[cle]=eval(valeur.strip())
    return diction


# diction = chg_dico('essaye_rahim.txt')
# print(diction['Petyr_Baelish'])

def parocoursLaregeur(start, file_name):
    # créer un itérable
    visited = []
    queue = [start]
    #peter
    while queue:
        vertex = queue.pop(0)
        #vertex = peter
        if vertex not in visited:
            visited.append(vertex)
            svg_dico({vertex:liste_liens(vertex)}, file_name)
            for lien in liste_liens(vertex):
                queue.append(lien)
    return visited

# print(parocoursLaregeur("Petyr_Baelish", "rahim.txt"))

def plus_court_chemin(depart, arrivee, graph):
    # Initialisation
    file = [depart] # File pour le parcours en largeur
    predecesseurs = {depart: None} # Prédécesseurs pour reconstruire le chemin

    # Parcours en largeur
    while file:
        u = file.pop(0)
        for v in graph[u]:
            if v not in predecesseurs:
                predecesseurs[v] = u
                if v == arrivee:
                    # On a trouvé le chemin le plus court, on le reconstruit et on le renvoie
                    chemin = [v]
                    while predecesseurs[v] != depart:
                        v = predecesseurs[v]
                        chemin.append(v)
                    chemin.append(depart)
                    chemin.reverse()
                    return chemin
                file.append(v)
    # Si on arrive ici, il n'y a pas de chemin entre les deux pages
    return None

def pcc_voyelles( depart, arrivee, graphe):
    #initialiser tootes  les valeurs des noeuds à l'infini
    distances = {noeud: float('inf') for noeud in graphe}
    distances[depart] = 0
    visite = {depart}
    predecesseurs = {}

    while visite:
        
        #selectionner le noued qui a le plus petite distance parmi les noueds de visite 
        # à partir des distances stockées dans le dictionnaire distances
        u = min(visite, key=distances.get)
        visite.remove(u)

        for v in graphe[u]:
            cout = len(v) + 2 * len([c for c in v.lower() if c in "aeiouy"])
            # si v n'existe pas dans distances OU si la distance de v qui existe déja dans la tableau distances est sup à la distance de deuxieme v
            #  il faut modifier la distance de v pour mettre la plus petite distance
            if v not in distances or distances[v] > distances[u] + cout:
                distances[v] = distances[u] + cout
                # on rajoute v et son predecesseur à predecesseurs
                predecesseurs[v] = u
                # on rajoute v à la liste des noueds visités
                visite.add(v)

    chemin = []
    u = arrivee
    # on teste si u existe dans les valeurs de dictionnaire predecesseurs
    while u in predecesseurs:
        # inserer à la position zero le u
        chemin.insert(0, u)
        u = predecesseurs[u]
    #on rajoute le noued de départ car son predecesseur est None
    chemin.insert(0, u)
    return chemin

graphe = chg_dico("rahim.txt")
# print(plus_court_chemin("Dorne", "Rhaego", graphe))
# print(pcc_voyelles("Dorne", "Rhaego", graphe))

# Question 7

# elle créer les trois types d'arretes pour un personage 
# et crée un dictionnaire qui a comme (clé,valeur) = (personne, liste
def famillePersonnage(personne):

    adresse = "https://iceandfire.fandom.com/wiki/" + personne

    response=requests.get(adresse)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Rechercher la div
    div = soup.find("div", {"class": "page-header__categories"})
    
    if(div != None):
        # Rechercher tous les liens avec title="Category:Characters"
        lien = div.find("a", {"title": "Category:Characters"})
        # Determiner le wiki est un wiki d'une personnage
        if(lien != None):
            dictionnaire = {}
            liste=[]
            diction=[]
            #diction = {}

            # Rechercher tous les spouse
            div = soup.find("div", {"data-source": "spouse"})
            if(div):
                liens = div.find_all("a")
                for lien in liens:
                    # On crée des couples de (Spouse, name_spouse)
                    liste.append(lien.get("title"))
                   
                spans = div.find_all("span", {"class": "new"})
                for span in spans:
                    # On crée des couples de (Spouse, name_spouse)
                    liste.append(span.text)
                    
                for memebre in liste:    
                    #diction["Spouses"] = liste 
                    diction.append(("Spouses",memebre))
                liste=[] 
        
            # Rechercher tous les fathers
            div = soup.find("div", {"data-source": "father"})
            if(div):
                liens = div.find_all("a")
                for lien in liens:
                    # On crée des couples de (father, name_father)
                    liste.append( lien.get("title"))

                spans = div.find_all("span", {"class": "new"})
                for span in spans:
                    # On crée des couples de (Father, name_Father)
                    liste.append(span.text)
                for memebre in liste:    
                    #diction["Fathers"] = liste 
                    diction.append(("Fathers",memebre))
                liste=[] 
                
            # Rechercher tous les mothers
            div = soup.find("div", {"data-source": "mother"})
            if(div):
                liens = div.find_all("a")
                for lien in liens:
                    # On crée des couples de (Mother, name_Mother)
                    liste.append(lien.get("title"))

                # On peut trouver aussi mother, father, lover, .. dans la balise span
                # comme l'indique par exemple le personnage Cersei_Lannister il a une span
                #  Lady Taena Merryweather qui est son lover 

                spans = div.find_all("span", {"class": "new"})
                for span in spans:
                    # On crée des couples de (Mother, name_Mother)
                    liste.append(span.text) 
                for memebre in liste:    
                    #diction["Mothers"] = liste 
                    diction.append(("Mothers",memebre))
                liste=[] 
            # Rechercher tous les siblings
            div = soup.find("div", {"data-source": "siblings"})
            if(div):
                liens = div.find_all("a")
                for lien in liens:
                    # On crée des couples de (Siblings, name_Sibling)
                    liste.append(lien.get("title"))

                spans = div.find_all("span", {"class": "new"})
                for span in spans:
                    # On crée des couples de (Sibling, name_Sibling)
                    liste.append(span.text)
                for memebre in liste:    
                    #diction["Siblings"] = liste 
                    diction.append(("Siblings",memebre))
                liste=[] 
            # Rechercher tous les childrens
            div = soup.find("div", {"data-source": "children"})
            if(div):
                liens = div.find_all("a")
                for lien in liens:
                    # On crée des couples de (children, name_childrens)
                    liste.append(lien.get("title"))

                spans = div.find_all("span", {"class": "new"})
                for span in spans:
                    # On crée des couples de (Children, name_Children)
                    liste.append(span.text)
                for memebre in liste:    
                    #diction["Children"] = liste 
                    diction.append(("Children",memebre))
                liste=[] 

            # Rechercher tous les Lover
            div = soup.find("div", {"data-source": "lover"})
            if(div):
                liens = div.find_all("a")
                for lien in liens:
                    # On crée des couples de (Lover, name_Lover)
                    liste.append(lien.get("title"))
                
                spans = div.find_all("span", {"class": "new"})
                for span in spans:
                    # On crée des couples de (Lover, name_Lover)
                    liste.append( span.text)
                for memebre in liste:    
                    #diction["Lover"] = liste 
                    diction.append(("Lover",memebre))
                liste=[] 

            dictionnaire[personne]= diction
            return dictionnaire

# print(famillePersonnage("Lysa_Arryn"))

# cette fonction récupère toutes les personnages à partir de fichier générer avec la question4
# et cree un nouveau graphe qui a trois type d'arrtes
# se graphe sera enregestrer dans un fichier
def famillePersonnage_S(file_name_famille, file_name_wiki):
    diction = chg_dico(file_name_wiki)

    for personne in diction.keys():
        famille = famillePersonnage(personne)
        if(famille):
            svg_dico(famille, file_name_famille)

# famillePersonnage_S("famille.txt", "rahim.txt")

# dition=chg_dico("famille.txt")
#print(dition)

# question8

def couples_incestueux(file_name_famille):
    diction = chg_dico(file_name_famille)
    liste_inceste =[]
    for key , value in diction.items():
        for membre in value:
            typePersonne, nom = membre
            if typePersonne=="Lover":
                for membre2 in value:
                    autreTypePersonne, autreNom=membre2
                    if autreNom != None:
                        # on a utilisé replace car des fois on un meme nom qui a "_" et des " " 
                        autreNom=autreNom.replace("_"," ")
                        nom=nom.replace("_"," ")
                        key=key.replace("_"," ")
                        # On teste si cette personne est presente dans Children, Mother, Father, Sibling
                        if autreTypePersonne!="Lover" and autreTypePersonne!="Spouses" and nom==autreNom: 
                            if not (nom,key) in liste_inceste:
                                liste_inceste.append((key,nom))    
    return liste_inceste

print(couples_incestueux("famille.txt"))
