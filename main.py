import math
import sys
import threading

import pyautogui as py
from pynput import keyboard

running = False
locations = []
prev_location = (0, 0)

(screen_x, screen_y) = py.size()
# Character is in the middle of the screen.
(X, Y) = (screen_x / 2, screen_y / 2)


def move_to_closest_location(req):
    return min(locations, key=lambda item: math.dist(item, req))


def watch_positions():
    global running, prev_location

    while running:
        h = int(X)
        k = int(Y)
        (x, y) = py.position()
        position = (x, y)

        a = 1000
        b = 220

        result = checkpoint(h, k, x, y, a, b)
        print(result)
        if result <= 1:
            prev_location = position
            print('Koy cocugu gitsin.', position)
        else:
            print('Disarida', position)

            if prev_location != (0, 0):
                py.moveTo(prev_location, _pause=False)


def checkpoint(h, k, x, y, a, b):
    # Formula: (x-h)^2/a^2 + (y-k)^2/b^2 <= 1
    # Example: Given an ellipse centered at(h, k), with semi - major axis a,
    # semi-minor axis b, both aligned with the Cartesian plane.The task is to determine if the point (x, y) is within
    # the area bounded by the ellipse.

    # Input: h = 0, k = 0, x = 2, y = 1, a = 4, b = 5
    # Output: Inside

    # Input: h = 1, k = 2, x = 200, y = 100, a = 6, b = 5
    # Output: Outside

    p = ((math.pow((x - h), 2) // math.pow(a, 2)) +
         (math.pow((y - k), 2) // math.pow(b, 2)))
    # == 1: On the ellipse.
    # > 1: Outside.
    # else: Inside.
    return p


def stop():
    global running
    running = False
    sys.exit()


def on_press(key):
    global running

    if key == keyboard.Key.esc:
        stop()

        return False

    try:
        k = key.char  # Single-char keys.
    except:
        k = key.name
    if k in ['shift']:
        running = not running
        threading.Thread(target=watch_positions).start()
    elif k in ['v']:
        for i in range(360):
            if i % 6 == 0:
                py.moveTo(locations[i])


with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
