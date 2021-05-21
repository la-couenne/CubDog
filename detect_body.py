#!/usr/bin/python
# -*- coding: utf-8 -*-
# détection d'humains et suivi avec la tête du robot
# source: https://www.pyimagesearch.com/2015/11/09/pedestrian-detection-opencv/
# Pour installer imutils: sudo pip install imutils Puis pip install --uppgrade imutils

# # # # # # #
#
# A faire: si perd l'humain > 6sec -> retour tete neutre (à 400)
#
# # # # # # #

from __future__ import print_function # pour qu'il soit compatible avec python 2.7 et 3
from imutils.object_detection import non_max_suppression
import numpy as np
import Adafruit_PCA9685  # Le module PCA9685 pour le ctrl des servo
import imutils
import cv2
import time
import random

pwm = Adafruit_PCA9685.PCA9685()  # Initialiser en utilisant l adresse I2C par defaut (0x40)
pwm.set_pwm_freq(60)  # Set frequency to 60hz, good for servos
# Ebat max des servo:
servo_max_droit = 270
servo_max_gauche = 530
servo_max_haut = 500
servo_max_bas = 900

# on recentre les 2 servo:
pwm.set_pwm(0, 0, 400) # pour horizontal: (num_du_servo_0, 0, impulsions)
pwm.set_pwm(1, 0, 590) # pour vertical: (num_du_servo_1, 0, impulsions)
servo_actuel_horizontal = 400  # on modifiera cette variable pour deplacer la tete
servo_actuel_vertical = 600
time.sleep(1)

capture = cv2.VideoCapture(0) # flux de la webcam (utiliser VideoCapture(1) pour faire plusieurs flux)
x=80
while 1:
    ret, img = capture.read() # on recupere une image du flux video
    image = img


    hog = cv2.HOGDescriptor() # on initialise le descripteur de l'histogramme des dégragés orientés
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector()) # puis le détecteur de piétons pré-formé

    # on redimensionne l'img (200->2sec de ttt, 400->10sec)
    image = imutils.resize(image, width=min(220, image.shape[1]))
    orig = image.copy()

    # détection des pietons ds l'img en construisant une pyramide d'img avec une échelle = 1.05
    (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4), padding=(8, 8), scale=1.05)

    # on dessine les rectanges autour des piétons détectés (à ce stade il peut y avoir plusieurs rect pour un piéton)
    for (x, y, w, h) in rects:
        cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)
        print("X: " + str(x))
        print("Y: " + str(y))
        print("H: " + str(h) + " de distance")
        print("Position horizontale tete: " + str(servo_actuel_horizontal) + " et position humain: " + str(x))
        # deplacements horizontaux de la tete:
        if x < 60:
            servo_actuel_horizontal = (servo_actuel_horizontal + 6)
            if servo_actuel_horizontal > servo_max_gauche:
                servo_actuel_horizontal = servo_max_gauche
                x = 80
        if x > 100:
            servo_actuel_horizontal = (servo_actuel_horizontal - 6)
            if servo_actuel_horizontal < servo_max_droit:
                servo_actuel_horizontal = servo_max_droit
                x = 80
        pwm.set_pwm(0, 0, servo_actuel_horizontal) # mouvement tete horizontal
        #pwm.set_pwm(1, 0, servo_actuel_vertical) # pour vertical
        print("")



    # On vérifie si un rectangle est contenu ds un autre, ds ce k on le supprime (appelé supression non-maxima)
    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
    pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

    # on dessine le rectangle final
    for (xA, yA, xB, yB) in pick:
        cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)


    #cv2.imshow("Before NMS", orig) # ctrl img avant supression non-maxima (plusieurs rectangles)
    cv2.imshow("After NMS", image) # ctrl img finale


    k = cv2.waitKey(30) & 0xff
    if k == 27: # si ESC on sort de la boucle
        break


capture.release()
cv2.destroyAllWindows()