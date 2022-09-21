import numpy as np
import discorpy.losa.loadersaver as io
import discorpy.proc.processing as proc
import discorpy.post.postprocessing as post

# Load image
file_path = "C:/data/demo/perspective_demo.jpg"
output_base = "./for_demo_07/"
mat = io.load_image(file_path, average=False)

# Provide the coordinates of 4-points. They can be in xy-order or yx-order, this info
# needs to be consistent with other functions. In this example, it's in the xy-order.
list_points = [[180, 1920], [1500, 1602], [2754, 2430], [942, 3246]]

# Generate undistorted points. Note that the output coordinate is in the yx-order.
s_points, t_points = proc.generate_4_source_target_perspective_points(
    list_points, input_order="xy", scale="mean", equal_dist=False)

# Calculate distortion coefficients
list_coef = proc.calc_perspective_coefficients(s_points, t_points,
                                               mapping="backward")
# Apply correction.
mat_cor = np.zeros_like(mat)
for i in range(mat_cor.shape[-1]):
    mat_cor[:, :, i] = post.correct_perspective_image(mat[:, :, i], list_coef)
io.save_image(output_base + "/corrected_image.jpg", mat_cor)

# The region of interest may be out of the field of view or rotated.
# We can rotate the output image, offset, and scale it by changing the target
# points as follows:

rotate_angle = 35.0
x_offset = 2600
y_offset = -1000
scale = 1.5

# Apply rotating
x = t_points[:, 1]
y = t_points[:, 0]
a = np.deg2rad(rotate_angle)
x_rot = x * np.cos(a) - y * np.sin(a)
y_rot = x * np.sin(a) + y * np.cos(a)

# Apply scaling
x_rot = x_rot * scale
y_rot = y_rot * scale

# Apply translating
x_rot = x_rot + x_offset
y_rot = y_rot + y_offset

# Update target points
t_points2 = np.asarray(list(zip(y_rot, x_rot)))

# Calculate coefficients
list_coef2 = proc.calc_perspective_coefficients(s_points, t_points2, mapping="backward")
# Correct the image.
mat_cor = np.zeros_like(mat)
for i in range(mat_cor.shape[-1]):
    mat_cor[:, :, i] = post.correct_perspective_image(mat[:, :, i], list_coef2, order=3)
io.save_image(output_base + "/adjusted_image.jpg", mat_cor)
print("!!! Done !!!")