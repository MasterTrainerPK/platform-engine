import pygame
import camera
import level
import input_manager
import sys
import engine
import player
import main

startPos = None
dragging = False


def quit_game(my_engine: engine.Engine):
    def quit(event):
        my_engine.running = False
    return quit


def play_game(_):
    input_manager.input_handler_push()
    camera.registered['foreground'].renderlist.append(player.render)
    main.myLevel = myLevel
    player.regiser_event_handlers()
    gameEngine = engine.Engine()
    input_manager.on_key_down('p')(quit_game(gameEngine))
    gameEngine.loop(main.tick, main.render, (lambda: None), 60)
    gameEngine.deinit()
    input_manager.input_handler_pop()
    pass


def start_drag(e):
    global dragging
    global startPos
    startPos = camera.registered['foreground'].toWorldSpace(e.pos, True)
    dragging = True


def end_drag(e):
    global dragging
    dragging = False
    print(e.pos)
    endPos = camera.registered['foreground'].toWorldSpace(e.pos, True)
    print(endPos)
    width = endPos[0] - startPos[0]
    height = endPos[1] - startPos[1]
    print("platform width:", width, "platform height:", height)
    rect = pygame.Rect(startPos, (width, height))
    rect.normalize()
    myLevel.platforms.append(rect)
    myLevel.refresh()


def render_drag(rect):
    if dragging:
        endPos = camera.registered['foreground'].toWorldSpace(
            pygame.mouse.get_pos(), True)
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


def move_camera():
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
    camera.registered['foreground'].rect.move_ip((vx, vy))


def register_event_handlers():
    input_manager.on_key_down('p')(play_game)
    input_manager.on_m_button_down(1)(start_drag)
    input_manager.on_m_button_up(1)(end_drag)


scaleFactor = 1
myLevel = None


def run():
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    else:
        filename = input("Filename:")
    global myLevel
    myLevel = level.Level()
    myLevel.platforms.append(pygame.Rect(0, 0, 50, 50))
    main = camera.Camera((0, 0), (640, 360))
    ui = camera.Camera()
    main.renderlist.append(myLevel.render)
    main.renderlist.append(render_drag)
    text = pygame.font.Font('freesansbold.ttf', 32) \
        .render("File: " + filename, False, pygame.Color(255, 100, 100, 255))
    register_event_handlers()
    ui.renderlist.append(lambda _: (text.get_rect(), text))
    camera.register(main, 'foreground')
    camera.register(ui, 'ui')
    myEngine = engine.Engine()
    myEngine.loop(move_camera, (lambda: None), (lambda: None), 60)
    myEngine.deinit()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_mode(pygame.display.get_desktop_sizes()[
                            0], pygame.FULLSCREEN)
    run()
