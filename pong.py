# Pong by Sarah Schwartz

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos = [WIDTH/2, HEIGHT/2]
ball_vel = [0, 0]
paddle1_pos = HEIGHT/2
paddle2_pos = HEIGHT/2
paddle1_vel = 0
paddle2_vel = 0
vel_constant = 3
collide = False
score1 = 0
score2 = 0


# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos[0] = WIDTH/2
    ball_pos[1] = HEIGHT/2
    if direction == LEFT:
        ball_vel[0] = random.randrange(-4, -2)
        ball_vel[1] = random.randrange(-3, -1)
    elif direction == RIGHT:
        ball_vel[0] = random.randrange(2, 4)
        ball_vel[1] = random.randrange(-3, -1)      

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    score1 = 0
    score2 = 0
    if LEFT:
        spawn_ball(LEFT)
    elif RIGHT:
        spawn_ball(RIGHT)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, strike_count
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "Yellow")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "Yellow")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "Yellow")
    
    # update ball position and collision against top/bottom walls
    if ((ball_pos[1] >= BALL_RADIUS)
        and (ball_pos[1] <= HEIGHT - BALL_RADIUS)):
        ball_pos[1] += ball_vel[1]
    else:
        ball_vel[1] = -(ball_vel[1])    
        ball_pos[1] += ball_vel[1] 
   
    # respawn ball if ball hits left/right gutters, but reflect if hits paddle
    if ((ball_pos[0] >= BALL_RADIUS)
        and (ball_pos[0] <= WIDTH - BALL_RADIUS)):
        ball_pos[0] += ball_vel[0]
    elif ball_pos[0] <= BALL_RADIUS:
        if is_strike():
            ball_vel[0] = -(ball_vel[0])*1.1
            ball_pos[0] += ball_vel[0]
        else:
            score2 += 1
            spawn_ball(RIGHT)
    elif ball_pos[0] >= BALL_RADIUS:
        if is_strike():
            ball_vel[0] = -(ball_vel[0])*1.1
            ball_pos[0] += ball_vel[0]
        else:
            score1 += 1
            spawn_ball(LEFT)          

    # draw ball
    canvas.draw_circle((ball_pos[0], ball_pos[1]), BALL_RADIUS, BALL_RADIUS/4, "Red", "Yellow")
    
    # update paddle's vertical position, keep paddle on the screen
    if (HEIGHT - HALF_PAD_HEIGHT) >= (paddle1_pos + paddle1_vel) >= HALF_PAD_HEIGHT:
        paddle1_pos += paddle1_vel
    if (HEIGHT - HALF_PAD_HEIGHT) >= (paddle2_pos + paddle2_vel) >= HALF_PAD_HEIGHT:      
        paddle2_pos += paddle2_vel
    
    # draw paddles
    canvas.draw_line((HALF_PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT), (HALF_PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT), PAD_WIDTH, 'Red')
    canvas.draw_line((WIDTH - HALF_PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT), (WIDTH - HALF_PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT), PAD_WIDTH, 'Red')

    # draw scores
    canvas.draw_text(str(score1), (WIDTH/4, 50), 40, 'White')
    canvas.draw_text(str(score2), (WIDTH - WIDTH/4, 50), 40, 'White')
    
    # determine whether paddle and ball collide 
def is_strike():
    if ((ball_pos[0] <= BALL_RADIUS)
        and (paddle1_pos - HALF_PAD_HEIGHT) <= ball_pos[1] <= (paddle1_pos + HALF_PAD_HEIGHT)):
        return True
    elif ((ball_pos[0] >= BALL_RADIUS)
        and (paddle2_pos - HALF_PAD_HEIGHT) <= ball_pos[1] <= (paddle2_pos + HALF_PAD_HEIGHT)):
        return True
    else:
        return False
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -(vel_constant)
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = vel_constant
    else:
        paddle1_vel = 0
    
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -(vel_constant)
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = vel_constant
    else:
        paddle2_vel = 0
        
        
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"] or key == simplegui.KEY_MAP ["s"]:
        paddle1_vel = 0
    
    if key == simplegui.KEY_MAP["up"] or key == simplegui.KEY_MAP ["down"]:
        paddle2_vel = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
title = frame.add_label('Pong!', 200)
instructions1 = frame.add_label('Player 1: Use "w" and "s"', 200)
instructions2 = frame.add_label('Player 2: Use "up" and "down"', 200)
button = frame.add_button('New Game', new_game, 200)

# start frame
new_game()
frame.start()
