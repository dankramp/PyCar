from car import Car
import math
import pygame

class BotDriver:


    def __init__(self):
        self.car = Car()

    def driveToPoint(self, point, screen):
        # some values
        car = self.car
        dist = math.hypot(car.x - point[0], car.y - point[1])

        if dist < 2:
            print("At target. Stopping")
            car.brake(1)
            return

        # drive forward or backward?
        angle_to_point = math.atan2(point[0] - car.x, car.y - point[1])
        direction = 1
        if math.cos(angle_to_point - car.angle) < 0:
            direction = -1
        turn = -1 # left turn
        if math.sin(car.angle - angle_to_point) < 0:
            turn = 1 # right turn        

        print("Turn: " + ("right" if turn == 1 else "left"))
        print("Direction: " + ("forward" if direction == 1 else "backwards"))
        # can we reach the point just by turning?
        min_turn_center = car.get_turn_info(car.MAX_ANGLE * turn)['center'] # check negative too
        min_rad = math.hypot(min_turn_center[0] - car.x, min_turn_center[1] - car.y)
        #pygame.draw.circle(screen, (255,0,0), min_turn_center, int(min_rad), 2)
        
        if ((point[0] - min_turn_center[0]) ** 2 + (point[1] - min_turn_center[1]) ** 2) ** .5 - (min_rad + car.MIN_TURN_RAD) / 2 < 0:
            # cannot reach, must turn around
            print("Point is within turn radius, turning around")
            car.turn_wheels(turn < 0)
            car.accelerate(direction * -1)
            return
        
        # are the wheels turned the right way?
        if turn * car.wheel_angle <= 0:
            print("Wheels aren't facing the right way!")
            #car.brake()
            car.turn_wheels(turn > 0)
            return

        # point is reachable, wheels are turned correctly
        turn_info = car.get_turn_info(car.wheel_angle)
        ti_inc = car.get_turn_info(car.wheel_angle - turn)
        ti_dec = car.get_turn_info(car.wheel_angle + turn)

        c1 = ti_inc['center']
        r1 = math.hypot(car.x - c1[0], car.y - c1[1])
        c2 = ti_dec['center']
        r2 = math.hypot(car.x - c2[0], car.y - c2[1])
        
        center = turn_info['center']
        turn_radius = math.hypot(car.x - center[0], car.y - center[1])
        dist_from_circle = math.hypot(point[0] - center[0], point[1] - center[1]) - turn_radius

        if ti_inc['radius'] < 100000:
            pygame.draw.circle(screen, (100,255,100), c1, int(r1), 1)
            pass
        if ti_dec['radius'] < 100000:
            pygame.draw.circle(screen, (100,255,100), c2, int(r2), 1)
            pass
        
        pygame.draw.circle(screen, (0,255,0), center, int(turn_radius), 2)
        if dist_from_circle > 0 and math.hypot(point[0] - c1[0], point[1] - c1[1]) > r1: # point is outside current turn radius; decrease wheel angle
            #car.brake()
            car.turn_wheels(turn < 0)
            print("Turning wheels straight")
        elif dist_from_circle < 0 and math.hypot(point[0] - c2[0], point[1] - c2[1]) < r2: # point is inside; increase angle
            #car.brake()
            car.turn_wheels(turn > 0)
            print("Turning wheels out")
        else:
            print("Accelerating " + ("forward" if direction > 0 else "backwards"))
            car.accelerate(direction)
            
        if dist < 10:
            print("Braking")
            car.brake(1)
                

    def alignAtPoint(self, point, angle):

        min_turn_rad = 2 * car.l / 3 * math.tan(math.pi / 2 - math.radians(car.MAX_ANGLE))

        # determine if 
        pass


if __name__ == "__main__":

    pygame.init()

    size = (600, 500)
    screen = pygame.display.set_mode(size) # set window size
    pygame.display.set_caption("AutoCar") # set title

    clock = pygame.time.Clock()

    # stuff
    bot = BotDriver()

    done = False
    pos = (300, 250)

    while not done:
        
        # Main event loop
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
        

        # Drawing code here
        screen.fill((255, 255, 255)) # Makes the background white
        bot.driveToPoint(pos, screen)
        bot.car.update()
        bot.car.draw(screen, (255, 0, 0))
        pygame.draw.circle(screen, (0, 255, 0), pos, 3)

        # draw line towards car
        angle = math.atan2(bot.car.y - size[1] / 2, bot.car.x - size[0] / 2)
        dist = max(105 - 100 / (math.hypot(bot.car.y - size[1] / 2, bot.car.x - size[0] / 2) + 1) ** .2, 5)
        pygame.draw.line(screen, (0, 0, 255), (300,250),
                         (size[0] / 2 + math.cos(angle) * dist,
                          size[1] / 2 + math.sin(angle) * dist))

        pygame.display.flip() # Draws the screen
        clock.tick(100) # 60 fps

    # out of loop 
    pygame.quit()
