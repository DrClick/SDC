**Traffic Sign Recognition** 

**Build a Traffic Sign Recognition Project**

The goals / steps of this project are the following:
* Load the data set (see below for links to the project data set)
* Explore, summarize and visualize the data set
* Design, train and test a model architecture
* Use the model to make predictions on new images
* Analyze the softmax probabilities of the new images
* Summarize the results with a written report


[//]: # (Image References)

[image1]: ./project_2_class_breakdown_by_set.png "Visualization"
[image2_before]: ./before_pipeline.png "before pipeline"
[image2_after]: ./after_pipeline.png "after pipeline"
[image3]: ./examples/random_noise.jpg "Random Noise"
[image4]: ./from_web/german_50.jpg "Traffic Sign 1"
[image5]: ./from_web/german_bumpy_road.jpg "Traffic Sign 2"
[image6]: ./from_web/german_no_passing.jpg "Traffic Sign 3"
[image7]: ./from_web/german_roundabout_mandatory.jpg "Traffic Sign 4"
[image8]: ./from_web/german_wild_animals_Crossing.jpg "Traffic Sign 5"

You're reading it! and here is a link to my [project code](https://github.com/DrClick/SDC/blob/master/sdc/project_2/carND-TSCP/Traffic_Sign_Classifier-Copy2.ipynb)

****Data Set Summary & Exploration

* The size of training set is 115430
* The size of the validation set is 4410
* The size of test set is 12630
* The shape of a traffic sign image is 32x32
* The number of unique classes/labels in the data set is 43

####2. Include an exploratory visualization of the dataset.

Here is an exploratory visualization of the data set showing class representation by data set

![alt text][image1]

***Design and Test a Model Architecture

As a first step, I decided to try and balance underrepresented classes by upsampling them randomly and applying a small rotation to the images to create new samples. I then corrected the image for Y channel as a lot of images were two dark for even human readability. I then applied Contrast Limited Adaptive Histogram Equalization and finally normalized the data for zero mean and values between small values 

Number of training examples after augmentation is = 115430

****before images
![alt text][image2_before]

****after images
![alt text][image2_after]




***2. Model Architecture

My final model consisted of the following layers:

| Layer         		|     Description	        					| 
|:---------------------:|:---------------------------------------------:|
|Layer 1----------------------------------------|
| Input         		     | 32x32x3 RGB image   							| 
| Convolution 3x3     	| 1x1 stride, valid padding, outputs 30x30x16 	|
| RELU	|	|
| Max pooling	      	  | 2x2 stride,  outputs 15x15x16 				|
| Dropout | .75 keep training only| 
|Layer 2----------------------------------------|
| Convolution 3x3	     | 1x1 stride, valid padding, outputs 13x13x32   |
| RELU||
| Max pooling          | 2x2 stride, outputs 6x6x32   |
| Dropout | .75 keep training only| 
|Layer 3----------------------------------------|
| flatten              | outputs 1152|
| Layer 4----------------------------------------|
| Fully connected		| outputs 120        									|
| RELU|
| Dropout | .75 keep training only| 
| Layer 5----------------------------------------|
| Fully connected		| outputs 43        									|
| RELU|
| Dropout | .75 keep training only| 
| Softmax				|      									|

| L2 regularization for each fully connected layer and bias|
 


####3. Describe how you trained your model. The discussion can include the type of optimizer, the batch size, number of epochs and any hyperparameters such as learning rate.

To train the model, I used a momentum optimizer, with a batch size of 128 over 50 epochs. 

####4. Describe the approach taken for finding a solution and getting the validation set accuracy to be at least 0.93. Include in the discussion the results on the training, validation and test sets and where in the code these were calculated. Your approach may have been an iterative process, in which case, outline the steps you took to get to the final solution and why you chose those steps. Perhaps your solution involved an already well known implementation or architecture. In this case, discuss why you think the architecture is suitable for the current problem.

My final model results were:
* training set accuracy of ?
* validation set accuracy of ? 
* test set accuracy of ?

If an iterative approach was chosen:
I started with the base lenet architecture and realized I needed a bit more. I encrased the number of convolutions significantly, added more neurons to the fully connected layers and added dropout. Additionally I went with a progressive learning rate. The dropout layers really helped to learn redundate representations and combat overfitting. I basically started with lenet and tweaked it with experience and intuition

###Test a Model on New Images


Here are five German traffic signs that I found on the web:

![alt text][image4] ![alt text][image5] ![alt text][image6] 
![alt text][image7] ![alt text][image8]

Here are the results of the prediction:

| Image			        |     Prediction	        					| 
|:---------------------:|:---------------------------------------------:| 
| Stop Sign      		| Stop sign   									| 
| U-turn     			| U-turn 										|
| Yield					| Yield											|
| 100 km/h	      		| Bumpy Road					 				|
| Slippery Road			| Slippery Road      							|


The model was able to correctly guess 4 of the 5 traffic signs, which gives an accuracy of 80%. This compares favorably to the accuracy on the test set of ...

####3. Describe how certain the model is when predicting on each of the five new images by looking at the softmax probabilities for each prediction. Provide the top 5 softmax probabilities for each image along with the sign type of each probability. (OPTIONAL: as described in the "Stand Out Suggestions" part of the rubric, visualizations can also be provided such as bar charts)

The code for making predictions on my final model is located in the 11th cell of the Ipython notebook.

For the first image, the model is relatively sure that this is a stop sign (probability of 0.6), and the image does contain a stop sign. The top five soft max probabilities were

| Probability         	|     Prediction	        					| 
|:---------------------:|:---------------------------------------------:| 
| .60         			| Stop sign   									| 
| .20     				| U-turn 										|
| .05					| Yield											|
| .04	      			| Bumpy Road					 				|
| .01				    | Slippery Road      							|


For the second image ... 

### (Optional) Visualizing the Neural Network (See Step 4 of the Ipython notebook for more details)
####1. Discuss the visual output of your trained network's feature maps. What characteristics did the neural network use to make classifications?

