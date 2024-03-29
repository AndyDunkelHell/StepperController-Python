# schemas module[¶](#module-schemas "Link to this heading")

## `class BoundryCoordinate()`

Bases: **BaseModel**

Represent a boundary coordinate with optional x, y, and z values.

This class inherits from the BaseModel and allows defining a
boundary condition in one dimension (x, y, or z) while keeping the
other dimensions unset (None).

Parameters:

- **x (float, optional)**: Optional float value representing the x-coordinate of the boundary. 
- **y (float, optional)**: Optional float value representing the y-coordinate of the boundary. 
- **z (float, optional)**: Optional float value representing the z-coordinate of the boundary.

Raises:

- **ValueError:** If more or less than one dimensions is defined as a
boundry.

## `class Coordinate()`

Bases: **BaseModel**

Represent a set of points in 3D space using cartesian coordinates
(x,y,z).

Parameters:

- **x (float)**: The x-coordinate of the point. 
- **y (float)**: The y-coordinate of the point. 
- **z (float)**: The z-coordinate of the point. 
- **description (str, optional)**: Description of the coordinate

## `Coordinate.hand_base_coordinate()`

    hand_base_coordinate(hand_dist_z: float = 150) → Coordinate

Get the center of the Coordinate System of the Hand in the
global coordinate system.

This class method returns a new Coordinate object representing
the center of the Coordinate System of the Hand in the global
Cartesian Coordinate System (x, y, z).

Parameters:

- hand_dist_z (float, optional): The z-coordinate value for the Hand base (default is HAND_BASE_Z_DIST).

Returns:

- Coordinate: The new Coordinate object representing the Hand base coordinate as (x=0,y=0,z=hand_dist_z).

## `Coordinate.is_greater_than()`

    is_greater_than(boundary: BoundryCoordinate) → bool

Compare if the Cartesian coordinate is greater than its boundary
value.

Parameters:

- boundary (BoundryCoordinate): The BoundaryCoordinate object
for comparison.

Returns:

- bool: True if the coordinate is greater than the boundary, False otherwise.

## `Coordinate.is_smaller_than()`

    is_smaller_than(boundary: BoundryCoordinate) → bool

Compare if the Cartesian coordinate is smaller than its boundary
value.

Parameters:

- boundary (BoundryCoordinate): The BoundaryCoordinate object
for comparison.

Returns:

- bool: True if the coordinate is smaller than the boundary, False otherwise.

## `Coordinate.motor_x_resting_coordinate()`

    motor_x_resting_coordinate() → Coordinate

Get the resting position of the Radial/Ulnar Motor (Motor X) in
the global cartesian Coordinate System x,y,z.

This class method returns a new Coordinate object representing
the resting position of the Radial/Ulnar Motor (Motor X) in the
global Cartesian Coordinate System (x, y, z) when both alpha and
beta angles are zero.

Returns:

- Coordinate: The new Coordinate object representing the           resting position of Motor X (x=0, y=0, z=MOTOR_RU_Z0).

## `Coordinate.motor_y_resting_coordinate()`

    motor_y_resting_coordinate() → Coordinate

Get the resting position of the Flexion/Extension Motor
(Motor Y) in the global cartesian Coordinate System x,y,z.

This class method returns a new Coordinate object representing
the resting position of the Flexion/Extension Motor (Motor Y) in
the global Cartesian Coordinate System (x, y, z) when both alpha
and beta angles are zero.

Returns:

- Coordinate: The new Coordinate object representing the resting position of Motor Y (x=x_min, y=0, z=MOTOR_FE_Z0).

## `class Hand()`

Bases: **BaseModel**

Returns the coordinate of the finger tip in the XYZ space.

This function calculates the coordinate of the finger tip in the
XYZ space based on the hand height, alpha angle, beta angle, and
base coordinate. The hand height is multiplied by the sine of
the beta angle to determine the x coordinate. The hand height is
multiplied by the sine of the alpha angle and the cosine of the
beta angle to determine the y coordinate. The hand height is
multiplied by the cosine of the alpha angle and the cosine of
the beta angle to determine the z coordinate. The alpha angle
represents the angle between the base of the hand and its
fingertip, and the beta angle represents the position of the
fingertip based on motor positions. The resulting coordinate is
then added to the base coordinate.

Parameters:

- None

Returns:

- Coordinate: The coordinate of the finger tip in the XYZ space.

Example:

- **finger_tip_coordinate** = finger_tip_coordinate()

Note:

- This function assumes that the hand height, alpha angle,
            beta angle, and base coordinate have been properly set
            before calling the function.

Methods:

- [finger_tip_coordinate_in_yz()](#schemas.Hand.finger_tip_coordinate_in_yz)
- [get_alpha()](#schemas.Hand.get_alpha)
- [get_beta()](#schemas.Hand.get_beta)


## `Hand.finger_tip_coordinate_in_yz()`

    @property 
    finger_tip_coordinate_in_yz() → Coordinate

Returns the coordinate of the finger tip in the YZ plane.

This function calculates the coordinate of the finger tip in the
YZ plane based on the hand height, alpha angle, and base
coordinate. The hand height is multiplied by the sine of the
alpha angle and the cosine of the alpha angle to determine the y
and z coordinates, respectively. The alpha angle represents the
hand position. The resulting coordinate is then added to the
base coordinate.

Parameters:

- None

Returns:

- Coordinate: The coordinate of the finger tip in the YZ plane.

Example:

- finger_tip_coordinate = finger_tip_coordinate_in_yz()

Note:

- This function assumes that the hand height, alpha angle, and base coordinate have been properly set before calling the
function.

## `Hand.get_alpha()`

    get_alpha() → float

Returns the alpha angle of the hand.

This function calculates the alpha angle of the hand based on
the beta angle, finger tip coordinate, and base coordinate. 

The beta angle is obtained by calling the get_beta() function. 

The alpha angle is calculated as 90 degrees minus the arctangent of
the ratio between the difference in z coordinates of the finger
tip and base coordinate, divided by the cosine of the beta
angle, and the difference in y coordinates of the finger tip and
base coordinate. The resulting alpha angle represents the angle between the base of the hand and its fingertip.

Parameters:

- None

Returns:

- float: The alpha angle of the hand in degrees.

Example:

- alpha_angle = get_alpha()

Note:

- This function assumes that the beta angle, finger tip
coordinate, and base coordinate have been properly set
before calling the function.

## `Hand.get_beta()`

    get_beta() → float

Returns the beta angle of the hand.

This function calculates the beta angle of the hand based on the
finger tip coordinate and base coordinate. 

The beta angle is calculated as 90 degrees minus the arctangent of the ratio between the difference in z coordinates of the finger tip and base coordinate, and the difference in x coordinates of the finger tip and base coordinate. 

The resulting beta angle represents the angle between the base of the hand and its fingertip.

Parameters:

- None

Returns:

- float: The beta angle of the hand in degrees.

Example:

- beta_angle = get_beta()

Note:

- This function assumes that the finger tip coordinate and base coordinate have been properly set before calling the function.


## `class Motor()`

Bases: **BaseModel**

Represents a general motor with its init and current position as
well as the movement boundaries.

Attributes:

- coordinate (Coordinate): The current coordinate (position) of the motor in the global coordinate system. 
- resting_coordinate (Coordinate):The resting position of the motor when alpha = 0 and beta = 0 in the global coordinate system. 
- min_coordinate (BoundryCoordinate): The minimum boundary position the motor can reach in the global coordinate system. 
- max_coordinate (BoundryCoordinate): The maximum boundary position the motor can reach in the global coordinate system.
- phi: (float): The phi angle (between the frame and the base) of the motor (default is 0). 
- name (str): A name or identifier for the motor (default is None).

Methods:

- [move()](#schemas.Motor.move)

## `Motor.move()`

    move(coordinate: Coordinate) → None

Moves the motor to the specified coordinate if it is within
the valid boundaries. If the specified coordinate is outside
the boundaries, a MotorOutOfBoundry exception is raised.

Raises:

- **MotorOutOfBoundry**: Raised when the specified coordinate is
outside the valid boundaries.

Parameters:

- coordinate (Coordinate): The target coordinate to move the
motor to.

## `class MotorX()`

Bases: **Motor**

MotorX class extends the Motor class for a motor in x (RU)
direction.

Attributes:

- hand_base_coordinate (Coordinate): The hand base coordinate of the motor. 
- yz_resting_coord (Optional[Coordinate]): The resting coordinate in the yz-plane.

Methods:

- [get_frame()](#schemas.MotorX.get_frame)
- [move_to_beta()](#schemas.MotorX.move_to_beta)
- [move_to_phi()](#schemas.MotorX.move_to_phi)
- [yz_resting_coordinate()](#schemas.MotorX.yz_resting_coordinate)
- [zy_coordinate()](#schemas.MotorX.zy_coordinate)

## `MotorX.get_frame()`

    get_frame() → List[Coordinate]

Get a list of four coordinates representing a square arch-like frame.

Returns:
- List[Coordinate]: A list of Coordinate objects representing the frame points.

## `MotorX.move_to_beta()`

    move_to_beta(beta: float) → None

Move the MotorX instance to the given beta angle.

Args:
- beta (float): The beta angle to move to. alpha: (float): The alpha angle.

Returns:
- None

## `MotorX.move_to_phi()`

    move_to_phi(phi: float) → None

Move the MotorX instance to the given phi angle.

Args:

- phi (float): The phi angle to move to.

Returns:

- None

## `MotorX.yz_resting_coordinate()`

    yz_resting_coordinate() → Coordinate

Get the resting coordinate in the yz-plane.

If the yz_resting_coord attribute is None, it calculates the yz resting coordinate based on the current coordinate and returns it.

Returns:

- Coordinate: The resting coordinate in the yz-plane.

## `MotorX.zy_coordinate()`

Get the projection of the Position (depending on phi) onto the x-z plane

Returns:
- Coordinate: The projection of the y-z Plane onto the x-z plane.

## `class MotorY()`

Bases: **Motor**


A class representing a Y-axis motor.

This class inherits from the Motor class and provides additional
methods to move the motor along the Y-axis and adjust its position
based on a given angle.

Calculation see "Doc"

Attributes:

- name (str): The name of the Y-axis motor. 
- coordinate (Coordinate): The current position of the Y-axis motor.
- min_coordinate (Coordinate): The minimum allowed coordinate for the Y-axis motor. 
- max_coordinate (Coordinate): The maximum allowed coordinate for the Y-axis motor. 
- phi (float): The current phi-angle (in degrees) of the Y-axis motor relative to its resting position in the global CS.

Methods:

- [move_to_new_y()](#schemas.MotorY.move_to_new_y)
- [move_to_phi()](#schemas.MotorY.move_to_phi)

## `MotorY.move_to_new_y()`

    move_to_new_y(new_y: float) → None

Move the Motor Y (FE-Movment) along the y-axis by a specified delta y.

This method calculates a new coordinate by adjusting the y-coordinate of the current position by the given delta_y. It then calls the ‘move’ method to move the motor to the new coordinate if it falls within the defined boundaries.

Calculation see “Doc”

Parameters:
- new_y (float): The amount to move the motor along the y-axis.

Returns:
- None

## `MotorY.move_to_phi()`

    move_to_phi(phi: float) → None

Move the motor to a specified ‘phi’ angle.

This method calculates the amount to move the motor along the y-axis (‘new_y’) based on the desired ‘phi’ angle provided. It then calls the ‘move_to_new_y’ method to move the motor by the calculated ‘new_y’ value. Additionally, the ‘phi’ attribute of the motor is updated to the provided angle.

Parameters:
- phi (float): The desired ‘phi’ angle (in degrees) to move the motor to.

Returns:
- None

## `class PolarCoord()`

Bases: **BaseModel**


Represent a set of points in 3D space using polar coordinates (r,phi,theta).

This class stores the radial distance (r), azimuth angle (phi), and polar angle (theta) to represent a point in 3D space using polar coordinates.

Parameters:

- r (float): The radial distance from the origin to the point. 
- phi (float): The azimuth angle (in degrees). 
- theta (float): The polar angle (in degrees).
