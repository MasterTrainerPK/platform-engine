import pygame
registered = []


class Camera:
    def __init__(self, world_x, world_y, width=0, height=0):
        if width == 0 or height == 0:
            self.surface = pygame.surface.Surface(
                pygame.display.get_surface().get_size(), 0, pygame.display.get_surface())
            width, height = pygame.display.get_surface().get_size()
            self.scaled = False
        else:
            self.surface = pygame.surface.Surface(
                (width, height), surface=pygame.display.get_surface())
            self.scaled_surface = pygame.surface.Surface(
                pygame.display.get_window_size(), 0, pygame.display.get_surface())
            self.scaled = True
        print("width: ", width, "height: ", height)
        self.rect = pygame.Rect(
            (world_x, world_y), (width, height))
        registered.append(self)
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
                              special_flags=pygame.BLEND_ALPHA_SDL2)

        pygame.display.get_surface().blit(self.surface, (0, 0))
