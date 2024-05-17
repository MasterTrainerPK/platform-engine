import pygame
import level
import camera
import input_manager
import player
import engine

# TODO: architect the engine with less or no global
myLevel = None


def tick():
    player.tick(myLevel)


def render():
    main = camera.registered['foreground']
    camera.registered['foreground'].rect.centerx = pygame.math.lerp(
        main.rect.centerx, player.rect.centerx, 0.2)
    main.rect.centery = pygame.math.lerp(
        main.rect.centery, player.rect.centery, 0.2)
    if player.rect.bottom + 100 > main.rect.bottom:
        main.rect.bottom = player.rect.bottom + 100


def run():
    player.regiser_event_handlers()
    global myLevel
    myEngine = engine.Engine(pygame.display.get_surface())
    myLevel = level.Level()
    myLevel.platforms.append(pygame.Rect(0, 300, 50, 200))
    myLevel.platforms.append(pygame.Rect(100, 300, 100, 2))
    myLevel.platforms.append(pygame.Rect(0, 10000, 1000, 1))
    main = camera.Camera((0, 0), (640, 360))
    main.renderlist.append(myLevel.render)
    main.renderlist.append(player.render)
    main.rect.center = player.rect.center
    camera.register(main, 'foreground')

    myEngine.loop(tick, render, (lambda: None), 60)
    myEngine.deinit()
    # for platform in level.platforms:
    # pygame.draw.rect(screen, "red", platform, width=2)
    # pygame.draw.rect(screen, "red", player.rect, width=1)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_mode(pygame.display.get_desktop_sizes()[
                            0], pygame.FULLSCREEN)
    run()
