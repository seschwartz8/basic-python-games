#Stopwatch the game by Sarah Schwartz
import simplegui
    
# define global variables
time = 0 #in tenths of seconds
attempts = 0
hits = 0
timer_on = False

# define helper function format that converts time to A:BC.D
def format(time): 
    """
    Converts time in tenths of seconds to formatted string A:BC.D
    """
    A = time // 600
    B = ((time // 10) % 60) // 10
    C = ((time // 10) % 60) % 10
    D = time % 10
    return str(A) + ":" + str(B) + str(C) + "." + str(D)

    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global timer_on
    timer_on = True
    timer.start()

def stop():
    global attempts, hits, timer_on
    if timer_on == True:
        attempts += 1
        if time % 10 == 0:
            hits += 1
    timer.stop()
    timer_on = False


def reset():
    global attempts, hits, time
    timer.stop()
    attempts = 0
    hits = 0
    time = 0

# define event handler for timer with 100msec (0.1 sec) interval
def timer_handler():
    global time
    time += 1

    
# define draw handler
def draw_handler(canvas):
    canvas.draw_text (format(time), (200,250), 50, "White")
    canvas.draw_text (str(hits) + "/" + str(attempts), (400,40), 30, "White") 

    
# create frame and labels
frame = simplegui.create_frame ("Stopwatch", 500, 500)
title = frame.add_label('Stopwatch Game', 300)
instructions = frame.add_label('Stop the watch on the second!', 300)


# register event handlers
timer = simplegui.create_timer (100, timer_handler)
button_start = frame.add_button ("Start", start, 100)
button_stop = frame.add_button ("Stop", stop, 100)
button_reset = frame.add_button ("Reset", reset, 100)
draw = frame.set_draw_handler(draw_handler)
background = frame.set_canvas_background ("Black")


# start frame
frame.start()


