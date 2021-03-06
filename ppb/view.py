from ppb.event import Tick
from ppb.vmath import Vector2 as Vector


class View(object):

    def __init__(self, scene, display, fps, hardware):
        self.render_wait = 1 / fps
        self.countdown = self.render_wait
        scene.subscribe(Tick, self.tick)
        self.display = display
        self.layers = [set()]
        self.hw = hardware

    def render(self):
        for layer in self.layers:
            for sprite in layer:
                sprite.update()
            self.hw.render(layer)
        self.hw.draw_screen()

    def tick(self, event):
        self.countdown += -1 * event.sec
        if self.countdown <= 0:
            self.render()
            self.countdown = self.render_wait

    def add(self, sprite, layer=0):
        """
        Add a sprite to the view.

        :param sprite: Sprite
        :param layer: Layer to render the sprite at.
        :return: None
        """
        while len(self.layers) < layer + 1:
            self.layers.append(set())
        self.layers[layer].add(sprite)

    def remove(self, sprite):
        """
        Remove a sprite from the view.

        :param sprite: Sprite
        :return: none
        """

        for layer in self.layers:
            try:
                layer.remove(sprite)
            except ValueError:
                pass

    def change_layer(self, sprite, layer):
        self.remove(sprite)
        self.add(sprite, layer)


class Sprite(object):

    def __init__(self, image, model):
        self.image = image
        self.size = image.size
        self.pos = Vector(0, 0)
        self.model = model

    def update(self):
        self.pos = Vector(self.model.pos.x - self.size, self.model.pos.y - self.size)
