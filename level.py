import pygame

platforms = []
surface = None
bounding_box = None


def get_bounding_box():
    global bounding_box
    if not platforms:
        return None
    bounding_box = pygame.rect.Rect((0, 0), (1, 1))
    for platform in platforms:
        bounding_box = pygame.rect.Rect.union(bounding_box, platform)


def create_surface():
    global surface
    global bounding_box
    get_bounding_box()
    surface = pygame.Surface((bounding_box.width, bounding_box.height))
    surface.fill(pygame.Color(0, 0, 0, 0))


# this will render assuming that the scene is static.
# it also doesn't do cunked loading/ unloading
def render(rect):
    global surface
    if not surface:
        create_surface()
        for platform in platforms:
            pygame.draw.rect(surface, "red", platform, width=2)
    return bounding_box, surface
