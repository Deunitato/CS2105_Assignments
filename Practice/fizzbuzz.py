#!/usr/bin/python
def fizzBuzz(input):
    if(input%3==0 and input%5 ==0):
        return "fizzBuzz"
    
    elif(input%3==0):
        return "fizz"
    
    elif(input%5==0):
      return "buzz"
    else:
        return input

print(fizzBuzz(15))