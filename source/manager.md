# manager module[¶](#module-manager "Link to this heading")

## `get_alpha()`
    manager.get_alpha(coord1, coord2)
Calculates and returns the alpha angle between two coordinates.

Arguments:

- **coord1 (Coordinate)**: The first coordinate. 
- **coord2 (Coordinate)**: The second coordinate.

Returns:

- **float**: The alpha angle in degrees.

## `get_beta()`
    manager.get_beta(coord1, coord2)

Calculates and returns the beta angle between two coordinates.

Args:

- **coord1 (Coordinate)**: The first coordinate.
- **coord2 (Coordinate)**: The second coordinate.

Returns:

- **float**: The beta angle in degrees.

## `init_position()`

Initialize the Hand and Motors Objects with their initial positions.

This function creates and initializes the Hand and Motors objects
along with their initial positions for Flexion/Extension (Motor Y)
and Radial/Ulnar (Motor X) angles.

Returns:

- **tuple:** A tuple containing three objects:

    -   *Hand:* The Hand object initialized with the initial alpha
    and beta angles.

    -   *MotorY:* The Flexion/Extension Motor (Motor Y) object
    with its initial settings.

    -   *MotorX:* The Radial/Ulnar Motor (Motor X) object with its
    initial settings.


## `move_to_alpha()`

    manager.move_to_alpha(alpha, hand: Hand, motor_y: MotorY, motor_x: MotorX)

Set the 'alpha' flexion/extension angle of the Hand.

The motor positions (motor_x = radial/ulnar, motor_y = flexion/extension) are calculated to achieve the specified 'alpha'
angle for the Hand.

Parameters:

- alpha (float): The desired 'alpha' angle to be set for the Hand.
- hand (Hand): The Hand object to which the 'alpha' angle will be
- set.motor_y (MotorY): The Flexion/Extension Motor (Motor Y)
- object. motor_x (MotorX): The Radial/Ulnar Motor (Motor X) object.

Returns:

- None

Side Effects:

- The function has the following side effects: 
- The 'alpha' angle of the Hand is set to the specified value. 
- The Flexion/Extension (Motor Y) and Radial/Ulnar (Motor X) Motors
are adjusted to achieve the 'alpha' hand angle.*

## `move_to_beta()`

    manager.move_to_beta(beta, hand: Hand, motor_y: MotorY, motor_x: MotorX)

Moves the motor to the specified beta position and updates the
hand's beta value.

Args:

- beta (float): The desired beta position. 
- hand (Hand): The hand object. 
- motor_x (MotorX): The motor_x object.

Returns:

- None
