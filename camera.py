import pygame
registered = dict()


class Camera:
    def __init__(self, worldpos=(0, 0), size=(0, 0), surface=None):
        if surface is None:
            surface = pygame.display.get_surface()
        self.dest = surface
        if size[0] == 0 or size[1] == 0:
            print("assuming screen size")
            size = surface.get_size()
            self.surface = pygame.surface.Surface(
                size
            ).convert_alpha()
            self.scaled_surface = self.surface
            self.scaled = False
        else:
            self.surface = pygame.surface.Surface(size).convert_alpha()
            self.scaled_surface = pygame.surface.Surface(
                surface.get_size()
            ).convert_alpha()
            self.scaled = True
        print("width: ", size[0], "height: ", size[1])
        self.rect: pygame.Rect = pygame.Rect(
            worldpos, size)
        self.renderlist = []

    def render(self):
        self.surface.fill(pygame.Color(0, 0, 0, 0))
        for render in self.renderlist:
            bounding_box, surface = render(self.rect)
            if surface is None:
                continue
            if not self.rect.colliderect(bounding_box):
                pass
            self.surface.blit(surface,
                              (bounding_box.x - self.rect.x,
                               bounding_box.y - self.rect.y),
                              special_flags=pygame.BLEND_ALPHA_SDL2
                              )
        if self.scaled:
            pygame.transform.scale(
                self.surface, self.scaled_surface.get_size(), self.scaled_surface)
            self.dest.blit(self.scaled_surface, (0, 0))
        else:
            self.dest.blit(
                self.surface, (0, 0), special_flags=pygame.BLEND_ALPHA_SDL2)

    def changeScale(self, newScale):
        self.surface = pygame.surface.Surface(newScale)

    def toScreenScale(self, point, round=False):
        if round:
            return (int(point[0] / self.rect.width * self.scaled_surface.get_width()),
                    int(point[1] / self.rect.height * self.scaled_surface.get_height()))
        else:
            return (point[0] / self.rect.width * self.scaled_surface.get_width(),
                    point[1] / self.rect.height * self.scaled_surface.get_height())

    def toWorldScale(self, point, round=False):
        if round:
            return (int(point[0] / self.scaled_surface.get_width() * self.rect.width),
                    int(point[1] / self.scaled_surface.get_height() * self.rect.height))
        else:
            return (point[0] / self.scaled_surface.get_width() * self.rect.width,
                    point[1] / self.scaled_surface.get_height() * self.rect.height)

    def toWorldSpace(self, screenPos, round=False):
        if self.scaled:
            screenPos = self.toWorldScale(screenPos, round)

        return (screenPos[0] + self.rect.left,
                screenPos[1] + self.rect.top)

    def toScreenSpace(self, worldPos, round=False):
        worldPos = (worldPos[0] - self.rect.left,
                    worldPos[1] - self.rect.top)
        if self.scaled:
            worldPos = self.toScreenScale(worldPos, round)
        return worldPos


def register(camera: Camera, name: str):
    if camera:
        registered[name] = camera
