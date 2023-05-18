# **Image Processing Code Explanation**

## **Shear Image**

The **`shear_image`** function performs image shearing based on the provided sheared angle. Here's a breakdown of the steps:

1. The sheared angle is negated to handle the correct direction of the shear.
2. The sheared amount is converted to radians.
3. The dimension information of the image is obtained.
4. A new sheared image array is created with zeros.
5. Variables for sheared height, sheared width, mid-row, and mid-column are calculated.
6. Nested loops iterate over the width and height of the image.
7. The coordinates (x, y) are calculated for each pixel relative to the center.
8. The new coordinates (new_x, new_y) are computed by applying the shearing transformation.
9. The new coordinates are adjusted to the original coordinate system by adding the mid-row and mid-column.
10. If the new coordinates are within the valid range, the pixel value from the original image is assigned to the sheared image array.
11. The sheared image is converted to a PIL Image object.
12. The image is converted to grayscale.
13. The sheared image is displayed in the user interface.

## **Rotation**

The **`rotation`** function handles the rotation of the image based on user input. Here's a summary of the steps:

1. The function checks if the user input for the rotation angle is a valid number. If not, an error message is displayed.
2. Depending on the selected interpolation method (nearest or linear), the corresponding rotation function (`Rotation_Nearest` or `Rotation_Linear`) is called.
3. If no interpolation method is chosen, an error message is displayed.

## **Load**

The **`Load`** function loads an image file, extracts relevant information, and displays the image in the user interface. Here's an overview of the process:

1. The user is prompted to select an image file using a file dialog.
2. The file extension is checked to determine the image type (DICOM or other).
3. For DICOM files:
   - The DICOM file is read and the pixel array is extracted.
   - The pixel values are rescaled and converted to integer format.
   - The image is saved as a temporary JPEG file.
   - Information about the DICOM file (such as patient name, age, modality, etc.) is displayed in the user interface.
4. For other image types:
   - The image is loaded using the provided file path.
   - The image is converted to grayscale.
5. The image is displayed in the user interface, and relevant information about the image (width, height, color mode, bit depth, etc.) is displayed.

## **Nearest Interpolation**

The **`Nearest_Interpolation`** function performs nearest neighbor interpolation to zoom in on the image based on the provided zoom factor. Here's an overview of the steps:

1. The function retrieves the size of the grayscale image.
2. The zoom factor is checked to ensure it is a positive number.
3. The dimensions of the zoomed image are calculated by multiplying the original dimensions with the zoom factor and rounding the results.
4. A new image array is created with zeros.
5. Nested loops iterate over the dimensions of the zoomed image.
6. The row and column in the original image corresponding to the current position in the zoomed image are calculated.
7. The pixel value from the original image is assigned to the corresponding position in the new image.
8. The new image is converted to a PIL Image object and grayscale.
9. The image is displayed in the user interface.

## **Bilinear Interpolation**

The **`Bilinear_Interpolation`** function performs bilinear interpolation to zoom in on the image based on the provided zoom factor. Here's a summary of the steps:

1. The function retrieves the size of the grayscale image.
2. The zoom factor is checked to ensure it is a positive number.
3. The dimensions of the zoomed image are calculated by multiplying the original dimensions with the zoom factor and rounding the results.
4. A new image array is created with zeros.
5. Ratios for x and y interpolation are calculated.
6. Nested loops iterate over the dimensions of the zoomed image.
7. The lower and higher coordinates for interpolation are determined based on the ratios and the current position.
8. Weights for interpolation are calculated based on the differences between the lower and higher coordinates and the current position.
9. The pixel values of the four surrounding pixels in the original image are retrieved.
10. The interpolated pixel value is calculated based on the weights and the surrounding pixel values.
11. The interpolated pixel value is assigned to the corresponding position in the new image.
12. The new image is converted to a PIL Image object and grayscale.
13. The image is displayed in the user interface.


## **Rotation_Nearest function**

The **`Rotation_Nearest`** function is a method that performs nearest neighbor rotation on an image. Here's a breakdown of the code:

1. Read the rotation angle from the user interface and convert it to radians.
2. Define the dimensions of the image as `height = 128` and `width = 128`.
3. Create a blank rotated image with the same dimensions.
4. Calculate the midpoint coordinates of the rotated image.
5. Iterate over each pixel in the output image.
    - Calculate the corresponding pixel position in the input image using the rotation matrix.
    - Adjust the position by adding the offset.
    - Round the position to the nearest integer values.
    - Check if the rounded position corresponds to a valid pixel in the input image.
        - If valid, assign the pixel value from the input image to the corresponding position in the rotated image.
6. Convert the rotated image to a PIL Image object.
7. Convert the PIL Image to grayscale.
8. Update the user interface with the rotated image and relevant information.

The **`Rotation_Nearest`** function performs nearest neighbor rotation by mapping each pixel in the output image to the nearest corresponding pixel in the input image. The rotation is performed using a rotation matrix, and the resulting image is displayed in the user interface.

---

## **Rotation_Linear function**

The **`Rotation_Linear`** function is a method that performs linear interpolation rotation on an image. Here's a breakdown of the code:

1. Read the rotation angle from the user interface and convert it to radians.
2. Define the dimensions of the image as `height = 128` and `width = 128`.
3. Create a blank rotated image with the same dimensions.
4. Calculate the midpoint coordinates of the rotated image.
5. Iterate over each pixel in the output image.
    - Calculate the corresponding pixel position in the input image using the rotation matrix.
    - Adjust the position by adding the offset.
    - Perform linear interpolation to calculate the pixel value at the non-integer positions.
    - Assign the interpolated pixel value to the corresponding position in the rotated image.
6. Convert the rotated image to a PIL Image object.
7. Convert the PIL Image to grayscale.
8. Update the user interface with the rotated image and relevant information.

The **`Rotation_Linear`** function performs linear interpolation rotation by calculating the weighted average of neighboring pixels to determine the pixel value at non-integer positions. This results in smoother and more accurate rotation compared to nearest neighbor interpolation.

---

## **Bi_scratch function**

The **`Bi_scratch`** function is a method that performs bi-linear interpolation rotation on an image. Here's a breakdown of the code:

1. Convert the rotation angle from degrees to radians.
2. Get the width and height of the input image.
3. Create a blank rotated image with the same dimensions.
4. Calculate the midpoint coordinates of the rotated image.
5. Iterate over each pixel in the output image.
    - Calculate the corresponding pixel position in the input image using the rotation matrix.
    - Adjust the position by adding the offset.
    - Round the position to the nearest integer values.
    - Check if the rounded position corresponds to a valid pixel in the input image.
        - If valid, perform bi-linear interpolation to calculate the pixel value at the non-integer positions.
        - Assign the interpolated pixel value to the corresponding position in the rotated image.
6. Return the rotated image.

The **`Bi_scratch`** function performs bi-linear interpolation rotation by calculating the weighted average of four neighboring pixels to determine the pixel value at non-integer positions. This interpolation technique provides smoother and higher quality results compared to nearest neighbor and linear interpolation.

##  **Histogram function**

The **`histogram`** function is a method that calculates and displays the histogram and equalized histogram of an image. Here's a breakdown of the code:

1. Initialize a list `pixels` to hold the intensity levels from 0 to 255.
2. Get the width and height of the image.
3. Calculate the total number of pixels.
4. Initialize an empty list `counts` to store the frequency of each intensity level in the image.
5. Iterate over each intensity level from 0 to 255.
    - Count the number of pixels in the image that have the current intensity level.
    - Append the frequency to the `counts` list.
6. Calculate the probability density function (pdf) by dividing each frequency by the total number of pixels.
7. Calculate the cumulative distribution function (cdf) by summing up the probabilities.
8. Map the cdf values to the range [0, 255] by multiplying them by 255 and rounding to the nearest integer.
9. Create a blank image `Equalized_image` with the same dimensions as the original image.
10. Iterate over each pixel in the image.
    - Get the intensity value of the pixel.
    - Use the mapped cdf value corresponding to the intensity value to assign a new intensity value to the pixel in the equalized image.
11. Calculate the new frequencies for the equalized histogram by counting the pixels with each intensity value in the equalized image.
12. Update the user interface with the original histogram, equalized histogram, and the original and equalized images.

The `histogram` function calculates the histogram of an image, performs histogram equalization to improve the contrast, and displays the results in the user interface.

## **Salt_and_papper**

The **`Salt_and_papper`** function adds salt and pepper noise to an image. Here's a breakdown of the code:

1. Check if the image has been loaded. If not, display an error message.
2. Get the dimensions of the grayscale image.
3. Calculate the total number of pixels in the image.
4. Convert the image to a NumPy array.
5. Randomly determine the number of pixels to add salt noise and pepper noise.
6. Add salt noise:
   - For each salt noise pixel, randomly select coordinates within the image dimensions.
   - Set the pixel value at those coordinates to 255 (white).
7. Add pepper noise:
   - For each pepper noise pixel, randomly select coordinates within the image dimensions.
   - Set the pixel value at those coordinates to 0 (black).
8. Convert the NumPy array back to a PIL Image object.
9. Convert the image to grayscale.
10. Convert the PIL Image to a QPixmap object.
11. Display the noised image in the user interface.

## **Quicksort**

The **`quicksort`** function is a recursive implementation of the quicksort algorithm. Here's a breakdown of the code:

1. Check the base case: if the length of the array is less than or equal to 1, return the array.
2. Choose the first element as the pivot.
3. Create two lists: `less` for items less than or equal to the pivot, and `great` for items greater than the pivot.
4. Use list comprehensions to populate the `less` and `great` lists based on the pivot value.
5. Recursively sort the `less` and `great` lists using the quicksort function.
6. Return the concatenation of the sorted `less`, pivot, and sorted `great` lists.

## **Median_filter**

The `median_filter` function applies a median filter to the image to remove noise. Here's a breakdown of the code:

1. Check if the image has been noised. If not, display an error message.
2. Get the desired filter size from the user interface.
3. Create an empty array `data_final` to store the filtered image data.
4. Iterate over each pixel in the image:
   - Define a temporary list `temp` to store the pixel values within the filter window.
   - Check the boundary conditions for each pixel in the filter window and handle them accordingly.
   - Append the pixel values within the filter window to the `temp` list.
   - Sort the `temp` list using the `quicksort` function.
   - Assign the median value from the `temp` list as the filtered pixel value.
5. Convert the `data_final` array to a PIL Image object.
6. Convert the image to grayscale.
7. Convert the PIL Image to a QPixmap object.
8. Display the filtered image in the user interface.

## **AddPadding**

The `addPadding` function adds padding to the image. Here's a breakdown of the code:

1. The function takes arguments `val` (padding value), `image` (input image), and `paddSize` (padding size).
2. Create a new array `resultImage` with dimensions expanded to accommodate the padding.
3. Fill the `resultImage` array with the padding value.
4. Copy the original image data to the corresponding positions in the `resultImage` array, taking into account the padding size and adjusting the coordinates.
5. Return the `resultImage` array.

## **Convolution**

The **`convolution`** function performs convolution between a filter and an image. Here's a breakdown of the code:

1. The function takes arguments `filter` (filter array) and `image` (input image array).
2. Reverse the `filter` array using the `np.flip` function.
3. Get the dimensions of the image and filter.
4. Calculate the padding size based on the filter dimensions.
5. Use the `addPadding` function to add padding to the image.
6. Iterate over each pixel in the image:
   - Define a sub-image using the filter dimensions centered around the current pixel.
   - Compute the element-wise product between the sub-image and the reversed filter.
   - Sum up the resulting values to obtain the convolved pixel value.
7. Convert the `resultImage` list to a NumPy array.
8. Return the `resultImage` array.

## **BoxFilter**

The **`boxFilter`** function applies a box filter to the image. Here's a breakdown of the code:

1. Get the desired filter size from the user interface.
2. Check if the filter size is odd. If not, display an error message.
3. Create a filter array `filter` filled with values equal to the inverse of the filter size squared.
4. Call the `convolution` function with the filter and the input image to obtain the filtered image.
5. Call the `Sharp` function to enhance the edges in the filtered image.

## **Sharp**

The `Sharp` function enhances the edges in the image. Here's a breakdown of the code:

1. Clear the scene for displaying the sharped image in the user interface.
2. Convert the input image to a NumPy array.
3. Get the dimensions of the image.
4. Remove the padding from the filtered image.
5. Compute the mask by subtracting the filtered image from the original image.
6. Get the edge factor from the user interface.
7. Multiply the mask by the edge factor.
8. Add the mask to the original image.
9. Clip the pixel values to the range [0, 255].
10. Convert the modified image to a PIL Image object.
11. Convert the image to grayscale.
12. Convert the PIL Image to a QPixmap object.
13. Display the sharped image in the user interface.

## **Original_Mag**

- This method clears the graphics scene (`self.ui.sceneoriginalMag`).
- The input grayscale image is converted to a numpy array (`Imagearray`).
- The Fourier transform of the image is calculated using `np.fft.fft2()`, and the result is shifted using `np.fft.fftshift()`.
- The magnitude spectrum of the shifted Fourier transform is calculated using `np.abs()`, and it is stored in `self.magnitudeSpectrum`.
- The magnitude spectrum is normalized to a range of [0, 255] by subtracting the minimum value, dividing by the maximum value, and scaling it.
- The normalized magnitude spectrum is converted back to an image using `PIL.Image.fromarray()` and converted to grayscale.
- The grayscale image is converted to a QPixmap and added to the graphics scene for display.

## **Logged_Mag**

- This method clears the graphics scene (`self.ui.sceneloggedMag`).
- If the magnitude spectrum is not available (`self.magnitudeSpectrum` is empty), an error message is displayed.
- The maximum pixel value in the magnitude spectrum is calculated.
- A logarithmic transformation is applied to the magnitude spectrum by scaling the values using a logarithmic formula.
- The logarithmic spectrum is normalized to a range of [0, 255].
- The normalized logarithmic spectrum is converted to an image, converted to grayscale, and added to the graphics scene for display.

## **Original_Phase**

- This method clears the graphics scene (`self.ui.sceneoriginalPhase`).
- The input grayscale image is converted to a numpy array (`Imagearray`).
- The Fourier transform of the image is calculated using `np.fft.fft2()`, and the result is shifted using `np.fft.fftshift()`.
- The phase spectrum of the shifted Fourier transform is calculated using `np.angle()`, and it is stored in `self.phaseSpectrum`.
- The phase spectrum is normalized to a range of [0, 255].
- The normalized phase spectrum is converted to an image, converted to grayscale, and added to the graphics scene for display.

## **Logged_Phase**

- This method clears the graphics scene (`self.ui.sceneloggedPhase`).
- If the phase spectrum is not available (`self.phaseSpectrum` is empty), an error message is displayed.
- The maximum value in the phase spectrum is calculated.
- A logarithmic transformation is applied to the phase spectrum by scaling the values using a logarithmic formula.
- The logarithmic spectrum is normalized to a range of [0, 255].
- The normalized logarithmic spectrum is converted to an image, converted to grayscale, and added to the graphics scene for display.

## **Blurring**

- This method performs blurring on the input grayscale image using a filter specified by the user.
- The size of the filter is obtained from the user interface (`self.ui.Filter_Size_Fourier_lineEdit.text()`).
- If the filter size is not a valid integer or is an even value, an error message is displayed.
- The blurring filter is created as a numpy array filled with equal weights.
- The blurring operation is performed by convolving the filter with the input grayscale image.
- The resulting blurred image is displayed in the graphics scene (`self.ui.sceneBlurredImage`).

## **Fourier_Filtering**

- This method performs Fourier filtering on the input grayscale image.
- The size of the filter is obtained from the user interface (`self.ui.Filter_Size_Fourier_lineEdit.text()`).
- If the filter size is not a valid integer or is an even value, an error message is displayed.
- The filter is created as a numpy array with the specified size, filled with equal weights.
- The Fourier transform of the input grayscale image is calculated, and the filter is also transformed using the Fourier transform.
- The Fourier filtering is performed by multiplying the transformed filter with the transformed image.
- The inverse Fourier transform is applied to obtain the filtered image.
- The filtered image is displayed in the graphics scene (`self.ui.sceneBlurredFourierImage`).

## **Difference()**

- Clears the scene for the difference image.
- Applies Fourier filtering to the image.
- Calculates the difference between the filtered image and the original image.
- Clips the pixel values to the range [0, 255].
- Converts the resulting image to grayscale.
- Displays the difference image.

## **notch_reject_filter(d0, u_k, v_k)**

- Creates a notch reject filter in the frequency domain.
- The filter suppresses frequencies in the vicinity of the specified notches.
- Returns the created filter.

### **Moire_Pattern()**

- Converts the grayscale image to a NumPy array.
- Performs Fourier transformation on the image.
- Creates multiple notch reject filters at different locations and sizes.
- Applies the notch reject filters to the Fourier-transformed image.
- Performs inverse Fourier transformation to obtain the filtered image.
- Converts the filtered image to grayscale.
- Displays the filtered Moire pattern image.

## **Original_ROI()**

- Creates a circular region of interest (ROI) array.
- Sets specific pixel values within and outside the circular region.
- Displays the original ROI image.

## **ROI_Noise()**

- Generates uniform noise and Gaussian noise arrays based on user-defined parameters.
- Adds the noise arrays to the ROI array.
- Clips the pixel values to the range [0, 255].
- Displays the noisy ROI image.

## **onselect_function(eclick, erelease)**

- Callback function for the rectangle selection in the Select_ROI() function.
- Records the selected extent of the rectangle.

## **Select_ROI()**

- Clears the scene and displays the noisy ROI image.
- Allows the user to select a rectangular region of interest.
- Calls the onselect_function() callback to record the selected extent.

## **ROI_Histogram()**

- Calculates the histogram of pixel intensities within the selected ROI.
- Normalizes the histogram.
- Calculates the mean and variance of the pixel intensities.
- Displays the ROI histogram and the statistics.

## **Phantom()**

- Creates a Shepp-Logan phantom image.
- Displays the phantom image.

## **Sinogram()**

- Performs the Radon transform on the phantom image.
- Displays the sinogram image.

## **Laminogram()**

- Performs the laminogram reconstruction using a strip sum approach.
- Displays the laminogram image.

## **LaminogramNoFilter()**

- Performs the laminogram reconstruction without applying any filtering.
- Displays the laminogram image.

## **LaminogramHamming()**

- Performs the laminogram reconstruction using the Hamming filter.
- Displays the laminogram image.

## **LaminogramRamlak()**

- Performs the laminogram reconstruction using the Ram-Lak filter.
- Displays the laminogram image.

## **OriginalDE()**

- Clears the scene for the original image in the erosion and dilation functions.
- Displays the original grayscale image.

## **MultBitWiseE(Mat1, Mat2)**

- Performs element-wise multiplication between two matrices, handling None values.
- Returns the resulting matrix.

## **MultBitWiseD(Mat1, Mat2)**

- Performs element-wise multiplication between two matrices, handling None values.
- Returns the resulting matrix.

## **Erosion()**

- Performs erosion on the grayscale image using a structuring element.
- Returns the eroded image.

## **DrawErosion()**

- Calls the Erosion() function to obtain the eroded image.
- Displays the eroded image.

## **Dilation()**

- Performs dilation on the grayscale image using a structuring element.
- Returns the dilated image.

## **DrawDilation()**

- Calls the Dilation() function to obtain the dilated image.
- Displays the dilated image.

## **Opening()**

- Performs the opening operation on the grayscale image using a structuring element.
- Returns the opened image.

## **DrawOpening()**

- Calls the Opening() function to obtain the opened image.
- Displays the opened image.

## **Closing()**

- Performs the closing operation on the grayscale image using a structuring element.
- Returns the closed image.

## **DrawClosing()**

- Calls the Closing() function to obtain the closed image.
- Displays the closed image.
