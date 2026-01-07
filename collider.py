import pygame

class Collider:
    def __init__(self, x, y, width, height, name):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.name = name

        self.zoom = 1
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def scale_collider(self, offset, zoom):
        scaled_rect = pygame.Rect((self.x + offset.x) * zoom,
                (self.y + offset.y)*zoom, self.width * zoom, self.height * zoom)
        
        self.set_rect(scaled_rect)
    

    def set_rect(self, new_rect):
        self.rect = new_rect