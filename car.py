import pygame
import math

class Car:

    MAX_SPEED = 5
    MAX_ANGLE = 30 # degrees

    def __init__(self):
        self.x = 300
        self.y = 250

        self.wheel_angle = 0 # degrees, integers
        self.angle = 0 # radians, float
        self.l = 80
        self.w = 30
        self.speed = 0

        self.turning = 0
        self.braking = False
        self.acc = 0

        self.MIN_TURN_RAD = 2 * self.l / 3 * math.tan(math.pi / 2 - math.radians(self.MAX_ANGLE))

    # To accelerate the car on next update
    # value is a float in range [-1, 1] that is a percentage of the maximum acceleration
    # Max acceleration is +-0.1
    def accelerate(self, value):
        # constrain to [-1,1]
        if abs(value) > 1:
            value = value / abs(value)

        # set acceleration for this tick
        self.acc = value

    # To turn wheels on next tick
    def turn_wheels(self, clockwise):        
        if clockwise and self.wheel_angle < self.MAX_ANGLE:
            self.turning = 1
        elif not clockwise and self.wheel_angle > -self.MAX_ANGLE:
            self.turning = -1

    # To reduce speed of car to zero, regardless of direction
    # value must be in range (0,1] -> 1 will brake with maximum effect
    # Max brake reduces speed by 30% each time
    def brake(self, value):
        # constrain to (0, 1]
        if value > 0:
            self.braking = min(value, 1)        

    # Returns an object that contains the center of the turn radius and the
    # value of the radius given the wheel angle
    def get_turn_info(self, wheel_angle):
        
        # find point of rotation from origin, no transformation
        sign = 1
        if wheel_angle < 0:
            sign = -1
        s = 2 * self.l / 3 * math.tan(math.pi / 2 - math.radians(wheel_angle))
        c = (sign * self.w / 2 + s, self.l / 3)
        
        return {
            'center': (int(self.x + c[0] * math.cos(self.angle) - c[1] * math.sin(self.angle)),
                       int(self.y + c[0] * math.sin(self.angle) + c[1] * math.cos(self.angle))),
            'radius': 2 * self.l / 3 * math.tan(math.pi / 2 - math.radians(wheel_angle)) * sign
            }
        

    # Called once per tick. Updates the parameters of the car based on
    # which functions were called in the last tick, then moves the car
    # to its new position if applicable
    def update(self):

        # check all values that were changed and reset them        
        self.wheel_angle = self.wheel_angle + self.turning
        self.turning = 0
        
        self.speed = self.speed + self.acc * 0.1
        self.acc = 0

        self.speed = self.speed * (1 - 0.3 * self.braking)
        self.braking = 0

        # Cap at max speed
        if abs(self.speed) > self.MAX_SPEED:
            self.speed = self.speed / abs(self.speed) * self.MAX_SPEED
            
        
        # case 1: wheel_angle = 0
        if self.wheel_angle == 0:
            self.x = self.x + self.speed * math.cos(-math.pi / 2 + self.angle)
            self.y = self.y + self.speed * math.sin(-math.pi / 2 + self.angle)
            self.speed = self.speed * .98
            return

        sign = 1
        if self.wheel_angle < 0:
            sign = -1           

        # center point of rotation
        turn_info = self.get_turn_info(self.wheel_angle)
        center = turn_info['center']
        turn_radius = turn_info['radius']

        # move car along circle
        # place center at origin
        self.x = self.x - center[0]
        self.y = self.y - center[1]
        # rotate about origin
        rot_angle = self.speed / turn_radius * sign
        new_point = (center[0] + self.x * math.cos(rot_angle) - self.y * math.sin(rot_angle),
                     center[1] + self.y * math.cos(rot_angle) + self.x * math.sin(rot_angle))

        # update values of car
        self.x = new_point[0]
        self.y = new_point[1]
        self.angle = self.angle + rot_angle
        if abs(self.angle) > math.pi * 2:
            self.angle = self.angle - self.angle / abs(self.angle) * math.pi * 2
        self.speed = self.speed * .98

    # Draws the car in its current state onto the provided screen
    # with its body colored by the given color
    def draw(self, screen, color):
        
        corners = [(1, -1), (-1, -1), (-1, 1), (1, 1)]
        tire_w = self.w / 12
        tire_l = self.l / 12
        BLACK = (0, 0, 0)
        
        # back wheels
        t1_points = []
        t2_points = []
        for i in range(4):
            # corner point from origin
            op1 = (self.w / 2 + tire_w * corners[i][0], self.l / 3 + tire_l * corners[i][1])
            op2 = (-self.w / 2 + tire_w * corners[i][0], self.l / 3 + tire_l * corners[i][1])
            # rotated and translated
            p1 = (self.x + op1[0] * math.cos(self.angle) - op1[1] * math.sin(self.angle),
                 self.y + op1[0] * math.sin(self.angle) + op1[1] * math.cos(self.angle))
            p2 = (self.x + op2[0] * math.cos(self.angle) - op2[1] * math.sin(self.angle),
                 self.y + op2[0] * math.sin(self.angle) + op2[1] * math.cos(self.angle))
            t1_points.append(p1)
            t2_points.append(p2)
        pygame.draw.polygon(screen, BLACK, t1_points)
        pygame.draw.polygon(screen, BLACK, t2_points)

        # front wheels
        t1_points = []
        t2_points = []
        for i in range(4):
            # corner point from origin
            op = (tire_w * corners[i][0], tire_l * corners[i][1])
            op1 = (self.w / 2 + op[0] * math.cos(math.radians(self.wheel_angle)) - op[1] * math.sin(math.radians(self.wheel_angle)),
                   -self.l / 3 + op[0] * math.sin(math.radians(self.wheel_angle)) + op[1] * math.cos(math.radians(self.wheel_angle)))
            op2 = (-self.w / 2 + op[0] * math.cos(math.radians(self.wheel_angle)) - op[1] * math.sin(math.radians(self.wheel_angle)),
                   -self.l / 3 + op[0] * math.sin(math.radians(self.wheel_angle)) + op[1] * math.cos(math.radians(self.wheel_angle)))
            # rotated and translated
            p1 = (self.x + op1[0] * math.cos(self.angle) - op1[1] * math.sin(self.angle),
                 self.y + op1[0] * math.sin(self.angle) + op1[1] * math.cos(self.angle))
            p2 = (self.x + op2[0] * math.cos(self.angle) - op2[1] * math.sin(self.angle),
                 self.y + op2[0] * math.sin(self.angle) + op2[1] * math.cos(self.angle))
            t1_points.append(p1)
            t2_points.append(p2)
        pygame.draw.polygon(screen, BLACK, t1_points)
        pygame.draw.polygon(screen, BLACK, t2_points)

        # body
        points = []
        for i in range(4):
            # corner point from origin
            op = (self.w / 2 * corners[i][0], self.l / 2 * corners[i][1])
            # rotated and translated
            p = (self.x + op[0] * math.cos(self.angle) - op[1] * math.sin(self.angle),
                 self.y + op[0] * math.sin(self.angle) + op[1] * math.cos(self.angle))
            points.append(p)
        pygame.draw.polygon(screen, color, points)

        # lights
        p1 = (-self.w / 4, -7 * self.l / 16)
        p2 = (self.w / 4, -7 * self.l / 16)
        pygame.draw.circle(screen, (255,255,100),
                           (int(self.x + p1[0] * math.cos(self.angle) - p1[1] * math.sin(self.angle)),
                            int(self.y + p1[0] * math.sin(self.angle) + p1[1] * math.cos(self.angle))),
                            int(self.l / 16))
        pygame.draw.circle(screen, (255,255,100),
                           (int(self.x + p2[0] * math.cos(self.angle) - p2[1] * math.sin(self.angle)),
                            int(self.y + p2[0] * math.sin(self.angle) + p2[1] * math.cos(self.angle))),
                            int(self.l / 16))

        

# test function        
if __name__ == "__main__":
    pygame.init()

    size = (600, 500)
    screen = pygame.display.set_mode(size) # set window size
    pygame.display.set_caption("Car") # set title

    clock = pygame.time.Clock()

    # stuff
    car = Car()

    done = False    

    while not done:
        
        # Main event loop
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done = True
                
        # moving the car
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            car.turn_wheels(False)
        if keys[pygame.K_RIGHT]:
            car.turn_wheels(True)
        if (keys[pygame.K_UP] or keys[pygame.K_DOWN]) and not (keys[pygame.K_UP] and keys[pygame.K_DOWN]):
            car.accelerate(1 if keys[pygame.K_UP] else -1)
        else:
            #car.speed = car.speed * .9
            pass

        # Update stuff
        car.update()

        # Drawing code here
        screen.fill(WHITE) # Makes the background white
        car.draw(screen, (255,0,0))

        # draw line towards car
        angle = math.atan2(car.y - size[1] / 2, car.x - size[0] / 2)
        dist = max(105 - 100 / (math.hypot(car.y - size[1] / 2, car.x - size[0] / 2) + 1) ** .2, 5)
        pygame.draw.line(screen, (0,0,255), (300,250),
                         (size[0] / 2 + math.cos(angle) * dist,
                          size[1] / 2 + math.sin(angle) * dist))

        pygame.display.flip() # Draws the screen
        clock.tick(100) # 60 fps

    # out of loop 
    pygame.quit()

