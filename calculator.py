import math

def perform_addition(numbers):
    return sum(numbers)

def perform_subtraction(numbers):
    result = numbers[0]
    for num in numbers[1:]:
        result -= num
    return result

def perform_multiplication(numbers):
    result = 1
    for num in numbers:
        result *= num
    return result

def perform_division(numbers):
    if len(numbers) < 2:
        return "At least two numbers are required for division."
    result = numbers[0]
    for num in numbers[1:]:
        if num == 0:
            return "Error: Division by zero is not allowed"
        result /= num
    return result

def perform_power(numbers):
    if len(numbers) != 2:
        return "Power operation requires exactly two numbers (base and exponent)"
    return math.pow(numbers[0], numbers[1])

def perform_square_root(numbers):
    if len(numbers) != 1:
        return "Square root requires exactly one number."
    if numbers[0] < 0:
        return "Error: Square root of negative number is not allowed."
    return math.sqrt(numbers[0])

def is_valid_number(value):
    if value.replace('.','',1).isdigit() or (value.startswith('-') and value[1:].replace('.', '', 1).isdigit()):
        return True
    return False

def valid_input():
    numbers = input("Enter numbers separated by space: ").split()
    if all(is_valid_number(num) for num in numbers):
        return [float(num) for num in numbers]
    else:
        return None

while True:
    print("\nCalculator")
    print("Select operation: ")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")
    print("5. Power (x^y)")
    print("6. Square Root")
    print("7. Exit")

    choice = input("Enter choice (1-7): ")

    if choice == '7':
        print("Exit the program.")
        break

    numbers = valid_input()

    if numbers:
        if choice == '1':
            result = perform_addition(numbers)
            print(f"The result of addition is {result}")
        elif choice == '2':
            result = perform_subtraction(numbers)
            print(f"The result of subtraction is {result}")
        elif choice == '3':
            result = perform_multiplication(numbers)
            print(f"The result of multiplication is {result}")
        elif choice == '4':
            result = perform_division(numbers)
            print(f"The result of division is {result}")
        elif choice == '5':
            result = perform_power(numbers)
            print(f"The result of power is {result}")
        elif choice == '6':
            result = perform_square_root(numbers)
            print(f"The result of square root is {result}")
        else:
            print("Invalid choice. Please try again.")
    else:
        print("Please try again with valid numbers.")
