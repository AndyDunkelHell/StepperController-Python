# utils module[¶](#module-utils "Link to this heading")

## `alpha2phi()`

    utils.alpha2phi(r: float, a: float, alpha: float) → float

Calculates the phi angle based on the given alpha angle, the base
coordinate (a), and the resting coordinate (r).

Args:

- r (float): The resting coordinate. 
- a (float): The base coordinate. 
- alpha (float): The alpha angle.

Returns:

- float: The phi angle.

Note:

- This function is used in the "move_to_alpha" function in the
"engine.py" module to calculate the phi angle before moving the
motors and updating the hand's alpha angle.

## `deg2rad()`

    utils.deg2rad(deg: float) → float

Converts an angle in degrees to radians.

Args:

- deg (float): The angle in degrees.

Returns:

- float: The angle in radians.

## `rad2deg()`

    utils.rad2deg(rad: float) → float

Converts an angle in radians to degrees.

Args:

- rad (float): The angle in radians.

Returns:

- float: The angle in degrees.