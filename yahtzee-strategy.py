"""
Simplified Yahtzee Strategy by Sarah Schwartz
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.
    hand: full yahtzee hand
    Returns an integer score 
    """
    possible_scores = []
    #Add each possible score to the list of possible scores
    for num in list(hand):
        poss_score = hand.count(num)*num
        possible_scores.append(poss_score)
    #Sort possible scores in ascending order
    possible_scores.sort()
    #Return the highest score
    return possible_scores[-1]



def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    #Generate all possible sequences rolled with free dice
    outcomes = range(1, (num_die_sides + 1))
    all_sequences = gen_all_sequences(outcomes, num_free_dice)
    #Calculate hypothetical scores for each sequence's hand
    total_score = 0.0
    for sequence in all_sequences:
        hand = list(held_dice)
        hand.extend(sequence)
        total_score += float(score(hand))
    #Return expected value
    return (total_score)/len(all_sequences)
    

def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.
    hand: full yahtzee hand
    Returns a set of tuples, where each tuple is dice to hold
    """
    all_holds = set([()])
    #Determine all possible ways to select combinations of dice from hand
    #where 0 signifies don't select, and 1 signifies select
    possible_selections = gen_all_sequences((0 , 1), len(hand))
    for selection in possible_selections:
        selection_tuple = []
        for die_idx in range(len(selection)):
            if selection[die_idx] == 1: #if the die in that combination is "select"
                selection_tuple.append(hand[die_idx])#add that die's value to the tuple
        selection_tuple = tuple(selection_tuple)
        #add the tuple with all the selected dice to the set of possible holds
        all_holds.add(selection_tuple)
    return all_holds


def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    greatest_value = 0.0
    best_hold = ()
    #Compute all holds
    all_holds = gen_all_holds(hand)
    #Get expected value for each hold
    for possible_hold in all_holds:
        num_free_dice = len(hand) - len(possible_hold)
        possible_value = expected_value(possible_hold, num_die_sides, num_free_dice)
    #Replace stored hold/value pair with maximum if applicable
        if possible_value > greatest_value:
            greatest_value = possible_value
            best_hold = possible_hold    
    return (greatest_value, best_hold)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
run_example()
                                       
    
    
    



