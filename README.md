# Votre journal de projet

## Entrée de l'enseignant, semaine 7
Au minimum chaque semaine, inscrivez ici vos avancements, problématiques et solutions pour la réalisation du projet d'avion. Vous pouvez inclure des images, du code, des vidéos. J'utiliserais votre journal pour valider vos connaissances et vous assitez lorsque vous avez des problèmes ou questions.

Les fichiers terminants par .md sont en Markdown. Il s'agit d'un langage pour mettre en forme du texte. Un [guide](https://guides.github.com/features/mastering-markdown/) produit par GitHub est disponible. Chaque entrée doit commencer par un titre de niveau 2 (## Entrée semaine x). Vous pouvez effacer mon entrée lorsque vous commencé votre journal. Laissez le dans ce fichier (README.md) pour que GitHub le détecte et l'afficher automatiquement lorsqu'on ouvre ce répertoire.

## Jour 1
* Set up visual studio code avec notre répertoire Git
* Trouver notre idée projet, en discuter avec les professeurs
* Obtenir les composantes nécessaires
* Tester le sonar et son code
* Rechercher, étudier et tester codes MQTT
* Monter les LEDs, Moteurs, et alimentation sur le board
* Trouver un moyen de connecter les deux Pis avec MQTT
* Chercher une facon de tout monter sur les pièces de voiture
* Trouver une manière d'alimenter par USB (chargeur de cell peut-être)
* Penser à coder un code Main()

## Jour 2
* Trouver de la documentation pour l'accéléromètre, trouver comment coder et brancher l'accéléromètre
* Trouver comment faire fonctionner les deux moteurs ensemble
* Monter les moteurs sur les deux roues avec de la colle chaude
* Tests de roues différentes, montages différents
* Tests de code pour le moteur: Deux roues fonctionnels
* Ajout de LEDs, bouton et Sonar
* Sonar et moteurs fonctionnel avec le montage sur le Pi directement et alimentation par la batterie 9V
* Deboggage pour problèmes d'alimentation/puissance
* Trouver une manière de transférer courant de chargeur USB au breadboard

## Jour 3
* Monter la voiture en carton, trouver ou placer les breadboard dans la voiture, et placer les capteurs sur le breadboard selon l'emplacement dans la voiture. Débogger les problèmes lors de déplacement de capteurs
* Lire la documentation sur l'accelerometre et essayer des branchements différents, essayer du code different
* Installer librairies Pi pour l'accelerometre
* Brancher le servo moteur pour tourner la roue avant
* Trouver un nom pour la voiture
* Installer le servo-moteur
* Demander et recuperer des collegues de classes des fils supplémentaires
* Tester nouveaux moteurs plus gros récupérés du prof

## Jour 4
* Copier le code écrit à date sur github
* Installer les breadboard et les composantes dans la voiture. Coller les breadboard au bonne endroit, couper des trous dans la boîte au besoin, arranger les roues.
* Accéléromètre et son code fonctionnel, reste à l'ajouter dans le code main
* Ajout du code de l'acceleromètre dans le code main de la voiture (voituremain.py)
* Réinstaller composantes dans la voiture

## Jour 5
* Trouver un moyen different d'installer la troisieme roue (soudage). Après plusieurs tests de soudage et colle chaude, notre roue devrait soutenir bien le poids
* Penser au fonctionnement du code (loops), remplacer le bouton par un joystick
* Palier au manque de fils en utilisant du tape électrique et du soudage.
* Continuer d'installer et deboguer composantes dans la voiture. Accéléromètre et LEDs fonctionnels
* Deboggage du code accelerometre (Probleme BCM vs board)
* Installer le servo

## Jour 6
* Travailler sur MQTT
* Sonar fonctionnel, reste à faire fonctionner moteurs, installer LCD (il nous manquait des fils femelles à male) et faire fonctionner le joystick
* Moteurs, sonar, LEDs, servo et accelerometre fonctionnel, reste à debogger joystick, installer LCD et coller + coder le servo-moteur 
* Fonctionnement de MQTT : broker et client fonctionnel sur le pi à sophie, reste à installer sur pi dans la voiture et coder boutons page web, javascript
* Debugger problème pi sophie, son OS est corrompu
* Installer LCD, debugger code. Pour le moment rien n'affiche a l'écran 
* Deboggage de ADC et joystick. Le reste des composantes et code fonctionnel
* LCD fonctionnel aussi, coupé trou pour le lcd
* Debogger problème pi corrompu de Sophie. On a du flasher l'OS de son Pi au complet

## Jour 7
* Commencer présentation oral, mettre photos, mots, thème
* Coder fonction acceleration pour calculer l'accélération (j'ai fait une fonction x2 - x1 avec une liste)
* Coller le servo sur la voiture
* Règler les problèmes d'ADC (avec LCD et joystick, conflits)
* Tenter de coder quelque chose de facile pour controler notre voiture a distance (dweet ou flask)
* rechercher sur comment connecter plusieurs composantes i2c ensembles (transformer gpio 19+13+6+5 deviennent pins sda et scl? creation de deux bus differents)
* changer leds dans le code pour indiquer etat davance de la voiture
* Changement des pins sda scl non fonctionnel, remise du filage comme avant. Problème détection i2c comme avant
* Probleme leds avec time.sleep dans le code
* Codage de dweet pour controler voiture, créer page html 
* Tester adc connexion et code avec le Pi à Sophie
* Deboggage html + dweet
* Deboggage servo moteur, dweet pour le reste des composantes fonctionne
* Deboggage flask, connexions, iterateurs pour accelerometre
