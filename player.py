import input_manager
import level
import pygame
rect = pygame.Rect((0, 0), (10, 10))
grounded = None
sliding = None
vx = 0
vy = 0
sprite = pygame.Surface((rect.width, rect.height))
sprite.fill("black")
pygame.draw.rect(sprite, "red", rect, width=2)


def init():
    global rect
    rect.bottom = pygame.display.get_surface().get_height()


@input_manager.on_key_down("w")
def jump():
    global grounded
    global vy
    # breakpoint()
    if grounded:
        print("Jump!!!")
        vy = -10


def tick():
    global rect
    global vy
    global grounded
    rect.move_ip(vx, vy)
    if grounded:
        check_grounded()
        check_walls()
    else:
        check_new_collisions()

    if not grounded:
        vy += 0.5

    process_inputs()

# this should go in iehter a entity util or collider file or something of the lsort


def check_grounded():
    global vy
    global rect
    if pygame.Rect.colliderect(rect, grounded):
        vy = 0
        rect.bottom = grounded.top
        print("aww...")
    elif (rect.bottom == grounded.top
            and rect.left < grounded.right
            and rect.right > grounded.left):
        pass
    else:
        check_new_collisions()


# FIXME: impliment.
def check_walls():
    pass


# TODO: force some of the funcionality of this into multiple utilities
def check_new_collisions():
    global grounded
    global rect
    global vy
    global vx
    grounded = None
    prev_hbox = rect.move(-vx, -vy)
    collider = pygame.Rect.union(rect, prev_hbox)
    for platform in level.platforms:
        if pygame.Rect.colliderect(collider, platform):
            # remember, up is smaller
            # roll back one step
            # figure out exast collision point based on that
            if prev_hbox.top < platform.bottom and prev_hbox.bottom > platform.top:
                sliding = True
                print("Side collision")
                # TODO: impliment something like grounding for sliding
                vx = 0
                if prev_hbox.left >= platform.right:
                    rect.left = platform.right
                else:
                    rect.right = platform.left
            else:
                sliding = False
                # if prev_hbox.left < platform.right and prev_hbox.right > platform.left:
                if prev_hbox.bottom <= platform.top:
                    if vy > 0:
                        vy = 0
                    # breakpoint()
                    rect.bottom = platform.top
                    grounded = platform
                else:
                    if vy < 0:
                        vy = 0
                    rect.top = platform.bottom


def process_inputs():
    global vx
    if ord('a') in input_manager.keys:
        vx = -2
    elif ord('d') in input_manager.keys:
        vx = 2
    else:
        vx = 0


def render(_):
    sprite.fill("black")
    if grounded:
        color = "green"
    else:
        color = "red"
    pygame.draw.rect(sprite, color, sprite.get_rect(), width=3)
    return ((rect), sprite)
