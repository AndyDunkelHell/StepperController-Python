# plotting module[¶](#module-plotting "Link to this heading")

## `create_frames()`

    plotting.create_frames(hand: Hand, motor_y: MotorY, motor_x: MotorX)

Creates frames for visualizing hand movements using Plotly.

Args:

- **hand (Hand):** The hand object containing the hand movements.
- **motor_y (MotorY):** The motor_y object containing the y-axis motor
- **movements. motor_x (MotorX)**: The motor_x object containing the x-axis motor movements.

Returns:

- **fig (Figure)**: The Plotly figure object containing the visualized
    hand movements.

## `delete_figures()`

Deletes all figures stored in the "figures" directory.

Args:

- None.

Returns:

- None.

## `get_coordinates()`

    plotting.get_coordinates(coordinate: Coordinate) → List[float]

Get a list of x, y, and z coordinates from a given Coordinate object.

Parameters:

- coordinate (Coordinate): The Coordinate object from which to
extract the coordinates.

Returns:

- **List[float]**: A list containing the x, y, and z coordinates in that order.

## `plot_path()`

    plotting.plot_path(ax: Axes3D, paths: List[Coordinate])

Plots a path in 3D space.

Args:

- **ax (Axes3D)**: The 3D axes object to plot the path on paths
- **paths (list)**: A list of points representing the path.

Returns:

- None.

## `plotly_go_visulize()`

    plotting.plotly_go_visulize(hand: Hand, motor_y: MotorY, motor_x: MotorX) → List[go.Scatter3d]

Visualize the hand, motors, and frame using Plotly 3D scatter plots.

This function takes a Hand, MotorY, and MotorX object as input and
generates a list of Plotly Scatter3d traces to visualize the hand,
motors, and frame in 3D space.

Parameters:

- **hand (Hand)**: The Hand object representing the hand's coordinates
- **motor_y (MotorY)**: The Flexion/Extension (Motor Y) object.
- **motor_x (MotorX)**: The Radial/Ulnar (Motor X) object.

Returns:

- **List [go.Scatter3d]**: A list of Plotly Scatter3d traces representing the visualization.

## `simulate_weg()`
    
        plotting.simulate_weg(profile_name='positions')

Simulate the movement of the motors along a predefined path of the
hand movement.

Configurations for path (see [configuration.py](configuration.md)):

- Alpha min/max: Set the FE range 
- Beta min/max: Set the RU range
- Theta: Set the Circumduction 
- Speed Theta: Set the angular speed

This function performs a simulation of the movement of a hand and
motors based on predefined alpha, beta ranges, theta angle and
speed. 

It calculates the alpha and beta angles for each step along a
given range of theta values, and then moves the hand and motors
accordingly. 

The function generates visualizations of the hand and
motor positions at each step and saves them as image files. 

It also saves the simulation data, including alpha, beta, and motor
coordinates, to a CSV file for further analysis.

Parameters:

- None

Returns:

- None

Side Effects:

-   The function saves visualizations of hand and motor
            positions as image files in the "figures" directory.

-   It saves simulation data, including alpha, beta, and motor
            coordinates, to a CSV file named "positions.csv".

## `store_as_gif()`

Stores a sequence of images as a *GIF* file.

Args:

- None.

Returns:

- None.

## `streamlit_go_visulize()`

    plotting.streamlit_go_visulize(hand: Hand, motor_y: MotorY, motor_x: MotorX) → Tuple[Figure, Axes]

Visualize the hand, motors, and frame in a 3D plot.

This function takes a Hand, MotorY, and MotorX object as input and
    creates a 3D plot using Matplotlib. It displays the hand, motors,
    and frame using scatter plots.

Parameters:

- hand (Hand): The Hand object representing the hand's coordinates (HCS= red, FCS= blue). 
- motor_y (MotorY): The Flexion/Extension (Motor Y) object (black square).
- motor_x (MotorX): The Radial/Ulnar (Motor X) object (black square).

Returns:

- **Tuple [plt.Figure, Axes3D]**: A tuple containing the Matplotlib Figure and Axes3D objects.
