# Créez une API sécurisée RESTful avec Django REST

Projet 10 / Créez une API sécurisée RESTful en utilisant Django REST. </br> 

Il s'agit d'une API RESTful qui doit permettre aux utilisateurs de remonter 
et suivre des problèmes techniques pour les trois plateformes (site web, 
applications Android et iOS).

L'application doit permettre aux utilisateurs de créer divers projets, 
d'ajouter des utilisateurs à des projets spécifiques, de créer des 
problèmes au sein des projets et d'attribuer des libellés à ces problèmes 
en fonction de leurs priorités, de balises.

Vous retrouverez l'ensemble des informations concerant l'API dans la [documentation Postman de l'API](https://documenter.getpostman.com/view/24417977/2s93K1oemR#7653e7f8-1bdd-4576-bcb7-bce741831aad).

____
## Lancer le programme sous Python 3.9.12 :

### 1. Récupérer le projet :

     git clone https://github.com/Sodev34/Creez_une_API_securise_RESTful_en_utilisant_Django_REST.git

### 2. Dans un terminal, aller dans le dossier de l'application :

     cd Creez_une_API_securise_RESTful_en_utilisant_Django_REST
       
### 3. Créer et activer un environnement virtuel :

     python3 -m venv env

     source env/bin/activate

### 4. Installer les dépendances :

     pip install -r requirements.txt

### 5. Créer un super user :

     cd SoftDeskApi 

     python3 manage.py createsuperuser
     
### 6. Démarrer le serveur : 

     python3 manage.py runserver 

### 7. Naviguer vers l'API :

- Ouvrir un navigateur, et aller à l'adresse du site : http://127.0.0.1:8000/.

- Il est également possible de naviguer dans l'API via la plateforme [Postman](https://www.postman.com/). 
    

  Nom d'utilisateur : UTILISATEURAPI1 </br>
  Mot de passe : API1UTILISATEUR


  




