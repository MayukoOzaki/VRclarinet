import numpy as np
import matplotlib.pyplot as plt
import cv2


def make_pattern(shape=(16, 16)):
    return np.random.uniform(0, 1, shape)


pattern = make_pattern((400, 400))
plt.imshow(pattern, cmap='gray')
plt.show()


