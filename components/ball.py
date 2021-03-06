from PPlay.sprite import Sprite
from PPlay.gameimage import load_image
import binary_break.globals as globals
import random

from binary_break.components.pad import Pad


class Ball(Sprite):
    def __init__(self):
        super().__init__("images/ball.png")
        self.old_x, self.old_y = self.x, self.y
        self.set_total_duration(1000)
        self.window = globals.window
        self.set_position(self.window.width / 2 - self.width / 2, self.window.height * 0.95)
        self.speed_x = 400 * globals.game_speed
        self.speed_y = -500 * globals.game_speed
        self.min_x = 0
        self.unstoppable = False

    def render(self):
        self.update_logic()
        self.draw()
        self.update()

    def update_logic(self):
        self.move()
        self.must_be_inside_window()
        if self.unstoppable:
            self.image, self.rect = load_image("images/ball2.png")
        else:
            self.image, self.rect = load_image("images/ball.png")

    def move(self):
        self.old_x, self.old_y = self.x, self.y
        self.move_x(self.speed_x * globals.delta_time)
        self.move_y(self.speed_y * globals.delta_time)

    def must_be_inside_window(self):
        if self.x < self.min_x:
            self.set_position(self.min_x, self.y)
            self.collision_change("LATERAL")
        elif self.x + self.width > self.window.width:
            self.set_position(self.window.width - self.width, self.y)
            self.collision_change("LATERAL")
        elif self.y < 0:
            self.set_position(self.x, 0)
            self.collision_change("VERTICAL")

    def collision_change(self, kind):
        r = random.uniform(-0.1, 0.1)
        if kind == "VERTICAL":
            self.speed_x *= 1 + r
            self.speed_y *= - 1 + r
        elif kind == "LATERAL":
            self.speed_x *= - 1 + r
            self.speed_y *= 1 + r

    def collided_with_bottom(self):
        return self.y + self.height > self.window.height

    def handle_collision(self, element: Sprite):
        if self.unstoppable and not (type(element) is Pad):
            return

        if self.speed_y > 0 and self.old_y + self.height < element.y:  # Verifica se a colisão foi de cima pra baixo
            self.collision_change("VERTICAL")
            self.y -= 10
        elif self.speed_y < 0 and self.old_y > element.y + element.height:  # Verifica se a colisão é de baixo para cima
            self.collision_change("VERTICAL")
            self.y += 10
        else:
            self.collision_change("LATERAL")

