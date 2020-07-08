import imageio
from DCTniDCT import dct2d,idct2d
import numpy as np
import matplotlib.pyplot as plt

image_source = 'sample.png'

image = imageio.imread(image_source)
_in = np.array(image)
size = image.shape[0]

first = dct2d(_in, size)
second = idct2d(first, size)
imageio.imwrite('sample_out.jpg', second[:, :])
print("Image has been successfully run through DCT and iDCT")

##first_special = np.zeros([size,size])
##first_special[0:size//2, 0:size//2] = first[size//2:,size//2:]
##first_special[0:size//2, size//2:] = first[size//2:,0:size//2]
##first_special[size//2:, 0:size//2] = first[0:size//2:,size//2:]
##first_special[size//2:, size//2:] = first[0:size//2,0:size//2]

plt.figure(200)
plt.imshow(np.log(np.abs(first)), cmap='gray')
plt.colorbar()
plt.figure(300)
plt.imshow(second, cmap='gray')
plt.show()
