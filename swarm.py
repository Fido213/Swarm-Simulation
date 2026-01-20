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
        distance = (dx**2 + dy**2) ** 0.5
        k = 0.001  # acceleration constant
        if distance != 0:
            member["ax"] = k * dx
            member["ay"] = k * dy
        else:
            member["ax"] = 0
            member["ay"] = 0


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


# data analysis and visualisation


def history_tracking(swarm):
    if len(swarm) == 1:
        print("Swarm spawned with 1 member.")
        print("History tracking initiated.")
        cycle = 0
        history = {cycle: swarm[0]}
    else:
        print(f"Swarm spawned with {len(swarm)} members.")
        print("History tracking initiated for the first member only.")
        cycle = 0
        history = {cycle: swarm[0]}
    return history, cycle


def data_processing(history):
    x_axis_timeline = []
    x_timeline_y_axis = []
    y_timeline_y_axis = []
    vx_timeline_y_axis = []
    vy_timeline_y_axis = []
    ax_axis_timeline_y_axis = []
    ay_axis_timeline_y_axis = []
    for key in history:
        x_axis_timeline.append(key)
    for cycle in x_axis_timeline:
        x_timeline_y_axis.append(history[cycle]["x"])
        y_timeline_y_axis.append(history[cycle]["y"])
        vx_timeline_y_axis.append(history[cycle]["vx"])
        vy_timeline_y_axis.append(history[cycle]["vy"])
        ax_axis_timeline_y_axis.append(history[cycle]["ax"])
        ay_axis_timeline_y_axis.append(history[cycle]["ay"])
    all_data = {
        "x_axis": x_axis_timeline,
        "x_timeline": x_timeline_y_axis,
        "y_timeline": y_timeline_y_axis,
        "vx_timeline": vx_timeline_y_axis,
        "vy_timeline": vy_timeline_y_axis,
        "ax_timeline": ax_axis_timeline_y_axis,
        "ay_timeline": ay_axis_timeline_y_axis,
    }
    return all_data


# main loop
swarm = spawn_swarm(1)
history, cycle = history_tracking(swarm)

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

all_data = data_processing(history)
# print(f"\n {all_data}")


def plot_swarm_history(all_data):
    # Extract data for readability
    cycles = all_data["x_axis"]
    # Create a figure with 3 vertical subplots
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
    # 1. Plot Position (x, y)
    ax1.plot(cycles, all_data["x_timeline"], label=r"$x$ Position", color="blue")
    ax1.plot(cycles, all_data["y_timeline"], label=r"$y$ Position", color="cyan")
    ax1.set_ylabel(r"Position (pixels)")
    ax1.set_title(r"Swarm Member Kinematics Over Time")
    ax1.legend()
    ax1.grid(True, linestyle="--", alpha=0.7)

    # 2. Plot Velocity (vx, vy)
    ax2.plot(cycles, all_data["vx_timeline"], label=r"$v_x$", color="green")
    ax2.plot(cycles, all_data["vy_timeline"], label=r"$v_y$", color="lime")
    ax2.set_ylabel(r"Velocity (pixels/frame)")
    ax2.legend()
    ax2.grid(True, linestyle="--", alpha=0.7)

    # 3. Plot Acceleration (ax, ay)
    ax3.plot(cycles, all_data["ax_timeline"], label=r"$a_x$", color="red")
    ax3.plot(cycles, all_data["ay_timeline"], label=r"$a_y$", color="orange")
    ax3.set_ylabel(r"Acceleration (pixels/frame$^2$)")
    ax3.set_xlabel(r"Cycle (Time)")
    ax3.legend()
    ax3.grid(True, linestyle="--", alpha=0.7)

    # Adjust layout to prevent overlap
    plt.tight_layout()
    plt.show()


plot_swarm_history(all_data)
