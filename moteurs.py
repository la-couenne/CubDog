#! /usr/bin/env python
# Script de test des moteurs

import os
import RPi.GPIO as gpio
import time

# on definit les numero de ports Gpio (16 et 20 pour declencher les moteurs)
moteur_gauche = 16
moteur_droit = 20

# on utilise le mode BMC ca veut dire qu on utilise le numero GPIO plutot que sa position physique sur la carte
gpio.setmode(gpio.BCM)
# On definit les ports en sorties
gpio.setup(moteur_gauche, gpio.OUT)
gpio.setup(moteur_droit, gpio.OUT)

# On RaZ tous les ports
gpio.output(moteur_gauche, gpio.LOW)
gpio.output(moteur_droit, gpio.LOW)

os.system('clear') # on utilise la librairie os pour effacer l'ecran
print('  ATTENTION  LE ROBOT EST SUCEPTIBLE DE SE METTRE EN MOUVEMENT !')
time.sleep(4) # on fait une pause de securite pour qu'on securise le robot au besoin
os.system('clear') # on utilise la librairie os pour effacer l'ecran
print(' Lancement du script check.py pour la gestion des mouvements du robot!')
print('')


print('2 moteurs a fond durant X sec..')
gpio.output(moteur_gauche, gpio.HIGH) # les 2 moteurs a fond
gpio.output(moteur_droit, gpio.HIGH)

time.sleep(0.4)

print('On arrete tout..')
gpio.output(moteur_gauche, gpio.LOW) # arret des 2 moteurs
gpio.output(moteur_droit, gpio.LOW)

os.system('clear') # on utilise la librairie os pour effacer l'ecran
