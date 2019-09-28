#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Encoding: UTF-8


def collatz(number, verbose):

    steps = 0

    while number !=1:
        steps += 1
        if number% 2 == 0:
            number= number//2
            if verbose:
                print(number)

        else:
            number=  3 * number + 1
            if verbose:
                print(number) 
            
    return steps   


if __name__ == "__main__":
    verbose = False
    
    number=int(input('Enter number:\n'))

    print()
    
    steps = collatz(number, verbose)

    print("\n" + str(steps) + " steps")