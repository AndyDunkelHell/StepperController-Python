# Configuration module[¶](#module-configuration "Link to this heading")
In this Module the variables required for Configuration of the FreeMove Python 2.5 Project are defined.

    # Distant in Neutral Position in
    MOTOR_FE_Z0 = 168  # alpha = 0
    MOTOR_RU_Z0 = 380  # beta = 0
    HAND_BASE_Z_DIST = 150  # Distance between the global z=0 and the Base of the Hand
    HAND_HEIGHT = 200  # Distance between the Hand Base and the Universal Joint
    Z_K = 50  # Distance between the Universal Joint and the Motor
    Y_MIN = -321  # MotorY (FE) Movement Boundry
    Y_MAX = 321  # MotorY (FE) Movement Boundry
    X_MIN = -165  # Motorx (RU) Movement Boundry
    X_MAX = 253  # Motorx (RU) Movement Boundry

    # Init Position
    ALPHA_INIT = 0  # Init FE Angle
    BETA_INIT = 0  # Init RU Angle

    # Flexion/Extension
    ALPHA_FE_MIN = -30  # Range for FE Angle
    ALPHA_FE_MAX = 45  # Range for FE Angle

    # Radial/Ulnar
    BETA_RU_MIN = -10  # Range for RU Angle
    BETA_RU_MAX = 35  # Range for RU Angle

    # Movement
    DELTA_THETA = 5  # Steps for Angle calculation with the Range
    SPEED_PER_THETA = 1  # Angular Speed
