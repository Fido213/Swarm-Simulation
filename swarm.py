import pygame
import random
import matplotlib.pyplot as plt

# screen setup for visualising mouse position for now
pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Mouse Position Tracker")
clock = pygame.time.Clock()
running = True

# Mouse position functions


def get_mouse_position():
    mouse_position = pygame.mouse.get_pos()
    return mouse_position


def get_mouse_x(mouse_position):
    return mouse_position[0]
    # mouse position is a tuple (x, y)


def get_mouse_y(mouse_position):
    return mouse_position[1]


# Visualisation loop
def mouse_circle(mouseposition):
    mouse_circle_radius = 15
    RED = (255, 0, 0)
    return pygame.draw.circle(screen, RED, mouseposition, mouse_circle_radius)
    # returns a circle at the mouse position
    # screen, color, position, radius


def swarm_visualisation(swarms):
    BLUE = (0, 0, 255)
    for swarm in swarms:
        pygame.draw.circle(screen, BLUE, (swarm["x"], swarm["y"]), 5)
    # draws all swarm members on the screen


# swarm logic


def spawn_swarm(population_size):
    swarms = []
    for _ in range(population_size):
        x = random.randint(0, 600)
        y = random.randint(0, 600)
        vx = 5  # vx being horizontal velocity
        vy = 5  # vy being vertical velocity
        ax = 0  # ax being horizontal acceleration
        ay = 0  # ay being vertical acceleration
        swarm = {"x": x, "y": y, "vx": vx, "vy": vy, "ax": ax, "ay": ay}
        swarms.append(swarm)
    return swarms


def distance_based_acceleration(swarm, target_position):
    for member in swarm:
        dx = target_position[0] - member["x"]
        dy = target_position[1] - member["y"]
        if dx > 0:
            member["ax"] += 0.01
        else:
            member["ax"] -= 0.01
        if dy > 0:
            member["ay"] += 0.01
        else:
            member["ay"] -= 0.01


def swarm_logic(swarm, target_position):
    for member in swarm:
        if member["x"] < target_position[0]:
            member["vx"] += member["ax"]
            member["x"] += member["vx"]
        elif member["x"] > target_position[0]:
            member["vx"] -= member["ax"]
            member["x"] -= member["vx"]
        if member["y"] < target_position[1]:
            member["vy"] += member["ay"]
            member["y"] += member["vy"]
        elif member["y"] > target_position[1]:
            member["vy"] -= member["ay"]
            member["y"] -= member["vy"]


# main loop
swarm = spawn_swarm(1)
if len(swarm) == 1:
    print("Swarm spawned with 1 member.")
    print("History tracking initiated.")
    cycle = 0
    history = {cycle: swarm[0]}
while running:
    cycle += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    mouse_position = get_mouse_position()
    mouse_x = get_mouse_x(mouse_position)
    mouse_y = get_mouse_y(mouse_position)
    screen.fill((0, 0, 0))
    mouse_circle(mouse_position)
    distance_based_acceleration(swarm, mouse_position)
    swarm_logic(swarm, mouse_position)
    swarm_visualisation(swarm)
    # print(mouse_x, mouse_y)
    print(swarm[0])
    history[cycle] = swarm[0].copy()
    print()
    clock.tick(60)  # limit to 60 FPS
    pygame.display.flip()  # update the display


print(f"\n {history}")


# Extracting data from your history dictionary
cycles = list(history.keys())
x_coords = [data['x'] for data in history.values()]
y_coords = [data['y'] for data in history.values()]

plt.figure(figsize=(10, 6))
plt.plot(x_coords, y_coords, marker='o', markersize=2, linestyle='-', alpha=0.6)
plt.title("Swarm Member Trajectory")
plt.xlabel("X Position (Pixels)")
plt.ylabel("Y Position (Pixels)")
plt.gca().invert_yaxis()  # Pygame Y-axis is inverted (0 is top)
plt.grid(True)
plt.show()