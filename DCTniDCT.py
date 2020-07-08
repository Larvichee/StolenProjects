import math
import numpy as np

#Lambda function for coefficient
def lambda_n(x):
    if x == 0 :
        return 1/math.sqrt(2)
    else:
        return 1

#Summation part of 1d DCT
def summ_ct_1d(array, a_size, n):
    summ = sum(map(lambda x: array[x] * math.cos( (n * math.pi / a_size) * (x + 1/2)), range(a_size)))
    return summ

#DCT 1d function
def dct_1d(array, a_size):
    def mini_map(i):
        return (2/a_size)**0.5 * lambda_n(i) * summ_ct_1d(array, a_size , i)
    
    output = list(map(mini_map, range(a_size)))
    return output

#DCT 1d function on an array of arrays
def dct2d_partial(array, a_size):
    output = np.array(np.zeros([a_size,a_size]))
    for i in range(a_size):
        if i % 16 == 15:
            print("1d dct progress : %d/%d" % (i+1,a_size))
        output[i] = dct_1d(array[i], a_size)
    return output

#DCT 2d function
def dct2d(array, a_size):
    inter = dct2d_partial(array, a_size)
    print("Progress : 50%")
    inter2 = dct2d_partial(np.transpose(inter), a_size)
    print("Progress : 100%")
    return np.transpose(inter2)

#Summation part of 1d iDCT 
def summ_ict_1d(array, a_size, n):
    summ = sum(map(lambda x: lambda_n(x) * array[x] * math.cos( (x * math.pi / a_size) * (n + 1/2)), range(a_size)))
    return summ

#iDCT 1d function
def idct_1d(array, a_size):
    def mini_map(i):
        return math.sqrt(2/a_size) * summ_ict_1d(array, a_size , i)

    output = list(map(mini_map, range(a_size)))
    return output

#iDCT 1d function on an array of arrys    
def idct2d_partial(array, a_size):
    output = np.array(np.zeros([a_size,a_size]))
    for i in range(a_size):
        if i % 16 == 15:
            print("1d idct progress : %d/%d" % (i+1,a_size))
        array_r = array[i]
        output_r = idct_1d(array_r, a_size)
        for j in range(a_size):
            output[i][j] = output_r[j]
    return output

#iDCT 2d function
def idct2d(array, a_size):
    inter = idct2d_partial(array, a_size)
    print("Progress : 50%")
    inter2 = idct2d_partial(np.transpose(inter), a_size)
    print("Progress : 100%")
    return np.transpose(inter2)
