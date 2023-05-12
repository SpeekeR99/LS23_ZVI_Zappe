# Edge Detection in Images

This project implements an application for edge detection in images using various methods.


## Introduction

This project focuses on implementing several edge detection methods in images, including:

*   Detection in a defined direction
*   Maximum gradient direction
*   Mask methods (Prewitt, Sobel, Robinson, Kirsch, Roberts)
*   Laplacian operator
*   Line and point detection (using Hough transform)
*   Canny edge detector
*   Marr-Hildreth edge detector

## Implemented Methods

The following edge detection methods are implemented:

*   **Detection in Defined Direction:** Uses masks (Sobel, Prewitt, Roberts) to detect edges in horizontal, vertical, or both directions.
*   **Maximum Gradient Direction:** Computes the gradient vector and its maximum value in each pixel, with options for forward, backward, or central difference.
*   **Mask Methods:** Allows users to define custom masks of sizes 2x2, 3x3, or 5x5 for edge detection.
*   **Laplacian Operator:** Implemented with options for 4-neighborhood and 8-neighborhood.
*   **Line and Point Detection:**
    *   Line detection uses the Probabilistic Hough Transform via OpenCV.
    *   Point detection uses a normalized Laplacian mask with a user-adjustable threshold.
*   **Canny Edge Detector:** Implemented in two ways:
    *   A custom implementation involving Gaussian blur, gradient calculation, non-maximum suppression, and double thresholding.
    *   Using the optimized OpenCV implementation.
*   **Marr-Hildreth:** Applies the Laplacian of Gaussian (LoG) operator and detects edges based on zero crossings.

## Implementation Details

The application is written in Python and uses the following libraries:

*   numpy
*   opencv-python
*   imgui\[glfw]
*   wxPython

The main script is `main.py`.

### Graphical User Interface

The GUI is built using Dear ImGui, with wxWidgets used for file dialogs. It provides the following menu options:

*   **File:** New project, open image(s), save image(s), exit.
*   **Edit:** Edge detection, blurring, thresholding.
*   **Settings:** Window size and color style.
*   **About:** Displays information about the application.

### Image Preprocessing and Postprocessing

The application includes functions for:

*   **Blurring:** Uses a Gaussian kernel with a user-defined size.
*   **Thresholding:** Allows manual threshold selection or Otsu's thresholding method.

### Edge Detection Methods

Each edge detection operation creates a new modal window that keeps track of the history of applied operations in its title. Collision detection is implemented to avoid naming conflicts when saving results.

## Experiments and Results

Experiments were performed on a Windows 10 Home PC with an AMD Ryzen 5 4600H 3.00 GHz processor, 16 GB RAM, and an NVIDIA GeForce GTX 1660 Ti graphics card.  The "Lenna" image (512x512 pixels) was used as the primary test image. (See results in original document)

The custom Canny implementation took approximately 5.25 seconds to process the test image, while the OpenCV implementation took only 0.003 seconds, due to the optimized C++ implementation in OpenCV.

## Requirements

*   Python 3.x
*   Libraries: numpy, opencv-python, imgui\[glfw], wxPython

## Usage

1.  Install the required Python libraries using pip:

    ```
    pip install numpy opencv-python imgui[glfw] wxPython
    ```

2.  Run the `main.py` script.

    ```
    python main.py
    ```

3.  Use the GUI to load images, apply edge detection methods, and save the results.
