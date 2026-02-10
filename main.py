import mysql.connector
from datetime import datetime
connection = mysql.connector.connect(
    host = 'localhost',
    user ='pythonuser',
    password ='Python@123',
    database ='boutique_pro'
)

if connection.is_connected():
    print("Connected to mysql database")

#menu choix
def afficher_menu():
    print("\n --Gestion du boutique Pro--")
    print("1. categories")
    print("2. Produits")
    print("3. recherches produits correspondant categories ")
    print("4. Indiquer le mouvement")


#menu categorie
def menu_categories():
    print("\n --Gestion du boutique Pro--")
    print("\n CATEGORIES")
    print("1. Ajouter categories")
    print("2. modifier")
    print("3. supprimer ")
    print("4. recherches ")
    print("5. retour accueil")
    while True:
        while True:
            try:
                choix=int(input("Veuillez choisir un nombre entre 1 et 5 : "))
                if 1 <= choix <=5:
                    break
                else:
                    print("incorrect! choisi bien")
            except ValueError:
                print("Invalid! Veuillez resaisir correctement")

        if choix == 1:
            categories()
        elif choix == 2:
            modifier_categories()
        elif choix == 3:
            delete_categorie()
        elif choix == 4:
            indique_mouvement()
        elif choix == 5:
            afficher_menu()
            break

# ajouter categories
def categories():
    cursor = connection.cursor()
    while True:
        try:
            nom_categorie = input("Veuillez indiquer le nom du categorie (les produits sont rangees en categories) : ")
            description_categorie = input("Fait une petite description de cette categorie : ")
            if nom_categorie.isalpha() and description_categorie.isalpha():
                break
        except ValueError:
            print("erreur ! veuillez reessayer")

    query = """
            insert into categories(nom_categorie, description_categorie) values(%s,%s)
        """
    cursor.execute(query, (nom_categorie, description_categorie ))
    connection.commit()
    cursor.close()

#modifier categories
def modifier_categories():
    cursor = connection.cursor()
    while True:
        try:
            id_categorie = int (input("indiquer l'id du categorie a modifier"))
        except ValueError:
            print("erreur id categorie")
        try:
            nom_categorie = input("Veuillez indiquer le nom du categorie (les produits sont rangees en categories) : ")
            description_categorie = input("Fait une petite description de cette categorie : ")
            if nom_categorie.isalpha() and description_categorie.isalpha():
                break
        except ValueError:
            print("oups!,erreur")
    query = """
            update categories
            set nom_categorie = %s ,
                description_categorie = %s 
            where id_categorie =%s
        """
    try:
        cursor.execute(query, (nom_categorie,description_categorie,id_categorie))
        connection.commit()
        print("Mise a jour reussi !")
    except Exception as e:
        print(f"ooup erreur ! {e}")
    cursor.close()

#delete categories
def delete_categorie():
    cursor = connection.cursor()
    while True:
        try:
            id_categorie = int (input ("Indiquez l'id de la ligne que vous voulez supprime : "))
        except ValueError:
            print("oups ! erreur , ressaisi")
    query = """
            delete from categories
            where id_categorie = %s
        """
    cursor.execute(query, (id_categorie ))
    connection.commit()
    cursor.close()


#recherches  
def recherches():
    cursor = connection.cursor()
    while True:
        try:
            id_produit = int(input("indiquez l'id du produits a rechercher : "))
        except ValueError:
            print("erreur! veuillez bien indiquer l'id")
        try:
            nom_produit = input("ou donnez le nom : ").lower()
            if nom_produit.isalpha():
                break
        except ValueError:
            print("erreur veuillez resaisir")
    query = """
                select * 
                from produits pro
                join categories cat on pro.id_categorie = cat.id_categorie
                where id_produit = %s or nom_produit = %s
        """
    cursor.execute(query, (id_produit,nom_produit))
    produit = cursor.fetchone()
    print(f"{produit}")
    cursor.close()



#menu produit
def menu_produits():
    print("\n --Gestion du boutique Pro--")
    print("\n Produits")
    print("1. Ajouter ")
    print("2. marquer le status")
    print("3. supprimer ")
    print("4. alert")
    print("5. modifier")
    print("5. retour accueil")
    while True :   
        while True:
            try:
                choix=int(input("Veuillez choisir un nombre entre 1 et 7 : "))
                if 1 <= choix <=7:
                    break
                else:
                    print("incorrect! choisi bien")
            except ValueError:
                print("Invalid! Veuillez resaisir correctement")

        if choix == 1:
            produits()
        elif choix == 2:
            marquer_status_produit()
        elif choix == 3:
            delete()
        elif choix == 4:
            alert()
        elif choix == 5:
            afficher_menu()
            break
        
# ajouter produits
def produits():
    cursor = connection.cursor()
    while True:
        try:
            nom_produit =str( input("Donner Le nom du produit : "))
            break
        except ValueError:
            print("erreur dans l'input nom!")
        try:    
            prix_produit =float(input("Donner Le prix du produit : "))
            break
        except ValueError:
            print("erreur au niveau du prix")
        try:
            description_produit =str( input("Donner Le description du produit : "))
            break
        except ValueError:
            print("erreur au niveau du description")
        try:
            quantite_produit =int( input("Donner Le quantite du produit : "))
            break
        except ValueError:
            print("erreur! dans la quantite")
        try:
            id_categorie =int( input("Donner L'id de la categorie qu'il correspond : "))
            break
        except ValueError:
            print("erreur ! au niveau de l'id categorie")

    query = """
            insert into produits(nom_produit, prix_produit, description_produit, quantite_produit, id_categorie) values(%s,%s,%s,%s,%s)
        """
    cursor.execute(query, (nom_produit, prix_produit, description_produit, quantite_produit, id_categorie))
    connection.commit()
    cursor.close()

# marquer le status du produits
def marquer_status_produit():
    cursor = connection.cursor()
    while True:
        print("Marquer le status enrupture si c'est epuiser ")
        try:
            id_produit = int(input("Indiquer l'id du produit : "))
        except ValueError:
            print("erreur au niveau de l'id produit")
        try:
            satus_produit = input("Veuillez indiquer l'etat du produit ")
            if satus_produit == 'disponible' or satus_produit == 'enrupture':
                break
        except ValueError:
            print("erreur veuillez reesayer")

    query = """
            update produits
            set satus_produit = %s 
            where id_produit = %s
        """
    cursor.execute(query, (satus_produit,id_produit))
    connection.commit()
    cursor.close()

#modifier le produit 
def modifier_produits():
    cursor = connection.cursor()

    while True:
        try:
            id_produit = int(input("indiquer l'id du produit a modifier"))
        except ValueError:
            print("erreur")
        try:
            nom_produit =str( input("Donner Le nom du produit : "))
            break
        except ValueError:
            print("erreur dans l'input nom!")
        try:    
            prix_produit =float(input("Donner Le prix du produit : "))
            break
        except ValueError:
            print("erreur au niveau du prix")
        try:
            description_produit =str( input("Donner Le description du produit : "))
            break
        except ValueError:
            print("erreur au niveau du description")
        try:
            quantite_produit =int( input("Donner Le quantite du produit : "))
            break
        except ValueError:
            print("erreur! dans la quantite")
        try:
            id_categorie =int( input("Donner L'id de la categorie qu'il correspond : "))
            break
        except ValueError:
            print("erreur ! au niveau de l'id categorie")

    query = """
            update produits
            set nom_produit = %s ,
                prix_produit = %s,
                description_produit = %s,
                quantite_produit = %s,
                id_categorie = %s 
            where id_produit =%s
        """
    try:
        cursor.execute(query, (nom_produit,prix_produit, description_produit,quantite_produit,id_categorie,id_produit))
        connection.commit()
        print("Mise a jour reussi !")
    except Exception as e:
        print(f"ooup erreur ! {e}")
    cursor.close()

# indiquer le mouvement ajouter les
def indique_mouvement():
    cursor = connection.cursor()

    type_mouvement = input("Action (ajouter / retirer) : ").lower()
    quantite = int(input("Quantité du mouvement : "))
    id_produit = int(input("ID du produit : "))
    dateHeure_mouvement = datetime.now()

    # Récupérer la quantité actuelle du produit
    cursor.execute(
        "SELECT quantite_produit FROM produits WHERE id_produit = %s",
        (id_produit,)
    )
    result = cursor.fetchone()
    quantite_produit = result[0]
    # Calculer la nouvelle quantité
    if type_mouvement == "ajouter":
        nouvelle_quantite = quantite_produit + quantite
    elif type_mouvement == "retirer":
        if quantite > quantite_produit:
            print("Stock insuffisant")
            cursor.close()
            return
        nouvelle_quantite = quantite_produit - quantite
    else:
        print("Action invalide")

    # Mettre à jour le stock du produit
    query ="""
            UPDATE produits 
            SET quantite_produit = %s 
            WHERE id_produit = %s"""
    
    cursor.execute(query,(nouvelle_quantite, id_produit))

    # Enregistrer le mouvement
    query2 =  """
        INSERT INTO mouvements (type_mouvement, dateHeure_mouvement, quantite, id_produit)
        VALUES (%s, %s, %s, %s)
        """
    cursor.execute(query2, (type_mouvement, dateHeure_mouvement, quantite, id_produit))
    print(" Quantité récupérée, calculée et mise à jour")
    connection.commit()
    cursor.close()

    
#afficher une message la quantite dans produits < 5
def alert():
    cursor = connection.cursor()

    query = """ select * from produits
                where qunatite_produit < 5
        """
    cursor.execute(query)
    return cursor.fetchall
    print("Alert solde de le stockage est insuffisant")
    cursor.close()

#fermeture de la connexion
def fermeture_connextion():
        connection.close()

#spprimer un produit
def delete():
    cursor = connection.cursor()
    while True:
        try:
            id_produit = int (input ("Indiquez l'id de la ligne que vous voulez supprime : "))
            break
        except ValueError:
            print("erreur")
    query = """
            delete from produit
            where id_produit = %s
        """
    cursor.execute(query, (id_produit ))
    connection.commit()
    cursor.close()


    # menu principal
while True:
    afficher_menu()
    while True:
        try:
            choix=int(input("Veuillez choisir un nombre entre 1 et 4 : "))
            if 1 <= choix <=4:
                break
            else:
                print("incorrect! choisi bien")
        except ValueError:
            print("Invalid! Veuillez resaisir correctement")

    if choix == 1:
        menu_categories()
    elif choix == 2:
        menu_produits()
    elif choix == 3:
        recherches()
    elif choix == 4:
        fermeture_connextion()