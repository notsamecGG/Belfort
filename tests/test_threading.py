import threading
import time
import sys


run = True
loop = 1


def background():
    global loop
    
    while True:
        time.sleep(3)
        print('disarm me by typing disarm')
        loop += 1


def other_function():
    print('You disarmed me! Dying now.')


def main():
    print('started')
    # now threading1 runs regardless of user input
    threading1 = threading.Thread(target=background)
    threading1.daemon = True
    threading1.start()
    
    # global loop
    # while run:
    #     # if args.disarm:
    #     #     other_function()
    #     #     sys.exit()
    #     print(loop)
    #     loop += 1

    #     time.sleep(3)

    # sys.exit()

