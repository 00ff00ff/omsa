from picamera import PiCamera
from time import sleep

# Import biblioteki SimpleCV
from SimpleCV import Camera, VideoStream, Color, Display, Image, VirtualCamera

def RecordAndSave():
    camera = PiCamera()
    camera.start_preview()

    print('Recording started')
    camera.start_recording('video.h264')
    sleep(5)
    print('Recording stopped')
    camera.stop_recording()


def MainLoop():
    # Pierwsza klatka
    first = cam.getImage()

    # Druga klatka
    second = cam.getImage()
    
    # Roznica miedzy nimi
    diff = second - first

    diff = diff.grayscale()
    
    # Kazdy piksel ma kolor 0 albo 255 (czarny or bialy)
    diff = diff.binarize(100)

    # Odwraca kolorki
    diff = diff.invert()

    return diff

RecordAndSave()

# Plik .mp4 jako wirtualna kamera
cam = VirtualCamera('video.h264', 'video')
FinalDiff = cam.getImage() - cam.getImage()
FinalDiff = FinalDiff.grayscale()
FinalDiff = FinalDiff.binarize(100)
FinalDiff = FinalDiff.invert()
fps = 1

while True:
    
    diff = MainLoop()
    
    # Wyswietlanie roznicy, czyli w tym przypadku ruchomych obiektow na niebie
    FinalDiff = FinalDiff + diff
    FinalDiff.show()
    fps+=1

