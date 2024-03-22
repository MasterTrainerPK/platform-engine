import pygame
import level
import camera
import input_manager
import player

pygame.init()

# should get display height and width, to help make a reasonably sized window
screen = pygame.display.set_mode((640, 360), pygame.SCALED, pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True
level.platforms.append(pygame.Rect(0, 300, 50, 200))
level.platforms.append(pygame.Rect(100, 300, 100, 2))
level.platforms.append(pygame.Rect(0, 10000, 1000, 1))
main = camera.Camera(0, 0)
main.renderlist.append(level.render)
main.renderlist.append(player.render)
main.rect.center = player.rect.center
# platofrms should be in chuncks for more efficient loading
while running:
    # tick
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            # manage event
            input_manager.event(event)
    player.tick()
    main.rect.centerx = pygame.math.lerp(
        main.rect.centerx, player.rect.centerx, 0.2)
    main.rect.centery = pygame.math.lerp(
        main.rect.centery, player.rect.centery, 0.2)
    if player.rect.bottom + 100 > main.rect.bottom:
        main.rect.bottom = player.rect.bottom + 100
    # roll back one step
    # figure out exast collision point based on that
    screen.fill("black")
    # NOTE: y is inverted. positive is up
    for view in camera.registered:
        view.render()
#     for platform in level.platforms:
#         pygame.draw.rect(screen, "red", platform, width=2)
    # pygame.draw.rect(screen, "red", player.rect, width=1)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
