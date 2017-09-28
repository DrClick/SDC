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
[image4]: ./from_web/german_50.jpg "[2] Speed limit (50km/h)
[image5]: ./from_web/german_bumpy_road.jpg "[22] Bumpy road"
[image6]: ./from_web/german_no_passing.jpg "[9] No passing"
[image7]: ./from_web/german_roundabout_mandatory.jpg "[40] Roundabout mandatory"
[image8]: ./from_web/german_wild_animals_Crossing.jpg "[31] Wild animals crossing"

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
|Layer 1----------------------------------------||
| Input         		     | 32x32x3 RGB image   							| 
| Convolution 3x3     	| 1x1 stride, valid padding, outputs 30x30x16 	|
| RELU	|	|
| Max pooling	      	  | 2x2 stride,  outputs 15x15x16 				|
| Dropout | .75 keep training only| 
|Layer 2----------------------------------------||
| Convolution 3x3	     | 1x1 stride, valid padding, outputs 13x13x32   |
| RELU|
| Max pooling          | 2x2 stride, outputs 6x6x32   |
| Dropout | .75 keep training only| 
|Layer 3----------------------------------------||
| flatten              | outputs 1152|
| Layer 4----------------------------------------||
| Fully connected		| outputs 120        									|
| RELU|
| Dropout | .75 keep training only| 
| Layer 5----------------------------------------||
| Fully connected		| outputs 43        									|
| RELU|
| Dropout | .75 keep training only| 
| Softmax				|      									|
| L2 regularization for each fully connected layer and bias||
 


**Model Training

To train the model, I used a momentum optimizer, with a batch size of 128 over 25 epochs. 

*Approach and Results

My final model results were:
TRAINING SET      - loss: 0.17178, acc: 0.97862, error: 2.13809
VALIDATION SET    - loss: 0.17930, acc: 0.97800, error: 2.19955
TEST SET          - loss: 0.24287, acc: 0.96548, error: 3.45210

I started with the base lenet architecture and realized I needed a bit more. I encrased the number of convolutions significantly, added more neurons to the fully connected layers and added dropout. Additionally I went with a progressive learning rate. The dropout layers really helped to learn redundate representations and combat overfitting. I basically started with lenet and tweaked it with experience and intuition.

**New examples from the web

Here are five German traffic signs that I found on the web:

![alt text][image4] ![alt text][image5] ![alt text][image6] 
![alt text][image7] ![alt text][image8]

Here are the results of the prediction:

| Image			        |     Prediction	        					| 
|:---------------------:|:---------------------------------------------:| 
| Speed limit (50km/h) | |
| Bumpy road | |
| No passing | |
| Roundabout mandatory | |
| Wild animals crossing | |


The model was able to correctly guess 3 of the 5 traffic signs, which gives an accuracy of 60%. This compares favorably to the accuracy on the test set of ...

Here are the top 5 softmax predictions for each images
(2, 'Speed limit (50km/h)')
[' 1', ' 6', ' 5', '42', ' 2'] ['10.27', '10.27', ' 6.58', ' 6.46', ' 5.73']
(22, 'Bumpy road')
['22', '25', '29', '17', ' 0'] ['44.68', '16.29', '14.42', '10.77', ' 9.35']
(9, 'No passing')
['11', '18', '41', '28', '27'] [' 7.32', ' 6.15', ' 5.01', ' 3.78', '  2.9']
(40, 'Roundabout mandatory')
['40', '38', '12', '34', '37'] ['26.13', '10.67', ' 8.85', ' 7.33', ' 7.03']
(31, 'Wild animals crossing')
['31', '21', '23', '22', '25'] ['13.82', ' 10.9', '10.03', ' 4.48', ' 4.15']

The code for making predictions on my final model is located in the 51st cell of the Ipython notebook.
