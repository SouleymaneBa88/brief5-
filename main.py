#https://github.com/SouleymaneBa88/brief5-.git
import mysql.connector
from datetime import datetime
from email_validator import validate_email,EmailNotValidError 
import getpass
import bcrypt
from dotenv import load_dotenv
import os

load_dotenv()


connection = mysql.connector.connect(
        host = os.getenv("DB_HOST"),
        user= os.getenv("DB_USER"),
        password= os.getenv("DB_PASSWORD"),
        database= os.getenv("DB_NAME")
)

if connection.is_connected():
    print("Connected to mysql database")

def controle_email(email):
    try: 
        infos = validate_email(email,check_deliverability= False)
        return infos.normalized
    except EmailNotValidError as e:
        print(f"Email invalide : {str(e)}")

def hash_password(passwordvalid):
    password_bytes = passwordvalid.encode('utf-8')
    salt= bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)

    if bcrypt.checkpw(password_bytes, hashed):
        print("hash avec succes !")
    else:
        print("erreur")
    return hashed


def main():
    # menu principal admin
    while True:
        afficher_menu()
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
            menu_categories()
        elif choix == 2:
            menu_produits()
        elif choix == 3:
            recherches()
        elif choix == 4:
            indique_mouvement()
        elif choix == 5:
            historiques()
        elif choix == 6:
            liste_user()
        elif choix == 7:
            menu_connect()
            break


def menu_connect():
    print("\n -----'Formulaire D'inscription' ----") 
    print("1. Connexion ")
    print("2. Quitter")


def nav_connect():
    while True:
        menu_connect()
        while True:
            try:
                choix=int(input("Veuillez choisir un nombre entre 1 et 2 : "))
                if 1 <= choix <=2:
                    break
                else:
                    print("incorrect! choisi bien")
            except ValueError:
                print("Invalid! Veuillez resaisir correctement")

        if choix == 1:
            login()
        elif choix == 2:
            fermeture_connextion()
            break
        
def menu_inscription():
    print("\n -----'Formulaire D'inscription' ----") 
    print("1. Inscription")
    print("2. Quitter")

def user_menu():
    print("\n --Gestion du boutique Pro--")
    print("1. categories")
    print("2. Produits")
    print("3. recherches produits correspondant categories ")
    print("4. Indiquer le mouvement")
    print("5.Deconnection")
    
def users():
    # menu principal user
    while True:
        user_menu()
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
            menu_categories()
        elif choix == 2:
            menu_produits()
        elif choix == 3:
            recherches()
        elif choix == 4:
            indique_mouvement()
        elif choix == 5:
            menu_connect()
            break
        break


def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


#inscription
def registre():
    cursor = connection.cursor()
    print("Formulaire d'inscription")

    nom = input("Votre nom : ")
    prenom = input("Votre prenom : ")
    email = input("Votre mail : ")
    while True:
        try:
            emailValide = controle_email(email)
            if email == emailValide:
                print("mail au top")
                break
        except  ValueError as e:
            print(f"Oups erreur niveau mail {e}")
            break

    password = input("Votre mot de passe : ")
    password_hash = hash_password(password)
    print(password)

    role = input("Votre role admin/utilisateur : ")
    
    query = """
        INSERT INTO users (nom, prenom, email, password, role)
        VALUES (%s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(query, (nom, prenom, email, password_hash, role))
        connection.commit()
    except Exception as e:
        print(" ERREUR SQL :", e)
    print("Inscription avec success !")
    cursor.close()
    return nav_connect()


#connection
def login():
    cursor = connection.cursor(dictionary=True)
    print("\n--- Connexion utilisateur ---")

    while True:
        email = input("Votre email : ").strip()

        if not email:
            print(" L'email est obligatoire")
            continue

        if not controle_email(email):
            print(" Format email invalide")
            continue

        break

    while True:
        password = input("Votre mot de passe : ").strip()

        if not password:
            print(" Le mot de passe est obligatoire")
            continue

        break

    query = """
        SELECT id_user, nom, prenom, email, password, role
        FROM users
        WHERE email = %s
    """
    cursor.execute(query, (email,))
    user = cursor.fetchone()

    if not user:
        print("2 Aucun compte associé à cet email")
        cursor.close()
        return

    if not verify_password(password, user['password']):
        print("Mot de passe incorrect")
        cursor.close()
        return

    print(f" Bienvenue {user['prenom']} ({user['role']})")

    if user['role'] == 'admin':
        main()
    else:
        users()

    cursor.close()


def liste_user():
    cursor = connection.cursor(dictionary=True)

    query ="""
            select id_user, nom, prenom,email,role
            from users
            """
    cursor.execute(query)
    users = cursor.fetchall()
    cursor.close()

    for user in users:
        print(f"ID : {user['id_user']}")
        print(f"Nom : {user['nom']}")
        print(f"Prenom : {user['prenom']}")
        print(f"Mail : {user['email']}")
        print(f"Role : {user['role']}")

#menu choix
def afficher_menu():
    print("\n --Gestion du boutique Pro--")
    print("1. categories")
    print("2. Produits")
    print("3. recherches produits correspondant categories ")
    print("4. Indiquer le mouvement")
    print("5.historiques")
    print("6.Listes personnes users")
    print("7.Deconnection")

#menu categorie
def menu_categories():
    print("\n --Gestion du boutique Pro--")
    print("\n CATEGORIES")
    print("1. Ajouter categories")
    print("2. modifier")
    print("3. supprimer ")
    print("4. Lister ")
    print("5. Deconnexion")
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
        list_categories()
        try:
            id_categorie = int (input("indiquer l'id du categorie a modifier"))
            break
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
        list_categories()
        try:
            id_categorie = int (input ("Indiquez l'id de la ligne que vous voulez supprime : "))
            break
        except ValueError:
            print("oups ! erreur , ressaisi")
    query = """
            delete from categories
            where id_categorie = %s
        """
    cursor.execute(query, (id_categorie ))
    connection.commit()
    cursor.close()

#liste des categories
def list_categories():
    cursor = connection.cursor(dictionary=True)  
    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()
    cursor.close()

    for cat in categories:
        print(f"ID: {cat['id_categorie']}")
        print(f"Nom: {cat['nom_categorie']}")
        print("-" * 20)  

#recherches  
def recherches():
    cursor = connection.cursor(dictionary=True)

    while True:
        try:
            id_produit = int(input("Indiquez l'id du produit à rechercher : "))
            break
        except ValueError:
            print("Erreur! Veuillez bien indiquer l'id")

    nom_produit = input("Ou donnez le nom du produit (optionnel) : ").lower()
    if nom_produit.strip() == "":
        nom_produit = None

    query = """
        SELECT *
        FROM produits pro
        JOIN categories cat ON pro.id_categorie = cat.id_categorie
        WHERE pro.id_produit = %s OR (%s IS NOT NULL AND pro.nom_produit = %s)
    """
    cursor.execute(query, (id_produit, nom_produit, nom_produit))
    produit = cursor.fetchone()

    if produit:
        print("Produit trouvé :")
        for key, value in produit.items():
            print(f"{key}: {value}")
    else:
        print("Aucun produit trouvé avec cet ID ou nom.")

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
    print("6.liste des produits")
    print("7. retour accueil")
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
        elif choix == 6:
            list_produits()
        elif choix == 7:
            print("bye bye")
            break
        
# ajouter produits
def produits():
    cursor = connection.cursor()
    print("\n ajouter des produits")
    while True:
        nom_produit = input("Donner le nom du produit : ")
        if nom_produit.strip() != "":
            break
        print("Erreur : le nom ne peut pas être vide")

    while True:
        try:
            prix_produit = float(input("Donner le prix du produit : "))
            break
        except ValueError:
            print("Erreur : prix invalide")

    while True:
        description_produit = input("Donner la description du produit : ")
        if description_produit.strip() != "":
            break
        print("Erreur : description vide")

    while True:
        try:
            quantite_produit = int(input("Donner la quantité du produit : "))
            break
        except ValueError:
            print("Erreur : quantité invalide")

    print(list_categories())
    while True:
        try:
            id_categorie = int(input("Donner l'id de la catégorie : "))
            break
        except ValueError:
            print("Erreur : id catégorie invalide")

    query = """
    INSERT INTO produits (nom_produit, prix_produit, description_produit, quantite_produit, id_categorie)
    VALUES (%s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(query, (
            nom_produit,
            prix_produit,
            description_produit,
            quantite_produit,
            id_categorie
        ))
        connection.commit()
    except Exception as e:
        print("erreur venant de list ",e)
    cursor.close()

    print("Produit ajouté avec succès")

# marquer le status du produits
def marquer_status_produit():
    cursor = connection.cursor()
    while True:
        print("Marquer le status enrupture si c'est epuiser ")
        try:
            id_produit = int(input("Indiquer l'id du produit : "))
            break
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
    try:
        cursor.execute(query, (satus_produit,id_produit))
        connection.commit()
    except Exception as e:
        print(f"erreur {e}")
    cursor.close()

#modifier le produit 
def modifier_produits():
    cursor = connection.cursor()

    while True:
        try:
            id_produit = int(input("indiquer l'id du produit a modifier"))
            break
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

#liste des produits
def list_produits():
    cursor = connection.cursor(dictionary=True)  
    cursor.execute("SELECT * FROM produits")
    produits = cursor.fetchall()
    cursor.close()

    for produit in produits:
        print(f"ID: {produit['id_produit']}")
        print(f"Nom: {produit['nom_produit']}")
        print(f"Prix: {produit['prix_produit']}")
        print(f"Description: {produit['description_produit']}")
        print(f"Quantite: {produit['quantite_produit']}")
        print(f"ID_categorie: {produit['id_categorie']}")
        print("-" * 20)  

# indiquer le mouvement ajouter les
def indique_mouvement():
    cursor = connection.cursor()

    type_mouvement = input("Action (ajouter / retirer) : ").lower()
    quantite = int(input("Quantité du mouvement : "))
    id_produit = int(input("ID du produit : "))
    dateHeure_mouvement = datetime.now()
    cursor.execute(
        "SELECT quantite_produit FROM produits WHERE id_produit = %s",
        (id_produit,)
    )
    result = cursor.fetchone()
    quantite_produit = result[0]
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

    query ="""
            UPDATE produits 
            SET quantite_produit = %s 
            WHERE id_produit = %s"""
    try:
        cursor.execute(query,(nouvelle_quantite, id_produit))
    except Exception as e:
        print("erreur ", e)

    query2 =  """
        INSERT INTO mouvements (type_mouvement, dateHeure_mouvement, quantite, id_produit)
        VALUES (%s, %s, %s, %s)
        """
    try:
        cursor.execute(query2, (type_mouvement, dateHeure_mouvement, quantite, id_produit))
        print(" Quantité récupérée, calculée et mise à jour")
        connection.commit()
    except Exception as e:
        print("erreur ",e)
    cursor.close()

def historiques():
        cursor = connection.cursor(dictionary=True)  
        cursor.execute("SELECT * FROM mouvements")
        mouvements = cursor.fetchall()
        cursor.close()

        for mouvement in mouvements:
            print(f"ID: {mouvement['id_mouvement']}")
            print(f"Quantites: {mouvement['quantite']}")
            print(f"Date et heure: {mouvement['dateHeure_mouvement']}")
            print(f"Action: {mouvement['type_mouvement']}")
            print(f"ID_produit: {mouvement['id_produit']}")

            print("-" * 20) 
def alert():
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM produits WHERE quantite_produit < 5"
    cursor.execute(query)
    produits_faible = cursor.fetchall()
    
    if produits_faible: 
        print(" Alert: le stock est insuffisant pour les produits suivants :")
        for prod in produits_faible:
            print(f"ID: {prod['id_produit']}, Nom: {prod['nom_produit']}, Quantité: {prod['quantite_produit']}")
            print("-" * 20)
    else:
        print("Tous les produits ont une quantité suffisante")

    cursor.close()
    return produits_faible

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
    try:
        cursor.execute(query, (id_produit ))
        connection.commit()
    except Exception as e:
        print("erreur detecter ",e)
    cursor.close()



 # menu principal
while True:
        menu_inscription()
        while True:
            try:
                choix=int(input("Veuillez choisir un nombre entre 1 et 2 : "))
                if 1 <= choix <=2:
                    break
                else:
                    print("incorrect! choisi bien")
            except ValueError:
                print("Invalid! Veuillez resaisir correctement")

        if choix == 1:
            registre()
        elif choix == 2:
            fermeture_connextion()
            break