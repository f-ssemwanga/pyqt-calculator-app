#Here is normal definition of a function

def squareIt(x):
    '''Normal function definition'''
    return x**2

result = lambda x:x**2 #use of a lambda function

#other applications of lambda
#1 Lambda with map
myNums = [3,5,7,9]
squaredNums = list(map(lambda x:x**2, myNums)) 
print(squaredNums)

#lambda with filter replaces a for loop and if statement
def returnEvens():
    '''rturns list of numbers that are even from a given list'''
    nums = [1,2,3,4,5,6,7,8,9,10]
    evens =[]
    for i in range(len(nums)):
        if nums[i]%2==0:
            evens.append(nums[i])
    return evens
#complete the previous with a lambda function
nums = [1,2,3,4,5,6,7,8,9,10]
evens = list(filter(lambda x:x%2==0,nums))
print(evens)

def useOfEval(expr):
    try:
        return eval(expr)
    except:
        return(-1)
    




            



