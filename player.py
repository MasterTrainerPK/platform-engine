import input_manager
import level
import pygame
rect = pygame.Rect((0, 0), (10, 10))
grounded = None
sliding = None
on_right = True
vx = 0
vy = 0
sprite = pygame.Surface((rect.width, rect.height))
sprite.fill("black")
pygame.draw.rect(sprite, "red", rect, width=2)


def init():
    global rect
    rect.bottom = pygame.display.get_surface().get_height()


def jump(_):
    global grounded
    global vy
    global vx
    # breakpoint()
    if grounded:
        print("Jump!!!")
        vy = -10
    if sliding:
        print("jump!!")
        vy -= 5
        if on_right:
            vx += 5
        else:
            vx -= 5


def tick(level):
    global rect
    global vy
    global grounded
    rect.move_ip(vx, vy)
    if grounded:
        check_grounded(level)
        check_walls(level)
    elif sliding:
        check_sliding(level)
    else:
        check_new_collisions(level)

    if not grounded:
        vy += 0.5
    if sliding:
        vy += -0.5 - vy / 5
    process_inputs()

# this should go in iehter a entity util or collider file or something of the lsort


def check_grounded(level):
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
        check_new_collisions(level)


# TODO: impliment.
def check_walls(level):
    pass


def check_sliding(level):
    global vx
    global rect
    if pygame.Rect.colliderect(rect, sliding):
        vx = 0
        if on_right:
            rect.left = sliding.right
        else:
            rect.right = sliding.left
    # hmm... this is starting to look funny...
    elif ((on_right and rect.left == sliding.right
            or not on_right and rect.right == sliding.left)
          and rect.bottom > sliding.top
          and rect.top < sliding.bottom):
        pass
    else:
        check_new_collisions(level)

# TODO: force some of the funcionality of this into multiple utilities


def check_new_collisions(level):
    # this is not looking too good, maybe shouldn't have 6 globals...
    global grounded
    global sliding
    global rect
    global vy
    global vx
    global on_right
    grounded = None
    sliding = None
    prev_hbox = rect.move(-vx, -vy)
    collider = pygame.Rect.union(rect, prev_hbox)
    for platform in level.platforms:
        if pygame.Rect.colliderect(collider, platform):
            # remember, up is smaller
            # roll back one step
            # figure out exast collision point based on that
            if prev_hbox.top < platform.bottom and prev_hbox.bottom > platform.top:
                sliding = platform
                print("Side collision")
                vx = 0
                vy -= 1
                vy = max(vy, 0)
                if prev_hbox.left >= platform.right:
                    rect.left = platform.right
                    on_right = True
                else:
                    rect.right = platform.left
                    on_right = False
            else:
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
    if grounded:
        if ord('a') in input_manager.keys:
            vx = -2
        elif ord('d') in input_manager.keys:
            vx = 2
        else:
            vx = 0
    else:
        if ord('a') in input_manager.keys and vx > -2:
            vx -= 0.5
        elif ord('d') in input_manager.keys and vx < 2:
            vx += 0.5


def render(_):
    sprite.fill("black")
    if grounded:
        color = "green"
    else:
        color = "red"
    pygame.draw.rect(sprite, color, sprite.get_rect(), width=3)
    return ((rect), sprite)


def regiser_event_handlers():
    input_manager.on_key_down('w')(jump)
