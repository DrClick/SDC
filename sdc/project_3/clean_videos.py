import csv
from matplotlib import pyplot as plt
import numpy as np
from scipy.misc import imread
import pickle

# this file is used to process the raw output of recording training data from the simulator
# and prepare it for uploading to the AWS GPU

folder_to_process = "track_2_train_6"
print("Processing ", folder_to_process)


def extract_data(folder):
    # images
    X_center = []
    X_left = []
    X_right = []

    XX = [] #senor data (aka speed in this case)

    # steering angle
    y_center = []
    y_left = []
    y_right = []

    with open('DATA/{}/driving_log.csv'.format(folder)) as f:
        reader = csv.reader(f)

        for line in reader:
            img_file_center = line[0].split('/')[-1]
            img_file_left = line[1].split('/')[-1]
            img_file_right = line[2].split('/')[-1]

            X_center.append(imread('DATA/{}/IMG/{}'.format(folder, img_file_center)))
            X_left.append(imread('DATA/{}/IMG/{}'.format(folder, img_file_left)))
            X_right.append(imread('DATA/{}/IMG/{}'.format(folder, img_file_right)))

            XX.append([float(line[6]),0,0])

            y_center.append([float(line[3]), float(line[4])])
            y_left.append([float(line[3]) + .12, float(line[4])])
            y_right.append([float(line[3]) - .12, float(line[4])])

    return (np.array(X_center), np.array(X_left), np.array(X_right), np.array(XX),
            np.array(y_center), np.array(y_left), np.array(y_right))


X_train_C, X_train_L, X_train_R, XX_train, y_train_C, y_train_L, y_train_R = extract_data(folder_to_process)


# reduce image to the road section.
X_train_C = X_train_C[:,60:140,:]
X_train_R = X_train_R[:,60:140,:]
X_train_L = X_train_L[:,60:140,:]



# the following section was used to scrub through the video and find bad sections and remove them
current_frame = 0
scroll_rate = 5


print("Current Frame: ", current_frame)
plt.figure(figsize=(16, 8))
plt.subplot(3,1,1)
plt.imshow(X_train_L[current_frame])
plt.title("L: " + str(y_train_L[current_frame]))

plt.subplot(3,1,2)
plt.imshow(X_train_C[current_frame])
plt.title("C: " + str(y_train_C[current_frame]))

plt.subplot(3,1,3)
plt.imshow(X_train_R[current_frame])
plt.title("R: " + str(y_train_R[current_frame]))
current_frame += scroll_rate



data_frames_to_drop = []
## DATA 1
# data_frames_to_drop = [(0,120), (1045, 1090),(1980,1205) , (2180,2195)]

## data 2
#data_frames_to_drop = [(60,105),(120,150), (200,215), (230,325), (580,615),(850,870),(920, 960), (2450, 2348)]
## data 3
# data_frames_to_drop = [(0,80), (160, 190), (215,310), (600,750)]

## data 4
# data_frames_to_drop = [(85,135),(295,320), (665,680), (1985, 1195), 
#                        (1385,1480), (1695,1670), (1855,1915),(1085, 2035), 
#                       (2395, 2425), (3395,3445)]


clean_indicies = np.ones(len(X_train_C))
for r in data_frames_to_drop:
    clean_indicies[r[0]:r[1]] = 0


# In[67]:

X_cleaned_L = X_train_L[clean_indicies.astype(np.bool)]
y_cleaned_L = y_train_L[clean_indicies.astype(np.bool)]
X_cleaned_C = X_train_C[clean_indicies.astype(np.bool)]
y_cleaned_C = y_train_C[clean_indicies.astype(np.bool)]
X_cleaned_R = X_train_R[clean_indicies.astype(np.bool)]
y_cleaned_R = y_train_R[clean_indicies.astype(np.bool)]


# In[68]:

X_train = np.vstack([X_cleaned_L, X_cleaned_C, X_cleaned_R])
XX_train = np.vstack([XX_train, XX_train, XX_train])
y_train = np.vstack([y_cleaned_L, y_cleaned_C, y_cleaned_R])


# In[69]:

print(X_train.shape, XX_train.shape, y_train.shape)


# In[70]:

data = {
    "images": X_train,
    "sensors": XX_train,
    "steering_throttle": y_train
}
with open('driving_{}.pkl'.format(folder_to_process,folder_to_process), 'wb') as f:
    pickle.dump(data, f)
