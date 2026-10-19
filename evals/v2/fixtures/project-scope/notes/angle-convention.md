# Angle convention used in our OBB pipeline

We use the le90 convention: angle θ ∈ [-90°, 90°). Boxes at exactly 90° are converted to
-90° with width/height swapped. Unit test test_angle_wrap covers 0°, 45°, 89.9°, 90° and -90°.
