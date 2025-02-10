import time

def countdown(seconds):
    for i in range(seconds, 0, -1):
        print(f"{i}...", end="\r")
        time.sleep(1)
    print("Ready!")
