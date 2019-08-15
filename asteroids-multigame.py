# Multi-game Spaceship by Sarah Schwartz
import simplegui
import math
import random

# globals
WIDTH = 1000
HEIGHT = 600
TURN_INCR = 0.15
ACC_REDUC = 0.3
MISSILE_SPEED = 5
FRIC = 0.03
SCORE_CAP = 10
ROCK_DISTANCE = 150
POINTS = 100
score1 = 0
score2 = 0
score = 0
lives = 3
asteroids_rules = True
spaceship_rules = False

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# helper function to restart game/reset score and lives
def restart_game():
    global started, score1, score2, missile_collisions, score, lives
    started = True

    if asteroids_rules:
        missile_collisions = 0
        score = 0
        lives = 3
    else:
        score1 = 0
        score2 = 0


# helper function for game over state
def game_over():
    global started, time, explosion_group, my_ship1, my_ship2, my_ship, rock_group, missile_collisions, canvas
    started = False
    time = 0
    explosion_group = set([])
    rock_group = set([])
    if asteroids_rules:
        if score == 0:
            missile_collisions = 0
        my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0,0], 0, ship_image, ship_info)
    else:            
        my_ship1 = Ship([WIDTH / 4, HEIGHT / 2], [0,0], 0, ship_image, ship_info)
        my_ship2 = Ship([3*WIDTH / 4, HEIGHT / 2], [0,0], 0, ship_image, ship_info)



# helper function to process drawing/updating sprite groups based on lifespan
def process_sprite_group(group, canvas):
    for i in list(group):
        if i.update() == False:
            i.draw(canvas)
            i.update()
        elif i.update():
            group.remove(i)            


# helper function to process group collisions with single object
def group_collide(group, other_object):
    for i in list(group):
        if i.collide(other_object):
            group.remove(i)
            an_explosion = Sprite(i.pos, [0,0], 0, 0, explosion_image, explosion_info)
            explosion_group.add(an_explosion)
            return True

# helper function to process group collisions with other group
def group_group_collide(group1, group2):
    global missile_collisions
    for i in list(group1):
        if group_collide(group2, i):
            group1.discard(i)
            missile_collisions += 1
    return missile_collisions


class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")    

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")
    
# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.missile_group = set([])
        self.sound = sound
        
    def draw(self,canvas):
        if self.thrust:
            thrusters_on_img = [(ship_info.center[0] + ship_info.size[0]), 
                                 ship_info.center[1]]
            canvas.draw_image(self.image, thrusters_on_img, ship_info.size, self.pos, self.image_size, self.angle)            
        else:
            canvas.draw_image(self.image, ship_info.center, ship_info.size, self.pos, self.image_size, self.angle)

    def update(self):
        #update position based on velocity and wrap screen
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        #increment angle by angular velocity
        self.angle += self.angle_vel
        #compute forward vector based on ship's angle
        forward = angle_to_vector(self.angle)        
        if self.thrust:
            self.vel[0] += ACC_REDUC * forward[0]
            self.vel[1] += ACC_REDUC * forward[1]
        #friction
        self.vel[0] *= (1-FRIC)
        self.vel[1] *= (1-FRIC)
   
    def incr_ang_vel(self):
        self.angle_vel += TURN_INCR
    
    def decr_ang_vel(self):
        self.angle_vel -= TURN_INCR
        
    def thrust_change(self):
        if self.thrust:
            self.thrust = False
        else:
            self.thrust = True
               
    def shoot(self):
        forward = angle_to_vector(self.angle)                
        a_missile = Sprite([self.pos[0] + self.radius*forward[0], self.pos[1] + self.radius*forward[1]], 
                           [self.vel[0] + forward[0]*MISSILE_SPEED, self.vel[1] + forward[1]*MISSILE_SPEED], 
                           0, 0, missile_image, missile_info)
        self.missile_group.add(a_missile)
    
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius



        
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
   
    def draw(self, canvas):
        global time
        if self.animated: # based on animation (e.g. explosions)
            number_tiles = 24
            current_sprite_index = (time % number_tiles) // 1
            current_sprite_center = [self.image_center[0] + current_sprite_index*self.image_size[0], self.image_center[1]]
            canvas.draw_image(self.image, current_sprite_center, self.image_size, self.pos, self.image_size, self.angle)
        else: # if not animated
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        time += 0.2
    
    def update(self):
        # increment angle by angular velocity
        self.angle += self.angle_vel
        # update position based on velocity and wrap screen
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        # increment age when update is called, determine when sprite hits lifespan
        self.age += 1
        if self.age <= self.lifespan:
            return False
        return True
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
        
    def collide(self, other_object):
        return dist(self.pos, other_object.get_position()) <= (self.radius + other_object.get_radius())
        
           
    
# draw handler           
def draw(canvas):
    global time, a_missile, started, my_ship1, my_ship2, score1, score2, missile_col1, missile_col2, explosion_group, lives, score
    
    # animate background (this code segment was provided by Coursera)
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship
    if asteroids_rules:
        my_ship.draw(canvas)
    else:
        my_ship1.draw(canvas)
        my_ship2.draw(canvas)

      
    # user interface
    if asteroids_rules:
        canvas.draw_text("Lives: " + str(lives), (30, 30), 22, 'White')
        canvas.draw_text("Score: " + str(score), (WIDTH - 120, 30), 22, 'White')   
    else:
        canvas.draw_text("Lefty: " + str(score1), (30, 30), 22, 'White')
        canvas.draw_text("Righty: " + str(score2), (WIDTH - 140, 30), 22, 'White')    
    
    # update ship
    if asteroids_rules:
        my_ship.update()
    else:
        my_ship1.update()
        my_ship2.update()
    
    # draw and update sprite groups and explosions
    if asteroids_rules:
        process_sprite_group(rock_group, canvas)
        process_sprite_group(my_ship.missile_group, canvas)
        process_sprite_group(explosion_group, canvas)
    else:
        process_sprite_group(my_ship1.missile_group, canvas)
        process_sprite_group(my_ship2.missile_group, canvas)
        process_sprite_group(explosion_group, canvas)
    
    # adjust scores for collisions
    if asteroids_rules:
        if (group_collide(rock_group, my_ship)) and (started == True):
            lives -= 1
        score = group_group_collide(rock_group, my_ship.missile_group)*POINTS  
    else:
        if (group_collide(my_ship1.missile_group, my_ship2)) and (started == True):
            score1 += 1
        if (group_collide(my_ship2.missile_group, my_ship1)) and (started == True):
            score2 += 1
    
    #restart UI if you lose
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
    if asteroids_rules:
        if lives == 0:
            game_over()
    else:
        if (score1 == SCORE_CAP) or (score2 == SCORE_CAP):
            game_over()
            
            
# timer handler that spawns a rock    
def rock_spawner():
    if (len(rock_group) <= 8) and started:
        a_rock = Sprite([random.randrange(0, WIDTH), random.randrange(0, HEIGHT)], 
                        [random.randrange (-3, 3), random.randrange (-3, 3)], 
                        0, random.choice([-0.1, 0.1]), asteroid_image, asteroid_info)
        if dist(a_rock.pos, my_ship.pos) > ROCK_DISTANCE:
            rock_group.add(a_rock)


# define keyhandlers to control ship/firing
def keydown(key):
    if started:
        if asteroids_rules:
            key_inputs = {"up" : my_ship.thrust_change,  
                          "left" : my_ship.decr_ang_vel, 
                          "right" : my_ship.incr_ang_vel,
                          "space" : my_ship.shoot}
            for i in key_inputs:
                if simplegui.KEY_MAP[i] == key:
                    key_inputs[i]()
        else:
            key_inputs = {"w" : my_ship1.thrust_change, 
                          "a": my_ship1.decr_ang_vel,
                          "d" : my_ship1.incr_ang_vel,
                          "z" : my_ship1.shoot,
                          "up" : my_ship2.thrust_change,  
                          "left" : my_ship2.decr_ang_vel, 
                          "right" : my_ship2.incr_ang_vel,
                          "m" : my_ship2.shoot}
            for i in key_inputs:
                if simplegui.KEY_MAP[i] == key:
                    key_inputs[i]()

                
def keyup(key):
    if started:
        if asteroids_rules:  
            key_ups = {"up" : my_ship.thrust_change,  
                       "left" : my_ship.incr_ang_vel, 
                       "right" : my_ship.decr_ang_vel}  
            for i in key_ups:
                if simplegui.KEY_MAP[i] == key:
                    key_ups[i]()          
        else:
            key_ups = {"w" : my_ship1.thrust_change, 
                       "a": my_ship1.incr_ang_vel,
                       "d" : my_ship1.decr_ang_vel,
                       "up" : my_ship2.thrust_change,  
                       "left" : my_ship2.incr_ang_vel, 
                       "right" : my_ship2.decr_ang_vel}  
            for i in key_ups:
                if simplegui.KEY_MAP[i] == key:
                    key_ups[i]()
                
# button handler
def asteroids_handler():
    global asteroids_rules, spaceship_rules
    asteroids_rules = True
    spaceship_rules = False
    game_over()

def spaceship_handler():
    global asteroids_rules, spaceship_rules
    spaceship_rules = True
    asteroids_rules = False
    game_over()

# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    in_width = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    in_height = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    #determine if your click is within the spash image and start the game if so
    if (not started) and in_width and in_height:
        restart_game()
        
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and sprites
game_over()
soundtrack.set_volume(0.1)
soundtrack.play()

# register handlers, buttons, instructions
frame.set_draw_handler(draw)
frame.set_mouseclick_handler(click)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
asteroids_button = frame.add_button("PLAY ASTEROIDS", asteroids_handler, 200)
spaceship_button = frame.add_button("PLAY SPACESHIP BATTLE", spaceship_handler, 200)
instructions = frame.add_label("For spaceship battle: Lefty:ASWDZ and Righty:Arrows+M", 10)

if asteroids_rules:
    timer = simplegui.create_timer(1000.0, rock_spawner)


# get things rolling
if asteroids_rules:
    timer.start()
frame.start()
