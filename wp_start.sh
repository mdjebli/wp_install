#!/bin/bash
jaune='\e[0;33m'

clear
echo -e "${jaune}BONJOUR `whoami` et BIENVENUE DANS WP_START!
Ce petit programme vous permet de saisir les paramètres pour votre installation de Wordpress.
Par ailleurs, il télécharge et installe les logiciels pré-requis pour wp_install (Python). 
Enfin, il lance le script d'installation de wp_install.
Vous aurez à entrer votre mot de passe pour cette procédure. Si vous souhaitez activer le parfeu sur vos serveurs, vous devrez fournir l'adresse du serveur DNS utilisé par vos serveurs"
read -p "Tapez sur Entrée pour continuer..."
clear

read -s -p "Entrez votre mot de passe d'administrateur local:" sudopwd
clear

#Parefeu
parefeu(){
clear
read -p "Souhaitez activer le pare-feu? Si oui, vous devrez entrer l'adresse du serveur DNS utilisé par vos serveurs distants. o/n:" fw_ok
export fw_ok 
if [ "$fw_ok" = "o" ]; then
read -p "Indiquez l'adresse du serveur DNS utilisé par vos serveurs: " dns
export dns
cp .fw/* .
mv wpfw.source wpfw
mv mariafw.source mariafw 
mv parefeu.service.source parefeu.service
iplocale=$(hostname -I | cut -d ' ' -f1)
sed -i s/ADRESSE_IP_SOURCE/$iplocale/g wpfw
sed -i s/ADRESSE_IP_SOURCE/$iplocale/g mariafw
sed -i s/ADRESSE_IP_DE_VOTRE_SERVEUR_DNS/$dns/g wpfw
sed -i s/ADRESSE_IP_DE_VOTRE_SERVEUR_DNS/$dns/g mariafw
sed -i s/ADRESSE_IP_DE_VOTRE_SERVEUR_MARIADB/$ipbdd/g wpfw
sed -i s/ADRESSE_IP_DE_VOTRE_SERVEUR_WORDPRESS/$ipwp/g mariafw

elif [ "$fw_ok" = "n" ]; then
echo  "Vous avez choisi de ne pas activer le parefeu!"
sleep 2 

else 
echo  "Choix incorrect. Le parefeu ne sera pas activé."
sleep 1
clear
fi
}

#Recueil variables
variables(){
clear
#IP et nom du serveur wp
echo  "ENTREZ LES PARAMETRES DU SERVEUR WORDPRESS:"
read -p "Indiquez l'adresse IP du serveur wordpress : " ipwp
export ipwp
read -p "Entrez le nouveau nom de machine du serveur wordpress : " nomsrvwp
export nomsrvwp
clear
#IP et nom du serveur de base de données
echo 'LES PARAMETRES DU SERVEUR MARIADB'
read -p "Indiquez l'adresse IP du serveur de base de données : " ipbdd
export ipbdd
read -p "Entrez le nouveau nom de machine du serveur de base de données : " nomsrvbdd
export nomsrvbdd 
clear
#Infos du serveur de bdd     
echo "ENTREZ LES PARAMETRES DE LA BASE DE DONNEES MARIADB POUR WORDPRESS:"
read -p "Indiquez le nom de l'utilisateur de la base de données (sera requis ultérieurement pour finaliser la configuration sur la page web) : " userwpbdd
export userwpbdd  
read -p "Indiquez le mot de passe de la base de données. Il sera requis ultérieurement pour finaliser la configuration sur la page web : " mdpbdd
export mdpbdd 
read -p "Indiquez le nom de la base de données. Il sera requis ultérieurement pour finaliser la configuration sur la page web: " nombdd
export nombdd
clear
nomMachine=nomMachine
export nomMachine
}

resume(){
clear
echo "RESUME DE LA CONFIGURATION"
echo "L'adresse IP du serveur Wordpress sera: $ipwp, Il sera renommé en " $nomsrvwp
sleep 1
echo "L'adresse IP du serveur de base de données sera: $ipbdd. Il sera renommé en " $nomsrvbdd 
sleep 1
echo "Le mot de passe de la base de données sera: " $mdpbdd 
sleep 1
echo "Le nom d'utilisateur de la base de données sera: "  $userwpbdd 
sleep 1
echo "Le nom de la base de données sera: "  $nombdd
sleep 1 
if [ "$fw_ok" != "o" ]; then
echo "Le parefeu sera désactivé"
sleep 1
else
echo "Le parefeu sera activé"
sleep 1
fi
read -p "Souhaitez-vous poursuivre avec ces paramètres?. Tapez oui, pour continuer, ou toute autre touche pour revenir au début du questionnaire:" variables_ok
}

variables
parefeu
resume

while  [ "$variables_ok" != "oui" ]; do
clear
echo "Pour valider vos paramètres, tapez oui. De nouveau, entrez vos paramètres"
sleep 2
variables
parefeu
resume
done

echo "INSTALLATION DE PYTHON..."
apt list python3-pip | grep install > /dev/null 2>&1
if [ $? != 0 ]; then
echo $sudopwd | sudo -S apt update && sudo apt install python3-pip  -y 
fi
clear
echo "INSTALLATION DE MODULES PYTHON COMPLEMENTAIRES"
pip3 install paramiko termcolor
clear
clear
read -p "Python a été téléchargé. Tapez sur Entrée pour continuer..."
python3 wp_install.py

