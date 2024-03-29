import math
import pathlib
from typing import List, Tuple

import plotly.graph_objects as go
import utils
from manager import init_position, move_to_alpha, move_to_beta
from matplotlib import pyplot as plt
from schemas import Coordinate, Hand, MotorX, MotorY
from tqdm import tqdm

import configuration


def plotly_go_visulize(
    hand: Hand, motor_y: MotorY, motor_x: MotorX
) -> List[go.Scatter3d]:
    """
    Visualize the hand, motors, and frame using Plotly 3D scatter plots.

    This function takes a Hand, MotorY, and MotorX object as input and generates a list of
    Plotly Scatter3d traces to visualize the hand, motors, and frame in 3D space.

    Parameters:
        hand (Hand): The Hand object representing the hand's coordinates.
        motor_y (MotorY): The Flexion/Extension (Motor Y) object.
        motor_x (MotorX): The Radial/Ulnar (Motor X) object.

    Returns:
        List[go.Scatter3d]: A list of Plotly Scatter3d traces representing the visualization.
    """
    frame = (
        motor_x.get_frame()
    )  # gets the for coordinates describing a sqaure arch like frame

    return [
        # Marker for the Hand-Base-Coordinate [HCS] system (red diamond)
        go.Scatter3d(
            x=[hand.base_coordinate.x],
            y=[hand.base_coordinate.y],
            z=[hand.base_coordinate.z],
            mode="markers",
            marker=dict(color="red", symbol="diamond"),
        ),
        # Marker for the Motor Y (black square)
        go.Scatter3d(
            x=[motor_y.coordinate.x],
            y=[motor_y.coordinate.y],
            z=[motor_y.coordinate.z],
            mode="markers",
            marker=dict(color="black", symbol="square"),
        ),
        # Marker for the Motor X (black square)
        go.Scatter3d(
            x=[motor_x.coordinate.x],
            y=[motor_x.coordinate.y],
            z=[motor_x.coordinate.z],
            mode="markers",
            marker=dict(color="black", symbol="square"),
        ),
        # Marker for sqaure arch like frame (black line)
        go.Scatter3d(
            x=[f.x for f in frame],
            y=[f.y for f in frame],
            z=[f.z for f in frame],
            mode="lines",
            line=dict(color="black"),
        ),
        # Connection between FCS and Motor X(black dash line)
        go.Scatter3d(
            x=[hand.finger_tip_coordinate.x, motor_x.coordinate.x],
            y=[hand.finger_tip_coordinate.y, motor_x.coordinate.y],
            z=[hand.finger_tip_coordinate.z, motor_x.coordinate.z],
            mode="lines",
            line=dict(color="black", dash="dash"),
        ),
        # Connection between HCS and FCS (blue dash line)
        go.Scatter3d(
            x=[hand.base_coordinate.x, hand.finger_tip_coordinate.x],
            y=[hand.base_coordinate.y, hand.finger_tip_coordinate.y],
            z=[hand.base_coordinate.z, hand.finger_tip_coordinate.z],
            mode="lines",
            line=dict(color="blue"),
        ),
        # Connection between HCS and Motor X (green dash line)
        go.Scatter3d(
            x=[hand.base_coordinate.x, motor_x.coordinate.x],
            y=[hand.base_coordinate.y, motor_x.coordinate.y],
            z=[hand.base_coordinate.z, motor_x.coordinate.z],
            mode="lines",
            line=dict(color="green", dash="dash"),
        ),
    ]


def create_frames(hand: Hand, motor_y: MotorY, motor_x: MotorX):
    """
    Creates frames for visualizing hand movements using Plotly.

    Args:
        hand (Hand): The hand object containing the hand movements.
        motor_y (MotorY): The motor_y object containing the y-axis motor movements.
        motor_x (MotorX): The motor_x object containing the x-axis motor movements.

    Returns:
        fig (Figure): The Plotly figure object containing the visualized hand movements.
    """
    fig = go.Figure(
        data=plotly_go_visulize(hand, motor_y, motor_x),
        layout=go.Layout(
            xaxis=dict(range=[configuration.X_MIN * 1.1, configuration.X_MAX * 1.1]),
            yaxis=dict(range=[configuration.Y_MIN * 1.1, configuration.Y_MAX * 1.1]),
            # zaxis=dict(range=[0, MOTOR_X_DIST_Z * 1.1]),
        ),
    )

    return fig


def streamlit_go_visulize(
    hand: Hand, motor_y: MotorY, motor_x: MotorX
) -> Tuple[plt.Figure, plt.Axes]:
    """
    Visualize the hand, motors, and frame in a 3D plot.

    This function takes a Hand, MotorY, and MotorX object as input and creates a 3D plot using Matplotlib.
    It displays the hand, motors, and frame using scatter plots.

    Parameters:
        hand (Hand): The Hand object representing the hand's coordinates (HCS= red, FCS= blue).
        motor_y (MotorY): The Flexion/Extension (Motor Y) object (black square).
        motor_x (MotorX): The Radial/Ulnar (Motor X) object (black square).

    Returns:
        Tuple[plt.Figure, Axes3D]: A tuple containing the Matplotlib Figure and Axes3D objects.
    """
    fig = plt.figure()
    plt.style.use("default")
    plt.rcParams["font.size"] = 9
    plt.rcParams["axes.labelsize"] = 9
    ax = fig.add_subplot(111, projection="3d")

    # Marker for the Hand-Base-Coordinate [HCS] system (red diamond)
    ax.scatter(
        hand.base_coordinate.x,
        hand.base_coordinate.y,
        hand.base_coordinate.z,
        c="red",
        marker="^",
    )
    # Marker for the Motor Y (black square)
    ax.scatter(
        motor_y.coordinate.x,
        motor_y.coordinate.y,
        motor_y.coordinate.z,
        c="black",
        marker="s",
    )

    # Marker for the Motor X (black square)
    ax.scatter(
        motor_x.coordinate.x,
        motor_x.coordinate.y,
        motor_x.coordinate.z,
        c="black",
        marker="s",
    )

    # Marker for the Finger-Tip-Coordination system (blue diamond)
    ax.scatter(
        hand.finger_tip_coordinate.x,
        hand.finger_tip_coordinate.y,
        hand.finger_tip_coordinate.z,
        c="blue",
        marker="^",
    )

    # Connection Line between FCS and Motor X (black dash line)
    ax.plot(
        [hand.finger_tip_coordinate.x, motor_x.coordinate.x],
        [hand.finger_tip_coordinate.y, motor_x.coordinate.y],
        [hand.finger_tip_coordinate.z, motor_x.coordinate.z],
        c="black",
        linestyle="dashed",
    )

    # Connection Line between HCS and FCS (blue line)
    ax.plot(
        [hand.base_coordinate.x, hand.finger_tip_coordinate.x],
        [hand.base_coordinate.y, hand.finger_tip_coordinate.y],
        [hand.base_coordinate.z, hand.finger_tip_coordinate.z],
        c="blue",
        label="hand",
    )

    # Connection Line between HCS and Motor X (black dash line)
    ax.plot(
        [hand.base_coordinate.x, motor_x.coordinate.x],
        [hand.base_coordinate.y, motor_x.coordinate.y],
        [hand.base_coordinate.z, motor_x.coordinate.z],
        c="green",
        linestyle="dashed",
    )

    # Get the frame and blot the frame (black line)
    frame = motor_x.get_frame()
    ax.plot(
        [f.x for f in frame],
        [f.y for f in frame],
        [f.z for f in frame],
        c="black",
    )
    # Set label names for the axes
    ax.set_xlabel("X - RU Axis")
    ax.set_ylabel("Y - FE Axis")
    ax.set_zlabel("Z Axis")

    # Set the limits
    ax.set_xlim3d([configuration.X_MIN * 1.1, configuration.X_MAX * 1.1])
    ax.set_ylim3d([configuration.Y_MIN * 1.1, configuration.Y_MAX * 1.1])
    ax.set_zlim3d([0, configuration.MOTOR_RU_Z0 * 1.1])

    return fig, ax


def get_coordinates(coordinate: Coordinate) -> List[float]:
    """
    Get a list of x, y, and z coordinates from a given Coordinate object.

    Parameters:
        coordinate (Coordinate): The Coordinate object from which to extract the coordinates.

    Returns:
        List[float]: A list containing the x, y, and z coordinates in that order.

    """
    return [coordinate.x, coordinate.y, coordinate.z]


def plot_path(ax, paths):
    """
    Plots a path in 3D space.

    Args:
        ax (Axes3D): The 3D axes object to plot the path on.
        paths (list): A list of points representing the path.

    Returns:
        None.
    """
    for p, pn in zip(paths[:-1], paths[1:]):
        ax.plot([p.x, pn.x], [p.y, pn.y], [p.z, pn.z], c="red")


def simulate_weg(profile_name="positions"):
    """
    Simulate the movement of the motors along a predefined path of the hand movement.

    Configurations for path (see configuration.py):
        Alpha min/max: Set the FE range
        Beta min/max: Set the RU range
        Theta: Set the Circumduction
        Speed Theta: Set the angular speed

    This function performs a simulation of the movement of a hand and motors
    based on predefined alpha, beta ranges, theta angle and speed.
    It calculates the alpha and beta angles for each step along a given range of theta values,
    and then moves the hand and motors accordingly. The function generates visualizations of the
    hand and motor positions at each step and saves them as image files. It also
    saves the simulation data, including alpha, beta, and motor coordinates, to
    a CSV file for further analysis.

    Parameters:
        None

    Returns:
        None

    Side Effects:
        - The function saves visualizations of hand and motor positions as image
          files in the "figures" directory.
        - It saves simulation data, including alpha, beta, and motor coordinates,
          to a CSV file named "positions.csv".
    """

    # Create a directory for saving figures
    pathlib.Path("figures").mkdir()

    # Generate theta values from 0 to 360 with the given step size
    theta = list(range(0, 361, configuration.DELTA_THETA))

    # # Calculate the list of the values for alpha and beta values based on theta
    # alpha_steps = [round(math.sin(utils.deg2rad(t)) * configuration.ALPHA_FE_MAX, 2) for t in theta]
    # beta_steps = [round(math.cos(utils.deg2rad(t)) * configuration.BETA_RU_MAX, 2) for t in theta]

    # # Lists to store the steps of alpha and beta for each theta value
    alpha_steps = []
    beta_steps = []

    # Calculate the steps for alpha and beta based theta range and steps
    for t in theta:
        if t <= 90:
            # alpha FE: 0 -> alpha_max
            alpha_steps.append(
                round(math.sin(utils.deg2rad(t)) * configuration.ALPHA_FE_MAX, 2)
            )
            # beta RU:  beta_max -> 0
            beta_steps.append(
                round(math.cos(utils.deg2rad(t)) * configuration.BETA_RU_MAX, 2)
            )
        if t > 90 and t <= 180:
            # alpha FE: alpha_max -> 0
            alpha_steps.append(
                round(math.sin(utils.deg2rad(t)) * configuration.ALPHA_FE_MAX, 2)
            )
            # beta RU:  0 -> beta_min
            beta_steps.append(
                -round(math.cos(utils.deg2rad(t)) * configuration.BETA_RU_MIN, 2)
            )
        # passt nicht
        if t > 180 and t <= 270:
            # alpha FE: 0 -> alpha_min
            alpha_steps.append(
                -round(math.sin(utils.deg2rad(t)) * configuration.ALPHA_FE_MIN, 2)
            )
            # beta RU:  beta_min -> 0
            beta_steps.append(
                -round(math.cos(utils.deg2rad(t)) * configuration.BETA_RU_MIN, 2)
            )
        # passt nicht
        if t > 270 and t <= 360:
            # alpha FE: alpha_min -> 0
            alpha_steps.append(
                -round(math.sin(utils.deg2rad(t)) * configuration.ALPHA_FE_MIN, 2)
            )
            # beta RU: 0 -> beta_max
            beta_steps.append(
                round(math.cos(utils.deg2rad(t)) * configuration.BETA_RU_MAX, 2)
            )

    hand, motor_y, motor_x = init_position()

    files = []
    positions = []
    paths = []
    motor_path = []

    for idx, (a, b) in tqdm(
        enumerate(zip(alpha_steps, beta_steps)), total=len(alpha_steps)
    ):
        move_to_alpha(a, hand, motor_y, motor_x)
        move_to_beta(b, hand, motor_x)
        fig, ax = streamlit_go_visulize(hand, motor_y, motor_x)

        paths.append(hand.finger_tip_coordinate)
        motor_path.append(motor_x.coordinate)

        plot_path(ax, paths)
        plot_path(ax, motor_path)

        ax.view_init(27, 22)
        fname = f"figures/f_{idx}_alpha_{a}_beta_{b}.png"
        fig.savefig(fname)
        files.append(files)
        plt.close()

        positions.append(
            {
                "alpha": a,
                "beta": b,
                "motor_x": motor_x.coordinate,
                "motor_y": motor_y.coordinate,
            }
        )
    p_name = profile_name + ".csv"
    with open(p_name, "w") as f:
        for p, pn in zip(positions[:-1], positions[1:]):
            f.write(
                ",".join(
                    [
                        f"{round(x, 3)}"
                        for x in [
                            int(get_coordinates(p["motor_x"])[0]),
                            abs(
                                int(
                                    ((pn["motor_x"]) - (p["motor_x"])).x
                                    / configuration.DELTA_THETA
                                    * configuration.SPEED_PER_THETA
                                )
                            ),
                            int(get_coordinates(p["motor_y"])[1]),
                            abs(
                                int(
                                    ((pn["motor_y"]) - (p["motor_y"])).y
                                    / configuration.DELTA_THETA
                                    * configuration.SPEED_PER_THETA
                                )
                            ),
                        ]
                    ]
                )
                + "\n"
            )


def store_as_gif():
    """
    Stores a sequence of images as a GIF file.

    Args:
        None.

    Returns:
        None.
    """
    import os

    import imageio

    files = [f for f in os.listdir("figures") if f.endswith(".png")]
    files = sorted(files, key=lambda x: int(x.split("_")[1]))

    with imageio.get_writer("mygif.gif", mode="I") as writer:
        for f in tqdm(files, total=len(files)):
            image = imageio.imread(f"figures/{f}")
            writer.append_data(image)


def delete_all_figures():
    """
    Deletes all figures stored in the "figures" directory.

    Args:
        None.

    Returns:
        None.
    """
    import shutil

    shutil.rmtree("figures")


if __name__ == "__main__":
    delete_all_figures()
    simulate_weg()
    store_as_gif()
    print("finished")
