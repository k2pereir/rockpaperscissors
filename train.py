import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import tensorflow as tf
import pandas as pd 
import numpy as np 
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from tf_keras.models import Sequential 
from tf_keras.layers import Dense, Dropout

from tensorflow.python.keras.engine import data_adapter
def _is_distributed_dataset(ds):
    return isinstance(ds, data_adapter.input_lib.DistributedDatasetSpec)
data_adapter._is_distributed_dataset = _is_distributed_dataset

#load data 
rock = pd.read_csv('./data/rock_extended.csv', header=None)
rock['label'] = 0
paper = pd.read_csv('./data/paper_extended.csv', header=None)
paper['label'] = 1
scissors = pd.read_csv('./data/scissors_extended.csv', header=None)
scissors['label'] = 2
print("success in loading")

#combine data 
all_data = pd.concat([rock, paper, scissors], axis=0)
print("combined")

#shuffle data 
all_data = shuffle(all_data)
print("shuffled")

#split into features and labels 
landmarks = all_data.iloc[:, :-1].values 
labels = all_data['label'].values
print("split first")

#normalize landmarks 
landmarks = landmarks / np.max(np.abs(landmarks), axis=0)
print("normalized")

#split into training and testing data 
X_train, X_test, y_train, y_test = train_test_split(landmarks, labels, test_size=0.33, random_state=42)
print("nice and split")

#build model 
model = Sequential(
    [
        Dense(128, activation="relu", input_shape=(X_train.shape[1],)),
        Dropout(0.2),
        Dense(64, activation="relu"),
        Dense(3, activation="softmax"),
    ]
)
print("model built")

#using scce because rock, paper, and scissors are mutually exclusive classses
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
print("model complied")

#train and evaluate model 
history = model.fit(landmarks, labels, epochs=20, batch_size=32, validation_split=0.2)
test_loss, test_acc = model.evaluate(X_test, y_test)

#save model
model.save('rps_model/my_model')
print("saved!!")