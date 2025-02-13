import multiprocessing
import pyttsx3
import keyboard
from pynput.keyboard import Key, Listener

def sayFunc(phrase):
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)
    engine.say(phrase)
    engine.runAndWait()

def say(phrase):
	
    p = multiprocessing.Process(target=sayFunc, args=(phrase,))
    p.start()
    while p.is_alive():
        if keyboard.is_pressed('q') or keyboard.is_pressed("space") or keyboard.is_pressed("enter"):
            p.terminate()
        else:
            continue
    p.join()

# say("this process is running  right now")