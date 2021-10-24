import argparse
import sys, os
import test_threading

parser = argparse.ArgumentParser(description='Console experimenting')
parser.add_argument('-d', '--stop', action='store_true', help='stops program')
parser.add_argument('-s', '--start', action='store_true', help='starts program')
parser.add_argument('-l', action='store_true', help='starts program')

args = parser.parse_args()

if __name__ == '__main__':
    if args.start:
        print('starting')
        test_threading.main()

    if args.l:
        print(test_threading.loop)

    if args.stop:
        test_threading.run = False
