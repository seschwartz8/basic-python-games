# Rock-paper-scissors-lizard-Spock by Sarah Schwartz

def name_to_number(name):
    """
    Converts name to number 0-4 and returns the number
    """
    if name == "rock":
        number = 0
    elif (name == "Spock") or (name == "spock"):
        number = 1
    elif name == "paper":
        number = 2
    elif name == "lizard":
        number = 3
    elif (name == "scissors") or (name == "scissor"):
        number = 4
    else:
        print ("Error, name input not valid")
    return number



def number_to_name(number):
    """
    Converts number 0-4 into a name and returns name
    """
    if number == 0:
        name = "rock"
    elif number == 1:
        name = "Spock"
    elif number == 2:
        name = "paper"
    elif number == 3:
        name = "lizard"
    elif number == 4:
        name = "scissors"
    else:
        print ("Error, number input not in valid range")
    return name
            
    

def rpsls(player_choice): 
    """
    Compares player's choice to random computer choice and returns winner
    """
    print ("\n")
    
    #Player's choice
    print ("Player chooses " + player_choice)
    player_number = name_to_number (player_choice)
    
    #Computer's choice
    import random
    comp_number = random.randrange (0,5)
    comp_choice = number_to_name (comp_number)
    print ("Computer chooses " + comp_choice)
    
    #Determining winner using modulo five
    c_p_difference = (comp_number - player_number) % 5
    if (c_p_difference == 1) or (c_p_difference == 2):
        print ("Player wins!")
    elif (c_p_difference == 3) or (c_p_difference == 4):
        print ("Computer wins!")
    elif c_p_difference == 0:
        print ("Player and computer tie!")

    
    
    
# test your code - THESE CALLS MUST BE PRESENT IN YOUR SUBMITTED CODE
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")