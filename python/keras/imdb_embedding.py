#!/usr/bin/env python3
# coding: utf-8

# IMDB Classification with "one-hot" vector encoding

# Source: https://gricad-gitlab.univ-grenoble-alpes.fr/talks/fidle/-/blob/master/IMDB/02-Keras-embedding.ipynb

from tensorflow import keras
import numpy as np

vocab_size           = 5000  # we use only the `vocab_size` most frequent words
hide_most_frequently = 0     # we delete the `hide_most_frequently` most used words (a, the, ...) because they do not carry any meaning
review_len           = 256   # review_len is the review length
dense_vector_size    = 32    # dense_vector_size is the size of the generated dense vectors

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

# Embedding ###################################################################

# In order to be processed by an NN, all entries must have the same length.
# We chose a review length of review_lenWe will therefore complete them with a padding (of \<pad\>\).

x_train = keras.preprocessing.sequence.pad_sequences(x_train,
                                                     value   = 0,
                                                     padding = 'post',
                                                     maxlen  = review_len)

x_test  = keras.preprocessing.sequence.pad_sequences(x_test,
                                                     value   = 0 ,
                                                     padding = 'post',
                                                     maxlen  = review_len)


# Build the model #############################################################

model = keras.Sequential()
model.add(keras.layers.Input( shape=(review_len,) ))
model.add(keras.layers.Embedding(input_dim    = vocab_size, 
                                 output_dim   = dense_vector_size, 
                                 input_length = review_len))
model.add(keras.layers.GlobalAveragePooling1D())
model.add(keras.layers.Dense(dense_vector_size, activation='relu'))
model.add(keras.layers.Dense(1,                 activation='sigmoid'))

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