import pygame


class Camera(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        super().__init__()
        self.game = game

        image = pygame.image.load('autre/transparent.png')
        self.image = self.get_image(0, 0, image)
        self.rect = self.image.get_rect()
        self.position = [496, 139]
        self._layer = 100
        self.speed = 1
        self.old_position_cam = self.position.copy()

    def update(self):
        self.rect.topleft = self.position

    def get_image(self, x, y, dessin):
        image = pygame.Surface([10, 10])
        image.blit(dessin, (0, 0), (x, y, 10, 10))
        return image

    def move_leftup(self):
        self.position[0] -= self.speed
        self.position[1] -= self.speed

    def move_leftdown(self):
        self.position[0] -= self.speed
        self.position[1] += self.speed

    def move_rightup(self):
        self.position[0] += self.speed
        self.position[1] -= self.speed

    def move_rightdown(self):
        self.position[0] += self.speed
        self.position[1] += self.speed

    def move_right(self):
        self.position[0] += self.speed

    def move_left(self):
        self.position[0] -= self.speed

    def move_up(self):
        self.position[1] -= self.speed

    def move_down(self):
        self.position[1] += self.speed

    def save_location(self):
        self.old_position_cam = self.position.copy()


    def move_back(self):

        self.position = self.old_position_cam.copy()
        self.rect.topleft = self.position
