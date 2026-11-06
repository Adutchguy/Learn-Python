secret = 42

guesses = 0
found = False

while guesses < 7:
    guess = int(input("Your guess: "))
    guesses += 1
    if guess < secret:
        print("Too low!")
    elif guess > secret:
        print("Too high!")
    else:
        print(f"Correct! Guesses used: {guesses}")
        found = True
        break

if not found:
    print(f"Out of guesses! The number was {secret}.")
