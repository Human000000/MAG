import pygame
import pytmx
import pyscroll

from player import Player
from camera import Camera

class Game:

    def __init__(self):
        self.dash_active = False
       #demarrage ecran de chargement jeu
        self.is_playing = False
        # fenetre
        self.screen = pygame.display.set_mode((1350, 675))
        pygame.display.set_caption("Jeu 1")
        self.compteur = 0
        self.time_dash_loop = 0
        #charger la carte
        tmx_data = pytmx.util_pygame.load_pygame('map/cimetiere.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())


        #changement de carte

        enter_cave = tmx_data.get_object_by_name('enter_cave')
        self.enter_cave_rect = pygame.Rect(enter_cave.x, enter_cave.y, enter_cave.width, enter_cave.height)

        # generer un joueurbdbgq

        player_initial_position = tmx_data.get_object_by_name("spawn j1")

        #dessiner le grp de calques

        self.playerlayer=2
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer)
        self.camera = Camera(self, player_initial_position.x, player_initial_position.y)
        self.group.add(self.camera)
        self.player = Player(player_initial_position.x, player_initial_position.y, 10.5, self)
        self.group.add(self.player)


        map_layer.zoom = 1.5

        #definir les listes d'objets
        self.colision1 = []
        self.colision2 = []
        self.colision3 = []
        self.etage1 = []
        self.etage2 = []
        self.etage3 = []
        self.obj1 = []
        self.obj1_2 = []
        self.obj2 = []
        self.obj2_2 = []
        for obj in tmx_data.objects:
            if obj.name == "collision étage 1":
                self.colision1.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.name == "collision étage 2":
                self.colision2.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.name == "collision étage 3":
                self.colision3.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.name == "mtn étage 1":
                self.etage1.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.name == "mtn étage 2":
                self.etage2.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.name == "mtn étage 3":
                self.etage3.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.name == "comp deco 1":
                self.obj1.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.name == "comp deco1.2":
                self.obj1_2.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.name == "comp deco 2":
                self.obj2.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.name == "comp deco 2.2":
                self.obj2_2.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))


    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if self.player.passeur_dash == 1 and self.dash_active == 1 and self.player.time_dash >=1 and self.player.mana > self.player.mana_cost:
            if pressed[pygame.K_RIGHT] and pressed[pygame.K_DOWN]:
                self.player.dash("bd")
                self.player.time_dash = 0
                self.player.mana -= self.player.mana_cost
            elif pressed[pygame.K_RIGHT] and pressed[pygame.K_UP]:
                self.player.dash("hd")
                self.player.time_dash = 0
                self.player.mana -= self.player.mana_cost
            elif pressed[pygame.K_LEFT] and pressed[pygame.K_DOWN]:
                self.player.dash("bg")
                self.player.time_dash = 0
                self.player.mana -= self.player.mana_cost
            elif pressed[pygame.K_LEFT] and pressed[pygame.K_UP]:
                self.player.dash("hg")
                self.player.time_dash = 0
                self.player.mana -= self.player.mana_cost
            elif pressed[pygame.K_UP]:
                self.player.dash("h")
                self.player.time_dash = 0
                self.player.mana -= self.player.mana_cost
            elif pressed[pygame.K_DOWN]:
                self.player.dash("b")
                self.player.time_dash = 0
                self.player.mana -= self.player.mana_cost
            elif pressed[pygame.K_LEFT]:
                self.player.dash("g")
                self.player.time_dash = 0
                self.player.mana -= self.player.mana_cost
            elif pressed[pygame.K_RIGHT]:
                self.player.dash("d")
                self.player.time_dash = 0
                self.player.mana -= self.player.mana_cost
            self.dash_active = False

        else:
            self.player.compteur_dash += 1
            if self.player.compteur_dash == 1:
                self.player.passeur_dash = True
                self.player.compteur_dash = 0

        self.player.save_location()
        self.camera.save_location()

        if pressed[pygame.K_RIGHT] and pressed[pygame.K_DOWN]:
            self.player.move_rightdown()
            self.camera.move_rightdown()
            self.player.change_animation('down-right')

        elif pressed[pygame.K_RIGHT] and pressed[pygame.K_UP]:
            self.player.move_rightup()
            self.camera.move_rightup()
            self.player.change_animation('up-right')

        elif pressed[pygame.K_LEFT] and pressed[pygame.K_DOWN]:
            self.player.move_leftdown()
            self.camera.move_leftdown()
            self.player.change_animation('down-left')
        elif pressed[pygame.K_LEFT] and pressed[pygame.K_UP]:
            self.player.move_leftup()
            self.camera.move_leftup()
            self.player.change_animation('up-left')
        elif pressed[pygame.K_UP]:
            self.player.move_up()
            self.camera.move_up()
            self.player.change_animation('up')
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
            self.camera.move_down()
            self.player.change_animation('down')
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
            self.camera.move_left()
            self.player.change_animation('left')
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.camera.move_right()
            self.player.change_animation('right')

    def switch_cave(self):
        self.screen = pygame.display.set_mode((1350, 675))
        pygame.display.set_caption("Jeu")

        self.compteur = 0
        self.time_dash_loop = 0
        # charger la carte
        tmx_data = pytmx.util_pygame.load_pygame('map/cave.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())

        # music
        # changement de carte
        # generer un joueur
        player_initial_position = tmx_data.get_object_by_name("spawn_cave")

        # dessiner le grp de calques
        self.playerlayer = 2
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer)
        self.player = Player(player_initial_position.x, player_initial_position.y, 10.5, self)
        self.group.add(self.player)
        map_layer.zoom = 1.5

        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))




    def update(self):
        self.group.update()

        if self.player.feet.colliderect(self.enter_cave_rect):
            self.switch_cave()


        for sprite in self.group.sprites():
            if self.player.feet.collidelist(self.etage1) > -1:
                self.playerlayer = 1
                self.player.move_etage1()
            elif self.player.feet.collidelist(self.etage2) > -1:
                self.playerlayer = 2
                self.player.move_etage2()
            elif self.player.feet.collidelist(self.etage3) > -1:
                self.playerlayer = 3
                self.player.move_etage3()


        # verfif colision
        if self.playerlayer == 1:
            for sprite in self.group.sprites():
                if self.player.feet.collidelist(self.colision1) > -1:
                    self.player.move_back()
                    self.camera.move_back()
                if self.player.feet.collidelist(self.obj1_2) > -1:
                    self.player.objet1_2()
                elif self.player.feet.collidelist(self.obj1) > -1:
                    self.player.objet1()
                else:
                    self.player.move_etage1()
        elif self.playerlayer == 2:
            for sprite in self.group.sprites():
                if self.player.feet.collidelist(self.colision2) > -1:
                    self.player.move_back()
                    self.camera.move_back()
                if self.player.feet.collidelist(self.obj2_2) > -1:
                    self.player.objet2_2()
                elif self.player.feet.collidelist(self.obj2) > -1:
                    self.player.objet2_2()
                else:
                    self.player.move_etage2()
        elif self.playerlayer == 3:
            for sprite in self.group.sprites():
                if self.player.feet.collidelist(self.colision3) > -1:
                    self.player.move_back()
                    self.camera.move_back()



    def run(self):

        clock = pygame.time.Clock()
        # boucle
        running = True

        while running:

            self.player.all_var_1()
            self.player.super_compteur_vie()
            self.player.save_location()
            self.camera.save_location()
            self.handle_input()
            self.player.time_dash_player()
            self.player.damage_take()
            self.update()
            self.group.center(self.camera.rect.center)
            self.group.draw(self.screen)
            self.player.tremblement_de_vol()
            self.player.update_barre_vie(self.screen)
            self.player.update_barre_mana(self.screen)

            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.dash_active = True
                    else:
                        self.dash_active = False
                elif event.type == pygame.KEYUP:
                    self.dash_active = False
            if self.player.pv < 0:
                running = False


            clock.tick(120)
        pygame.quit()

