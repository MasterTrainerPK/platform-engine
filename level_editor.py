import pygame
import camera
import level
import input_manager
import sys
import re

startPos = None
dragging = False


@input_manager.on_key_down('p')
def play_game(_):
    global running
    global main
    running = False
    main.renderlist.clear()
    pygame.quit()
    import main


@input_manager.on_m_button_down(1)
def startDrag(e):
    global dragging
    global startPos
    startPos = main.toWorldSpace(e.pos, True)
    dragging = True


@input_manager.on_m_button_up(1)
def endDrag(e):
    global dragging
    dragging = False
    print(e.pos)
    endPos = main.toWorldSpace(e.pos, True)
    print(endPos)
    width = endPos[0] - startPos[0]
    height = endPos[1] - startPos[1]
    print("platform width:", width, "platform height:", height)
    rect = pygame.Rect(startPos, (width, height))
    rect.normalize()
    level.platforms.append(rect)
    level.refresh()


def renderDrag(rect):
    if dragging:
        endPos = main.toWorldSpace(pygame.mouse.get_pos(), True)
        size = (endPos[0] - startPos[0], endPos[1] - startPos[1])
        rect = pygame.Rect(startPos, size)
        rect.normalize()
        size = rect.size
        if any(x == 0 for x in size):
            return (None, None)
        surface = pygame.Surface(size).convert_alpha()
        surface.fill(pygame.Color(0, 0, 0, 0))
        pygame.draw.rect(surface, pygame.Color(
            255, 0, 0, 255), pygame.Rect((0, 0), size), 1)
        return rect, surface

    return (None, None)


def moveCamera():
    vx = 0
    vy = 0
    if ord('a') in input_manager.keys:
        vx += -scaleFactor * 2
    if ord('d') in input_manager.keys:
        vx += scaleFactor * 2
    if ord('w') in input_manager.keys:
        vy += -scaleFactor * 2
    if ord('s') in input_manager.keys:
        vy += scaleFactor * 2
    main.rect.move_ip((vx, vy))


if len(sys.argv) == 2:
    filename = sys.argv[1]
else:
    filename = input("Filename:")

scaleFactor = 1
pygame.init()
pattern = re.compile(r'mono')
print([x for x in pygame.font.get_fonts() if pattern.match(x)])
# should get display height and width, to help make a reasonably sized window
screen = pygame.display.set_mode(pygame.display.get_desktop_sizes()[0],
                                 pygame.SCALED,
                                 pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True
level.platforms.append(pygame.Rect(0, 0, 50, 50))
main = camera.Camera(0, 0, (640, 360))
main.renderlist.append(level.render)
main.renderlist.append(renderDrag)
text = pygame.font.Font('freesansbold.ttf', 32) \
    .render("File: " + filename, False, pygame.Color(255, 100, 100, 255))
screen.blit(text, (0, 0))
while running:
    # tick
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            input_manager.event(event)
            # manage event
    moveCamera()
    screen.blit(text, (0, 0))
    main.render()
    pygame.display.flip()
    pygame.display.get_surface().fill((0, 0, 0))
    clock.tick(60)
