from typing import Union

# Input: Add(5,3)-> Output 8
def add(x: Union[int,float], y: Union[int,float]):
    return x + y

# Input: Deduct(5,3)-> Output 2
def Deduct(x: Union[int,float], y: Union[int,float]):
  return x - y

# Input: Multiply(5,3)-> Output 15
def Multiply(x: Union[int,float], y: Union[int,float]):
  return x * y

# Input Divide(10,2)-> Output 2
def Divide(x: Union[int,float], y: Union[int,float]):
    return x / y

# Dictionary mapping
operations = {
  '1': add,
  '2': Deduct,
  '3': Multiply,
  '4': Divide
}

#User Input through python calculator.py
if __name__ == "__main__":
    print ("=== Welcome to Calculator ===\n")

    while True:
        print ("Choose operation:")
        print ("1. Add (+)")
        print ("2. Substract (-)")
        print ("3. Multiply (*)")
        print ("4. Divide (/)")
        print ("5. Exit")

        choice = input("\nEnter choice (1/2/3/4/5): ").strip()

        if choice == '5':
            print("Goodbye")
            break

        if choice not in ['1', '2', '3', '4']:
            print("Invalid choice. Try again.\n")
            continue

        try:
            # Get first number with blank validation
            while True:
                num1_input = input("Enter first number: ").strip()
                if num1_input == "":
                    print("Error: The input must not be blank\n")
                    continue
                try:
                    num1 = float(num1_input)
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid number.\n")
            
            # Get second number with blank validation
            while True:
                num2_input = input("Enter second number: ").strip()
                if num2_input == "":
                    print("Error: The input must not be blank\n")
                    continue
                try:
                    num2 = float(num2_input)
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid number.\n")
            
            # Check if dividing by zero
            if choice == '4' and num2 == 0:
                print("Error: The second number must not be zero\n")
                continue
            
            result = operations[choice](num1, num2)
            print(f"Result: {result}\n")
        
        except ValueError:
            print("Invalid input. Please enter valid numbers.\n")

        






