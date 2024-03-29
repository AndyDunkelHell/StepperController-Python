import math


def rad2deg(rad: float) -> float:
    """
    Converts an angle in radians to degrees.

    Args:
        rad (float): The angle in radians.

    Returns:
        float: The angle in degrees.
    """
    return rad * 180 / math.pi


def deg2rad(deg: float) -> float:
    """
    Converts an angle in degrees to radians.

    Args:
        deg (float): The angle in degrees.

    Returns:
        float: The angle in radians.
    """
    return deg * math.pi / 180


def alpha2phi(r: float, a: float, alpha: float) -> float:
    """
    Calculates the phi angle based on the given alpha angle, the base coordinate (a), and the resting coordinate (r).

    Args:
        r (float): The resting coordinate.
        a (float): The base coordinate.
        alpha (float): The alpha angle.

    Returns:
        float: The phi angle.

    Note:
        This function is used in the "move_to_alpha" function in the "engine.py" module to calculate the phi angle before moving the motors and updating the hand's alpha angle.
    """
    # Calculation see "Doc"
    gamma = rad2deg(math.asin(a / r * math.sin(deg2rad(180 - alpha))))
    return alpha - gamma

    # Old engine.py
    # import math

    # import utils
    # from schemas import Coordinate, Hand, MotorX, MotorY

    # def move_to_alpha(
    #     alpha,
    #     hand: Hand,
    #     motor_y: MotorY,
    #     motor_x: MotorX,
    # ):
    #     a = hand.base_coordinate.z
    #     r = motor_x.resting_coordinate.z

    #     phi = utils.alpha2phi(r, a, alpha)

    #     motor_y.move_to_phi(phi)
    #     motor_x.move_to_phi(phi)
    #     hand.alpha = alpha
