import pygame

pygame.init()
clock = pygame.time.Clock()
running = True
lucas = pygame.image.load("lucas_down.png")
lucas = pygame.transform.scale_by(lucas, 2)



#player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
horizontal_walking_anims = [pygame.image.load("lucas_walk_right_1.png"), pygame.image.load("lucas_right.png"), pygame.image.load("lucas_walk_right_2.png"), pygame.image.load("lucas_right.png")]
walking_anims_up= [pygame.image.load("lucas_up.png"), pygame.image.load("lucas_walk_up_1.png"), pygame.image.load("lucas_up.png"), pygame.image.load("lucas_walk_up_2.png"),pygame.image.load("lucas_up.png")]
walking_anims_down = [pygame.image.load("lucas_down.png"), pygame.image.load("lucas_walk_down_1.png"), pygame.image.load("lucas_down.png"), pygame.image.load("lucas_walk_down_2.png"), pygame.image.load("lucas_down.png")]
walking_anims_u = [pygame.transform.scale_by(img, 2) for img in walking_anims_up]
walking_anims_d = [pygame.transform.scale_by(img, 2) for img in walking_anims_down]
walking_animations_r = [pygame.transform.scale_by(img, 2) for img in horizontal_walking_anims]
walking_animations_l = [pygame.transform.flip(img,True, False) for img in walking_animations_r]
facing_img = [pygame.image.load("lucas_up.png"), pygame.image.load("lucas_down.png"), pygame.image.load("lucas_left.png"), pygame.image.load("lucas_right.png")]
scaled_facing_img = [pygame.transform.scale_by(img, 2) for img in facing_img]

class Player(pygame.sprite.Sprite):
    def __init__(self, walkanim_up, walkanim_down, walkanim_left, walkanim_right, facing_img):
        super().__init__()
        self.screen_width = 1280
        self.screen_height = 720
        self.index = 0
        self.movement = pygame.Vector2(0,0)
        #Player facing direction
        self.facing = "down"
        self.pressed_keys = []
        #Facing PNGs
        self.facing_img = facing_img
        #Walking animation PNGs
        self.walkanim_up = walkanim_up
        self.walkanim_down = walkanim_down
        self.walkanim_left = walkanim_left
        self.walkanim_right = walkanim_right

        #Sprite
        self.img = facing_img[1]
        self.rect = self.img.get_rect()
        self.zoom = 1
        self.scaled = pygame.Vector2(0,0)

        #Positioning
        self.pos_world = pygame.Vector2(1111,1130)

        #Collision
        self.screen_hitbox = pygame.Rect(0,0, self.rect.width, self.rect.height)
        self.world_hitbox = pygame.Rect(self.pos_world.x, self.pos_world.y, self.rect.width, self.rect.height)
    def update_scaled_dimensions(self):
        self.scaled.x = 32 * self.zoom
        self.scaled.y = 32 * self.zoom

    def animate_walk(self):
        if self.index > 4:
            self.index = 0
        if self.movement.x == 1:
            self.img = walking_animations_r[int(self.index)]
            self.index += 0.1
        elif self.movement.x == -1:
            self.img= walking_animations_l[int(self.index)]
            self.index += 0.1
        elif self.movement.y == 1:
            self.img = walking_anims_u[int(self.index)]
            self.index += 0.1
        elif self.movement.y == -1:
            self.img = walking_anims_d[int(self.index)]
            self.index += 0.1
        else:
            self.img = self.draw_facing()

        w, h = self.img.get_size()   
        scaled_img = pygame.transform.scale(self.img, (w * self.zoom, h* self.zoom))
        self.img = scaled_img
        
    
    def reset_movement_direction(self):
        self.move_right = False
        self.move_left = False
        self.move_up = False
        self.move_down = False
        self.movement = pygame.Vector2(0,0)

    def set_movement_direction(self, direction):
        self.reset_movement_direction()
        #Sets movement direction
        if direction == "up":
            self.move_up = True
            self.update_facing()
            self.animate_walk()
        if direction == "down":
            self.move_down = True
            self.animate_walk()
        if direction == "left":
            self.move_left = True
            self.animate_walk()
        if direction == "right":
            self.move_right = True
            self.animate_walk()
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d):
                if event.key not in self.pressed_keys:
                    self.pressed_keys.append(event.key)

        elif event.type == pygame.KEYUP:
            if event.key in self.pressed_keys:
                self.pressed_keys.remove(event.key)


    def set_movement(self):
        self.reset_movement_direction()
        
        if self.pressed_keys:
            active_key = self.pressed_keys[-1]

            if active_key == pygame.K_w:
                self.movement.y = 1
            elif active_key == pygame.K_s:
                self.movement.y = -1
            elif active_key == pygame.K_a:
                self.movement.x = -1
            elif active_key == pygame.K_d:
                self.movement.x = 1
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            self.zoom += 0.1     
        elif keys[pygame.K_e]:
            if self.zoom > 0.2:
                self.zoom -= 0.1
            
        self.update_scaled_dimensions()
        self.update_hitbox()
        self.update_facing()
        self.animate_walk()

    def update_facing(self):
        if self.movement.y == 1:
            self.facing = "up"
        elif self.movement.y == -1:
            self.facing = "down"
        elif self.movement.x == -1:
            self.facing = "left"
        elif self.movement.x == 1:
            self.facing = "right"

    def draw_facing(self):
        if self.facing == "up":
            return scaled_facing_img[0]
        elif self.facing == "down":
            return scaled_facing_img[1]
        elif self.facing == "left":
            return scaled_facing_img[2]
        elif self.facing == "right":
            return scaled_facing_img[3]
    
    def update_hitbox(self):
        self.screen_hitbox = pygame.Rect((self.screen_width // 2 - self.rect.width // 2 - self.scaled.x //2),(self.screen_height // 2 - self.rect.height // 2 - self.scaled.y // 2), self.rect.width * self.zoom, self.rect.height * self.zoom)
        
player = Player(walking_anims_u, walking_anims_d, walking_animations_l, walking_animations_r, facing_img)
