import imageio
from DCTniDCT2 import dct2d,idct2d
import numpy as np
import matplotlib.pyplot as plt

image_source = 'sample.png'
image = np.array(imageio.imread(image_source))

def imcomp(im, ratio):
    im = np.array(im)
    m,n = im.shape
    out = np.zeros([m,n])

    k,l = m//8,n//8
    for i in range(k):
        for j in range(l):
            out[i*8:(i+1)*8,j*8:(j+1)*8] = dct2d(im[i*8:(i+1)*8,j*8:(j+1)*8], 8)
    outer = out.astype(np.float32)
    threshold = np.partition(np.absolute(out).flatten(), -2)[int(m*n*(1-1/ratio))]
    outer[np.abs(outer)< threshold] = 0
    outer = outer.astype(np.int32)
    return outer

def imdecomp(im):
    coeff = np.array(im)
    x,y = coeff.shape
    out2 = np.zeros([x,y])
    a,b = x//8, y//8
    for i in range(a):
        for j in range(b):
            out2[i*8:(i+1)*8,j*8:(j+1)*8] = idct2d(im[i*8:(i+1)*8,j*8:(j+1)*8], 8)
##    out2 = np.uint8(out2)
    np.clip(out2, 0, 255, out=out2)
    out2 = out2.astype('uint8')
    return out2

ratio = 10
inter11 = imcomp(image, ratio)
inter12 = imdecomp(inter11)

##np.savetxt("debug_coeff.csv", inter11)
##np.savetxt("final.csv", inter12)

imageio.imwrite('sample_new.jpg', inter12[:, :])

plt.figure(200)
plt.imshow(image, cmap='gray')
plt.colorbar()
plt.figure(300)
plt.imshow(inter12, cmap='gray')
plt.show()


########debug#########
##def counter(x):
##	if x == 0:
##		return 1
##	else:
##		return 0
##
##a = sum(map(counter, inter11.flatten()))
##b = image.shape[0] * image.shape[1]
##print("Number of zeros:", a)
##print("Number of entries:", b)
##print("Perctange:", a/b)
