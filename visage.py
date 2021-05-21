#!/usr/bin/python
'''
detecte la position des visages
commentaires sur plusieurs lignes :)
'''
import numpy as np
import cv2

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
        print("")



    cv2.imshow('Image capturee',image) # on affiche l image pour ctrl
    k = cv2.waitKey(30) & 0xff
    if k == 27: # si ESC on sort de la boucle
        break

capture.release()
cv2.destroyAllWindows()