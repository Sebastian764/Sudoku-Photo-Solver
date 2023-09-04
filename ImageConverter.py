import numpy as np
# import matplotlib.pyplot as plt
import tensorflow as tf


def imagesToGrid(boardCell):

    if boardCell is None:
        raise Exception("Invalid grid")
    
    res = [[None for _ in range(9)] for _ in range(9)]

    model = tf.keras.models.load_model('digitsSafe.h5')


    threshold = 10*255 # at most 10 
    for i in range(9):
        for j in range(9):
            tmp = np.copy(boardCell[i][j])

            #Checking if the board cell is empty or not
            finsum = 0
            for k in range(28):
                rowsum = sum(tmp[k])
                finsum += rowsum
            if finsum < threshold:
                res[i][j] = 0
            else: # only gets executed if cell is not mostly empty
                # try:
                img = tmp
                img = np.array([img])
                prediction = model.predict(img)
                # print(f"This digit is probably {np.argmax(prediction)}"
                res[i][j] = np.argmax(prediction)

    return res




