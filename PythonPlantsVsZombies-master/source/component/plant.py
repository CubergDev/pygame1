__author__ = 'from cuberg with love'

import os
import pygame as pg
from .. import tool
from .. import constants as c

class Car(pg.sprite.Sprite):
    def __init__(self, x, y, map_y):
        super().__init__()
        rect = tool.GFX[c.CAR].get_rect()
        self.image = tool.get_image(tool.GFX[c.CAR], 0, 0, rect.w, rect.h)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y
        self.map_y = map_y
        self.state = c.IDLE
        self.dead = False

    def update(self, game_info):
        self.current_time = game_info[c.CURRENT_TIME]
        if self.state == c.WALK:
            self.rect.x += 4
            if self.rect.x > c.SCREEN_WIDTH:
                self.dead = True

    def setWalk(self):
        if self.state == c.IDLE:
            self.state = c.WALK

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Bullet(pg.sprite.Sprite):
    def __init__(self, x, start_y, dest_y, name, damage, ice=False):
        super().__init__()
        self.name = name
        self.frames = []
        self.frame_index = 0
        self.load_images()
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = start_y
        self.dest_y = dest_y
        self.y_vel = 4 if (dest_y > start_y) else -4
        self.x_vel = 4
        self.damage = damage
        self.ice = ice
        self.radius = self.rect.w // 2
        self.state = c.FLY
        self.current_time = 0

    def loadFrames(self, frames, name):
        frame_list = tool.GFX[name]
        if name in tool.PLANT_RECT:
            data = tool.PLANT_RECT[name]
            x, y, width, height = data['x'], data['y'], data['width'], data['height']
        else:
            x = y = 0
            rect = frame_list[0].get_rect()
            width, height = rect.w, rect.h
        for frame in frame_list:
            frames.append(tool.get_image(frame, x, y, width, height))

    def load_images(self):
        self.fly_frames = []
        self.explode_frames = []
        self.loadFrames(self.fly_frames, self.name)
        self.loadFrames(self.explode_frames, 'PeaNormalExplode')
        self.frames = self.fly_frames

    def update(self, game_info):
        self.current_time = game_info[c.CURRENT_TIME]
        if self.state == c.FLY:
            if self.rect.y != self.dest_y:
                self.rect.y += self.y_vel
                if self.y_vel * (self.dest_y - self.rect.y) < 0:
                    self.rect.y = self.dest_y
            self.rect.x += self.x_vel
            if self.rect.x > c.SCREEN_WIDTH:
                self.kill()
        elif self.state == c.EXPLODE:
            if(self.current_time - self.explode_timer) > 500:
                self.kill()

    def setExplode(self):
        self.state = c.EXPLODE
        self.explode_timer = self.current_time
        self.frames = self.explode_frames
        self.image = self.frames[self.frame_index]

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Plant(pg.sprite.Sprite):
    def __init__(self, x, y, name, health, bullet_group=None, scale=1):
        super().__init__()
        self.frames = []
        self.frame_index = 0
        self.loadImages(name, scale)
        self.frame_num = len(self.frames)
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.name = name
        self.health = health
        self.max_health = health
        self.state = c.IDLE
        self.bullet_group = bullet_group
        self.can_sleep = False
        self.animate_timer = 0
        self.animate_interval = 100
        self.hit_timer = 0
        self.fire_rate_multiplier = 1
        self.sun_multiplier = 1

        sound_path = os.path.join("resources", "sound", f"{name}.wav")
        self.sound = pg.mixer.Sound(sound_path) if os.path.exists(sound_path) else None

    def loadFrames(self, frames, name, scale, color=c.BLACK):
        frame_list = tool.GFX[name]
        if name in tool.PLANT_RECT:
            data = tool.PLANT_RECT[name]
            x, y, width, height = data['x'], data['y'], data['width'], data['height']
        else:
            x = y = 0
            rect = frame_list[0].get_rect()
            width, height = rect.w, rect.h
        for frame in frame_list:
            frames.append(tool.get_image(frame, x, y, width, height, color, scale))

    def loadImages(self, name, scale):
        self.loadFrames(self.frames, name, scale)

    def changeFrames(self, frames):
        self.frames = frames
        self.frame_num = len(self.frames)
        self.frame_index = 0
        bottom = self.rect.bottom
        x = self.rect.x
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.bottom = bottom
        self.rect.x = x

    def update(self, game_info):
        self.current_time = game_info[c.CURRENT_TIME]
        self.handleState()
        self.animation()

    def handleState(self):
        if self.state == c.IDLE:
            self.idling()
        elif self.state == c.ATTACK:
            self.attacking()

    def idling(self):
        pass

    def attacking(self):
        pass

    def animation(self):
        if (self.current_time - self.animate_timer) > self.animate_interval:
            self.frame_index += 1
            if self.frame_index >= self.frame_num:
                self.frame_index = 0
            self.animate_timer = self.current_time
        self.image = self.frames[self.frame_index]
        if(self.current_time - self.hit_timer) >= 200:
            self.image.set_alpha(255)
        else:
            self.image.set_alpha(192)

    def play_sound(self):
        if self.sound:
            self.sound.play()

    def canAttack(self, zombie):
        if self.state != c.SLEEP and zombie.state != c.DIE and self.rect.x <= zombie.rect.right:
            return True
        return False

    def setAttack(self):
        self.state = c.ATTACK

    def setIdle(self):
        self.state = c.IDLE

    def setDamage(self, damage, zombie):
        self.health -= damage
        self.hit_timer = self.current_time

    def getPosition(self):
        return self.rect.centerx, self.rect.bottom

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if self.max_health > 0:
            bar_width = self.rect.w
            bar_height = 4
            bar_x = self.rect.x
            bar_y = self.rect.y - bar_height - 2
            pg.draw.rect(surface, c.RED, (bar_x, bar_y, bar_width, bar_height))
            ratio = max(self.health, 0) / self.max_health
            pg.draw.rect(surface, c.GREEN, (bar_x, bar_y, int(bar_width * ratio), bar_height))

class Sun(Plant):
    def __init__(self, x, y, dest_x, dest_y):
        super().__init__(x, y, c.SUN, 0, None, 0.9)
        self.sun_value = c.SUN_VALUE
        self.move_speed = 1
        self.dest_x = dest_x
        self.dest_y = dest_y
        self.die_timer = 0

    def handleState(self):
        if self.rect.centerx != self.dest_x:
            self.rect.centerx += self.move_speed if self.rect.centerx < self.dest_x else -self.move_speed
        if self.rect.bottom != self.dest_y:
            self.rect.bottom += self.move_speed if self.rect.bottom < self.dest_y else -self.move_speed
        if self.rect.centerx == self.dest_x and self.rect.bottom == self.dest_y:
            if self.die_timer == 0:
                self.die_timer = self.current_time
            elif(self.current_time - self.die_timer) > c.SUN_LIVE_TIME:
                self.kill()

    def checkCollision(self, x, y):
        if(x >= self.rect.x and x <= self.rect.right and y >= self.rect.y and y <= self.rect.bottom):
            self.kill()
            return True
        return False

class EomukVendor(Plant):
    def __init__(self, x, y, sun_group):
        super().__init__(x, y, c.EOMUKVENDOR, c.PLANT_HEALTH, None)
        self.sun_timer = 0
        self.sun_group = sun_group
        self.sun_interval = c.FLOWER_SUN_INTERVAL
    def idling(self):
        interval = self.sun_interval / self.sun_multiplier
        if self.sun_timer == 0:
            self.sun_timer = self.current_time - (interval - 6000)
        elif (self.current_time - self.sun_timer) > interval:
            self.sun_group.add(Sun(self.rect.centerx, self.rect.bottom, self.rect.right, self.rect.bottom + self.rect.h // 2))
            self.play_sound()
            self.sun_timer = self.current_time


class SojuBottleSlingshot(Plant):
    def __init__(self, x, y, bullet_group):
        super().__init__(x, y, c.SOJUBOTTLESLINGSHOT, c.PLANT_HEALTH, bullet_group)
        self.shoot_timer = 0
        self.shoot_interval = 900

    def attacking(self):
        interval = self.shoot_interval / self.fire_rate_multiplier
        if (self.current_time - self.shoot_timer) > interval:
            self.bullet_group.add(Bullet(self.rect.right, self.rect.y, self.rect.y,
                                         c.BULLET_PEA, c.BULLET_DAMAGE_NORMAL, ice=True))
            self.play_sound()
            self.shoot_timer = self.current_time


class TaekwondoGuard(Plant):
    def __init__(self, x, y):
        super().__init__(x, y, c.TAEKWONDOGUARD, c.PLANT_HEALTH, None)
        self.attack_timer = 0
        self.attack_interval = 2000
        self.attack_zombie = None

    def canAttack(self, zombie):
        return self.rect.colliderect(zombie.rect)

    def setAttack(self, zombie):
        self.state = c.ATTACK
        self.attack_zombie = zombie
        self.attack_timer = self.current_time

    def attacking(self):
        if (self.attack_zombie is None or self.attack_zombie.state == c.DIE or not self.canAttack(self.attack_zombie)):
            self.setIdle()
            return
        interval = self.attack_interval / self.fire_rate_multiplier
        if (self.current_time - self.attack_timer) > interval:
            self.attack_zombie.setDamage(2)
            self.attack_zombie.rect.x += c.GRID_X_SIZE
            self.play_sound()
            self.attack_timer = self.current_time

    def setIdle(self):
        self.state = c.IDLE
        self.attack_zombie = None

class SuitcaseBarricade(Plant):
    def __init__(self, x, y):
        super().__init__(x, y, c.SUITCASEBARRICADE, c.SUITCASEBARRICADE_HEALTH, None)
        self.cracked1 = False
        self.cracked2 = False
        self.load_images()

    def load_images(self):
        self.cracked1_frames = []
        self.cracked2_frames = []
        cracked1_name = self.name + '_cracked1'
        cracked2_name = self.name + '_cracked2'
        self.loadFrames(self.cracked1_frames, cracked1_name, 1)
        self.loadFrames(self.cracked2_frames, cracked2_name, 1)

    def idling(self):
        if not self.cracked1 and self.health <= c.SUITCASEBARRICADE_CRACKED1_HEALTH:
            self.changeFrames(self.cracked1_frames)
            self.cracked1 = True
        elif not self.cracked2 and self.health <= c.SUITCASEBARRICADE_CRACKED2_HEALTH:
            self.changeFrames(self.cracked2_frames)
            self.cracked2 = True


class MolotovProjectile(pg.sprite.Sprite):
    def __init__(self, centerx, bottom, level):
        super().__init__()
        self.image = pg.Surface((20, 20), pg.SRCALPHA)
        pg.draw.circle(self.image, (255, 120, 0), (10, 10), 10)
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.bottom = bottom
        self.level = level
        self.x_vel = 4
        self.state = c.FLY
        self.current_time = 0
        self.radius = 10

    def update(self, game_info):
        self.current_time = game_info[c.CURRENT_TIME]
        if self.state == c.FLY:
            self.rect.x += self.x_vel
            if self.rect.x > c.SCREEN_WIDTH:
                self.kill()

    def on_hit(self):
        fire = MolotovFire(self.rect.centerx, self.rect.bottom, self.current_time)
        self.level.addBurnArea(fire)
        self.kill()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class MolotovStudent(Plant):
    def __init__(self, x, y, level):
        _, map_y = level.map.getMapIndex(x, y)
        super().__init__(x, y, c.MOLOTOVSTUDENT, c.PLANT_HEALTH, level.bullet_groups[map_y])
        self.state = c.ATTACK
        self.level = level
        self.throw_interval = 10000
        self.throw_timer = -self.throw_interval

    def attacking(self):
        interval = self.throw_interval / self.fire_rate_multiplier
        if (self.current_time - self.throw_timer) > interval:
            bottle = MolotovProjectile(self.rect.centerx, self.rect.bottom, self.level)
            self.bullet_group.add(bottle)
            self.play_sound()
            self.throw_timer = self.current_time

class MolotovFire(pg.sprite.Sprite):
    def __init__(self, centerx, bottom, start_time):
        super().__init__()
        width = c.GRID_X_SIZE * 3
        height = c.GRID_Y_SIZE * 3
        self.image = pg.Surface((width, height), pg.SRCALPHA)
        self.image.fill((255, 80, 0, 100))
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.bottom = bottom + c.GRID_Y_SIZE
        self.start_time = start_time
        self.damage_timer = start_time

    def update(self, game_info, zombie_groups):
        current_time = game_info[c.CURRENT_TIME]
        if current_time - self.start_time > 6000:
            self.kill()
            return
        if current_time - self.damage_timer >= 1000:
            for group in zombie_groups:
                for zombie in group:
                    if self.rect.colliderect(zombie.rect):
                        zombie.setDamage(1)
            self.damage_timer = current_time

class KPopIdol(Plant):
    def __init__(self, x, y):
        super().__init__(x, y, c.KPOPIDOL, c.PLANT_HEALTH, None)
        radius = c.GRID_X_SIZE * 2
        self.aura_image = pg.Surface((radius * 2, radius * 2), pg.SRCALPHA)
        pg.draw.circle(self.aura_image, (255, 192, 203, 80), (radius, radius), radius)

    def draw(self, surface):
        aura_rect = self.aura_image.get_rect()
        aura_rect.center = self.rect.center
        surface.blit(self.aura_image, aura_rect)
        super().draw(surface)

