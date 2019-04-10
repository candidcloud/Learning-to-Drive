import os
import pygame
from math import tan, radians, degrees, copysign
from pygame.math import Vector2


class Car:
    def __init__(self, x, y, angle=0.0, length=2, max_steering=30, max_acceleration=5.0):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.length = length
        self.max_acceleration = max_acceleration
        self.max_steering = max_steering
        self.max_velocity = 20
        self.brake_deceleration = 25
        self.free_deceleration = 5

        self.acceleration = 0.0
        self.steering = 0.0

    def update(self, dt):
        self.velocity += (self.acceleration * dt, 0)
        self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))

        if self.steering:
            turning_radius = self.length / tan(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0

        self.position += self.velocity.rotate(-self.angle) * dt
        self.angle += degrees(angular_velocity) * dt


class Environment:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Go Q-Racer, go Q-Racer, go!")
        self.display_width = 1280
        self.display_height = 720
        self.screen = pygame.display.set_mode((self.display_width, self.display_height))
        self.clock = pygame.time.Clock()
        self.ticks = 60 # frames per second. Or iterations of the while loop per second. Might need to adjust depending on how long calculations take
        self.exit = False # flag for overall game loop

    colors = {'black': (0,0,0), 'white':(255,255,255), 'red':(255,0,0), 'green':(0,255,0), 'asphalt':(160,160,160)}

    def get_track(self):
        pygame.draw()

    def run(self):
        # Define colors in RGB format
        BLACK =     (0,0,0)         #
        WHITE =     (255,255,255)   #
        RED =       (255,0,0)       # car color when wall is hit?
        GREEN =     (76,153,0)      # grass
        ASPHALT =   (160,160,160)   # track

        # find and load car picture in current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "car25.png")
        car_image = pygame.image.load(image_path)
        ppu = 8 # pixel per unit ratio
        car = Car(self.display_width//2//ppu, self.display_height//5//ppu) #initializes car sprite
        # track = self.get_track()


        while not self.exit:
            dt = self.clock.get_time() / 1000

            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # if user clicks 'close'
                    self.exit = True

            # User input
            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_UP]:
                if car.velocity.x < 0:
                    car.acceleration = car.brake_deceleration
                else:
                    car.acceleration += 3 * dt
            elif pressed[pygame.K_DOWN]:
                if car.velocity.x > 0:
                    car.acceleration = -car.brake_deceleration
                else:
                    car.acceleration -= 3 * dt
            elif pressed[pygame.K_SPACE]:
                if abs(car.velocity.x) > dt * car.brake_deceleration:
                    car.acceleration = -copysign(car.brake_deceleration, car.velocity.x)
                else:
                    car.acceleration = -car.velocity.x / dt
            else:
                if abs(car.velocity.x) > dt * car.free_deceleration:
                    car.acceleration = -copysign(car.free_deceleration, car.velocity.x)
                else:
                    if dt != 0:
                        car.acceleration = -car.velocity.x / dt
            car.acceleration = max(-car.max_acceleration, min(car.acceleration, car.max_acceleration))

            if pressed[pygame.K_RIGHT]:
                car.steering -= 50 * dt
            elif pressed[pygame.K_LEFT]:
                car.steering += 50 * dt
            else:
                car.steering = 0
            car.steering = max(-car.max_steering, min(car.steering, car.max_steering))

            # Logic
            car.update(dt)

            # Drawing
            self.screen.fill(GREEN)
            rotated = pygame.transform.rotate(car_image, car.angle)
            rect = rotated.get_rect()
            self.screen.blit(rotated, car.position * ppu - (rect.width / 2, rect.height / 2))
            pygame.display.update() #draws contents on screen

            self.clock.tick(self.ticks)
        pygame.quit()



if __name__ == '__main__':
    environment = Environment()
    environment.run()
