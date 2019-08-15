
# Memory Game by Sarah Schwartz


import simplegui
import random
WIDTH = 800
HEIGHT = 100
card_size = [50, 100]
prev_click = None
current_click = None
turn_count = 0
numbers1 = [0, 1, 2, 3, 4, 5, 6, 7]
numbers2 = [0, 1, 2, 3, 4, 5, 6, 7]
memory_deck = numbers1 + numbers2
exposed = [False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False]

# helper function to initialize globals
def new_game():
    global state, exposed, turn_count
    state = 0
    turn_count = 0
    exposed = [False, False, False, False, False, False, False, False,
              False, False, False, False, False, False, False, False]
    random.shuffle(memory_deck)

     
# define event handlers
def mouseclick(pos):
    global prev_click, current_click, turn_count, state, exposed
    # game state logic
    global state
    if state == 0:
        state = 1
        prev_click = None
        current_click = pos[0]//50
    elif state == 1:
        if exposed[pos[0]//50] == False:
            prev_click = current_click
            current_click = pos[0]//50
            state = 2
            turn_count += 1
    elif state == 2:
        #Check if cards match
        if memory_deck[prev_click] == memory_deck[current_click]:
            state = 1
            if exposed[pos[0]//50] == False:
                current_click = pos[0]//50
                prev_click = None
        else:
            exposed[prev_click] = False
            exposed[current_click] = False
            state = 1
            if exposed[pos[0]//50] == False:
                current_click = pos[0]//50
                prev_click = None
    #flips the card clicked on
    if exposed[pos[0]//50] == False:
        exposed[pos[0]//50] = True
                        
def draw(canvas):
    iteration = 0
    for card_idx in range(len(memory_deck)):
        if exposed[card_idx] == True:
            canvas.draw_text(str(memory_deck[card_idx]), 
                    [(card_size[0]*(iteration) + card_size[0]/2)-15, HEIGHT*.75],
                    50, 'Red')
        if exposed[card_idx] == False:
            canvas.draw_polygon([(card_size[0]*iteration, 0), 
                                 (card_size[0]*iteration, HEIGHT),
                                 (card_size[0]*(iteration+1), HEIGHT),
                                 (card_size[0]*(iteration+1), 0)], 
                                1, 'Black', 'Green')
        iteration += 1
        label.set_text("Turns = " + str(turn_count))


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", WIDTH, HEIGHT)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()