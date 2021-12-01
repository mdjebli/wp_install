

--------------------------------------------------------------------------------------
#1)Présentation de wp_install                                     
-------------------------------------------------------------------------------------
Ce script installe Wordpress sur un serveur distant et sa base de données Mariadb sur un serveur séparé de manière totalement automatisée. 
Ce programme fonctionne depuis un client GNU/Linux de type Debian ou Ubuntu (une portabilité vers d'autres distributions ou vers Windows nécessiterait de changer quelques commandes ou  liens dans le code) et sous GNU/Linux Debian exclusivement en ce qui concerne les serveurs cibles.


-------------------------------------------------------------------------------------
#2)Procédure
-------------------------------------------------------------------------------------
Téléchargez une image d'intallation de Debian et procédez à une installation minimale.
Si vous travaillez avec des machines virtuelles, vous pouvez vous contenter d'une seule installation et cloner la machine (clone intégral).
Attribuez des IP fixes à ces machines (éditez le fichier /etc/network/interfaces)
Vous pouvez garder les noms par défaut de ces machines. Le renommage explicite se fera au lancement du script.

Vous devez autoriser la connexion SSH pour l'utilisateur root. Pour ce faire, veillez à disposer d'un serveur ssh sur le serveur, ouvrez un terminal et éditez le fichier sshd_config :

'''nano /etc/ssh/sshd_config'''

Allez à la ligne débutant par "PermitRootLogin", décommentez-la et ajouter "yes" comme directive. Le programme se charge de recommenter la ligne ultérieurement à des fins de sécurité.

Ensuite, depuis votre client, tapez:

'''ssh-copy-id root@ip_du_serveur_cible'''

et tapez entrée afin de valider l'échange de clé. Le programme pourra alors se connecter en SSH sans intervention manuelle supplémentaire. 
Si un message d'erreur indique: "no identity found", cela signifie que vous ne possédez pas de clé SSH. En ce cas, tapez:

'''ssh-keygen'''

Vous pouvez valider toutes les options par défaut en tapant entrée. Vous disposerez alors d'une clé à échanger avec le serveur.

Le client doit quant à lui disposer de Python ainsi que d'un module complémentaire, à savoir paramiko, pour envoyer des commandes en SSH depuis Python. Ces logiciels sont installés automatiquement au lancement du programme grâce au script de lancement wp_start.sh. En cas de soucis, tapez ces commandes:
'''sudo apt update && sudo apt upgrade
sudo apt install python3 python3-pip
pip3 install paramiko 
python3 wp_install.py'''

Pour lancer wp_install:
###1- Dézippez l'archive:
'''tar -xvf'''
###2- rendre les scripts executables sur votre machine:
'''chmod +x wp_start.sh wp_install.py'''
###3-Exécutez le programme:
'''./wm_start.sh ou bash wp_start.sh'''

Vous devrez entrer quelques informations au lancement du premier script (votre mot de passe administrateur pour permettre l'installation des paquets pré-requis) et peu après, au lancement du script principal, à savoir noms et adresses IP des serveurs, nom d'utilisateur et mot de passe pour la base MariaDB et, enfin, nom de la base de données.

----------------------------------------------------------------------------------------------------
#3)Parefeu
Vous pouvez activer le parefeu sur vos serveurs distant avec un ensemble de règles minimal 
----------------------------------------------------------------------------------------------------
Vous pouvez activer le parefeu sur vos serveurs distant avec un ensemble de règles minimal permettant le bon fonctionnement de wordpress.
Pour ce faire, vous devrez fournir l' adresse de serveur DNS utilisé par vos serveurs. Si vous souhaitez utiliser vos propres scripts de règles iptables, copiez les dans le dossier caché .wp et donnez leur le même noms que les fichiers déja présents (wpfw.source et mariafw.source) après avoir renommé ou supprimé ces derniers.
Le fichier parefeu.service crée un service systemd pour le chargement de ces règles au démarrage. Si vous souhaitez utiliser votre propre fichier, nommez-le parefeu.service également. Notez que ce service s'appellera dorénavant parefeu.service. Si cela ne vous convient pas, vous devrez le renommer ultérieurement. 

Notez aussi que l'accès SSH sera configuré uniquement pour le client que vous utilisez pour lancer ce script. Si vous avez reçu votre adresse ip par dhcp, il se peut que vous perdiez cet accès ultérieurement suite à une nouvelle attribution d'adresse. Prenez donc vos précautions en la matière, afin, soit de conserver votre adresse actuelle de manière pérenne, soit en paramétrant vos règles de pare-feu de manière adéquate après l'installation.


---------------------------------------------------------------------------------------------------
#4)Dépannage
---------------------------------------------------------------------------------------------------
A priori, vous ne devriez faire face à aucune difficulté dès lors que les pré-requis sont satisfaits et que les informations fournies sont correctes. 
Le principal problème potentiel consiste dans l'incapacité de worpdress à communiquer avec sa base de données. Pour ce faire, deux conditions doivent être réunies:
i) MariaDB doit accepter les connexions non-locales. Assurez-vous que la directive bind-address du fichier /etc/mysql/mariadb.conf.d/50-server.cnf du serveur MariaDB soit positionnée à la valeur 0.0.0.0
ii)L'utilisateur de la base données MariaDB doit être parfaitement configuré. Assurez vous que les informations apparaissant dans le fichier wp-config.php soient correctes ou recréez un utilisateur de base de données sur la bases des informations qui y apparaissent. Le format d'identification de ce dernier doit être le suivant nom_utilisateur@IP_du_serveur_wordpress. Notez bien qu'il s'agit de l'IP du serveur Wordpress et non du serveur Mariadb.




