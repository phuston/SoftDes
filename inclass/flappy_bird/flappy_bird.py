""" A Collaboratively-Coded Clone of Flappy Bird """

import pygame
import random
import time

class DrawableSurface():
    """ A class that wraps a pygame.Surface and a pygame.Rect """
    def __init__(self, surface, rect):
        """ Initialize the drawable surface """
        self.surface = surface
        self.rect = rect

    def get_surface(self):
        """ Get the surface """
        return self.surface

    def get_rect(self):
        """ Get the rect """
        return self.rect

class Player():
    """ A class that represents the player """
    def __init__(self):
        self.image = pyagme.image.load('images/olin_o.png')

    def get_drawables(self):
        return DrawableSurface(self.image, pygame.Rect(image.get_rect.size()))


class Background():
    """ Represents the background (at first just the ground) """
    def __init__(self,width,height):
        self.image = pygame.image.load('images/plant_tile.png')
        self.height = height

    def get_drawables(self):
        """ Gets the drawables for the background """
        drawables = []
        for i in range(100):
            drawables.append(DrawableSurface(self.image,
                                             pygame.Rect(i*32,self.height - 32,32,32)))
        return drawables

class FlappyModel():
    """ Represents the game state of our Flappy bird clone """
    def __init__(self, width, height):
        """ Initialize the flappy model """
        self.width = width
        self.height = height
        self.background = Background(width, height)
        self.player = player()

    def get_drawables(self):
        """ Return a list of DrawableSurfaces for the model """
        return self.background.get_drawables()
        return self.player.get_drawables()

    def update(self):
        """ Updates the model and its constituent parts """
        pass

class FlappyView():
    def __init__(self, model, width, height):
        """ Initialize the view for Flappy Bird.  The input model
            is necessary to find the position of relevant objects
            to draw. """
        pygame.init()
        # to retrieve width and height use screen.get_size()
        self.screen = pygame.display.set_mode((width, height))
        # this is used for figuring out where to draw stuff
        self.model = model

    def draw(self):
        """ Redraw the full game window """
        self.screen.fill((0,51,102))
        # get the new drawables
        self.drawables = self.model.get_drawables()
        for d in self.drawables:
            rect = d.get_rect()
            surf = d.get_surface()
            self.screen.blit(surf, rect)
        pygame.display.update()

class FlappyBird():
    """ The main Flappy Bird class """

    def __init__(self):
        """ Initialize the flappy bird game.  Use FlappyBird.run to
            start the game """
        self.model = FlappyModel(640, 480)
        self.view = FlappyView(self.model, 640, 480)
        # we will code the controller later

    def run(self):
        """ the main runloop... loop until death """
        last_update_time = time.time()
        while True:
            self.view.draw()
            self.model.update()
            last_update_time = time.time()

if __name__ == '__main__':
    flappy = FlappyBird()
    flappy.run()