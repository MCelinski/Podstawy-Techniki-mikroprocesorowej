#Import bibliotek
# biblioteka machine służy do kotrolowania pinów GPIO
from machine import Pin,PWM
import utime
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import framebuf #biblioteka potrzebna do przesłania danych na wyświetlacz
import math
import utime
# Rozdzielczość wyświetlacza
WIDTH  = 128 
HEIGHT = 64

speaker = PWM(Pin(15)) #deklaracja  input buzzera
sda=machine.Pin(0)     #deklaracja lini danych
scl=machine.Pin(1)     #deklaracja lini zegara
i2c=machine.I2C(0,sda=sda, scl=scl, freq=400000)#deklaracja magistrali I2C
oled = SSD1306_I2C(128, 64, i2c)
oled.text("STechiezDIY !!!",5,5)
oled.text("Pico",5,15)
oled.text("HCSR04",5,25)
oled.text("SSD1306",5,35)
trigger = Pin(3, Pin.OUT) #deklaracja impulu wyzwolenia. W naszym przypadku do wysłania fali 
echo = Pin(2, Pin.IN) #deklaracja pinu echo. Służy on do odebrania wracającego sygnału 
def get_distance():
   trigger.low()#ustawienie trigger pinu na stan niski
   utime.sleep_us(2)#zapauzowanie na 2s
   trigger.high()#ustawienie pinu trigger na stan wysoki na 5s i zatrzymanie go 
   utime.sleep_us(5)
   trigger.low()
  #Jeśli nie zostanie odebrany żaden impuls echa,
  #zaktualizuj zmienną, signaloff, tak aby zawierała czas w ms
   while echo.value() == 0:
       signaloff = utime.ticks_us()
  #Kolejna pętla while,sprawdza czy echo zostało odebrane.
   while echo.value() == 1:
       signalon = utime.ticks_us()
   timepassed = signalon - signaloff # zmienna przechowywujaca czas w jakim sygnał wyszedł, odbił się i wrócił
   distance = (timepassed * 0.0343) / 2 #obliczanie odległości na podstawie czasu i prędkości dźwięku
   print("The distance from object is ",distance,"cm")
   return distance
while True:
   #implementacja wyświetlania odległości na wyświetlaczu 
   oled.fill(0)   
   ret_val = get_distance()
   oled.text("Distance:",0,0)
   oled.text(str(ret_val) + " cm",0,10) 
   oled.show()
   utime.sleep(1)
   #implementacja wykrywania odległości mniejszej niż 20cm i działanie buzzera
   if get_distance() < 2000:
        speaker.duty_u16(3000)
        speaker.freq(1700)
        utime.sleep(0.05)
        speaker.duty_u16(0)
        utime.sleep(get_distance() / 1000)
   