import sys
import os

def block_print():
    sys.stdout = open(os.devnull, 'w')

def enable_print():
    if "close" in sys.stdout:
        sys.stdout.close()
    sys.stdout = sys.__stdout__