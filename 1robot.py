#!/usr/bin/python
# -*- coding: utf-8 -*-
# détection d'humains et suivi avec la tête du robot
# Pour installer imutils: sudo pip install imutils

from imutils.object_detection import non_max_suppression
import Adafruit_PCA9685  # Le module PCA9685 pour le ctrl des servo
import imutils
import numpy as np
import cv2
import time

pwm = Adafruit_PCA9685.PCA9685()  # Initialiser en utilisant l'adresse I2C par defaut (0x40)
pwm.set_pwm_freq(60)  # on définit une fréquence de 60Hz pour le signal des servo
# Ebat max des servo:
servo_max_droit = 270
servo_max_gauche = 530
servo_max_haut = 500
servo_max_bas = 900

# on recentre les 2 servo de la tête:
pwm.set_pwm(0, 0, 400) # pour horizontal: (num_du_servo_0, 0, impulsions)
pwm.set_pwm(1, 0, 590) # pour vertical: (num_du_servo_1, 0, impulsions)
servo_actuel_horizontal = 400  # on modifiera cette variable pour deplacer la tete de gauche à droite
servo_actuel_vertical = 600
time.sleep(1)

capture = cv2.VideoCapture(0) # flux de la webcam (utiliser VideoCapture(1) pour faire plusieurs flux)
x = 80 # pixel si l'humain est pile au milieu du champs de vision
while 1:
    ret, img = capture.read() # on récupère une image du flux video
    hog = cv2.HOGDescriptor() # on initialise le descripteur de l'histogramme des dégragés orientés
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector()) # puis le détecteur de piétons pré-formé inclu ds imutils
    img = imutils.resize(img, width=min(220, img.shape[1])) # on redimensionne l'img (200->2sec de ttt, 400->10sec)

    # détection des pietons ds l'img en construisant une pyramide d'img avec une échelle = 1.05
    (rects, weights) = hog.detectMultiScale(img, winStride=(4, 4), padding=(8, 8), scale=1.05)

    # on dessine les rectanges autour des piétons détectés (à ce stade il peut y avoir plusieurs rect pour un piéton)
    for (x, y, w, h) in rects:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        print("X: " + str(x))
        print("Y: " + str(y))
        print("H: " + str(h) + " de distance")
        print("Position horizontale tete: " + str(servo_actuel_horizontal) + " et position humain: " + str(x))
        print("")
        # deplacements horizontaux de la tete:
        if x < 60:
            servo_actuel_horizontal = (servo_actuel_horizontal + 6)
            if servo_actuel_horizontal > servo_max_gauche:
                servo_actuel_horizontal = servo_max_gauche
        if x > 100:
            servo_actuel_horizontal = (servo_actuel_horizontal - 6)
            if servo_actuel_horizontal < servo_max_droit:
                servo_actuel_horizontal = servo_max_droit
        pwm.set_pwm(0, 0, servo_actuel_horizontal) # mouvement tete horizontal

    cv2.imshow("Vision", img) # ctrl img finale

    k = cv2.waitKey(30) & 0xff # si ESC on sort de la boucle
    if k == 27:
        break
capture.release()
cv2.destroyAllWindows()