#!/usr/bin/env python
'''
Suivi de la couleur bleue, par la tete pour le mouvement vertical, par les 2 moteurs pour l horizontal

'''
import Adafruit_PCA9685  # Le module PCA9685 pour le ctrl des servo
import time
import cv2  # OpenCV pour le ttt des img
import numpy as np
import cv2.cv as cv
import os
import RPi.GPIO as gpio  # Ctrl des Gpio pour les moteurs

pwm = Adafruit_PCA9685.PCA9685()  # Initialiser en utilisant l adresse I2C par defaut (0x40)
pwm.set_pwm_freq(60)  # Set frequency to 60hz, good for servos
# Ebat max des servo:
servo_max_droit = 250
servo_max_gauche = 550
servo_max_haut = 500
servo_max_bas = 900

# on recentre les 2 servo:
pwm.set_pwm(0, 0, 400) # pour horizontal: (num_du_servo_0, 0, impulsions)
pwm.set_pwm(1, 0, 600) # pour vertical: (num_du_servo_1, 0, impulsions)
servo_actuel_horizontal = 400  # on modifiera cette variable pour deplacer la tete
servo_actuel_vertical = 600
time.sleep(1)


# parametres pour la gestion des 2 moteurs
# on definit les numero de ports Gpio (16 et 20 pour declencher les moteurs)
moteur_gauche = 16
moteur_droit = 20
marche_mot_g = 0 # si > 0 le moteur gauche tournera (afin de ne pas bloquer le
marche_mot_d = 0 #  script le temps de le faire tourner qques secondes..)

# on utilise le mode BMC ca veut dire qu on utilise le numero GPIO plutot que sa position physique sur la carte
gpio.setmode(gpio.BCM)
# On definit les ports en sorties
gpio.setup(moteur_gauche, gpio.OUT)
gpio.setup(moteur_droit, gpio.OUT)

# On RaZ tous les ports
gpio.output(moteur_gauche, gpio.LOW)
gpio.output(moteur_droit, gpio.LOW)

print('  ATTENTION  LE ROBOT EST SUCEPTIBLE DE SE METTRE EN MOUVEMENT !')
time.sleep(4) # on fait une pause de securite pour qu'on securise le robot au besoin



# on extrait la position X et Y de la couleur bleue
capture = cv2.VideoCapture(0) # flux de la webcam (utiliser VideoCapture(1) pour faire plusieurs flux)

while 1:
    ret, image = capture.read() # on recupere une image du flux video
    newsize = (int(image.shape[1]/1.5), int(image.shape[0]/1.5)) # nouvelle taille: essayer entre 1.5 et 2
    image = cv2.resize(image, newsize) # fonction qui redimensionne pour gagner en temps de calcul

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) # on converti l image en HSV dans $hsv

    # on definit des seuils de couleurs bleues en HSV
    bleu_bas = np.array([110,50,50])
    bleu_haut = np.array([130,255,255])

    bleu = cv2.inRange(hsv, bleu_bas, bleu_haut) # on filtre que le bleu dans l image $hsv que l on met dans $bleu
    cv2.imshow('Ctrl vision de la couleur',bleu) # on affiche l image pour ctrl


    # on trouve le contour de la couleur
    contour = cv2.findContours(bleu.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    #print(contour)


    # et on calcule un cercle autour de ce contour
    centre = max(contour, key=cv2.contourArea)
    ((x, y), radius) = cv2.minEnclosingCircle(centre)
    #print(radius)


    if radius > 10: # seuil minimum avant de dessiner le cercle
        cv2.circle(image, (int(x), int(y)), int(radius), (0, 255, 255), 2)  # cercle jaune
        cv2.circle(image, (int(x), int(y)), int((radius / radius) + 1), (255, 255, 255), 2)  # point blanc
        print("Distance: " + str(radius))
        print("X: " + str(x))
        print("Y: " + str(y))
        print("")









    x = int(x)
    y = int(y)
    # on utilise les 2 moteurs pour les deplacements horizontaux:
    if x < 150:
        print('GO moteur droit car x < 150..')
        marche_mot_d = 10 # definit un temps de rotation




    if x > 300:
        print('GO moteur gauche car x > 300..')
        marche_mot_g = 10 # definit un temps de rotation



    if marche_mot_g > 0:
        gpio.output(moteur_gauche, gpio.HIGH) # moteur gauche a fond
        marche_mot_g = (marche_mot_g - 1)
        print("On continue moteur gauche car $marche_mot_g = " + str(marche_mot_g))
    else:
        gpio.output(moteur_gauche, gpio.LOW) # si marche_mot_g = 0 on arrete le moteur gauche
        print("STOP moteur gauche.. (Pour ctrl $marche_mot_g = " + str(marche_mot_g))


    if marche_mot_d > 0:
        gpio.output(moteur_droit, gpio.HIGH) # moteur droit a fond
        marche_mot_d = (marche_mot_d - 1)
        print("On continue moteur droit car $marche_mot_d = " + str(marche_mot_d))
    else:
        gpio.output(moteur_droit, gpio.LOW) # si marche_mot_d = 0 on arrete le moteur droit
        print("STOP moteur droit.. (Pour ctrl $marche_mot_d = " + str(marche_mot_d))





    # deplacements verticaux de la tete:
    #print("Pr ctrl servo_actuel_vertical: " + str(servo_actuel_vertical))
    if y > 190:
        servo_actuel_vertical = (servo_actuel_vertical + 5)
        if servo_actuel_vertical > servo_max_bas:
            servo_actuel_vertical = servo_max_bas

    if y < 80:
        servo_actuel_vertical = (servo_actuel_vertical - 5)
        if servo_actuel_vertical < servo_max_haut:
            servo_actuel_vertical = servo_max_haut

    pwm.set_pwm(1, 0, servo_actuel_vertical) # pour vertical
    #print("Nouvelle position du servo vertical: " + str(servo_actuel_vertical))






    cv2.imshow('image',image)



    '''
    x = 100
    y = 100
    w = 200
    h = 200
    cv2.rectangle(image,(x,y),(x+w,y+h),(255,7,8),2) # on dessine un rectangle
    '''



    k = cv2.waitKey(30) & 0xff
    if k == 27: # si ESC on sort de la boucle
        break

capture.release()
cv2.destroyAllWindows()