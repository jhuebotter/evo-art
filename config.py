import os
import sys

def main(sin):
    sys.stdin = os.fdopen(sin)  # open stdin in this process

    user_input = ''
    while True:
        user_input = input(">>>")
        print(user_input)
        if user_input == 'exit':
            return
