import pygame
import level
import camera
import input_manager
import player

pygame.init()

# should get display height and width, to help make a reasonably sized window
screen = pygame.display.set_mode((500, 500), pygame.SCALED)
clock = pygame.time.Clock()
running = True
level.platforms.append(pygame.Rect(0, 300, 50, 200))
level.platforms.append(pygame.Rect(100, 300, 100, 2))
main = camera.Camera(0, 0)
main.renderlist.append(level.render)
main.renderlist.append(player.render)
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
