import pygame

def draw(screen, clock, size):
    
    WHITE = (255, 255, 255)

    # Titles
    font = pygame.font.SysFont(None, 32)
    titleImg = font.render('Settings', True, (200, 200, 200))
    vpropImg = font.render('Visualizer Properties', True, WHITE)

    # Options
    fontO = pygame.font.SysFont(None, 28)

    optImgs = [fontO.render('Sensitivity:', True, WHITE),
        fontO.render('Smoothing Level:', True, WHITE),
        fontO.render('Multiplier:', True, WHITE),
        fontO.render('Bar Width:', True, WHITE),
        fontO.render('Bar Height:', True, WHITE),
        fontO.render('Bar Gap:', True, WHITE),
        fontO.render('Bar Count:', True, WHITE)]
    

    xPos = size[0] // 3 + 20
        
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    return False, True

        screen.fill( (30, 30, 30))

        # Display title text
        screen.blit(titleImg, (20, 20))
        screen.blit(vpropImg, (xPos, 20))

        # Display option text images
        yPos = 50
        for index, img in enumerate(optImgs):
            yPos += 30 + (30 if index == 3 else 0)
            screen.blit(img, (xPos, yPos))

        pygame.display.flip()
        clock.tick(30)

