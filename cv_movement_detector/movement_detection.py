import time
import cv2
import threading
from pygame import mixer
import keyboard


def play_sound(file):
    mixer.init()
    mixer.music.load(file)
    mixer.music.play()
    while mixer.music.get_busy():  # do while music to finish playing
        if keyboard.read_key() != '':
            mixer.music.stop()
    mixer.stop()


# asynchronous calling of sound player
def alert():
    threading.Thread(target=play_sound, args=['sounds/alarm2.mp3'], daemon=True).start()


def main():
    # Movement detector
    cam = cv2.VideoCapture(0)
    while cam.isOpened():
        ret, frame1 = cam.read()
        time.sleep(0.0001)  # sensibility to movement
        ret, frame2 = cam.read()

        diff = cv2.absdiff(frame1, frame2) # Detects difference in frames (movement)
        gray_scale = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(gray_scale, (5, 5), 0)
        _, threshold = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(threshold, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)

        # draw rectangles around contours
        for c in contours:
            if cv2.contourArea(c) < 5000:
                continue

            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
            alert()

        cv2.imshow('main_cam', frame1)

        if cv2.waitKey(5) == ord(' '):
            break


if __name__ == '__main__':
    main()


