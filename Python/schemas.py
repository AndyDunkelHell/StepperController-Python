from __future__ import annotations

import math
from typing import Optional

import utils
from pydantic import BaseModel

from configuration import (
    HAND_BASE_Z_DIST,
    HAND_HEIGHT,
    MOTOR_FE_Z0,
    MOTOR_RU_Z0,
    X_MAX,
    X_MIN,
    Z_K,
)


class MotorOutOfBoundry(Exception):
    pass


class BoundryCoordinate(BaseModel):
    """
    Represent a boundary coordinate with optional x, y, and z values.

    This class inherits from the BaseModel and allows defining a boundary condition
    in one dimension (x, y, or z) while keeping the other dimensions unset (None).

    Parameters:
        x (float, optional): Optional float value representing the x-coordinate of the boundary.
        y (float, optional): Optional float value representing the y-coordinate of the boundary.
        z (float, optional): Optional float value representing the z-coordinate of the boundary.

    Raises:
        ValueError: If more or less than one dimensions is defined as a boundry.
    """

    x: Optional[float] = None
    y: Optional[float] = None
    z: Optional[float] = None

    # Initate the Class and inheritate the init_Function of the BaseModel
    def __init__(self, *args, **kwrags):
        """
        Initialize the BoundryCoordinate object.

        Raises:
            ValueError: If more or less than one dimensions are defined as boundaries.
        """

        super().__init__(*args, **kwrags)

        # Each Object can only define a boundry condition in one dimension
        if sum([self.x is None, self.y is None, self.z is None]) != 2:
            raise ValueError("boundry should only have boudnry in one dimension")


class PolarCoord(BaseModel):
    """
    Represent a set of points in 3D space using polar coordinates (r,phi,theta).

    This class stores the radial distance (r), azimuth angle (phi), and polar angle (theta)
    to represent a point in 3D space using polar coordinates.

    Parameters:
        r (float): The radial distance from the origin to the point.
        phi (float): The azimuth angle (in degrees).
        theta (float): The polar angle (in degrees).
    """

    r: float
    phi: float
    theta: float


class Coordinate(BaseModel):
    """
    Represent a set of points in 3D space using cartesian coordinates (x,y,z).

    Parameters:
        x (float): The x-coordinate of the point.
        y (float): The y-coordinate of the point.
        z (float): The z-coordinate of the point.
        description (str, optional): Description of the coordinate
    """

    x: float
    y: float
    z: float
    description: Optional[str] = ""

    def __eq__(self, other: Coordinate) -> bool:
        """
        Compare if two Cartesian Coordinates are equal.

        Parameters:
            other (Coordinate): The other Coordinate object to compare.

        Returns:
            bool: True if the coordinates are equal, False otherwise.
        """
        # if (self.x == other.x) and (self.y == other.y) and (self.z == other.z):
        #     return True
        # else:
        #     return False

    def is_smaller_than(self, boundry: BoundryCoordinate) -> bool:
        """
        Compare if the Cartesian coordinate is smaller than its boundary value.

        Parameters:
            boundary (BoundryCoordinate): The BoundaryCoordinate object for comparison.

        Returns:
            bool: True if the coordinate is smaller than the boundary, False otherwise.
        """
        if boundry.x is not None:
            return self.x < boundry.x
        elif boundry.y is not None:
            return self.y < boundry.y
        elif boundry.z is not None:
            return self.z < boundry.z
        return True

    def is_greater_than(self, boundry: BoundryCoordinate) -> bool:
        """
        Compare if the Cartesian coordinate is greater than its boundary value.

        Parameters:
            boundary (BoundryCoordinate): The BoundaryCoordinate object for comparison.

        Returns:
            bool: True if the coordinate is greater than the boundary, False otherwise.
        """
        if boundry.x is not None:
            return self.x > boundry.x
        elif boundry.y is not None:
            return self.y > boundry.y
        elif boundry.z is not None:
            return self.z > boundry.z
        return True

    def __add__(self, other: Coordinate) -> Coordinate:
        """
        Add another Coordinate to the current Coordinate.

        Parameters:
            other (Coordinate): The other Coordinate object to add.

        Returns:
            Coordinate: A new Coordinate object resulting from the addition.
        """
        return Coordinate(
            x=self.x + other.x,
            y=self.y + other.y,
            z=self.z + other.z,
            description=self.description,
        )

    def __sub__(self, other: Coordinate) -> Coordinate:
        """
        Subtract another Coordinate from the current Coordinate.

        Parameters:
            other (Coordinate): The other Coordinate object to subtract.

        Returns:
            Coordinate: A new Coordinate object resulting from the subtraction.
        """
        return Coordinate(
            x=self.x - other.x,
            y=self.y - other.y,
            z=self.z - other.z,
            description=self.description,
        )

    @classmethod
    def hand_base_coordinate(cls, hand_dist_z: float = HAND_BASE_Z_DIST) -> Coordinate:
        """
        Get the center of the Coordinate System of the Hand in the global coordinate system.

        This class method returns a new Coordinate object representing the center of the Coordinate System of the Hand
        in the global Cartesian Coordinate System (x, y, z).

        Parameters:
            hand_dist_z (float, optional): The z-coordinate value for the Hand base (default is HAND_BASE_Z_DIST).

        Returns:
            Coordinate: The new Coordinate object representing the Hand base coordinate as (x=0,y=0,z=hand_dist_z).
        """
        return cls(
            x=0,
            y=0,
            z=hand_dist_z,
            description="Hand base coordinate",
        )

    @classmethod
    def motor_y_resting_coordinate(cls) -> Coordinate:
        """
        Get the resting position of the Flexion/Extension Motor (Motor Y) in the global cartesian Coordinate System x,y,z.

        This class method returns a new Coordinate object representing the resting position of the Flexion/Extension Motor (Motor Y)
        in the global Cartesian Coordinate System (x, y, z) when both alpha and beta angles are zero.

        Returns:
            Coordinate: The new Coordinate object representing the resting position of Motor Y (x=x_min, y=0, z=MOTOR_FE_Z0).
        """
        return cls(
            x=X_MIN,
            y=0,
            z=MOTOR_FE_Z0,
            description="motor y resting coordinate",
        )

    @classmethod
    def motor_x_resting_coordinate(cls) -> Coordinate:
        """
        Get the resting position of the Radial/Ulnar Motor (Motor X) in the global cartesian Coordinate System x,y,z.

        This class method returns a new Coordinate object representing the resting position of the Radial/Ulnar Motor (Motor X)
        in the global Cartesian Coordinate System (x, y, z) when both alpha and beta angles are zero.

        Returns:
            Coordinate: The new Coordinate object representing the resting position of Motor X (x=0, y=0, z=MOTOR_RU_Z0).
        """
        return cls(
            x=0,
            y=0,
            z=MOTOR_RU_Z0,
            description="motor x resting coordinate",
        )


class Hand(BaseModel):
    base_coordinate: Coordinate = Coordinate.hand_base_coordinate()
    hand_height: float = HAND_HEIGHT
    alpha: float = 0
    beta: float = 0

    # Returns the Finger_tip_Coordinate in the YZ Plane
    # only MotorY is moving
    # Changes of the Coordinates only resulting form changes of alpha
    @property
    def finger_tip_coordinate_in_yz(self) -> Coordinate:
        """

        Returns the coordinate of the finger tip in the YZ plane.

        This function calculates the coordinate of the finger tip in the YZ plane based on the hand height, alpha angle, and base coordinate. The hand height is multiplied by the sine of the alpha angle and the cosine of the alpha angle to determine the y and z coordinates, respectively. The alpha angle represents the hand position. The resulting coordinate is then added to the base coordinate.

        Parameters:
            None

        Returns:
            Coordinate: The coordinate of the finger tip in the YZ plane.

        Example:
            finger_tip_coordinate = finger_tip_coordinate_in_yz()

        Note:
            This function assumes that the hand height, alpha angle, and base coordinate have been properly set before calling the function.

        """
        return (
            Coordinate(
                x=0,
                y=self.hand_height * math.sin(utils.deg2rad(self.alpha)),
                z=self.hand_height * math.cos(utils.deg2rad(self.alpha)),
                description=f"hand position for alpha: {self.alpha}",
            )
            + self.base_coordinate
        )

        # Returns the Finger_tip_Coordinate in the XYZ Space
        # MotorY and MotorX are moving
        # Changes of the Coordinates resulting form changes of alpha and beta

    @property
    def finger_tip_coordinate(self) -> Coordinate:
        """
        Returns the coordinate of the finger tip in the XYZ space.

        This function calculates the coordinate of the finger tip in the XYZ space based on the hand height, alpha angle, beta angle, and base coordinate. The hand height is multiplied by the sine of the beta angle to determine the x coordinate. The hand height is multiplied by the sine of the alpha angle and the cosine of the beta angle to determine the y coordinate. The hand height is multiplied by the cosine of the alpha angle and the cosine of the beta angle to determine the z coordinate. The alpha angle represents the angle between the base of the hand and its fingertip, and the beta angle represents the position of the fingertip based on motor positions. The resulting coordinate is then added to the base coordinate.

        Parameters:
            None

        Returns:
            Coordinate: The coordinate of the finger tip in the XYZ space.

        Example:
            finger_tip_coordinate = finger_tip_coordinate()

        Note:
            This function assumes that the hand height, alpha angle, beta angle, and base coordinate have been properly set before calling the function.
        """
        return (
            Coordinate(
                x=self.hand_height * math.sin(utils.deg2rad(self.beta)),
                y=self.hand_height
                * math.sin(utils.deg2rad(self.alpha))
                * math.cos(utils.deg2rad(self.beta)),
                z=self.hand_height
                * math.cos(utils.deg2rad(self.alpha))
                * math.cos(utils.deg2rad(self.beta)),
                description=f"hand position for alpha: {self.alpha}, beta: {self.beta}",
            )
            + self.base_coordinate
        )

        # Calculate alpha as the angle between in the base of the Hand and its fingertip
        # The position of the fingertip based of Motor Positions

    def get_alpha(self):
        """
        Returns the alpha angle of the hand.

        This function calculates the alpha angle of the hand based on the beta angle, finger tip coordinate, and base coordinate. The beta angle is obtained by calling the get_beta() function. The alpha angle is calculated as 90 degrees minus the arctangent of the ratio between the difference in z coordinates of the finger tip and base coordinate, divided by the cosine of the beta angle, and the difference in y coordinates of the finger tip and base coordinate. The resulting alpha angle represents the angle between the base of the hand and its fingertip.

        Parameters:
            None

        Returns:
            float: The alpha angle of the hand in degrees.

        Example:
            alpha_angle = get_alpha()

        Note:
            This function assumes that the beta angle, finger tip coordinate, and base coordinate have been properly set before calling the function.
        """
        beta = self.get_beta()
        return 90 - utils.rad2deg(
            math.atan2(
                (self.finger_tip_coordinate.z - self.base_coordinate.z)
                / math.cos(utils.deg2rad(beta)),
                self.finger_tip_coordinate.y - self.base_coordinate.y,
            )
        )

        # Calculate beta as the angle between in the base of the Hand and its fingertip
        # The position of the fingertip based of Motor Positions

    def get_beta(self):
        """
        Returns the beta angle of the hand.

        This function calculates the beta angle of the hand based on the finger tip coordinate and base coordinate. The beta angle is calculated as 90 degrees minus the arctangent of the ratio between the difference in z coordinates of the finger tip and base coordinate, and the difference in x coordinates of the finger tip and base coordinate. The resulting beta angle represents the angle between the base of the hand and its fingertip.

        Parameters:
            None

        Returns:
            float: The beta angle of the hand in degrees.

        Example:
            beta_angle = get_beta()

        Note:
            This function assumes that the finger tip coordinate and base coordinate have been properly set before calling the function.
        """
        return 90 - utils.rad2deg(
            math.atan2(
                self.finger_tip_coordinate.z - self.base_coordinate.z,
                self.finger_tip_coordinate.x - self.base_coordinate.x,
            )
        )


class Motor(BaseModel):
    """
    Represents a general motor with its init and current position as well as the movement boundaries.

    Attributes:
        coordinate (Coordinate): The current coordinate (position) of the motor in the global coordinate system.
        resting_coordinate (Coordinate):The resting position of the motor when alpha = 0 and beta = 0 in the global coordinate system..
        min_coordinate (BoundryCoordinate): The minimum boundary position the motor can reach in the global coordinate system..
        max_coordinate (BoundryCoordinate): The maximum boundary position the motor can reach in the global coordinate system..
        phi: (float): The phi angle (between the frame and the base) of the motor (default is 0).
        name (str): A name or identifier for the motor (default is None).

    Methods:
        move(coordinate: Coordinate) -> None
            Moves the motor to the specified coordinate if it is within the valid boundaries.
            If the specified coordinate is outside the boundaries, a MotorOutOfBoundry exception is raised.

    Raises:
        MotorOutOfBoundry: Raised when the specified coordinate is outside the valid boundaries.

    """

    coordinate: Coordinate
    resting_coordinate: Coordinate
    min_coordinate: BoundryCoordinate
    max_coordinate: BoundryCoordinate
    phi: float = 0
    name: str = None

    def move(self, coordinate: Coordinate):
        """
        Move the motor to the specified coordinate.

        This method moves the motor to the given coordinate if it falls within the
        defined boundaries. If the coordinate is outside the allowed range, a
        MotorOutOfBoundry exception is raised.

        Parameters:
            coordinate (Coordinate): The target coordinate to move the motor to.

        Raises:
            MotorOutOfBoundry: If the target coordinate is outside the valid range.
        """
        if coordinate.is_smaller_than(
            self.max_coordinate
        ) and self.coordinate.is_greater_than(self.min_coordinate):
            self.coordinate = coordinate
        else:
            raise MotorOutOfBoundry(
                f"{self.name} can not go to x={coordinate.x},y={coordinate.y},z={coordinate.z}.\n"
                f"Min-Boundry: x={self.min_coordinate.x},y={self.min_coordinate.y},z={self.min_coordinate.z}\n"
                f"Max-Boundry: x={self.max_coordinate.x},y={self.max_coordinate.y},z={self.max_coordinate.z}\n"
            )


class MotorY(Motor):
    """
    A class representing a Y-axis motor.

    This class inherits from the Motor class and provides additional methods to move
    the motor along the Y-axis and adjust its position based on a given angle.

    Calculation see "Doc"

    Attributes:
        name (str): The name of the Y-axis motor.
        coordinate (Coordinate): The current position of the Y-axis motor.
        min_coordinate (Coordinate): The minimum allowed coordinate for the Y-axis motor.
        max_coordinate (Coordinate): The maximum allowed coordinate for the Y-axis motor.
        phi (float): The current phi-angle (in degrees) of the Y-axis motor relative to its resting position in the global CS.

    Methods:
        move_y_by_delta(delta_y: float) -> None
            Move the motor along the Y-axis by the given delta_y value.

        move_to_phi(phi: float) -> None
            Move the motor to the specified angle (phi) relative to its resting position.
    """

    def move_to_new_y(self, new_y: float) -> None:
        """
        Move the Motor Y (FE-Movment) along the y-axis by a specified delta y.

        This method calculates a new coordinate by adjusting the y-coordinate of the current
        position by the given delta_y. It then calls the 'move' method to move the motor to
        the new coordinate if it falls within the defined boundaries.

        Calculation see "Doc"

        Parameters:
            new_y (float): The amount to move the motor along the y-axis.

        Returns:
            None
        """
        new_coordinate = Coordinate(
            x=self.coordinate.x,
            y=new_y,
            z=self.coordinate.z,
            description=self.coordinate.description,
        )
        self.move(new_coordinate)

    def move_to_phi(self, phi: float) -> None:
        """
        Move the motor to a specified 'phi' angle.

        This method calculates the amount to move the motor along the y-axis ('new_y')
        based on the desired 'phi' angle provided. It then calls the 'move_to_new_y'
        method to move the motor by the calculated 'new_y' value. Additionally, the 'phi'
        attribute of the motor is updated to the provided angle.

        Parameters:
            phi (float): The desired 'phi' angle (in degrees) to move the motor to.

        Returns:
            None
        """
        new_y = self.resting_coordinate.z * math.tan(utils.deg2rad(phi))
        self.move_to_new_y(new_y)
        self.phi = phi


class MotorX(Motor):
    """
    MotorX class extends the Motor class for a motor in x (RU) direction.

    Attributes:
        hand_base_coordinate (Coordinate): The hand base coordinate of the motor.
        yz_resting_coord (Optional[Coordinate]): The resting coordinate in the yz-plane.

    Methods:
        yz_resting_coordinate() -> Coordinate:
            Get the resting coordinate in the yz-plane. If the yz_resting_coord attribute is None,
            it calculates the yz resting coordinate based on the current coordinate and returns it.

        __init__(*args, **kwargs):
            Initialize the MotorX instance. It checks if the hand base coordinate and resting coordinate
            are in the same axis and raises a ValueError if they are not.

        zy_coordinate() -> Coordinate:
            Get the yz-coordinate representation in the xz-plane of the current MotorX instance (depending on phi).

        move_to_phi(phi: float) -> None:
            Move the MotorX instance to the given phi angle.

        move_to_beta(beta: float, alpha) -> None:
            Move the MotorX instance to the given beta angle. (Note: Implementation is missing.)

        get_frame() -> List[Coordinate]:
            Get a list of four coordinates representing a square arch-like frame.
    """

    hand_base_coordinate: Coordinate = Coordinate.hand_base_coordinate()
    yz_resting_coord: Optional[Coordinate] = None

    @property
    def yz_resting_coordinate(self) -> Coordinate:
        """
        Get the resting coordinate in the yz-plane.

        If the yz_resting_coord attribute is None, it calculates the yz resting coordinate
        based on the current coordinate and returns it.

        Returns:
            Coordinate: The resting coordinate in the yz-plane.
        """
        if self.yz_resting_coord is None:
            self.yz_resting_coord = self.coordinate
        return self.yz_resting_coord

    def __init__(self, *args, **kwrags):
        """
        Initialize the MotorX instance.

        It checks if the hand base coordinate and resting coordinate are in the same axis
        and raises a ValueError if they are not.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwrags)
        if self.hand_base_coordinate.x != self.resting_coordinate.x:
            raise ValueError(
                "hand base coordinate and resting coordinate must be in the same axis"
            )

        if self.hand_base_coordinate.y != self.resting_coordinate.y:
            raise ValueError(
                "hand base coordinate and resting coordinate must be in the same axis"
            )

    def zy_coordinate(self) -> Coordinate:
        """
        Get the projection of the Position (depending on phi) onto the x-z plane

        Returns:
            Coordinate: The projection of the y-z Plane onto the x-z plane.
        """
        new_y = self.resting_coordinate.z * math.sin(utils.deg2rad(self.phi))
        new_z = self.resting_coordinate.z * math.cos(utils.deg2rad(self.phi))

        return Coordinate(
            x=0,
            y=new_y,  # Projection of the movement in y-z Plane (Flexion)
            z=new_z,  # Projection of the movement in y-z Plane (Flexion)
            description="zy coordinate",
        )

    def move_to_phi(self, phi: float) -> None:
        """
        Move the MotorX to the given phi angle.

        Args:
            phi (float): The phi angle to move to.
        """
        self.phi = phi
        new_coordinate = self.zy_coordinate()
        new_coordinate.x = self.coordinate.x
        self.move(new_coordinate)

    def move_to_beta(self, beta: float, alpha) -> None:
        """
        Move the MotorX instance to the given beta angle.

        Args:
            beta (float): The beta angle to move to.
            alpha: (float): The alpha angle.
        """

        # Alte Version: Bevor das Kardangelenk eingebaut wurde
        # l1 = (
        #     self.resting_coordinate.z
        #     - self.hand_base_coordinate.z
        #     - HAND_HEIGHT * math.cos(utils.deg2rad(beta))
        # )
        # delta_x = HAND_HEIGHT * math.sin(utils.deg2rad(beta)) + l1 * math.tan(
        #     utils.deg2rad(beta)
        # )

        # Anpassung für Kardangelenk
        l1 = self.resting_coordinate.z - self.hand_base_coordinate.z - Z_K
        new_x = l1 * math.tan(utils.deg2rad(beta))
        new_coordinate = Coordinate(
            x=new_x,
            y=self.coordinate.y,
            z=self.coordinate.z,
            description=self.coordinate.description,
        )
        self.move(new_coordinate)

    def get_frame(self):
        """
        Get a list of four coordinates representing a square arch-like frame.

        Returns:
            List[Coordinate]: A list of `Coordinate` objects representing the frame points.
        """
        return [
            Coordinate(
                x=X_MIN,
                y=0,
                z=0,
            ),
            Coordinate(
                x=X_MIN,
                y=self.coordinate.y,
                z=self.coordinate.z,
            ),
            Coordinate(
                x=X_MAX,
                y=self.coordinate.y,
                z=self.coordinate.z,
            ),
            Coordinate(
                x=X_MAX,
                y=0,
                z=0,
            ),
        ]
