import pygame
from map import twinleaf_town
from player import player

class Camera:
    def __init__(self):
        self.background_group = None
        self.object_group = None
        self.mov_dir = None
        
        self.screen_width = 1280
        self.screen_height = 720
        self.offset = pygame.Vector2(player.rect.centerx - self.screen_width // 2,player.rect.centery - self.screen_height // 2)
        
        #Zoom
        self.zoom = 1

        #Colliders
        self.display_colliders = True
        self.scaled_colliders = []

    def set_groups(self):
        self.background_group, self.object_group, self.colliders = twinleaf_town.get_groups()


    def draw_map(self, screen):
        self.scaled_colliders.clear()
        self.set_groups()

        temp_surface = pygame.Surface((twinleaf_town.world_size[0], twinleaf_town.world_size[1]), pygame.SRCALPHA)
        for sprite in self.background_group:
            temp_surface.blit(sprite.image, sprite.rect.topleft + self.offset)

        for obj in self.object_group:
            temp_surface.blit(obj.image, obj.rect.topleft + self.offset)
        
        twinleaf_town.scaled.x = twinleaf_town.world_size[0] * self.zoom
        twinleaf_town.scaled.y = twinleaf_town.world_size[1] * self.zoom
        scaled_surface = pygame.transform.scale(temp_surface,(int(twinleaf_town.world_size[0] * self.zoom), int(twinleaf_town.world_size[1] * self.zoom))
    )   
        if self.display_colliders:
            for col in twinleaf_town.colliders:
                col.scale_collider( self.offset, self.zoom)
                pygame.draw.rect(scaled_surface, (255,0,0), col.rect, 2)
                if player.world_hitbox.colliderect(col.rect):
                    print(f"collided with {col.name}")

        scaled_map = pygame.Vector2(self.screen_width // 2 - twinleaf_town.scaled.x // 2, self.screen_height // 2 - twinleaf_town.scaled.y // 2)

        screen.blit(scaled_surface, (scaled_map.x,scaled_map.y))
        screen.blit(player.img, (self.screen_width // 2, self.screen_height // 2))
        #pygame.draw.rect(screen, (255,0,0), player.screen_hitbox, 2)
        print(twinleaf_town.spawn_point.x, twinleaf_town.spawn_point.y)

    def update_offset(self):
        if self.mov_dir == "up":
            self.offset += pygame.Vector2(0,2)
        elif self.mov_dir == "down":
            self.offset += pygame.Vector2(0,-2)
        elif self.mov_dir == "right":
            self.offset += pygame.Vector2(-2,0)
        elif self.mov_dir == "left":
            self.offset += pygame.Vector2(2,0)
        

    def get_movement(self):
        self.reset_movement_direction()
        #Get user input for map movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.mov_dir = "up"
        elif keys[pygame.K_s]:
            self.mov_dir = "down"
        elif keys[pygame.K_a]:
            self.mov_dir = "left"
        elif keys[pygame.K_d]:
            self.mov_dir = "right"
        self.update_offset()
    
    def reset_movement_direction(self):
        self.mov_dir = None

    def zoom_in(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            self.zoom += 0.1
        elif keys[pygame.K_e]:
            if self.zoom > 0.2:
                self.zoom -= 0.1
            else: 
                pass

camera = Camera()