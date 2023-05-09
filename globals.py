import numpy as np

#  Window width
WINDOW_WIDTH = 1280
#  Window height
WINDOW_HEIGHT = 720

#  Whether to show the settings window
show_settings_window = False
#  Whether to show the about window
show_about_window = False
#  Whether to show the edge detection window
show_edge_detection_window = False
#  Whether to show the blur window
show_blur_window = False
#  Whether to show the threshold window
show_threshold_window = False
#  Whether to show the save as dialog window
show_save_as_dialog = False

#  Loaded images
imgs = {}
#  Currently selected image
current_img = 0

#  Edge detection methods
edge_detection_methods = ["Defined Direction Edge Detection", "Gradient Magnitude Direction Edge Detection",
                          "Mask Methods", "Laplacian Operator", "Line Detection", "Point Detection",
                          "Canny Edge Detection", "Canny Edge Detection (OpenCV)", "Marr-Hildreth Edge Detection"]
#  Currently selected edge detection method
current_edge_detection_method = 0
#  Kernel size for Gaussian blur
blur_kernel_size = 3
#  Whether to use Otsu threshold
otsu_threshold = False
#  Current threshold value
threshold_value = 127

#  Currently selected direction method
current_defined_direction_method = 0
#  Whether to use horizontal direction
defined_direction_horizontal = True
#  Whether to use vertical direction
defined_direction_vertical = False

#  Whether to use forward difference
forward_difference = True
#  Whether to use backward difference
backward_difference = False

#  Whether to use laplacian square or cross
laplacian_square = True

#  Current mask size
mask_size = 3
#  Default mask for size 2x2
default_mask_2 = np.array([[1, 0], [0, -1]])
#  Default mask for size 3x3
default_mask_3 = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]])
#  Default mask for size 5x5
default_mask_5 = np.array([[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, -24, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1]])
#  Currently created mask
mask_methods_kernel = default_mask_3

#  Current point detection threshold
point_detection_threshold = 240

#  Current sigma for Gaussian blur in Canny edge detection
canny_sigma = 2
#  Current lower threshold for Canny edge detection
canny_lower_thresh = 20
#  Current upper threshold for Canny edge detection
canny_upper_thresh = 50

#  Current sigma for Gaussian blur in Marr-Hildreth edge detection
marr_hildreth_sigma = 2
