import numpy as np
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Flatten, Dropout, Lambda
from keras.layers.convolutional import Convolution2D
from keras.layers.pooling import MaxPooling2D
import pickle

# load data
X_train = []
y_train = []
drives = ['driving_track_1_train_1.pkl',
          'driving_track_1_train_2.pkl',
          'driving_track_1_train_3.pkl',
          'driving_track_2_train_4.pkl',
          'driving_track_2_train_5.pkl',
          'driving_track_2_train_6.pkl']

for drive in drives:
    with open(drive, 'rb') as f:
        data = pickle.load(f)

    # load the images and steering angles
    X_train.extend(data['images'])
    y_train.extend(data['steering_throttle'].astype(np.float64))

    # flip the images and invert the steering angle to augment the data
    X_train.extend(np.array([np.fliplr(x) for x in data['images']]))
    y_train.extend(np.negative(data['steering_throttle'].astype(np.float64)))

X_train = np.array(X_train)
y_train = np.array(y_train)[:, [0]]


def create_model():
    model = Sequential()

    # preprocess
    model.add(Lambda(lambda x: x / 255.0 - 0.5, input_shape=(80, 320, 3)))

    # conv1 layer
    model.add(Convolution2D(32, (5, 5)))
    model.add(MaxPooling2D((2, 2)))
    model.add(Activation('relu'))

    # conv2 layer
    model.add(Convolution2D(64, (5, 5)))
    model.add(MaxPooling2D((3, 3)))
    model.add(Activation('relu'))

    # conv3 layer
    model.add(Convolution2D(128, (3, 3)))
    model.add(MaxPooling2D((2, 2)))
    model.add(Activation('relu'))

    # conv4 layer
    model.add(Convolution2D(128, (3, 3)))
    model.add(MaxPooling2D((2, 2)))
    model.add(Activation('relu'))

    # add fully connected layers
    model.add(Flatten())  # Flatten input image

    # fc1
    model.add(Dense(1024))
    model.add(Dropout(0.5))
    model.add(Activation('relu'))

    # fc2
    model.add(Dense(128))
    model.add(Dropout(0.5))
    model.add(Activation('relu'))

    # fc2
    model.add(Dense(64))
    model.add(Dropout(0.5))
    model.add(Activation('relu'))

    model.add(Dense(1))  # output layer with 1 regression value
    model.compile(loss="mse", optimizer="adam")

    return model


# create the model
model = create_model()

# train the network
history = []
for i in range(30):
    h = model.fit(X_train, y_train, shuffle=True, epochs=3, validation_split=.2, batch_size=64)
    history.append(h)
    model.save("data_model_deeper{}.h5".format(i))
