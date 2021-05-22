#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import paramiko, sys, os, platform
from os import system, name
import getpass
from time import sleep
import subprocess
import shutil

ipwp = os.environ['ipwp']
nomsrvwp = os.environ['nomsrvwp']
ipbdd = os.environ['ipbdd']
nomsrvbdd = os.environ['nomsrvbdd']
userwpbdd = os.environ['userwpbdd']
mdpbdd = os.environ['mdpbdd']
nombdd = os.environ['nombdd']
nomMachine = os.environ['nomMachine']
fw_ok = os.environ['fw_ok']

#Capture de l'ID de l'utilisateur pour la personnalisation de l'accueil
id_session = getpass.getuser()

########################################################WPINSTALL.PY########################################################################################################
#Ce  script installe Télécharge et installe Wordpress sur un serveur distant ainsi que la base de données sur un serveur séparé#############################################

#variable pour paramiko
cmd = paramiko.SSHClient()
cmd.set_missing_host_key_policy(paramiko.AutoAddPolicy())

 ####################################################################################Définitions des fonctions transverses##################################################################
	
# fonction test de connection_________________________________________________________________________________________________________________________________________________________________
def test_connect():
    print("VERIFICATION DE LA CONNECTIVITE INTERNET DU SERVEUR"+" "+ nomMachine.upper())
    I, O, E = cmd.exec_command('ping -c 3 wordpress.org &> /dev/null')
    sleep(5)
    ok = (O.channel.recv_exit_status() == 0)
    
    if not ok:
        I, O, E = cmd.exec_command('ping -c 3 8.8.8.8 &> /dev/null')
        ok = (O.channel.recv_exit_status() == 0)
        if ok:
            print("Problème dans la résolution de nom. Vérifiez votre DNS ou contactez votre administrateur réseau. Le programme va s'arrêter")
            sleep(5)
            exit()
        else:
              print("\033[2;31;47m Votre connexion est en panne. Le programme va s'arrêter. Vérifiez votre connexion Internet ou contactez votre administrateur réseau")
              sleep(5) 
              exit()
    else:
         print("\033[2;34;47m La connexion internet est OK!")
    sleep(2)
    system('clear')

# Fonction affichage de version de debian________________________________________________________________________________________________________________________________________________________
def DebVer():
    system('clear')
    print("VERIFICATION DE LA COMPATIBILITE DU SYSTEME D\'EXPLOITATION DU SERVEUR" +" "+ nomMachine.upper() )
    I, O, E = cmd.exec_command('if [ -e /etc/debian_version ]; then echo true; fi')
    output = O.read().decode('UTF-8').rstrip()
    
    if output != "true":
        print("Le système d'exploitation distant n'est pas supporté. Il doit être une version de GNU/Linux Debian.\nInstallez Debian et relancez ce script.\n Le programme va s'arrêter." )
        sleep(5)
        exit()
    else:
        I, O, E = cmd.exec_command('cat /etc/debian_version')
        debver = O.read().decode('UTF-8').rstrip()
        print("\033[2;34;47m Le serveur distant est sous Debian, version " + debver) 
    
    sleep(3)
    system('clear')
    
# Fonction renommage machine_______________________________________________________________________________________________________________________________________________________________________
def Renommage_Machine():
    print("RENOMMAGE DU SERVEUR" +" "+ nomMachine.upper() )
    I, O, E = cmd.exec_command('hostname')
    nom = O.read().decode('UTF-8').rstrip()
    print("\033[2;34;47m Le nom du serveur distant avant renommage est: " + nom)
    I, O, E = cmd.exec_command('hostnamectl set-hostname' + " " + nomMachine)
    I, O, E = cmd.exec_command('cat /etc/hosts | grep 127.0.1.1 | cut -f2 ')
    nomhost = O.read().decode('UTF-8').rstrip()
    sleep(5)
    I, O, E = cmd.exec_command( 'sed -i \' s/'+ nomhost +  '/' + nomMachine + ' /g \' /etc/hosts')
    I, O, E = cmd.exec_command('hostname')
    print("\033[2;34;47m Le serveur distant a été renommé en" + " " + nomMachine)
    sleep(3)
    system('clear')
    
# Fonction MAJ______________________________________________________________________________________________________________________________________________________________________________________
def MAJ():
    print("MISE A JOUR DU SYSTEME SUR LE SERVEUR" +" "+ nomMachine.upper() )
    print("\033[2;34;47m Lancement de la procédure de mise à jour du système, veuillez patienter...")
    I, O, E = cmd.exec_command('apt update -y && apt upgrade -y')
    ok = (O.channel.recv_exit_status() == 0)
    if not ok:
        print("\033[2;31;47m Un problème est survenu lors de la mise à jour du système. Le programme va s'arrêter. Contactez votre administrateur système")
        sleep(5)
        exit()
    else:
        print('Nettoyage du système ...' )
        I, O, E = cmd.exec_command('apt autoremove --purge')
        print('Mise à jour du système effectuée avec succès')
        sleep(2)
    system('clear')

# Fonction installation de wordpress___________________________________________________________________________________________________________________________________________________________
def install_wp():
    system('clear')
    print("INSTALLATION ET CONFIGURATION DE WORDPRESS" )
    print("Téléchargement des paquets pré-requis pour l'installation de Wordpress...")
    I, O, E = cmd.exec_command('apt install apache2 php7.3 libapache2-mod-php7.3 php7.3-common php7.3-mbstring php7.3-xmlrpc php7.3-soap php7.3-gd php7.3-xml php7.3-intl \
	php7.3-mysql php7.3-cli php7.3-ldap php7.3-zip php7.3-curl -y')
    ok = (O.channel.recv_exit_status() == 0)
    if ok:
        print("\033[2;34;47m Installation des paquets requis effectuée avec succès.")
    else:
        print("\033[2;31;40m Echec du téléchargement. Le programme sa s'arrêter.")
        exit()
    I, O, E = cmd.exec_command('apt autoremove --purge')
    sleep(2)
    
    print(" Téléchargement de l'archive Wordpress")
    I, O, E = cmd.exec_command('cd /var/www/html && wget -c https://fr.wordpress.org/latest-fr_FR.tar.gz')
    print(O.read().decode('UTF-8').rstrip())
    ok = (O.channel.recv_exit_status() == 0)
    if ok:
        print("\033[2;34;47m L'archive a été téléchargée.")
    else:
        print("\033[2;31;40m Echec du téléchargement. Le programme va s'arrêter.")
        exit()
	
    print("\033[2;34;47m Copie des fichiers")
    I, O, E = cmd.exec_command('cd /var/www/html && tar -xf latest-fr_FR.tar.gz')
    print(O.read().decode('UTF-8').rstrip())
    I, O, E = cmd.exec_command('cd /var/www/html/wordpress/ && mv * ..')
    print(O.read().decode('UTF-8').rstrip())
    I, O, E = cmd.exec_command('chown -R www-data:www-data /var/www/')
    ok = (O.channel.recv_exit_status() == 0)
    if ok:
        print("\033[2;34;47m Tous les fichiers ont été copiés")
    else:
        print("\033[2;31;40m Il semble y avoir eu une erreur, le programme risque de ne pas être fonctionnel.")
    sleep(2)
    
    print("Configuration de Wordpress")
    I, O, E = cmd.exec_command('rm /var/www/html/index.html')
    I, O, E = cmd.exec_command('rm /var/www/html/latest-fr_FR.tar.gz')
    I, O, E = cmd.exec_command('sed -i \'s/votre_nom_de_bdd/' + nombdd + '/g\' /var/www/html/wp-config-sample.php')
    I, O, E = cmd.exec_command('sed -i \'s/votre_utilisateur_de_bdd/' + userwpbdd + '/g\' /var/www/html/wp-config-sample.php')
    I, O, E = cmd.exec_command('sed -i \'s/votre_mdp_de_bdd/' + mdpbdd + '/g\'/var/www/html/wp-config-sample.php')
    I, O, E = cmd.exec_command('sed -i \'s/localhost/' + ipbdd + '/g\' /var/www/html/wp-config-sample.php')
    ok = (O.channel.recv_exit_status() == 0)
    if ok:
        print("\033[2;34;47m Wordpress a été configuré")
        sleep(2)
    else:
        print("\033[2;31;40m Il semble y avoir eu une erreur, le programme risque de ne pas être fonctionnel.")
        sleep(2)
    print("Rechargement du serveur web")
    sleep(2)
    
    I, O, E = cmd.exec_command('systemctl reload apache2')
    ok = (O.channel.recv_exit_status() == 0)
    if ok:
        print("\033[2;34;47m Le serveur web est fonctionnel")
        sleep(2)
    else:
        print("\033[2;31;40m Erreur fatale. Le serveur web ne fonctionne pas. Le programme va s'arrêter.")
        sleep(2)
        exit()
    I, O, E = cmd.exec_command('sed -i \'s/PermitRootLogin/#PermitRootLogin/g\' /etc/ssh/sshd_config')
    system('clear')
    print("\033[2;34;47m Wordpress est installé et préconfiguré!")
    sleep(5)
    system('clear')
# Fonction installation MariaDB________________________________________________________________________________________________________________________________________________________________
def install_bdd():
    print("Le programme va à présent télécharger, installer et configurer la base de données MariaDB")
    sleep(2)
    system('clear')
    print("INSTALLATION ET CONFIGURATION DE MARIADB" )
    print("Téléchargement et installation de Mariadb...")
    I, O, E = cmd.exec_command('apt install mariadb-server -y')
    ok = (O.channel.recv_exit_status() == 0)
    if ok:
        print("\033[2;34;47m Installation des paquets requis effectuée avec succès.")
    else:
        print("\033[2;31;40m Echec du téléchargement. Le programme va s'arrêter.")
        exit()
    print('Nettoyage du système ...' )
    I, O, E = cmd.exec_command('apt autoremove')
    print("Configuration basique de Mariadb")
    I, O, E = cmd.exec_command('sed -i \'s/127.0.0.1/0.0.0.0/g\' /etc/mysql/mariadb.conf.d/50-server.cnf')
    I, O, E = cmd.exec_command('systemctl restart mariadb')
    ok = (O.channel.recv_exit_status() == 0)
    if ok:
        print("\033[2;34;47m MariaDB est installé et configuré.")
    else:
        print("\033[2;31;40m Echec de mariadb. Le programme risque de ne pas être fonctionnel.")
        exit()
    print()
    
    sleep(2)
    print("Création de l'utilisateur et de la table pour Wordpress")
    I, O, E = cmd.exec_command('mysql -u root -e "CREATE DATABASE' + " " + nombdd + " " + '" ')
    I, O, E = cmd.exec_command('mysql -u root -e "GRANT ALL PRIVILEGES on'+""+ nombdd+'.* TO \'     ' + userwpbdd + '\'@\'' + ipwp + '\' IDENTIFIED BY \'' + mdpbdd + '\'"')
    I, O, E = cmd.exec_command('mysql -u root -e "GRANT ALL PRIVILEGES on *.* TO \'' + userwpbdd + '\'@\'' + ipwp + '\' IDENTIFIED BY \'' + mdpbdd + '\'"')
    I, O, E = cmd.exec_command('mysql -u root -e "FLUSH PRIVILEGES"')
    
    I, O, E = cmd.exec_command('sed -i \'s/PermitRootLogin/#PermitRootLogin/g\' /etc/ssh/sshd_config')
    print("La base de données Mariadb est installée et préconfigurée.")
    sleep(2)
    system('clear')
   
   #Fonction reboot
def reboot():
    I, O, E = cmd.exec_command('find /boot -atime -1 | grep "vmlinuz*"')
    ok = (O.channel.recv_exit_status() == 0)
    if ok:
        sleep(2)
        print("Un noyau plus récent a été téléchargé pendant la mise-à-jour. Le serveur distant va redémarrer pour permettre sont chargement")
        sleep(2)
        I, O, E = cmd.exec_command('/sbin/reboot')
    else:
        print("Rechargement du service SSH")
        sleep(2)
        I, O, E = cmd.exec_command('systemctl reload ssh')
        print("Activation du parefeu")
        I, O, E = cmd.exec_command('systemctl start parefeu.service')

def fw():
    if fw_ok == "o":
        print("CONFIGURATION BASIQUE DU FIREWALL")
        I, O, E = cmd.exec_command('hostname -I')
        pfFile = O.read().decode('UTF-8').rstrip()
        str(pfFile)
        subprocess.run(["scp", pfFile, "root@"+pfFile+":/etc/init.d/parefeu.sh"])
        subprocess.run(["scp", "parefeu.service", "root@"+pfFile+":/lib/systemd/system/"])
        os.remove(pfFile)
        I, O, E = cmd.exec_command('systemctl enable parefeu.service')
        ok = (O.channel.recv_exit_status() == 0)
        if ok:
            print("\033[2;34;47m Pare-feu configuré avec un ensemble de règles minimal")
        else:
            print("\033[2;31;40m Il semble y avoir eu une erreur, le parefeu risque de ne pas être fonctionnel.")
        print("")
        sleep(2)
	
###########################Les fonctions intermédiares sont définies ci-dessous##################################################################################################################

# FONCTION_WORDPRESS_SRV_____________________________________________________________________________________________________________________________________________________________________
def WORDPRESS():
    cmd.connect(hostname=ipwp, username='root', key_filename='/home/'+id_session+'/.ssh/id_rsa.pub')
    DebVer()
    Renommage_Machine()
    test_connect()
    MAJ()
    install_wp()
    fw()
    reboot()

# FONCTION_MARIADB_SRV______________________________________________________________________________________________________________________________________________________________________
def MARIADB():
    
    nomMachine = nomsrvbdd
    cmd.connect(hostname=ipbdd, username='root', key_filename='/home/'+id_session+'/.ssh/id_rsa.pub')
    DebVer()
    Renommage_Machine()
    test_connect()
    MAJ()
    install_bdd()
    fw()
    reboot()
###########################################################################################################################################################################
###########################################################################################################################################################################
# _____________________________________________________PROGRAMME_PRINCIPAL__________________________________________________________________________________________________
###########################################################################################################################################################################
###########################################################################################################################################################################
print("\033[2;34;47m \n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

if fw_ok == "o":
    os.rename('wpfw',ipwp)
    os.rename('mariafw',ipbdd)

nomMachine = nomsrvwp
WORDPRESS()
nomMachine = nomsrvbdd
MARIADB()
os.remove("parefeu.service")

###################################################FINALLY!!!###################################
print("\033[2;31;47mWordpress est installé. Rendez-vous sur la page web pour vous connecter!")
print("\033[2;31;47mL'adresse de la page est: " + ipwp )
print("\033[2;31;47mLe nom de la base de données est: " + nombdd)
print("\033[2;31;47mLe nom d'utilisateur est: " +  userwpbdd )
print("\033[2;31;47mLe mot de passe est: "+ mdpbdd )
print("\033[2;31;47mL'adresse de la base de données Mariadb pour Wordpress est: " + ipbdd )
print("\033[2;31;47m Attention! Votre parefeu n'autorise l'accès SSH qu'à votre adresse IP actuelle, à savoir" + iplocale) 
print("\033[2;31;47m Si cette dernière est amenée à changer prochainement, vous n'aurez plus accès à vos serveurs.")
print("\033[2;31;47m Veillez donc à vérifiez vos règles de parefeu (fichier /etc/init.d/parefeu.sh) ou à garder votre adresse actuelle en tant qu'IP fixe!")

print("AU REVOIR "+id_session.upper() +" !")
sleep(3)
exit()
