import axinite.tools as axtools
import axinite as ax
import matplotlib.pyplot as plt
import os, signal
from itertools import cycle

color_cycle = cycle(['r', 'b', 'g', 'orange', 'purple', 'yellow', 'gray', 'black'])

def mpl_frontend(args: axtools.AxiniteArgs, mode: str, type: str = "2D", **kwargs):
    if type == "2D" and mode == "show":
        return mpl_2d_static(args, **kwargs)
    elif type == "2D" and (mode == "live" or mode == "run"):
        return mpl_2d_live(args, **kwargs)
    elif type == "3D" and mode == "show":
        return mpl_3d_static(args, **kwargs)
    else:
        raise Exception("Unsupported mode or type for mpl_frontend")

def mpl_2d_static(args: axtools.AxiniteArgs, **kwargs):
    if args.rate is None:
        args.rate = 100
    if args.radius_multiplier is None:
        args.radius_multiplier = 1
    if args.retain is None:
       args.retain = 200

    fig, axs = plt.subplots(2, 2, figsize=(15, 15))
    plt.ion()
    fig.show()

    for _ax in axs.flat:
        _ax.set_aspect('equal', adjustable='datalim')

    def update_plot(body: axtools.Body):
        color = axtools.string_to_color(body.color, "mpl") if body.color != "" else next(color_cycle)
        trajectory_x, trajectory_y, trajectory_z = ([], [], [])
        for r in body._inner["r"]:
            trajectory_x.append(r[0])
            trajectory_y.append(r[1])
            trajectory_z.append(r[2])

        axs[0, 0].plot(trajectory_x, trajectory_y, label=body.name, color=color)
        axs[0, 1].plot(trajectory_x, trajectory_z, label=body.name, color=color)
        axs[1, 0].plot(trajectory_y, trajectory_z, label=body.name, color=color)

        if trajectory_x and trajectory_y and trajectory_z:
            radius = body.radius * body.radius_multiplier * args.radius_multiplier
            start_circle_xy = plt.Circle((trajectory_x[0], trajectory_y[0]), radius, color=color, fill=True, alpha=0.3)
            start_circle_xz = plt.Circle((trajectory_x[0], trajectory_z[0]), radius, color=color, fill=True, alpha=0.3)
            start_circle_yz = plt.Circle((trajectory_y[0], trajectory_z[0]), radius, color=color, fill=True, alpha=0.3)
            axs[0, 0].add_artist(start_circle_xy)
            axs[0, 1].add_artist(start_circle_xz)
            axs[1, 0].add_artist(start_circle_yz)

            axs[0, 0].plot(trajectory_x[-1], trajectory_y[-1], 'x', color=color)
            axs[0, 1].plot(trajectory_x[-1], trajectory_z[-1], 'x', color=color)
            axs[1, 0].plot(trajectory_y[-1], trajectory_z[-1], 'x', color=color)

        axs[0, 0].set_xlabel('X')
        axs[0, 0].set_ylabel('Y')
        axs[0, 1].set_xlabel('X')
        axs[0, 1].set_ylabel('Z')
        axs[1, 0].set_xlabel('Y')
        axs[1, 0].set_ylabel('Z')

        axs[0, 0].legend()
        axs[0, 1].legend()
        axs[1, 0].legend()
        plt.tight_layout()

        plt.draw()
        plt.pause(0.001)

    def show():
        axs[0, 0].set_title('XY Plane')
        axs[0, 1].set_title('XZ Plane')
        axs[1, 0].set_title('YZ Plane')

        plt.show(block=True)

    def stop():
        os.kill(os.getpid(), signal.SIGINT)

    return update_plot, show, stop

def mpl_2d_live(args: axtools.AxiniteArgs, **kwargs):
    if args.rate is None:
        args.rate = 100
    if args.radius_multiplier is None:
        args.radius_multiplier = 1
    if args.retain is None:
       args.retain = 200

    fig, axs = plt.subplots(2, 2, figsize=(15, 15))
    plt.ion()
    fig.show()

    for _ax in axs.flat:
        _ax.set_aspect('equal', adjustable='datalim')

    radii = {body.name: body.radius * body.radius_multiplier * args.radius_multiplier for body in args.bodies}
    colors = {body.name: axtools.string_to_color(body.color, "mpl") if body.color != "" else next(color_cycle) for body in args.bodies}

    def setup_plot():
        axs[0, 0].set_title('XY Plane')
        axs[0, 1].set_title('XZ Plane')
        axs[1, 0].set_title('YZ Plane')

        axs[0, 0].set_xlabel('X')
        axs[0, 0].set_ylabel('Y')
        axs[0, 1].set_xlabel('X')
        axs[0, 1].set_ylabel('Z')
        axs[1, 0].set_xlabel('Y')
        axs[1, 0].set_ylabel('Z')

        plt.tight_layout()

    def update_plot(bodies, t, **kwargs):
        try:
            axs[0, 0].clear()
            axs[0, 1].clear()
            axs[1, 0].clear()
            axs[1, 1].clear()

            bodies = ax.create_outer_bodies(bodies, kwargs["limit"], kwargs["delta"])
            n = kwargs["n"]

            for body in bodies:
                trajectory_x, trajectory_y, trajectory_z = ([], [], [])
                for r in body.rs[:kwargs["n"]]:
                    trajectory_x.append(r[0])
                    trajectory_y.append(r[1])
                    trajectory_z.append(r[2])

                axs[0, 0].plot(trajectory_x, trajectory_y, label=body.name, color=colors[body.name])
                axs[0, 1].plot(trajectory_x, trajectory_z, label=body.name, color=colors[body.name])
                axs[1, 0].plot(trajectory_y, trajectory_z, label=body.name, color=colors[body.name])

                if trajectory_x and trajectory_y and trajectory_z:
                    circle_xy = plt.Circle((trajectory_x[-1], trajectory_y[-1]), radii[body.name], color=colors[body.name], fill=True, alpha=0.5)
                    circle_xz = plt.Circle((trajectory_x[-1], trajectory_z[-1]), radii[body.name], color=colors[body.name], fill=True, alpha=0.5)
                    circle_yz = plt.Circle((trajectory_y[-1], trajectory_z[-1]), radii[body.name], color=colors[body.name], fill=True, alpha=0.5)
                    axs[0, 0].add_artist(circle_xy)
                    axs[0, 1].add_artist(circle_xz)
                    axs[1, 0].add_artist(circle_yz)
            axs[0, 0].legend()
            axs[0, 1].legend()
            axs[1, 0].legend()

            setup_plot()

            plt.draw()
            plt.pause(1 / args.rate)
        except KeyboardInterrupt:
            os.kill(os.getpid(), signal.SIGINT)

    def show():
        setup_plot()
        plt.show(block=True)

    def stop():
        os.kill(os.getpid(), signal.SIGINT)

    return update_plot, show, stop

def mpl_3d_static(args: axtools.AxiniteArgs, **kwargs):
    if args.rate is None:
        args.rate = 100
    if args.radius_multiplier is None:
        args.radius_multiplier = 1
    if args.retain is None:
       args.retain = 200

    fig = plt.figure(figsize=(15, 15))
    ax = fig.add_subplot(111, projection='3d')
    plt.ion()
    fig.show()

    def update_plot(body: axtools.Body):
        color = axtools.string_to_color(body.color, "mpl") if body.color != "" else next(color_cycle)
        trajectory_x, trajectory_y, trajectory_z = ([], [], [])
        for r in body._inner["r"]:
            trajectory_x.append(r[0])
            trajectory_y.append(r[1])
            trajectory_z.append(r[2])

        ax.plot(trajectory_x, trajectory_y, trajectory_z, label=body.name, color=color)

        if trajectory_x and trajectory_y and trajectory_z:
            ax.scatter(trajectory_x[0], trajectory_y[0], trajectory_z[0], color=color, alpha=0.6)
            ax.scatter(trajectory_x[-1], trajectory_y[-1], trajectory_z[-1], color=color, marker='x')

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        ax.legend()
        fig.tight_layout(rect=[0, 0, 1, 0.95])

        plt.draw()
        plt.pause(0.001)

    def show():
        ax.set_title('3D Trajectory')
        plt.show(block=True)

    def stop():
        os.kill(os.getpid(), signal.SIGINT)

    return update_plot, show, stop
