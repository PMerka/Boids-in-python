import pygame
import tkinter as tk
import numpy as np
import random

class Boid:
    def __init__(self):
        self.position = np.array([random.randrange(200, 800), random.randrange(200, 600)], dtype=float)
        self.speed = np.array(self.random_speed(2), dtype=float)
    
    def getvalues(self):
        #get value from tkinter gui
        self.align_force_constant = alignment.force_constant.get()
        self.cohesion_force_constant = atraction.force_constant.get()
        self.separation_force_constant = repulsion.force_constant.get()*100

        self.align_perception_radius = alignment.perception_radius.get()
        self.cohesion_perception_radius = atraction.perception_radius.get()
        self.separation_perception_radius = repulsion.perception_radius.get()

        self.align_max_force_constant = alignment.max_force_constant.get()
        self.cohesion_max_force_constant = atraction.max_force_constant.get()
        self.separation_max_force_constant = repulsion.max_force_constant.get()

    def random_speed(self, speed_size):
        #create random speed
        angle = random.randrange(0, 360)
        speed = [speed_size*np.sin(np.deg2rad(angle)), speed_size*np.cos(np.deg2rad(angle))]
        return speed

    def change_position(self):
        self.position += self.speed
        if self.position[0] > 1000:
            self.position[0] = 0
        if self.position[0] < 0:
            self.position[0] = 1000
        if self.position[1] > 800:
            self.position[1] = 0
        if self.position[1] < 0:
            self.position[1] = 800
    
    def change_speed(self):
        self.speed = self.speed + self.align_force_constant * self.align_force +  self.cohesion_force_constant * self.cohesion_force + self.separation_force_constant * self.separation_force + 100 * self.wall_force
        size = np.sqrt(self.speed.dot(self.speed))
        if size > 5:
            self.speed= 5 * self.speed / size

    def align(self, boids_list):
        R_perception = self.align_perception_radius
        number_percepted = 0
        force_maxsize = self.align_max_force_constant
        local_speed = np.array([0, 0], dtype=float)
        for boid in boids_list:
            dist = distance(boid.position, self.position)
            if dist < R_perception:
                local_speed += boid.speed
                number_percepted += 1
        avg_local_speed = local_speed / number_percepted
        self.align_force = avg_local_speed - self.speed

        size = np.sqrt(self.align_force.dot(self.align_force))
        if size > force_maxsize:
            self.align_force = 5 *self.align_force/size

    def cohesion(self, boids_list):
        R_perception = self.cohesion_perception_radius
        number_percepted = 0
        force_maxsize = self.cohesion_max_force_constant
        local_position = np.array([0, 0], dtype=float)
        for boid in boids_list:
            dist = distance(boid.position, self.position)
            if (dist < R_perception) and (self != boid):
                local_position += boid.position
                number_percepted += 1
        if number_percepted > 0:
            avg_local_position = local_position / number_percepted
            self.cohesion_force = avg_local_position - self.position
        else:
            self.cohesion_force = np.array([0, 0], dtype=float)

        size = np.sqrt(self.cohesion_force.dot(self.cohesion_force))
        if size > force_maxsize:
            self.cohesion_force = 5 *self.cohesion_force/size


    def separation(self, boids_list):
        R_perception = self.separation_perception_radius
        number_percepted = 0
        force_maxsize = self.separation_max_force_constant
        separation_force = np.array([0, 0], dtype=float)
        for boid in boids_list:
            dist = distance(boid.position, self.position)
            if (dist < R_perception) and (self != boid):
                separation_force += (self.position - boid.position) / (dist * dist)
                number_percepted += 1
        self.separation_force = separation_force   
        size = np.sqrt(self.separation_force.dot(self.separation_force))
        if size > force_maxsize:
            self.separation_force = 10 * self.separation_force/size 

    def walls_force(self):
        self.wall_force = np.array([0, 0], dtype=float)
        if self.position[1] < 150:
            self.wall_force = np.array([0, 1], dtype=float) / (150 - self.position[1])
        if self.position[1] > 650:
            self.wall_force = np.array([0, -1], dtype=float) / (self.position[1] - 650)
        if self.position[0] < 150:
            self.wall_force = np.array([1, 0], dtype=float) / (150 - self.position[0])
        if self.position[0] > 850:
            self.wall_force = np.array([-1, 0], dtype=float) / (self.position[0] - 850)

    def draw(self):    
        rotated = pygame.transform.rotate(myimg, pngangle(self.speed))
        screen.blit(rotated, tuple(self.position))


def pngangle(vector):
    size = np.sqrt(vector.dot(vector))
    if size > 0:
        x = vector / np.sqrt(vector.dot(vector))
        alpha = np.rad2deg(np.arcsin(x[1]))
        if x[0] < 0:
            if x[1] < 0:
                return 180 + alpha
            else:
                return -180 + alpha
        else:    
            return -alpha
    else:
        return 0
    
def distance(vector1, vector2):
    vector = vector1 - vector2
    return np.sqrt(vector.dot(vector))

boids_list = []
boids_number = 50


#pygame window init
pygame.init()
size = (1000,800)
screen = pygame.display.set_mode(size)
FPS = 60 # frames per second setting
fpsClock = pygame.time.Clock()
myimg = pygame.image.load('arrow1.png')

#tkinter window init
root = tk.Tk()
framex = tk.Frame(root, width = 100, height = 500)

class Condition_segment:
    #one frame with parametrs
    def __init__(self, row_num, title):
        frame = tk.LabelFrame(root, text=title, font="Arial 12", padx=5, pady=5)
        
        collumn_separation=5 #space between columns

        #Labels
        self.force_constant_title = tk.Label(frame, text="Force constant", font="Arial 10")
        self.force_constant_title.grid(row=(row_num), column=0, sticky=tk.W, pady=(10, 0), padx=collumn_separation)

        self.perception_radius_title = tk.Label(frame, text="Perception radius", font="Arial 10")
        self.perception_radius_title.grid(row=(row_num), column=1, sticky=tk.W, pady=(10, 0), padx=collumn_separation)

        self.perception_radius_title = tk.Label(frame, text="Max force", font="Arial 10")
        self.perception_radius_title.grid(row=(row_num), column=2, sticky=tk.W, pady=(10, 0), padx=collumn_separation)

        #Sliders
        self.force_constant = tk.Scale(frame, from_=0.0, to=5.0, digits = 3, resolution = 0.01, orient=tk.HORIZONTAL, length=150)
        self.force_constant.grid(row=(row_num+1), column=0, padx=collumn_separation)
        self.force_constant.set(1.00)

        self.perception_radius = tk.Scale(frame, from_=0.0, to=100.0, digits = 3,resolution = 0.1, orient=tk.HORIZONTAL, length=150)
        self.perception_radius.grid(row=(row_num+1), column=1, padx=collumn_separation)
        self.perception_radius.set(50.00)

        self.max_force_constant = tk.Scale(frame, from_=0.0, to=10.0, digits = 3, resolution = 0.1, orient=tk.HORIZONTAL, length=150)
        self.max_force_constant.grid(row=(row_num+1), column=2, padx=collumn_separation)
        self.max_force_constant.set(1.00)

        frame.pack(padx=15, pady=5)

alignment = Condition_segment(0, "Alignment")
repulsion = Condition_segment(3, "Repulsion")
atraction = Condition_segment(3, "Atraction")


class Main_loop:
    def __init__(self):
        self.running = True
        self.main()

    def main(self):
        for i in range(boids_number):
            boids_list.append(Boid())

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()

            screen.fill((200, 250, 250))

            for boid in boids_list:
                boid.getvalues()
                boid.draw()
                boid.align(boids_list)
                boid.cohesion(boids_list)
                boid.separation(boids_list)
                boid.walls_force()
                boid.change_speed()
                boid.change_position()

            pygame.display.update()

            root.update() 
            root.protocol("WM_DELETE_WINDOW", self.close)
            fpsClock.tick(FPS)

    def close(self):
        self.running = False

mainloop=Main_loop()
