import pygame
import math
import random
import numpy as np

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('2D Object Transform')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARKGRAY = (240, 240, 240)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

clock = pygame.time.Clock()

font_style = pygame.font.SysFont(None, 20)
button_font_style = pygame.font.SysFont(None, 30)

def transform(vec, mat):
    return np.dot(mat, vec)

def affine_transform(vec, mat):
        vec_input = np.append(vec, 1)
        vec_transformed = np.dot(mat, vec_input)
        return vec_transformed[:2]

class Object:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rotation_angle = 0
        self.xscale = 1
        self.yscale = 1
    
    def translate(self, event):
        # update self.points, self.x, self.y
        if event.key == pygame.K_RIGHT:
            if local_coordinate:
                rad = self.rotation_angle * math.pi / 180
                translate_matrix = np.array([[1, 0, 10 * math.cos(rad)], [0, 1, 10 * math.sin(rad)], [0, 0, 1]])
            else:
                translate_matrix = np.array([[1, 0, 10], [0, 1, 0], [0, 0, 1]])
            for i in range(len(self.points)): 
                self.points[i] = affine_transform(self.points[i], translate_matrix) 
            self.x = int((self.points[0][0] + self.points[2][0]) / 2)
            self.y = int((self.points[0][1] + self.points[2][1]) / 2)

        if event.key == pygame.K_LEFT:
            if local_coordinate:
                rad = self.rotation_angle * math.pi / 180
                translate_matrix = np.array([[1, 0, -10 * math.cos(rad)], [0, 1, -10 * math.sin(rad)], [0, 0, 1]])
            else: 
                translate_matrix = np.array([[1, 0, -10], [0, 1, 0], [0, 0, 1]])
            for i in range(len(self.points)): 
                self.points[i] = affine_transform(self.points[i], translate_matrix) 
            self.x = int((self.points[0][0] + self.points[2][0]) / 2)
            self.y = int((self.points[0][1] + self.points[2][1]) / 2)

        if event.key == pygame.K_UP:
            if local_coordinate:
                rad = self.rotation_angle * math.pi / 180
                translate_matrix = np.array([[1, 0, 10 * math.sin(rad)], [0, 1, -10 * math.cos(rad)], [0, 0, 1]])
            else: 
                translate_matrix = np.array([[1, 0, 0], [0, 1, -10], [0, 0, 1]])
            for i in range(len(self.points)): 
                self.points[i] = affine_transform(self.points[i], translate_matrix) 
            self.x = int((self.points[0][0] + self.points[2][0]) / 2)
            self.y = int((self.points[0][1] + self.points[2][1]) / 2)

        if event.key == pygame.K_DOWN:
            if local_coordinate:
                rad = self.rotation_angle * math.pi / 180
                translate_matrix = np.array([[1, 0, -10 * math.sin(rad)], [0, 1, 10 * math.cos(rad)], [0, 0, 1]])
            else:     
                translate_matrix = np.array([[1, 0, 0], [0, 1, 10], [0, 0, 1]])
            for i in range(len(self.points)): 
                self.points[i] = affine_transform(self.points[i], translate_matrix) 
            self.x = int((self.points[0][0] + self.points[2][0]) / 2)
            self.y = int((self.points[0][1] + self.points[2][1]) / 2)

    def rotate(self, event):
        # update self.points, self.rotation_angle
        # move the object to origin -> rotate -> move the object to previous position

        origin_matrix = np.array([[1, 0, -self.x], [0, 1, -self.y], [0, 0, 1]])
        inverse_origin_matrix = np.array([[1, 0, self.x], [0, 1, self.y], [0, 0, 1]])

        if event.key == pygame.K_RIGHT:
            rotate_matrix = np.array([[math.cos(math.pi / 18), -math.sin(math.pi / 18)], [math.sin(math.pi / 18), math.cos(math.pi / 18)]])
            for i in range(len(self.points)): 
                self.points[i] = affine_transform(self.points[i], origin_matrix)
                self.points[i] = transform(self.points[i], rotate_matrix)
                self.points[i] = affine_transform(self.points[i], inverse_origin_matrix)
            self.rotation_angle = (self.rotation_angle + 10) % 360

        if event.key == pygame.K_LEFT:
            rotate_matrix = np.array([[math.cos(-math.pi / 18), -math.sin(-math.pi / 18)], [math.sin(-math.pi / 18), math.cos(-math.pi / 18)]])
            for i in range(len(self.points)): 
                self.points[i] = affine_transform(self.points[i], origin_matrix)
                self.points[i] = transform(self.points[i], rotate_matrix)
                self.points[i] = affine_transform(self.points[i], inverse_origin_matrix)
            self.rotation_angle = (self.rotation_angle - 10) % 360

    def scale(self, event):
        # update self.points, self.xscale, self.yscale
        # move the object to origin -> rotate the object to 0 -> scaling -> rotate the object to previous angle -> move the object to previous position
        
        rad = self.rotation_angle * math.pi / 180
        origin_matrix = np.array([[math.cos(-rad), -math.sin(-rad), -self.x * math.cos(-rad) + self.y * math.sin(-rad)],
                                   [math.sin(-rad), math.cos(-rad), -self.x * math.sin(-rad) -self.y * math.cos(-rad)],
                                     [0, 0, 1]])
        inverse_origin_matrix = np.array([[math.cos(rad), -math.sin(rad), self.x],
                                   [math.sin(rad), math.cos(rad), self.y],
                                     [0, 0, 1]])

        if event.key == pygame.K_RIGHT:
            scale_matrix = np.array([[3/2, 0], [0, 1]])
            for i in range(len(self.points)): 
                self.points[i] = affine_transform(self.points[i], origin_matrix)
                self.points[i] = transform(self.points[i], scale_matrix)
                self.points[i] = affine_transform(self.points[i], inverse_origin_matrix)
            self.xscale = round(self.xscale * 3/2, 2)

        if event.key == pygame.K_LEFT:
            scale_matrix = np.array([[2/3, 0], [0, 1]])
            for i in range(len(self.points)): 
                self.points[i] = affine_transform(self.points[i], origin_matrix)
                self.points[i] = transform(self.points[i], scale_matrix)
                self.points[i] = affine_transform(self.points[i], inverse_origin_matrix)
            self.xscale = round(self.xscale * 2/3, 2)

        if event.key == pygame.K_UP:
            scale_matrix = np.array([[1, 0], [0, 3/2]])
            for i in range(len(self.points)): 
                self.points[i] = affine_transform(self.points[i], origin_matrix)
                self.points[i] = transform(self.points[i], scale_matrix)
                self.points[i] = affine_transform(self.points[i], inverse_origin_matrix)
            self.yscale = round(self.yscale * 3/2, 2)

        if event.key == pygame.K_DOWN:
            scale_matrix = np.array([[1, 0], [0, 2/3]])
            for i in range(len(self.points)): 
                self.points[i] = affine_transform(self.points[i], origin_matrix)
                self.points[i] = transform(self.points[i], scale_matrix)
                self.points[i] = affine_transform(self.points[i], inverse_origin_matrix)
            self.yscale = round(self.yscale * 2/3, 2)

class Rectangle(Object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y)
        self.width = width
        self.height = height
        self.points = [[self.x - self.width / 2, self.y - self.height / 2],
                        [self.x + self.width / 2, self.y - self.height / 2],
                          [self.x + self.width / 2, self.y + self.height / 2],
                            [self.x - self.width / 2, self.y + self.height / 2],]

    def draw(self):
        pygame.draw.polygon(screen, GREEN, self.points)
    
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            return self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <=self.y + self.height
        return False

class Button:
    def __init__(self, text, x, y, width, height, color, hover_color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, current_color, self.rect)
        text_surface = button_font_style.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            return self.rect.collidepoint(event.pos)
        return False
    
object_list = []
target_object = Rectangle(300, 300, 30, 30)
object_list.append(target_object)

rectangle_button = Button("Draw Rectangle", 605, 5, 190, 40, DARKGRAY, WHITE)

current_mode = ""
local_coordinate = False

# Game Loop
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if rectangle_button.is_clicked(event):
            target_object = Rectangle(random.randint(100, 500), random.randint(100, 500), 30, 30)
            object_list.append(Rectangle(random.randint(100, 500), random.randint(100, 500), 30, 30))

        for obj in object_list:
            if obj.is_clicked(event):
                target_object = obj

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                current_mode = "Translation"
            if event.key == pygame.K_e:
                current_mode = "Rotation"
            if event.key == pygame.K_r:
                current_mode = "Scale"

            if current_mode == "Translation":
                if event.key == pygame.K_q:
                    local_coordinate = not local_coordinate
                target_object.translate(event)
            if current_mode == "Rotation":
                target_object.rotate(event)
            if current_mode == "Scale":
                target_object.scale(event)

    # Draw
    for obj in object_list:
        obj.draw()

    pygame.draw.rect(screen, GRAY, (600, 0, 200, screen_height))
    rectangle_button.draw(screen)

    text = font_style.render("Transform", True, BLACK)
    text_translation = font_style.render(f"Translation: x: {target_object.x}, y: {target_object.y}", True, BLACK)
    text_rotation = font_style.render(f"Rotation: {target_object.rotation_angle}", True, BLACK)
    text_scale = font_style.render(f"Scale: x: {target_object.xscale}, y: {target_object.yscale}", True, BLACK)
    text_mode = font_style.render(f"Current Mode: {current_mode}", True, BLACK)
    text_coordinate = font_style.render(f"Current Coordinate: {"Local" if local_coordinate else "World"}", True, BLACK)
    screen.blit(text, (620, 100))
    screen.blit(text_translation, (620, 150))
    screen.blit(text_rotation, (620, 200))
    screen.blit(text_scale, (620, 250))
    screen.blit(text_mode, (620, 350))
    screen.blit(text_coordinate, (620, 400))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()