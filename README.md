# noSql
* redis ne fonctionne pas bien pour le chemin et pour vérifier l'intégrité des fichiers car il renvoie un dictionnaire ou un fichier json il ne peut donc pas avoir 2 fois les memes valuers. Si le fichier est passé plusieurs fois par le même état ça ne sera pas enregistré par redis a moins de stocker chaque chemin de chaque fichier dans un tableau avec comme nom le nom du fichier
