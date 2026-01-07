from pytmx.util_pygame import load_pygame
import pytmx
import pygame
from collider import Collider


filename = "[Tiled] Pokémon Platinum/Twinleaf Town.tmx"

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        

class Map:
    def __init__(self, filename):
        self.tmxdata = load_pygame(filename)
        self.background_group = pygame.sprite.Group()
        self.object_group = pygame.sprite.Group()
        self.colliders = []
        self.spawn_point = pygame.Vector2(0,0)

        self.mov_dir = None
        self.world_size = (self.tmxdata.width * self.tmxdata.tilewidth, self.tmxdata.height * self.tmxdata.tileheight)
        self.scaled = pygame.Vector2(0,0)

        self.offset = pygame.Vector2(0,0)

    
        for layer in self.tmxdata.layers:
            if hasattr(layer, "data"):
                for x,y,surf in layer.tiles():
                    pos = (x * 32, y * 32)
                    Tile(pos = pos, surf = surf, groups = self.background_group)


        
        for obj in self.tmxdata.objects:
            pos = (obj.x, obj.y)
            if obj.image:
                Tile(pos, surf = obj.image, groups = self.object_group)
                for gid, colliders in self.tmxdata.get_tile_colliders():
                    for collider in colliders:
                        if obj.name in collider.name:
                            col = Collider(obj.x + collider.x, obj.y + collider.y, collider.width, collider.height, collider.name)
                            self.colliders.append(col)
        
        entities = self.tmxdata.get_layer_by_name("Entities")

        for ent in entities:
            if ent.properties["pos"] == "Home":
                self.spawn_point = pygame.Vector2(ent.x, ent.y)

    
    
    
    def get_groups(self):

        return self.background_group, self.object_group, self.colliders

twinleaf_town = Map("[Tiled] Pokémon Platinum/Twinleaf Town.tmx")

