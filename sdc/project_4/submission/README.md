Advanced Lane Finding Project
---
The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

---
### Camera Calibration

#### 1. Briefly state how you computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image.

The code for this step is contained in the in an this [ipython notebook](https://github.com/DrClick/SDC/blob/master/sdc/project_4/submission/camera_calibration.ipynb)

I start by preparing "object points", which will be the (x, y, z) coordinates of the chessboard corners in the world. Here I am assuming the chessboard is fixed on the (x, y) plane at z=0, such that the object points are the same for each calibration image.  Thus, `objp` is just a replicated array of coordinates, and `objpoints` will be appended with a copy of it every time I successfully detect all chessboard corners in a test image.  `imgpoints` will be appended with the (x, y) pixel position of each of the corners in the image plane with each successful chessboard detection.  

I then used the output `objpoints` and `imgpoints` to compute the camera calibration and distortion coefficients using the `cv2.calibrateCamera()` function.  I applied this distortion correction to the test image using the `cv2.undistort()` function and obtained this result: 
<table>
  <tr><td>Original</td><td>Undistorted</td></tr>
  <tr>
  <td><img src="https://raw.githubusercontent.com/DrClick/SDC/master/sdc/project_4/submission/camera_calibration_distorted.jpg" width="420" /></td>
  <td><img src="https://raw.githubusercontent.com/DrClick/SDC/master/sdc/project_4/submission/camera_calibration_undistorted.jpg" width="420" /></td></tr>
</table>

### Pipeline (single images)

#### 1. Provide an example of a distortion-corrected image.

This is the original image and the undistorte image. Its hard to tell in this perspective, but if you look carefully you can see the fisheye effet is removed. Look at how straight the left line looks in comparison.

https://raw.githubusercontent.com/DrClick/SDC/master/sdc/project_4/cnd-all/output_images/pipeline_undistorted.jpg
<table>
  <tr><td>Original</td><td>Undistorted</td></tr>
  <tr>
  <td><img src="https://raw.githubusercontent.com/DrClick/SDC/master/sdc/project_4/cnd-all/test_images/straight_lines1.jpg" width="420" /></td>
  <td><img src="https://raw.githubusercontent.com/DrClick/SDC/master/sdc/project_4/cnd-all/output_images/pipeline_undistorted.jpg" width="420" /></td></tr>
</table>

#### 2. Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image.  Provide an example of a binary image result.

I used a combination of color and gradient thresholds to generate a binary image. The following images are from a particularlly tricky section of the road. They combination of filters is as follows:

    binary[((x_threshold == 1) | (y_threshold == 1) | (c_threshold == 1)) & (d_threshold == 1)] = 1
    
This code can be found in lines 22-110 in the LanePositionDetector class in [project pipeline](https://github.com/DrClick/SDC/blob/master/sdc/project_4/submission/project_pipeline.ipynb)
    
<table>
  <tr><td>Undistorted</td><td>Binary Threshlolded</td></tr>
  <tr>
  <td><img src="https://raw.githubusercontent.com/DrClick/SDC/master/sdc/project_4/cnd-all/output_images/pipeline_undistorted.jpg" width="420" /></td>
  <td><img src="https://raw.githubusercontent.com/DrClick/SDC/master/sdc/project_4/cnd-all/output_images/pipeline_binary_2.jpg" width="420" /></td></tr>
</table>



#### 3. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.

Creating the birds image is done with the cv2 function as follows:
```python
warped = cv2.warpPerspective(binary, self.M, self.img_size, flags=cv2.INTER_LINEAR )
```

I hand picked my source and destination points in order to focus on the section of the image I felt I could
best predict at for this image size :


| Source        | Destination   | 
|:-------------:|:-------------:| 
| 600, 450      | 300,100       |
| 680,450       | 940,100       |
| 300,700       | 300,700       |
| 940,700       | 940,700       |

I verified that my perspective transform was working as expected by drawing the `src` and `dst` points onto a test image and its warped counterpart to verify that the lines appear parallel in the warped image.The yellow points are the source, the blue the destination.

<table>
  <tr><td>Base Image</td><td>Warped Image</td></tr>
  <tr>
  <td><img src="https://raw.githubusercontent.com/DrClick/SDC/master/sdc/project_4/cnd-all/output_images/pipeline_points.png" width="420" /></td>
  <td><img src="https://raw.githubusercontent.com/DrClick/SDC/master/sdc/project_4/cnd-all/output_images/pipeline_warped_raw.png" width="420" /></td>
  </tr>
  <tr>
  <td colspan="2"><h4>Binary and warped image </h4>
  <img src="https://raw.githubusercontent.com/DrClick/SDC/master/sdc/project_4/cnd-all/output_images/pipeline_warped_binary.jpg" width="800" /></td>
  </tr>
</table>

#### 4. Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial?

From here, I now have pixels that are either on or off. I looked at the bottom 1/3 of the image to identify where the majority of pixals are: This can be show on a histogram here. I smoothed this to denoise and picked the highest peak on the left and right half of the image as a starting point for the search for lane line pixels.

```python
def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n
```
<img src="https://raw.githubusercontent.com/DrClick/SDC/master/sdc/project_4/cnd-all/output_images/pipeline_smooth_histogram.png" width="800" />

Once I have these points to start from. I created a sliding window that looks for points. I collect this pixels I find "on" and then fit a curve to this. The code for can be found in the `historgram_search_lane_lines` and `confident_lane_search` methods of the `LanePositionDetector` class in the [project pipeline](https://github.com/DrClick/SDC/blob/master/sdc/project_4/submission/project_pipeline.ipynb)
    
<table>
  <tr><td>Sliding Window Search</td><td>Targeted Window Last Curve</td></tr>
  <tr>
  <td><img src="https://raw.githubusercontent.com/DrClick/SDC/master/sdc/project_4/cnd-all/output_images/pipeline_sliding_window_search.png" width="420" /></td>
  <td><img src="https://raw.githubusercontent.com/DrClick/SDC/master/sdc/project_4/cnd-all/output_images/pipeline_targeted_search.png" width="420" /></td></tr>
</table>


#### 5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

In order to calculate the curvature of the road and the current offset. I first calculated the curvature in pixel space and then transformed the curvature into worldspace. Using the equation of the line for each lane marking, I calculte the X position of both lines. From there I can find the offset of the camera to the center of the image(assuming the camera is positioned in the middle of the car). This code is can be found in the `calc_curvature` method of the Line object and the `update` method of the `LanePositionDetector`.

#### 6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

Generating the output image is simply creating a polygon to fit the curves of the lef and right lines and applying the inverse transform "warping" matrix we did to get the birds_eye image in previous steps. This code is avaialble in the `draw_lane` method of the `LanePositionDector` object

<img src="https://raw.githubusercontent.com/DrClick/SDC/master/sdc/project_4/cnd-all/output_images/pipeline_final.png" width="800" />

---

### Pipeline (video)

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).

<iframe width="560" height="315" src="https://www.youtube.com/embed/EedjZb1Q5cs" frameborder="0" allowfullscreen></iframe>

---

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?
My pipeline will fail on really curvy roads, and roads that are not well defined. I also tried this approach on my self driving RC car track with limited success. I actually think computer vision is a problematic approach to this problem and  its much better suited to Neural Networks. This being said, how could the pipeline be imporved. 
1) Using a Kalman filter for each new frame to update the belief of the lane lines. 
2) Using genetic algorithm to tune the parameters of the filters based on road conditions. Use this to find the optimum filter parameters in a variety of road/lighting conditions. Then a simple NN could be used to detect the current lighting/road situation and apply the best filter parameters to the image for detection.