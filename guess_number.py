
# Guess The Number by Sarah Schwartz

import simplegui


r1000 = True

# helper function to start and restart the game

def new_game():
    """
    Restarts the game and chooses a new random number in desired range
    """
    global secret_number, turn_count
    import random
    print ("\n" + "New game!")
    if r1000:
        secret_number = random.randrange(0, 1000)
        turn_count = 10
        print ("Guess a number between 0 and 1000.")
        print ("Number of guesses left: " + str(turn_count))
    else:
        secret_number = random.randrange(0, 100)
        turn_count = 7
        print ("Guess a number between 0 and 100.")
        print ("Number of guesses left: " + str(turn_count))



# define event handlers for control panel
def range100():
    """
    Sets number range to [0,100) and starts a new game
    """
    global r100, r1000
    r1000 = False
    new_game() 


def range1000():
    """
    Sets number range to [0,1000) and starts a new game
    """
    global r100, r1000, turn_count
    r1000 = True
    new_game()

    
def input_guess(guess):
    """
    Takes guess, compares it against the number, and prints the result.
    Ends the game if you're out of guesses.
    """
    global turn_count
    type(guess)
    turn_count -= 1
    if int(guess) == secret_number:
        print ("\n" + "You guessed " + str(guess))
        print ("THAT'S IT! Dang, you got me! Good game bud.")
        new_game()
    elif int(guess) > secret_number and turn_count > 0:
        print ("\n" + "As if, guess lower!")
        print ("You guessed " + str(guess))
        print ("Number of guesses left: " + str(turn_count))
    elif (int(guess) < secret_number) and (turn_count > 0):
        print ("\n" + "Pitiful attempt, guess higher!")
        print ("You guessed " + str(guess))
        print ("Number of guesses left: " + str(turn_count))
    elif turn_count == 0 and int(guess) != secret_number:
        print ("\n" + "You're out of guesses! Game over, loser!")
        print ("You guessed " + str(guess))
        print ("The number was " + str(secret_number))
        new_game()
    
# create frame
frame = simplegui.create_frame("Guess The Number", 300, 300)
                                         

# register event handlers for control elements and start frame
frame.add_button("New Game: \n Range of [0,100)", range100, 100)
frame.add_button("New Game: \n Range of [0,1000)", range1000, 100)  
frame.add_input('Your guess (hit enter):', input_guess, 100)
frame.start()

# call new_game 
new_game()

