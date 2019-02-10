#-*- coding: utf-8 -*-#
# 4 wire SPI interface
#  RASPBERRY PI GPIO >>> SH1106 1.3 inch display
# 3.3v P1-17 3.3v    ->- VCC  alimentaiton 3,3 Volts
# RES  P1-18 GPIO-24 ->- RES  remise à l'état initial de l'afficheur (reset)
# MOSI P1-19 GPIO-10 ->- MOSI sortie des données vers l'affichage
# MISO P1-21 GPIO-09 ->-      entrée des données : pas utilisé
# A0   P1-22 GPIO-25 ->- SDC  GPIO pour indiquer si on ecrit vers les registres ou vers la mémoire d'affichage
# SCLK P1-23 GPIO-11 ->- CLK  horloge de synchronisaion des données
# CE0  P1-24 GPIO-08 ->- CCS  selection de l'afficheur
# GND  P1-25 GND     ->- GND  referentiel electrique
# CE1  P1-26 GPIO-07 ->-      selection pour un autre péripherique SPI (pas utilisé)
import spidev, time, sys
import RPi.GPIO as GPIO
from PIL import Image

#initialisation des GPIO
GPIO.setmode(GPIO.BOARD)
A0 = 22 #GPIO pin for A0 pin : 0 -> command; 1 -> display data RAM
RESN = 18 #GPIO pin for display reset (active low)
GPIO.setup(A0, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(RESN, GPIO.OUT, initial=GPIO.HIGH)

#initialisation de l'interface SPI
spi = spidev.SpiDev()
spi.open(0, 0) #bus = 0 , device = 0
spi.max_speed_hz = 1000000 #defini la vistesse de transfer (7629 à 125000000)
spi.mode = 0b00 #defini le sequencementdes pin data et clock
#spi.bits_per_word = 8

#fonction d'affichage d'un image PIL
def display_img(image):
    data_slice=[[],[],[],[],[],[],[],[]]
    GPIO.output(A0, 0)
    for p in range (0,8): #l'image est découpée en 8 tranches horizontales de 8 pixels
        data_set = []
        for c in range (0,128): #chaque tranche fait 8x128 px
            by = 0x00
            for b in range (0,8):
                by = by>>1 | (image.getpixel((c, p*8+b))& 0x80)
            data_set.append(by)
        data_slice[p]=data_set
    spi.xfer([0xAF]) #active l'afficheur (0xAE pour l'éteindre)
    for p in range (0,8):
        GPIO.output(A0, 0)
        spi.xfer([0xB0+p, 0x02, 0x10]) #initialise l'adresse des colonnes
        GPIO.output(A0, 1)
        spi.xfer(data_slice[p]) #transfer 1 tranche de 128x8 pixels

#applicaton d'un impulsion de remise à zéro du circuit sh1106
GPIO.output(RESN, 0)
time.sleep(0.1)
GPIO.output(RESN, 1)
time.sleep(0.1)

try:
    while True:
        file = input("filename : ") #ouverture du fichier, en python 2.x : raw_input
        img = Image.open(file).convert('1') #ouverture et conversion en noir et blan
        display_img(img)
except:
    print("cause de l'arrêt du programme : ", sys.exc_info())

spi.close()
GPIO.cleanup()

