Vehicle Detection Project (CAR / NOT A CAR)
----------------------

<img src="https://raw.githubusercontent.com/DrClick/SDC/master/sdc/project_5/resources/car_and_not_a_car.png"/>

The goals / steps of this project are the following:

* Perform a Histogram of Oriented Gradients (HOG) feature extraction on a labeled training set of images and train a classifier Linear SVM classifier
* Optionally, you can also apply a color transform and append binned color features, as well as histograms of color, to your HOG feature vector. 
* Note: for those first two steps don't forget to normalize your features and randomize a selection for training and testing.
* Implement a sliding-window technique and use your trained classifier to search for vehicles in images.
* Run your pipeline on a video stream (start with the test_video.mp4 and later implement on full project_video.mp4) and create a heat map of recurring detections frame by frame to reject outliers and follow detected vehicles.
* Estimate a bounding box for vehicles detected.

### Histogram of Oriented Gradients (HOG)

#### 1. Explain how (and identify where in your code) you extracted HOG features from the training images.

The training data for my classifier came from [cars](https://s3.amazonaws.com/udacity-sdc/Vehicle_Tracking/vehicles.zip) and [not a car](https://s3.amazonaws.com/udacity-sdc/Vehicle_Tracking/non-vehicles.zip), all of which are normalized to 64x64px images. No pre-processing is done before the pipeline.


I started by reading in all the `vehicle` and `non-vehicle` images.  Here is an example of one of each of the `vehicle` and `non-vehicle` classes:
<table style="margin: 0 auto 0 auto;">
  <tr>
    <td colspan="2">CAR / NOT A CAR</td>
  </tr>
  <tr>
    <td><img src="https://raw.githubusercontent.com/DrClick/SDC/master/sdc/project_5/output_images/example_car.png"></td>
    <td><img src="https://raw.githubusercontent.com/DrClick/SDC/master/sdc/project_5/output_images/example_notacar.png"></td>
  </tr>
</table>




I then explored different color spaces and different `skimage.hog()` parameters (`orientations`, `pixels_per_cell`, and `cells_per_block`).  I grabbed random images from each of the two classes and displayed them to get a feel for what the `skimage.hog()` output looks like.

Here is an example using the `HLS` color space and HOG parameters of `orientations=9`, `pixels_per_cell=(4, 4)` and `cells_per_block=(2, 2)`:


<img src="https://raw.githubusercontent.com/DrClick/SDC/master/sdc/project_5/resources/hog_of_car_and_not_a_car.png">

#### 2. Explain how you settled on your final choice of HOG parameters.

I tried various combinations of parameters and eventually decided on this combination as it seems to give the best results empericaly to my classifier and the final detection. There is plenty of room for further research / literature review in this area.

#### 3. Describe how (and identify where in your code) you trained a classifier using your selected HOG features (and color features if you used them).

I trained a rbf SVM using an an `auto` Gamma and C=10 which I found using Grid search. Which you can find in cells 8-15. The accuracty of my classifer is 98.6% and here are some example predictions:

<img src="https://raw.githubusercontent.com/DrClick/SDC/master/sdc/project_5/resources/predictions.png">
### Sliding Window Search

#### 1. Describe how (and identify where in your code) you implemented a sliding window search.  How did you decide what scales to search and how much to overlap windows?

I created scaled images to try and detect the cars as early as possible. Because this technique is slow, I only searched the right half of the image for this project (Clearly, this can be expanded for a real implementation. My windows varried in size from 256px to 64px. For each window, I would extract the image, and rescale to 64x64px and run in through the featurizer/predict pipeline in parallel. 

Here is the overlay of all of my search windows and the results of a raw search on an image.

<img src="https://raw.githubusercontent.com/DrClick/SDC/master/sdc/project_5/resources/search_boxes.png">

#### 2. Show some examples of test images to demonstrate how your pipeline is working.  What did you do to optimize the performance of your classifier?

Ultimately I searched on five scales using HLS L-channel HOG features plus LS and SV histograms of color in the feature vector, which provided a nice result.  Here are some example images:

<img src="https://raw.githubusercontent.com/DrClick/SDC/master/sdc/project_5/resources/detected_cars.png">
---

### Video Implementation

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (somewhat wobbly or unstable bounding boxes are ok as long as you are identifying the vehicles most of the time with minimal false positives.)

<a href="http://www.youtube.com/watch?feature=player_embedded&v=olke-bTAEr8
" target="_blank"><img src="http://img.youtube.com/vi/olke-bTAEr8/0.jpg" 
alt="IMAGE ALT TEXT HERE" width="800" border="0" /></a>



#### 2. Describe how (and identify where in your code) you implemented some kind of filter for false positives and some method for combining overlapping bounding boxes.

In order to filter false positives and to create a smoother bounding box. I took several steps.
1. Created a heatmap of the detected windows. Where each window adds "heat" to the pixels it covers
2. Combine the last 3 frames to get the combined heat over three frames
3. Threshold this heatmap imperically at 20 (meaning, it would take a total of 20 windows over 3 frames to register as a car.)
4. Use `scipy.ndimage.measurements.label` to extract lables and bounding boxes for the "islands" of pixels in the heatmap (where each island reprsents a car)

Here are examples of the steps:
* Heatmap: You can see the region for the two cars distinctly
<img src="https://raw.githubusercontent.com/DrClick/SDC/master/sdc/project_5/resources/heatmap.png">
Inspecting this histogram of the heatmap is the basis for my `20` threshold for heat
<img src="https://raw.githubusercontent.com/DrClick/SDC/master/sdc/project_5/resources/histogram_heatmap.png">
* Thresholding heatmap
<img src="https://raw.githubusercontent.com/DrClick/SDC/master/sdc/project_5/resources/heatmap_thresholding.png">

---

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

Much could be done. In order for this system to be useful in realtime. It has to be completely overhauled. I think is was a valuable exercise to see where we have come from as these techniques are widely known and not state of the art. To be trulely useful, car not a car, would hve to be trained for all otehr objects of interest and would not work in real time. If more time permitted, I would have liked to experiment in that field and I will probably revisit this and other projects! All of these projects have been implemented in my own self driving car RC car project which you can see whippig around my office here: 

<a href="http://www.youtube.com/watch?feature=player_embedded&v=OcFY8DKpTGc
" target="_blank"><img src="http://img.youtube.com/vi/OcFY8DKpTGc/0.jpg" 
alt="IMAGE ALT TEXT HERE" width="800" border="0" /></a>


