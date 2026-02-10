Gestion de Stock - Boutique Pro
Description

Application Python/MySQL pour gérer un stock de matériel. Permet :

Gestion des catégories (ajout, modification, suppression, liste)

Gestion des produits (ajout, modification, suppression, liste, statut disponible/enrupture)

Gestion des mouvements de stock (entrée/sortie) avec historique

Alertes pour produits en faible stock (<5 unités)

Recherches par ID ou nom de produit

Structure de la base de données

Tables principales :

categories (id_categorie, nom_categorie, description_categorie)

produits (id_produit, nom_produit, prix_produit, description_produit, quantite_produit, id_categorie, satus_produit)

mouvements (id_mouvement, type_mouvement, dateHeure_mouvement, quantite, id_produit)

Chaque mouvement met à jour le stock et est historisé.

Installation et exécution

Installer les dépendances :

pip install mysql-connector-python


Créer la base boutique_pro et les tables.

Configurer la connexion dans main.py :

connection = mysql.connector.connect(
    host='localhost',
    user='pythonuser',
    password='Python@123',
    database='boutique_pro'
)


Lancer le programme :

python main.py

Fonctionnalités principales

Menu interactif pour gérer catégories, produits et mouvements

Historique des mouvements consultable

Alertes produits à faible stock

Recherche de produit par ID ou nom