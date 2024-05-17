import pygame
# TODO: make this an object maybe


class Level:
    platforms = []
    surface = None
    bounding_box = None

    def get_bounding_box(self):
        if not self.platforms:
            return None
        self.bounding_box = pygame.rect.Rect((0, 0), (1, 1))
        for platform in self.platforms:
            self.bounding_box = pygame.rect.Rect.union(
                self.bounding_box, platform)

    def create_surface(self):
        self.get_bounding_box()
        self.surface = pygame.Surface(
            (self.bounding_box.size)).convert_alpha()
        self.surface.fill(pygame.Color(0, 0, 0, 0))

    def refresh(self):
        self.surface = None

    # this will render assuming that the scene is static.
    # it also doesn't do cunked loading/ unloading
    def render(self, rect):
        if not self.surface:
            self.create_surface()
            for platform in self.platforms:
                translatedPlatform = platform.move(
                    -self.bounding_box.left, -self.bounding_box.top)
                pygame.draw.rect(self.surface, "red",
                                 translatedPlatform, width=2)
        return self.bounding_box, self.surface
