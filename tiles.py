import pygame, csv, os
import spritesheet

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, spritesheet):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))
class Tilemap():
    def __init__(self, filename, spritesheet):
        self.tilesize = 32
        self.start_x, self.start_y = 0, 0
        self.spritesheet = spritesheet
        self.tiles = self.load_tiles(filename)
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.map_surface.set_colorkey((0, 0, 0))
        self.load_map()


    def draw_map(self, surface, cameraX, cameraY):
        surface.blit(self.map_surface, (cameraX, cameraY))


    def load_map(self):
        for tile in self.tiles:
            tile.draw(self.map_surface)

    def read_csv(self, filename):
        map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
        return map

    def load_tiles(self, filename):
        tiles = []
        map = self.read_csv(filename)
        x, y = 0, 0
        for row in map:
            x = 0
            for tile in row:
                if tile == '0':
                    self.start_x, self.start_y = x * self.tilesize, y * self.tilesize
                elif tile == '1':
                    tiles.append(Tile('industrialTile_02.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '2':
                    tiles.append(Tile('industrialTile_03.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '3':
                    tiles.append(Tile('industrialTile_04.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '4':
                    tiles.append(Tile('industrialTile_05.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '5':
                    tiles.append(Tile('industrialTile_06.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '6':
                    tiles.append(Tile('industrialTile_07.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '7':
                    tiles.append(Tile('industrialTile_08.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '8':
                    tiles.append(Tile('industrialTile_09.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '9':
                    tiles.append(Tile('industrialTile_10.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '10':
                    tiles.append(Tile('industrialTile_11.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '11':
                    tiles.append(Tile('industrialTile_12.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '12':
                    tiles.append(Tile('industrialTile_13.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '13':
                    tiles.append(Tile('industrialTile_14.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '14':
                    tiles.append(Tile('industrialTile_15.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '15':
                    tiles.append(Tile('industrialTile_16.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '16':
                    tiles.append(Tile('industrialTile_17.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '17':
                    tiles.append(Tile('industrialTile_18.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '18':
                    tiles.append(Tile('industrialTile_19.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '19':
                    tiles.append(Tile('industrialTile_20.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '20':
                    tiles.append(Tile('industrialTile_21.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '21':
                    tiles.append(Tile('industrialTile_22.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '22':
                    tiles.append(Tile('industrialTile_23.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '23':
                    tiles.append(Tile('industrialTile_24.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '24':
                    tiles.append(Tile('industrialTile_25.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '25':
                    tiles.append(Tile('industrialTile_26.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '26':
                    tiles.append(Tile('industrialTile_27.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '27':
                    tiles.append(Tile('industrialTile_28.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '28':
                    tiles.append(Tile('industrialTile_29.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '29':
                    tiles.append(Tile('industrialTile_30.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '30':
                    tiles.append(Tile('industrialTile_31.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '31':
                    tiles.append(Tile('industrialTile_32.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '32':
                    tiles.append(Tile('industrialTile_33.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '33':
                    tiles.append(Tile('industrialTile_34.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '34':
                    tiles.append(Tile('industrialTile_35.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '35':
                    tiles.append(Tile('industrialTile_36.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '36':
                    tiles.append(Tile('industrialTile_37.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '37':
                    tiles.append(Tile('industrialTile_38.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '38':
                    tiles.append(Tile('industrialTile_39.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '39':
                    tiles.append(Tile('industrialTile_40.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '40':
                    tiles.append(Tile('industrialTile_41.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '41':
                    tiles.append(Tile('industrialTile_42.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '42':
                    tiles.append(Tile('industrialTile_43.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '43':
                    tiles.append(Tile('industrialTile_44.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '44':
                    tiles.append(Tile('industrialTile_45.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '45':
                    tiles.append(Tile('industrialTile_46.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '46':
                    tiles.append(Tile('industrialTile_47.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '47':
                    tiles.append(Tile('industrialTile_48.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '48':
                    tiles.append(Tile('industrialTile_49.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '49':
                    tiles.append(Tile('industrialTile_50.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '50':
                    tiles.append(Tile('industrialTile_51.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '51':
                    tiles.append(Tile('industrialTile_52.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '52':
                    tiles.append(Tile('industrialTile_53.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '53':
                    tiles.append(Tile('industrialTile_54.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '54':
                    tiles.append(Tile('industrialTile_55.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '55':
                    tiles.append(Tile('industrialTile_56.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '56':
                    tiles.append(Tile('industrialTile_57.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '57':
                    tiles.append(Tile('industrialTile_58.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '58':
                    tiles.append(Tile('industrialTile_59.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '59':
                    tiles.append(Tile('industrialTile_60.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '60':
                    tiles.append(Tile('industrialTile_61.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '61':
                    tiles.append(Tile('industrialTile_62.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '62':
                    tiles.append(Tile('industrialTile_63.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '63':
                    tiles.append(Tile('industrialTile_64.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '64':
                    tiles.append(Tile('industrialTile_65.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '65':
                    tiles.append(Tile('industrialTile_66.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '66':
                    tiles.append(Tile('industrialTile_67.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '67':
                    tiles.append(Tile('industrialTile_68.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '68':
                    tiles.append(Tile('industrialTile_69.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '69':
                    tiles.append(Tile('industrialTile_70.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '70':
                    tiles.append(Tile('industrialTile_71.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '71':
                    tiles.append(Tile('industrialTile_72.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '72':
                    tiles.append(Tile('industrialTile_73.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '73':
                    tiles.append(Tile('industrialTile_74.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '74':
                    tiles.append(Tile('industrialTile_75.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '75':
                    tiles.append(Tile('industrialTile_76.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '76':
                    tiles.append(Tile('industrialTile_77.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '77':
                    tiles.append(Tile('industrialTile_78.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '78':
                    tiles.append(Tile('industrialTile_79.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '79':
                    tiles.append(Tile('industrialTile_80.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '80':
                    tiles.append(Tile('industrialTile_81.png', x * self.tilesize, y * self.tilesize, self.spritesheet))
                elif tile == '81':
                    tiles.append(Tile('industrialTile_82.png', x * self.tilesize, y * self.tilesize, self.spritesheet))

                
                x += 1

            y += 1 
        self.map_w, self.map_h = x * self.tilesize, y * self.tilesize
        return tiles
    
import json

class Spritesheet:
    def __init__(self, filename):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert()
        self.meta_data = self.filename.replace('png', 'json')
        with open(self.meta_data) as f:
            self.data = json.load(f)
        f.close()



    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey((0,0,0))
        sprite.blit(self.sprite_sheet,(0, 0),(x, y, w, h))
        return sprite

    def parse_sprite(self, name):
        sprite = self.data['frames'][name]['frame']
        x, y, w, h = sprite["x"], sprite["y"], sprite["w"], sprite["h"]
        image = self.get_sprite(x, y, w, h)
        return image