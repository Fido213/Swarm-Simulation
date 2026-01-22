import pygame
import random
import matplotlib.pyplot as plt
import math

# screen setup for visualising mouse position for now
pygame.init()
screen = pygame.display.set_mode((1000, 700))
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


def swarm_visualisation(swarms_triangle_coord):
    BLUE = (0, 0, 255)
    # print(swarms_triangle_coord)
    for triangle_coord in swarms_triangle_coord:
        pygame.draw.polygon(screen, BLUE, triangle_coord)
    # draws all swarm members on the screen


def swarm_member_visualisation(swarms, size):
    swarms_triangle_coord = []
    for swarm in swarms:
        x = swarm["x"]
        y = swarm["y"]
        angle = swarm["angle"]
        # now we will use the unit circle
        # my thought process is:
        # so basically we take take the angle from the swarm dict
        # this angle is already turning to face the mouse
        # we then use the cosine and sin of that angle to get x and y
        # components, since this is a local world, we multiply by size directly
        # then we add the oringinal x and y to get the new point (since
        # cos and sin give us offsets from origin)
        # then after calculating it we can draw our vertices based on that
        local_x = math.cos(angle) * size
        local_y = math.sin(angle) * size
        upper_point_x = x + local_x
        upper_point_y = y + local_y
        right_base_point_x = x + math.cos(angle + 2.4) * (size * 0.7)
        right_base_point_y = y + math.sin(angle + 2.4) * (size * 0.7)
        left_base_point_x = x + math.cos(angle - 2.4) * (size * 0.7)
        left_base_point_y = y + math.sin(angle - 2.4) * (size * 0.7)
        list_coord = [
            (upper_point_x, upper_point_y),
            (left_base_point_x, left_base_point_y),
            (right_base_point_x, right_base_point_y),
        ]
        swarms_triangle_coord.append(list_coord)
    return swarms_triangle_coord


def hitbox_visualisation(swarm):
    for member in swarm:
        hitbox = member["hitbox"]
        hitbox_rect = pygame.Rect(
            hitbox[0][0],
            hitbox[2][0],
            hitbox[1][0] - hitbox[0][0],
            hitbox[3][0] - hitbox[2][0],
        )
        RED = (255, 0, 0)
        pygame.draw.rect(screen, RED, hitbox_rect, 1)


# swarm logic


def spawn_swarm(population_size):
    swarms = []
    for _ in range(population_size):
        x = random.randint(0, 600)
        y = random.randint(0, 600)
        vx = 0  # vx being horizontal velocity
        vy = 0  # vy being vertical velocity
        ax = 0  # ax being horizontal acceleration
        ay = 0  # ay being vertical acceleration
        angle = 0  # facing right
        hitbox_coord = ()
        swarm = {
            "x": x,
            "y": y,
            "vx": vx,
            "vy": vy,
            "ax": ax,
            "ay": ay,
            "angle": angle,
            "hitbox": hitbox_coord,
        }
        swarms.append(swarm)
    return swarms


def distance_based_acceleration(swarm, target_position):
    stop_threshold = 50  # pixels
    damping_factor = 0.95
    max_velocity = 12.25
    for member in swarm:
        if member["vx"] ** 2 + member["vy"] ** 2 > max_velocity:
            member["vx"] *= damping_factor
            member["vy"] *= damping_factor
        dx = target_position[0] - member["x"]
        dy = target_position[1] - member["y"]
        distance = (dx**2 + dy**2) ** 0.5
        k = 0.001  # acceleration constant
        if distance > stop_threshold:
            member["ax"] = k * dx
            member["ay"] = k * dy
        else:
            member["ax"] = 0
            member["ay"] = 0
            member["vx"] *= damping_factor
            member["vy"] *= damping_factor


def smooth_turning(swarm, target_position):
    turn_rate = 0.2  # so 10% of the angle difference per update
    for member in swarm:
        dx = target_position[0] - member["x"]
        dy = target_position[1] - member["y"]
        target_angle = math.atan2(dy, dx)
        diff = target_angle - member["angle"]
        if diff > math.pi:
            diff -= 2 * math.pi
        if diff < -math.pi:
            diff += 2 * math.pi
        member["angle"] += diff * turn_rate


def seperation(swarm):
    push_strength = 0.05  # Adjust this to make the 'bounce' harder or softer
    for member in range(len(swarm)):
        # 00 = left edge
        # 10 = right edge
        # 20 = top edge
        # 30 = bottom edge
        for member_check in range(member + 1, len(swarm)):
            if member + 1 >= len(swarm):
                break
            dx = swarm[member]["x"] - swarm[member_check]["x"]
            dy = swarm[member]["y"] - swarm[member_check]["y"]
            current_hitbox_left = swarm[member]["hitbox"][0][0]
            current_hitbox_right = swarm[member]["hitbox"][1][0]
            current_hitbox_top = swarm[member]["hitbox"][2][0]
            current_hitbox_bottom = swarm[member]["hitbox"][3][0]
            overlap_x = (
                current_hitbox_left < swarm[member_check]["hitbox"][1][0]
                and current_hitbox_right > swarm[member_check]["hitbox"][0][0]
            )
            overlap_y = (
                current_hitbox_top < swarm[member_check]["hitbox"][3][0]
                and current_hitbox_bottom > swarm[member_check]["hitbox"][2][0]
            )
            if overlap_x and overlap_y:
                # collision on x axis
                swarm[member]["vx"] += dx * push_strength
                swarm[member_check]["vx"] += -dx * push_strength
                # collision on y axis
                swarm[member]["vy"] += dy * push_strength
                swarm[member_check]["vy"] += -dy * push_strength


def hitbox(swarm, hitbox_size):
    for member in swarm:
        hitbox_rect_left_edge = (member["x"] - hitbox_size,)
        hitbox_rect_right_edge = (member["x"] + hitbox_size,)
        hitbox_rect_top_edge = (member["y"] - hitbox_size,)
        hitbox_rect_bottom_edge = (member["y"] + hitbox_size,)
        member["hitbox"] = (
            hitbox_rect_left_edge,
            hitbox_rect_right_edge,
            hitbox_rect_top_edge,
            hitbox_rect_bottom_edge,
        )


def swarm_logic(swarm):
    for member in swarm:
        # update velocity
        member["vx"] += member["ax"]
        member["vy"] += member["ay"]
        # update position
        member["x"] += member["vx"]
        member["y"] += member["vy"]


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
    angle_timeline_y_axis = []
    for key in history:
        x_axis_timeline.append(key)
    for cycle in x_axis_timeline:
        x_timeline_y_axis.append(history[cycle]["x"])
        y_timeline_y_axis.append(history[cycle]["y"])
        vx_timeline_y_axis.append(history[cycle]["vx"])
        vy_timeline_y_axis.append(history[cycle]["vy"])
        ax_axis_timeline_y_axis.append(history[cycle]["ax"])
        ay_axis_timeline_y_axis.append(history[cycle]["ay"])
        angle_timeline_y_axis.append(history[cycle]["angle"])
    all_data = {
        "x_axis": x_axis_timeline,
        "x_timeline": x_timeline_y_axis,
        "y_timeline": y_timeline_y_axis,
        "vx_timeline": vx_timeline_y_axis,
        "vy_timeline": vy_timeline_y_axis,
        "ax_timeline": ax_axis_timeline_y_axis,
        "ay_timeline": ay_axis_timeline_y_axis,
        "angle_timeline": angle_timeline_y_axis,
    }
    return all_data


# main loop
size = 10
swarm = spawn_swarm(100)
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
    smooth_turning(swarm, mouse_position)
    swarm_logic(swarm)
    swarms_triangle_coord = swarm_member_visualisation(swarm, size)
    hitbox(swarm, size)
    seperation(swarm)
    # hitbox_visualisation(swarm)
    swarm_member_visualisation(swarm, size)
    swarm_visualisation(swarms_triangle_coord)
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
    # Create a figure with 4 vertical subplots
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(10, 12), sharex=True)
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

    # 4. Plot Angle
    ax4.plot(cycles, all_data["angle_timeline"], label=r"$\theta$", color="purple")
    ax4.set_ylabel(r"Angle (radians)")
    ax4.set_xlabel(r"Cycle (Time)")
    ax4.legend()
    ax4.grid(True, linestyle="--", alpha=0.7)
    # Adjust layout to prevent overlap
    plt.tight_layout()
    plt.show()


plot_swarm_history(all_data)
