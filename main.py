import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def calculate(u, gamma, max_iter_time, plate_length, delta_x):
    u = u.copy()
    for k in range(0, max_iter_time - 1, 1):
        for i in range(1, plate_length - 1, delta_x):
            for j in range(1, plate_length - 1, delta_x):
                u[k + 1, i, j] = gamma * (
                        u[k, i + 1, j] + u[k, i - 1, j] + u[k, i, j + 1] + u[k, i, j - 1] - 4 * u[k, i, j]) + u[
                                     k, i, j]
    return u


def plotheatmap(u_k, k, delta_t):
    # Clear the current plot figure
    plt.clf()

    plt.title(f"Temperature at t = {k * delta_t:.3f} unit time")
    plt.xlabel("x")
    plt.ylabel("y")

    # This is to plot u_k (u at time-step k)
    plt.pcolormesh(u_k, cmap=plt.cm.jet, vmin=0, vmax=100)
    plt.colorbar()

    return plt


if __name__ == '__main__':
    print("2D heat equation solver")
    plate_length = 100
    max_iter_time = 750

    alpha = 2
    delta_x = 1

    delta_t = (delta_x ** 2) / (4 * alpha)
    gamma = (alpha * delta_t) / (delta_x ** 2)

    # Initialize solution: the grid of u(k, i, j)
    u = np.empty((max_iter_time, plate_length, plate_length))

    # Initial condition everywhere inside the grid
    u_initial = 0

    # Boundary conditions
    u_top = 100.0
    u_left = 0.0
    u_bottom = 0.0
    u_right = 0.0

    # Set the initial condition
    u.fill(u_initial)

    # Set the boundary conditions
    u[:, (plate_length - 1):, :] = u_top
    u[:, :, :1] = u_left
    u[:, :1, 1:] = u_bottom
    u[:, :, (plate_length - 1):] = u_right

    # Do the calculation here
    u = calculate(u, gamma, max_iter_time, plate_length, delta_x)

    def animate(k):
        plotheatmap(u[k], k, delta_t)

    anim = animation.FuncAnimation(plt.figure(), animate, interval=1, frames=max_iter_time, repeat=False)
    anim.save("heat_equation_solution.gif")

    print("Done!")
