#!/usr/bin/python
# suivi du regard
import Adafruit_PCA9685  # Le module PCA9685 pour le ctrl des servo
import cv2  # OpenCV pour le ttt des img
#import numpy as np
import time


print("Debut")

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

# Chemin du fichier .xml qui contient des modeles de visages (classifier)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#face_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

capture = cv2.VideoCapture(0) # flux de la webcam (utiliser VideoCapture(1) pour faire plusieurs flux)

while 1:
    ret, img = capture.read() # on recupere une image du flux video
    #image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # on la met en nuances de gris pour gagner du temps de traitement
    image = img # tester si c est vraiment utile de ne pas la laisser en couleur...

    newsize = (int(image.shape[1]/1.5), int(image.shape[0]/1.5)) # nouvelle taille: essayer entre 1.5 et 2
    image = cv2.resize(image, newsize) # fonction qui redimensionne pour gagner en temps de calcul

    # la fonction detectMultiScale retourne les positions de visages detecter avec les modeles contenu dans le .xml
    faces = face_cascade.detectMultiScale(image, 1.4, 3) # voir internet pour les differents parametres




    for (x,y,w,h) in faces: # on recupere les coordonnees de la tronche detectee
        cv2.rectangle(image,(x,y),(x+w,y+h),(255,7,8),2) # on dessine un rectangle
        print("X: " + str(x))
        print("Y: " + str(y))
        print("H: " + str(h) + " donc la distance")
        #cv2.circle(image,(x + (x/2), y),(5),(255,255,8),0) # on dessine un cercle mais ca BUG
        print("")

        #xxxxxxxxxxx
        # deplacements horizontaux de la tete:
        if x < 120:
            servo_actuel_horizontal = (servo_actuel_horizontal + 3)
            if servo_actuel_horizontal > servo_max_gauche:
                servo_actuel_horizontal = servo_max_gauche

        if x > 170:
            servo_actuel_horizontal = (servo_actuel_horizontal - 3)
            if servo_actuel_horizontal < servo_max_droit:
                servo_actuel_horizontal = servo_max_droit

        pwm.set_pwm(0, 0, servo_actuel_horizontal) # pour horizontal
        print("Nouvelle position du servo horizontal: " + str(servo_actuel_horizontal))


        # deplacements verticaux de la tete:
        print("Pr ctrl servo_actuel_vertical: " + str(servo_actuel_vertical))
        if y > 95:
            servo_actuel_vertical = (servo_actuel_vertical + 2)
            if servo_actuel_vertical > servo_max_bas:
                servo_actuel_vertical = servo_max_bas

        if y < 55:
            servo_actuel_vertical = (servo_actuel_vertical - 2)
            if servo_actuel_vertical < servo_max_haut:
                servo_actuel_vertical = servo_max_haut

        pwm.set_pwm(1, 0, servo_actuel_vertical) # pour vertical
        print("Nouvelle position du servo vertical: " + str(servo_actuel_vertical))
        #xxxxxxxxxxx

    cv2.imshow('Image capturee',image) # on affiche l image pour ctrl
    k = cv2.waitKey(30) & 0xff
    if k == 27: # si ESC on sort de la boucle
        break

capture.release()
cv2.destroyAllWindows()
print("fin")