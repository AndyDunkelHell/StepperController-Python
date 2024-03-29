import math

import utils
from schemas import BoundryCoordinate, Coordinate, Hand, MotorX, MotorY

from configuration import ALPHA_INIT, BETA_INIT, X_MAX, X_MIN


def init_position():
    """
    Initialize the Hand and Motors Objects with their initial positions.

    This function creates and initializes the Hand and Motors objects along with their initial positions
    for Flexion/Extension (Motor Y) and Radial/Ulnar (Motor X) angles.

    Returns:
        tuple: A tuple containing three objects:
            - Hand: The Hand object initialized with the initial alpha and beta angles.
            - MotorY: The Flexion/Extension Motor (Motor Y) object with its initial settings.
            - MotorX: The Radial/Ulnar Motor (Motor X) object with its initial settings.
    """

    # Define the init Position of the hand alpha
    hand = Hand(
        alpha=ALPHA_INIT,
        beta=BETA_INIT,
    )

    # Define the init Position of the Flexion/Extension Motor (Motor Y)
    motor_y = MotorY(
        name="MotorY - FE",
        coordinate=Coordinate.motor_y_resting_coordinate(),
        resting_coordinate=Coordinate.motor_y_resting_coordinate(),
        min_coordinate=BoundryCoordinate(y=-1000),
        max_coordinate=BoundryCoordinate(y=1000),
    )

    # Define the init Position of the Radial/Ulnar Motor (Motor Y)
    motor_x = MotorX(
        name="MotorX - RU",
        coordinate=Coordinate.motor_x_resting_coordinate(),
        resting_coordinate=Coordinate.motor_x_resting_coordinate(),
        min_coordinate=BoundryCoordinate(x=X_MIN),
        max_coordinate=BoundryCoordinate(x=X_MAX),
    )

    # print(
    #     f"HCS: x={hand.base_coordinate.x},y={hand.base_coordinate.y},z={hand.base_coordinate.z}"
    #     f"FCS: x={hand.finger_tip_coordinate.x},y={hand.finger_tip_coordinate.y},z={hand.finger_tip_coordinate.z}"
    #     f"Motor X: x={motor_x.coordinate.x},y={motor_x.coordinate.y},z={motor_x.coordinate.z}"
    #     f"Motor Y: x={motor_y.coordinate.x},y={motor_y.coordinate.y},z={motor_y.coordinate.z}"
    # )
    return hand, motor_y, motor_x


def move_to_alpha(
    alpha,
    hand: Hand,
    motor_y: MotorY,
    motor_x: MotorX,
):
    """
    Set the 'alpha' flexion/extension angle of the Hand.

    The motor positions (motor_x = radial/ulnar, motor_y = flexion/extension)
    are calculated to achieve the specified 'alpha' angle for the Hand.

    Parameters:
        alpha (float): The desired 'alpha' angle to be set for the Hand.
        hand (Hand): The Hand object to which the 'alpha' angle will be set.
        motor_y (MotorY): The Flexion/Extension Motor (Motor Y) object.
        motor_x (MotorX): The Radial/Ulnar Motor (Motor X) object.

    Returns:
        None

    Side Effects:
        The function has the following side effects:
        - The 'alpha' angle of the Hand is set to the specified value.
        - The Flexion/Extension (Motor Y) and Radial/Ulnar (Motor X) Motors are adjusted to achieve the 'alpha' hand angle.
    """
    # Get the z-Values of the Hand and the Motor X
    a = hand.base_coordinate.z  # z-Position of the Hand
    r = motor_x.resting_coordinate.z  # z-Position of the MotorX

    # Calculates the phi angle base on the distance of the hand and the Motor x (z-Values)
    phi = utils.alpha2phi(r, a, alpha)

    # Moves both motors to the angle phi
    motor_y.move_to_phi(phi)
    motor_x.move_to_phi(phi)
    hand.alpha = alpha


def move_to_beta(
    beta,
    hand: Hand,
    motor_x: MotorX,
):
    """
    Moves the motor to the specified beta position and updates the hand's beta value.

    Args:
        beta (float): The desired beta position.
        hand (Hand): The hand object.
        motor_x (MotorX): The motor_x object.

    Returns:
        None.
    """
    motor_x.move_to_beta(beta, hand.alpha)
    hand.beta = beta


def get_alpha(coord1, coord2):
    """
    Calculates and returns the alpha angle between two coordinates.

    Args:
        coord1 (Coordinate): The first coordinate.
        coord2 (Coordinate): The second coordinate.

    Returns:
        float: The alpha angle in degrees.
    """
    return 90 - utils.rad2deg(
        math.atan2(
            coord1.z - coord2.z,
            coord1.y - coord2.y,
        )
    )


def get_beta(coord1, coord2):
    """
    Calculates and returns the beta angle between two coordinates.

    Args:
        coord1 (Coordinate): The first coordinate.
        coord2 (Coordinate): The second coordinate.

    Returns:
        float: The beta angle in degrees.
    """
    return 90 - utils.rad2deg(
        math.atan2(
            coord1.z - coord2.z,
            coord1.x - coord2.x,
        )
    )
