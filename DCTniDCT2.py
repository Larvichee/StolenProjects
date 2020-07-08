import math
import imageio
import datetime
import numpy as np

from scipy.fftpack import dct, idct

image = imageio.imread('sample.png')

size = 256

_in = np.array(image)
_out = np.array([[0.0]*size]*size, dtype='f')
_out2 = np.array([[0.0]*size]*size, dtype='f')

def dct_1d(array, a_size):
    array1 = np.array(array)
        
    array3 = np.ones(a_size)
    array3[0] = 1/math.sqrt(2)
    array3 = array3 * (2/a_size)**0.5
    output = np.zeros(a_size)
    for i in range(a_size):
        array2 = np.zeros(a_size)
        for j in range(a_size):
            array2[j] = math.cos( (i * math.pi / a_size) * (j + 1/2))
        output[i] = np.dot(array1, array2) 
    output = np.multiply(output, array3)
    return output

#assume array is a_size by a_size
def dct2d_partial(array, a_size):
    output = np.zeros([a_size,a_size])    

    array3 = np.ones(a_size)
    array3[0] = 1/math.sqrt(2)
    array3 = array3 * (2/a_size)**0.5

    arrays2 = np.zeros([a_size,a_size])
    for j in range(a_size):
        for k in range(a_size):
            arrays2[j][k] = math.cos( (j * math.pi / a_size) * (k + 1/2))
    
    for i in range(a_size):
        if i % 16 == 15:
            print(i)
        
        output1 = np.zeros(a_size)
        for j in range(a_size):
            output1[j] = np.dot(array[i], arrays2[j]) 
        output[i] = np.multiply(output1, array3)

##    for i in range(a_size):            
##        output[i] = dct_1d(array[i], a_size)
    return output

def dct2d(array, a_size):
    inter = dct2d_partial(array, a_size)
##    print("Now transpose")
    inter2 = dct2d_partial(np.transpose(inter), a_size)
    return inter2

def idct_1d(array, a_size):
    array1 = np.array(array)
    array3 = np.ones(a_size)
    array3[0] = 1/math.sqrt(2)
    array3 = array3 * math.sqrt(2/a_size)
    output = np.zeros(a_size)

    for i in range(a_size):
        array2 = np.zeros(a_size)
        for j in range(a_size):
            array2[j] = math.cos( (j * math.pi / a_size) * (i + 1/2))
        output[i] = np.dot(np.multiply(array3, array1), array2)
    return output
    
def idct2d_partial(array, a_size):
    output = np.zeros([a_size,a_size])

    array3 = np.ones(a_size)
    array3[0] = 1/math.sqrt(2)
    array3 = array3 * math.sqrt(2/a_size)

    arrays2 = np.zeros([a_size,a_size])
    for i in range(a_size):
        for j in range(a_size):
            arrays2[i][j] = math.cos( (j * math.pi / a_size) * (i + 1/2))
    
    for i in range(a_size):
        if i % 16 == 15:
            print(i)
        output1 = np.zeros(a_size)
        for j in range(a_size):
            output1[j] = np.dot(array[i], arrays2[j]) 
            output[i][j] = np.dot(np.multiply(array3, array[i]), arrays2[j])
##        array_r = array[i]
##        output_r = idct_1d(array_r, a_size)
##        for j in range(a_size):
##            output[i][j] = output_r[j]
    return output

def idct2d(array, a_size):
    inter = idct2d_partial(array, a_size)
##    print("Now transpose")
    inter2 = idct2d_partial(np.transpose(inter), a_size)
    return inter2

##_out3 = np.load("dct_r.npy")
##
##print(1, datetime.datetime.now())
##first = dct2d(_in, size)
##second = idct2d(first, size)
##print(2, datetime.datetime.now())
##imageio.imwrite('sample_out.jpg', second[:, :])
