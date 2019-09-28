#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Encoding: UTF-8

def collatz(number):
    if number % 2 == 0:
        return number // 2
    else:
        return number*3 + 1


number = 0
while number == 0:
    try:
        number = int(input('Please enter a number: '))
        if number == 0:
            print('Number must be an integer not equal to zero.')
        else:
            while True:
                number = collatz(number)
                print(number)
                if abs(number) == 1 or number == -5 or number == -17: 
                    break #Collatz seq ends/enters recurring loop when number hits -17, -5, -1 or 1
    except ValueError:
        print('Number must be an integer.')