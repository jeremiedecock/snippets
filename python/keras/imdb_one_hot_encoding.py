#!/usr/bin/env python3
# coding: utf-8

# IMDB Classification with "one-hot" vector encoding

# Source: https://gricad-gitlab.univ-grenoble-alpes.fr/talks/fidle/-/blob/master/IMDB/01-One-hot-encoding.ipynb

from tensorflow import keras
import numpy as np

vocab_size           = 5000  # we use only the `vocab_size` most frequent words
hide_most_frequently = 0     # we delete the `hide_most_frequently` most used words (a, the, ...) because they do not carry any meaning

epochs               = 10
batch_size           = 512

# Prepare the data ############################################################

# IMDb dataset can bet get directly from Keras (see https://www.tensorflow.org/api_docs/python/tf/keras/datasets).
# 
# Note : Due to their nature, textual data can be somewhat complex.
# 
# Data structure :
# 
# The dataset is composed of 2 parts: 
# - reviews, this will be our x
# - opinions (positive/negative), this will be our y
# 
# There are also a dictionary, because words are indexed in reviews
# 
# <dataset> = (<reviews>, <opinions>)
# 
# with :  <reviews>  = [ <review1>, <review2>, ... ]
#         <opinions> = [ <rate1>,   <rate2>,   ... ]   where <ratei>   = integer
# 
# where : <reviewi> = [ <w1>, <w2>, ...]    <wi> are the index (int) of the word in the dictionary
#         <ratei>   = int                   0 for negative opinion, 1 for positive
# 
# <dictionary> = [ <word1>:<w1>, <word2>:<w2>, ... ]
# 
# with :  <wordi>   = word
#         <wi>      = int
#
# 
# For simplicity, we will use a pre-formatted dataset (see https://www.tensorflow.org/api_docs/python/tf/keras/datasets/imdb/load_data).
# However, Keras offers some usefull tools for formatting textual data (see https://www.tensorflow.org/api_docs/python/tf/keras/preprocessing/text).
# 
# By default: 
# - Start of a sequence will be marked with : 1
# - Out of vocabulary word will be : 2
# - First index will be : 3


(x_train, y_train), (x_test, y_test) = keras.datasets.imdb.load_data(num_words=vocab_size, skip_top=hide_most_frequently)

y_train = np.asarray(y_train).astype('float32')
y_test  = np.asarray(y_test ).astype('float32')

# When we loaded the dataset, we asked for using \<start\> as 1, \<unknown word\> as 2.
# So, we shifted the dataset by 3 with the parameter index_from=3

# Retrieve dictionary {word:index}, and encode it in ascii
word_index = keras.datasets.imdb.get_word_index()

# Shift the dictionary from +3
word_index = {w:(i+3) for w,i in word_index.items()}

# Add <pad>, <start> and <unknown> tags
word_index.update( {'<pad>':0, '<start>':1, '<unknown>':2, '<undef>':3,} )

# Create a reverse dictionary : {index:word}
index_word = {index:word for word, index in word_index.items()} 

# Add a nice function to transpose
def dataset2text(review):
    return ' '.join([index_word.get(i, '?') for i in review])

# Print a review example

x = x_train[12]
print(x)
print(dataset2text(x))

# One Hot encoding ############################################################

# Each sentence is encoded with a vector of length equal to the size of the dictionary.
# Each sentence will therefore be encoded with a simple vector.
# The value of each component is 0 if the word is not present in the sentence or 1 if the word is present.
# For a sentence s=[3,4,7] and a dictionary of 10 words, we will have a vector v=[0,0,0,1,1,0,0,1,0,0,0]

def one_hot_encoder(x, vector_size):

    # Set all to 0
    x_encoded = np.zeros((len(x), vector_size))

    # For each sentence
    for i,sentence in enumerate(x):
        for word in sentence:
            x_encoded[i, word] = 1.

    return x_encoded

x_train = one_hot_encoder(x_train, vector_size=vocab_size)
x_test  = one_hot_encoder(x_test,  vector_size=vocab_size)


# Build the model #############################################################

model = keras.Sequential()
model.add(keras.layers.Input( shape=(vocab_size,) ))
model.add(keras.layers.Dense( 32, activation='relu'))
model.add(keras.layers.Dense( 32, activation='relu'))
model.add(keras.layers.Dense( 1, activation='sigmoid'))

model.compile(optimizer = 'adam',
              loss      = 'binary_crossentropy',
              metrics   = ['accuracy'])

model.summary()


# Train the model #############################################################

print("\n# Fit", "#" * (80-5), "\n")
model.fit(x_train,
          y_train,
          epochs          = epochs,
          batch_size      = batch_size,
          validation_data = (x_test, y_test))


# Evaluate the trained model ##################################################

print("\n# Evaluate", "#" * (80-12), "\n")
score = model.evaluate(x_test, y_test, verbose=0)

print(f"Test loss: {score[0]}")
print(f"Test accuracy: {score[1]}\n")


# Predict an example ##########################################################

for i in range(5):
    print("# Predict", "#" * (80-12), "\n")
    prediction = model.predict(x_test[i:i+1])

    print(f"\nPredicted raw output: {prediction}")

    print(f"Predicted class: {prediction.round()}")
    print(f"Actual class: {y_test[i]}\n")