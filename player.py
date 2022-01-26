import pygame
import pytmx
import pyscroll


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, _layer, game):
        super().__init__()
        self.game = game
        self.sprite_sheet1 = pygame.image.load('fantome/fantome__face1.png')
        self.image = self.get_image(24, 9, self.sprite_sheet1)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()

        self.compteur_dash = 0
        self.passeur_dash = True
        self.compteur = 0
        self.time_dash = 5
        self.time_dash_reel = 1

        self.barre_mana_x = 147
        self.barre_mana_y = 107
        self.mana = 125
        self.mana_reel= 125
        self.mana_cost = 20
        self.mana_regen = False

        self.barre_x = 150
        self.barre_x_save = self.barre_x
        self.barre_y = 65
        self.barre_y_save = self.barre_y
        self.pv = 210
        self.pv_reel = 210
        self.super_compteur = 0
        self.position = [x, y]
        self._layer = _layer
        self.speed = 1
        self.sprite_sheet2 = pygame.image.load('fantome/fantome__face2.png')
        self.sprite_sheet3 = pygame.image.load('fantome/fantome__face3.png')
        self.sprite_sheet4 = pygame.image.load('fantome/fantome__face4.png')
        self.sprite_sheet5 = pygame.image.load('fantome/fantome__face5.png')
        self.sprite_sheet6 = pygame.image.load('fantome/fantome__face6.png')
        self.sprite_sheet7 = pygame.image.load('fantome/fantome__face7.png')
        self.sprite_sheet8 = pygame.image.load('fantome/fantome__face8.png')
        self.images = {
            'up': self.get_image(24,9,self.sprite_sheet5),
            'down': self.get_image(24,9, self.sprite_sheet1),
            'left': self.get_image(24,9, self.sprite_sheet7),
            'right': self.get_image(24,9, self.sprite_sheet3),
            'up-right': self.get_image(24,9, self.sprite_sheet4),
            'up-left': self.get_image(24,9, self.sprite_sheet6),
            'down-right': self.get_image(24,9, self.sprite_sheet2),
            'down-left': self.get_image(24,9, self.sprite_sheet8)

        }
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 1)
        self.old_position = self.position.copy()
        image__barre = pygame.image.load('autre/barre_de_vie.png')
        self.image_barre = pygame.transform.scale(image__barre, (400, 550))



    def change_animation(self, name):
        self.image = self.images[name]
        self.image.set_colorkey((0, 0, 0))

    def objet1_2(self):
        self.game.group.change_layer(sprite=self, new_layer=4)

    def objet1(self):
        self.game.group.change_layer(sprite=self, new_layer=5)

    def objet2(self):
        self.game.group.change_layer(sprite=self, new_layer=11)

    def objet2_2(self):
        self.game.group.change_layer(sprite=self, new_layer=12)

    def move_etage1(self):
        self.game.group.change_layer(sprite=self, new_layer=7)

    def move_etage2(self):
        self.game.group.change_layer(sprite=self, new_layer=14)

    def move_etage3(self):
        self.game.group.change_layer(sprite=self, new_layer=19)

    def save_location(self):
        self.old_position=self.position.copy()


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

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom


    def get_image(self, x, y, dessin):
        image = pygame.Surface([47, 61])
        image.blit(dessin, (0, 0), (x, y, 47,61))
        return image

    def update_barre_vie(self, surface):

        self.bar_couleur = (57, 155, 20)
        self.bar_position = [self.barre_x, self.barre_y, self.pv, 30]
        pygame.draw.rect(surface, self.bar_couleur, self.bar_position)
        if self.pv <= self.pv_reel * 25 / 100:
            self.bar_couleur = (254, 27, 0)
            self.bar_position = [self.barre_x, self.barre_y, self.pv, 30]
            pygame.draw.rect(surface, self.bar_couleur, self.bar_position)
        elif self.pv <= self.pv_reel * 50 / 100:
            self.bar_couleur = (255, 131, 0)
            self.bar_position = [self.barre_x, self.barre_y, self.pv, 30]
            pygame.draw.rect(surface, self.bar_couleur, self.bar_position)


    def draw_rect_alpha(self, surface, color, rect):
        shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
        surface.blit(shape_surf, rect)

    def update_barre_mana(self, surface):
        self.bar_couleur = (44, 117, 255)
        self.bar_position = [self.barre_mana_x, self.barre_mana_y, self.mana, 13]
        pygame.draw.rect(surface, self.bar_couleur, self.bar_position)
        if self.mana < self.mana_reel:
            self.mana_regen = True
        self.game.screen.blit(self.image_barre, (-15, -130))

        longueur_barre_verre = self.pv_reel + 1 - self.pv
        x_barre_verre = self.barre_x + self.pv
        self.draw_rect_alpha(self.game.screen, (0, 0, 0, 90), (x_barre_verre, self.barre_y, longueur_barre_verre, 30))

        longueur_verre_mana = self.mana_reel + 1 - self.mana
        x_verre_mana = self.barre_mana_x + self.mana
        self.draw_rect_alpha(self.game.screen, (0, 0, 0, 90), (x_verre_mana, self.barre_mana_y, longueur_verre_mana, 13))

    def super_compteur_vie(self):
        if self.compteur%5 == 0 :
            self.super_compteur += 1


    def damage_take(self):
        if self.super_compteur == 1:
            self.barre_x += 1
            self.barre_y += 1
        elif self.super_compteur == 2:
            self.barre_x -= 2.5
            self.barre_y -= 2.5
        elif self.super_compteur == 3:
            self.barre_x += 2.5
            self.barre_y += 2.5
        elif self.super_compteur == 4:
            self.barre_x -= 1
            self.barre_y -= 1
        elif self.super_compteur == 5:
            self.barre_x = self.barre_x_save
            self.barre_y = self.barre_y_save
            self.super_compteur -= 40
            self.pv -= 10

    def dash(self, direction):
        self.passeur_dash = False
        if direction == "hd":
            for i in range(50):
                self.save_location()
                self.move_rightup()
                self.game.update()
        elif direction == "hg":
            for i in range(50):
                self.save_location()
                self.move_leftup()
                self.game.update()
        elif direction == "bg":
            for i in range(50):
                self.save_location()
                self.move_leftdown()
                self.game.update()
        elif direction == "bd":
            for i in range(50):
                self.save_location()
                self.move_rightdown()
                self.game.update()
        elif direction == "h":
            for i in range(75):
                self.save_location()
                self.move_up()
                self.game.update()
        elif direction == "d":
            for i in range(75):
                self.save_location()
                self.move_right()
                self.game.update()
        elif direction == "b":
            for i in range(75):
                self.save_location()
                self.move_down()
                self.game.update()
        elif direction == "g":
            for i in range(75):
                self.save_location()
                self.move_left()
                self.game.update()

    def time_dash_player(self):
        if self.game.time_dash_loop %30 == 0 :
            self.time_dash += 1

    def all_var_1(self):

        self.game.time_dash_loop += 1
        self.compteur += 1
        if self.mana % self.mana_reel == 0:
            self.mana_regen = False
        elif self.mana < self.mana_reel:
            self.mana += 0.2

    def tremblement_de_vol(self):
        if self.compteur%30 == 0:
            self.position[1] += 1
        elif self.compteur%15 == 0:
            self.position[1] -= 1