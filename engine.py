import pygame
import camera
import input_manager


class Engine:
    running = False
    screen = None
    clock = None

    def __init__(self, surface: pygame.Surface = None):
        if surface is None:
            surface = pygame.display.get_surface()

        self.screen = surface
        self.clock = pygame.time.Clock()
        self.running = True

    frameCounter = 0

    def loop(self, tick, prerender, postrender, framerate):
        while self.running:
            self.frameCounter += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    input_manager.event(event)
            tick()
            prerender()
            # you must register cameras yourself!
            self.screen.fill(pygame.Color(0, 0, 0, 255))
            for view in camera.registered:
                camera.registered[view].render()
            postrender()
            pygame.display.flip()
            self.clock.tick(framerate)

    def deinit(self):
        pass
