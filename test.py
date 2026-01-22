import pygame


pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Mouse Position Tracker")
clock = pygame.time.Clock()
running = True


def generate_triangle_points(center, size):
    # here size is the distance from center to each vertex
    # the triangle will be pointing to the right
    # so the upper point would be the right most point
    upper_point = (center[0] + size, center[1])
    lower_base_point = (center[0] - size, center[1] + size)
    right_base_point = (center[0] - size, center[1] - size)
    list_coord = [upper_point, lower_base_point, right_base_point]
    return list_coord


def swarm_visualisation(list_coord):
    BLUE = (0, 0, 255)
    pygame.draw.polygon(screen, BLUE, list_coord)


list_coord = generate_triangle_points((300, 300), 20)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((255, 255, 255))  # Fill the screen with white
    swarm_visualisation(list_coord)
    clock.tick(60)
    pygame.display.flip()