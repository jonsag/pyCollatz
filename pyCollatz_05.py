#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Encoding: UTF-8

steps = 0

def collatz(number, steps):
    while number == 1:
        steps += 1
        print("3 * " + str(number) + " + 1 = " + str(3*number+1))
        number = 3*number+1 ##this while loop only runs once if at all b/c at end of it the value of the variable is not equal to 1
    else:
        while number != 1:
            steps += 1
            if number % 2 == 0:
                print(str(number) + ' // 2 = ' + str(number//2))
                number = number//2
            else:
                print("3 * " + str(number) + " + 1 = " + str(3*number+1))
                number = 3*number+1
    return steps

print('Please input any integer to begin the Collatz sequence.')

while True:
    try:
        number = int(input())
        steps = collatz(number, steps)
        break
    except ValueError:
        print('please enter an integer')
        
print("\n" + str(steps) + " steps")
        
