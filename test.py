# dict = {'Name': 'Runoob', 'Age': 7, 'Class': 'First'}
# str = str(dict)
# print(dict.items())

# seq = ("hello", "world")
# dict = dict.fromkeys(seq)


# print(dict)
a, b = 0, 1
while b < 10:
    print (b, end = ',')
    a, b = b, a + b
print (b)

number = 7
guess  = -1
print ("guess game")
while guess != number:
    guess = int (input("Please input the number")) 
    if guess == number: 
        print ("right!")
    elif guess < number:
        print ("small")
    elif guess > number:
        print ("bigger")