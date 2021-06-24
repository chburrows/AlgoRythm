import pygame

def draw(screen, clock):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                return False, True

    screen.fill( (50, 50, 50))

    pygame.display.flip()
    clock.tick(20)

    return True, True

