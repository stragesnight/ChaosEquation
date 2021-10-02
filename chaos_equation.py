import numpy as np
from numpy.random import default_rng
import pygame

class vec2d:
    def __init__(self, x = 0, y = 0, color = (255, 255, 255)):
        self.x = x
        self.y = y
        self.color = color

N_POINTS = 10000
POINT_SIZE = 5

TIME_DELTA = 0.00001
MOVEMENT_DELTA = 1.8
MOVEMENT_SHIFT_MODIFIER = 3.5
ZOOM_DELTA = 0.5

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

camera_pos_x = SCREEN_WIDTH / 2
camera_pos_y = SCREEN_HEIGHT / 2
camera_zoom = 500
t = 0

rng = default_rng()


def randomize(vec:vec2d):
    vec.x = rng.random() * 10 - 5
    vec.y = rng.random() * 10 - 5
    vec.color = (rng.random() * 256, rng.random() * 256, rng.random() * 256)

def update_position(vec:vec2d):
    x = vec.x
    y = vec.y
    vec.x = -(t * t) - (x * y) + t
    vec.y = -(x * y) + (x * t) + y + t

def handle_input():
    global camera_pos_x, camera_pos_y, camera_zoom
    keys = pygame.key.get_pressed()
    delta = MOVEMENT_DELTA

    if keys[pygame.KMOD_SHIFT]:
        delta *= MOVEMENT_SHIFT_MODIFIER

    # update camera position
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        camera_pos_y += delta
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        camera_pos_y -= delta
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        camera_pos_x -= delta
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        camera_pos_x += delta

    # update camera zoom
    if keys[pygame.K_q]:
        camera_zoom -= ZOOM_DELTA
    if keys[pygame.K_e]:
        camera_zoom += ZOOM_DELTA


if __name__ == "__main__":
    # create an array of vec2d objects
    vVec2d = np.vectorize(vec2d)
    points = np.empty((N_POINTS), dtype=object)
    points[:] = vVec2d(np.zeros((N_POINTS)), np.zeros((N_POINTS)))

    # randomize points
    randomize_vectorized = np.vectorize(randomize)
    randomize_vectorized(points)

    # initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    pygame.display.set_caption("Chaos Equation")

    # initialize font
    font = pygame.font.SysFont(None, 24)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        # clear screen
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        s.set_alpha(50)
        s.fill((0, 0, 0))
        screen.blit(s, (0, 0))

        # update point positions
        update_vectorized = np.vectorize(update_position)
        update_vectorized(points)

        # handle user input
        handle_input()

        # update time variable
        t += TIME_DELTA

        # draw points
        for p in points:
            pos_x = p.x * camera_zoom + camera_pos_x
            pos_y = p.y * camera_zoom + camera_pos_y
            pygame.draw.rect(screen, p.color, (pos_x, pos_y, POINT_SIZE, POINT_SIZE), 0)

        # draw debug text
        text_img = font.render("t: {}".format(t), True, (255, 255, 255))
        screen.blit(text_img, (0, 0))

        text_img = font.render("zoom: {}".format(camera_zoom), True, (255, 255, 255))
        screen.blit(text_img, (0, 24))

        pygame.display.update()
        #flip screen buffer
        pygame.display.flip()

    pygame.quit()

