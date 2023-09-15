"""
Generators
"""
# =============================================================================
# Generators: Yield Keyword
# =============================================================================
def fibonacci(limit):
    a, b = 0, 1
    while a < limit:
        yield a
        a, b = b, a + b

fib_gen = fibonacci(10)
for number in fib_gen:
    print(number)
    
# =============================================================================
# Using next with a generator
# =============================================================================
def even_numbers():
    num = 0
    while True:
        yield num
        num += 2

even_gen = even_numbers()

# Get the first 5 even numbers
for _ in range(5):
    print(next(even_gen))

# =============================================================================
# Using next with default value
# =============================================================================
def limited_alphabet(limit):
    for i in range(65, 65 + limit):
        yield chr(i)

alphabet_gen = limited_alphabet(5)

print(next(alphabet_gen, "End of sequence"))
print(next(alphabet_gen, "End of sequence"))
print(next(alphabet_gen, "End of sequence"))
print(next(alphabet_gen, "End of sequence"))
print(next(alphabet_gen, "End of sequence"))

# This would return "End of sequence" since there are no more elements
print(next(alphabet_gen, "End of sequence"))

"""
Comprehension
"""
# =============================================================================
# List Comprehension
# =============================================================================
numbers = [1, 2, 3, 4, 5]
squares = [x * x for x in numbers if x % 2 == 0]
print(squares)  # Output: [4, 16]

# =============================================================================
# Nested List Comprehensions
# =============================================================================
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = [num for row in matrix for num in row]
print(flattened)  # Output: [1, 2, 3, 4, 5, 6, 7, 8, 9]

# =============================================================================
# Dictionary Comprehension
# =============================================================================
words = ['apple', 'banana', 'orange']
word_lengths = {word: len(word) for word in words}
print(word_lengths)  # Output: {'apple': 5, 'banana': 6, 'orange': 6}

# =============================================================================
# Set Comprehensions
# =============================================================================
input_list = ['LARGE WHITE HEART OF WICKER', 
              'MEDIUM CERAMIC TOP STORAGE JAR', 
              'POLKADOT JAR', 
              'RED T-SHIRT', 
              'Red T-shirt'
              ]
output_set = {word.lower() 
              for sentence in input_list 
              for word in sentence.split()
              }
print(output_set)  
# Output: {'large', 'white', 'heart', 'of', 'wicker', 'medium', 'ceramic', 
# 'top', 'storage', 'jar', 'polkadot', 'red', 't-shirt'}

# =============================================================================
# Generator Comprehensions
# =============================================================================
numbers = [1, 2, 3, 4, 5]
squares_generator = (x * x for x in numbers if x % 2 == 0)

for square in squares_generator:
    print(square)  # Output: 4, 16


"""
Higher-Order Functions
"""
# =============================================================================
# Storing a Function in a Variable
# =============================================================================
def greet(name):
    return f"Hello, {name}!"

greet_func = greet
print(greet_func("John"))  # Output: Hello, John!

# =============================================================================
# Passing a Function as a Parameter
# =============================================================================
def apply_operation(numbers, operation):
    return [operation(num) for num in numbers]

def square(x):
    return x**2

def cube(x):
    return x**3

numbers = [1, 2, 3, 4, 5]
print(apply_operation(numbers, square))  # Output: [1, 4, 9, 16, 25]
print(apply_operation(numbers, cube))    # Output: [1, 8, 27, 64, 125]

# =============================================================================
# Returning a Function
# =============================================================================
def create_power_function(power):
    def power_function(x):
        return x ** power
    return power_function

square = create_power_function(2)
cube = create_power_function(3)

print(square(4))  # Output: 16
print(cube(4))    # Output: 64

# =============================================================================
# Lambda Function Example
# =============================================================================
# Sort a list of strings by length
strings = ["apple", "banana", "cherry", "date", "fig", "grape"]
sorted_strings = sorted(strings, key=lambda x: len(x))
print(sorted_strings)  # Output: ['fig', 'apple', 'date', 'banana', 'cherry', 'grape']

# =============================================================================
# Map Function
# =============================================================================
# Convert a list of temperatures from Celsius to Fahrenheit
def celsius_to_fahrenheit(temp):
    return (9/5) * temp + 32

temperatures_celsius = [0, 20, 37, 100]
temperatures_fahrenheit = list(map(celsius_to_fahrenheit, temperatures_celsius))
print(temperatures_fahrenheit)  # Output: [32.0, 68.0, 98.6, 212.0]

# =============================================================================
# Filter Function
# =============================================================================
# Find prime numbers in a list of integers
def is_prime(num):
    if num < 2:
        return False
    for i in range(2, num):
        if num % i == 0:
            return False
    return True

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
primes = list(filter(is_prime, numbers))
print(primes)  # Output: [2, 3, 5, 7]

# =============================================================================
# Reduce Function
# =============================================================================
from functools import reduce

# Calculate the factorial of a number
def factorial(n):
    return reduce(lambda x, y: x * y, range(1, n+1))

number = 5
print(factorial(number))  # Output: 120

# =============================================================================
# Reduce Function
# =============================================================================
from functools import reduce

# Calculate the factorial of a number
def factorial(n):
    return reduce(lambda x, y: x * y, range(1, n+1))

number = 5
print(factorial(number))  # Output: 120

"""
Object Oriented Programming
"""
# =============================================================================
# Class Example
# =============================================================================
class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed

    def bark(self):
        print(f"{self.name} says: Woof! Woof!")

# Creating Objects
dog1 = Dog("Buddy", "Golden Retriever")
dog2 = Dog("Max", "Labrador")

# Accessing Attributes and Methods
print(dog1.name)  # Output: Buddy
dog1.name = "Rocky"
print(dog1.name)  # Output: Rocky
dog1.bark()  # Output: Rocky says: Woof! Woof!

# =============================================================================
# Inheritance
# =============================================================================
class Animal:
    def __init__(self, species):
        self.species = species

class Dog(Animal):
    def __init__(self, species, name, breed):
        super().__init__(species)
        self.name = name
        self.breed = breed

# Inheritance Example
dog = Dog("Mammal", "Buddy", "Golden Retriever")
print(dog.species)  # Output: Mammal
print(dog.name)  # Output: Buddy
print(dog.breed)  # Output: Golden Retriever

# =============================================================================
# Multiple Inheritance
# =============================================================================
class Swim:
    def swim(self):
        print("I can swim")

class Fly:
    def fly(self):
        print("I can fly")

class Duck(Swim, Fly):
    pass

duck = Duck()
duck.swim()  # Output: I can swim
duck.fly()  # Output: I can fly

# =============================================================================
# Method Resolution Order
# =============================================================================
print(Duck.mro())
# Output: [
# <class '__main__.Duck'>, 
# <class '__main__.Swim'>, 
# <class '__main__.Fly'>, 
# <class 'object'>
# ]

# =============================================================================
# MRO in Multiple Inheritance
# =============================================================================
class Animal:
    def speak(self):
        print("Animal.speak")

class Bird(Animal):
    def speak(self):
        print("Bird.speak")
        super().speak()

class Mammal(Animal):
    def speak(self):
        print("Mammal.speak")
        super().speak()

class Platypus(Bird, Mammal):
    def speak(self):
        print("Platypus.speak")
        super().speak()

p = Platypus()
p.speak()

# =============================================================================
# Python Encapsulation
# =============================================================================
class Temperature:
    def __init__(self, celsius=0):
        self.__celsius = celsius

    def set_celsius(self, celsius):
        self.__celsius = celsius

    def get_celsius(self):
        return self.__celsius

    def set_fahrenheit(self, fahrenheit):
        self.__celsius = (fahrenheit - 32) * (5 / 9)

    def get_fahrenheit(self):
        return self.__celsius * (9 / 5) + 32

temp = Temperature()
temp.set_fahrenheit(68)
print(temp.get_celsius())

# =============================================================================
# Polymorphism
# =============================================================================
class MediaFile:
    def play(self):
        pass

class AudioFile(MediaFile):
    def play(self):
        print("Playing audio file")

class VideoFile(MediaFile):
    def play(self):
        print("Playing video file")

class ImageFile(MediaFile):
    def play(self):
        print("Displaying image file")

media_files = [AudioFile(), VideoFile(), ImageFile()]

for media_file in media_files:
    media_file.play()


# =============================================================================
# @classmethod
# =============================================================================
class Pizza:
    total_pizzas = 0
    most_popular_topping = ""

    def __init__(self, topping):
        Pizza.total_pizzas += 1
        Pizza.most_popular_topping = topping

    @classmethod
    def get_total_pizzas(cls):
        return cls.total_pizzas

    @classmethod
    def get_most_popular_topping(cls):
        return cls.most_popular_topping


class Employee:
    def __init__(self, name, id):
        self.name = name
        self.id = id

    @classmethod
    def from_string(cls, employee_string):
        name, id = employee_string.split(',')
        return cls(name, id)


# =============================================================================
# @staticmethod
# =============================================================================
class StringUtils:
    @staticmethod
    def reverse_string(s):
        return s[::-1]

    @staticmethod
    def is_palindrome(s):
        return s == s[::-1]

    @staticmethod
    def word_count(s):
        return len(s.split())

print(StringUtils.reverse_string("hello"))
print(StringUtils.is_palindrome("racecar"))
print(StringUtils.word_count("Hello, world!"))

