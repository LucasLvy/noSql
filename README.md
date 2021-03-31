# noSql
## Prerequisites:
* Pour lancer le projet il faut avoir redis, mongodb, mySQL de lancé ainsi qu'une base de donnée qui s'appelle application_pedagogique qui contient une table element.
* Il faut également mettre son mot de passe sql ligne 30 dans le fichier injector.py et ligne 6 dans le fichier mySQL_data_collector.py.
* Il faut ensuite installer toutes les dépendeances (pymysql, mysql.connector, pymongo, redis)
* Il suffit maintenant de lancer le script execute_project.py et toutes les 5 minutes le script injectera les données dans la base sql, mongodb et redis, les traitera et affichera les résultats. Le fichier de données devra s'appeler jeuDeDonnees_1.log et il faut éviter d'insérer 2 fois les memes données dans la base de données sql.

## Choix:
* Les données sont insérées telles quelles dans mongodb car il supporte plus de types de valeurs et des requêtes plus complexes il est donc plus facile de traiter les données avec des requêtes qu'avant de les insérer.
* Sur redis nous avons créé 3 dictionnaires, le premier comptant combien d'élément est passé par chaque état, le deuxième compte le nombre d'élément qui est passé par chaque état sur la dernière heure et le dernier c'est une hashmap qui prend en clé l'identifiant:states et en valeur quel chemin il a emprunté.
* Pour avoir le chemin complet d'un fichier redis n'est pas idéal car c'est un système de clé valeur donc une clé ne peut être présente qu'une fois. Ceci implique que si un fichier passe 2 fois par le même état on ne peut pas garder l'ordre de passage, on ne peut donc pas vérifier l'intégrité d'un fichier et le chemin ne sera pas forcément dans l'ordre non plus.

## Conclusion:
Tout est fonctionnel mais mongodb est plus adapté pour les données ou des valeurs peuvent se répéter et où l'ordre est important cependant redis propose des requêtes plus simples et rapides.

Par Quentin GIBON et Lucas LEVY
