"""Learn a dictionary from MNIST digits
"""

import sklearn.datasets
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import random
import util
import time
import numpy as np

from sklearn.decomposition import MiniBatchDictionaryLearning
from sklearn.decomposition import DictionaryLearning
from sklearn.feature_extraction.image import extract_patches_2d
from sklearn.feature_extraction.image import reconstruct_from_patches_2d

# Load MNIST digits
data = sklearn.datasets.fetch_mldata('MNIST original')
X = data.data  # (n_examples, n_features)
n_examples, n_features = X.shape

# Sample from digits
sample_size = 1000
sample = X[random.sample(range(n_examples), sample_size), :]
#sample = sample.reshape(-1, 28, 28)

patches = sample
np.random.shuffle(patches)
patch_size = (28, 28)

minibatch_kwargs = {
        'n_components': 100,
        'alpha': 1.,
        }
dico = MiniBatchDictionaryLearning(**minibatch_kwargs)
print('Learning the dictionary with')
for key, value in minibatch_kwargs.items(): print('\t', key, value)

def display_components(V):
    plt.figure(figsize=(4.2, 4))

    patches = [row.reshape(patch_size) for row in V]
    canvas = util.tile(patches)
    plt.imshow(canvas, interpolation='nearest', cmap=cm.gray)
    plt.title('Dictionary learned from Lena patches\n' +
                 'Train time %.1fs on %d patches' % (dt, len(patches)),
                 fontsize=16)

batch_size = 10
for bi in range(len(patches) // batch_size):
    t0 = time.time()
    curr_patches = patches[bi * batch_size: (bi+1) * batch_size]
    dico.n_iter = 1
    V = dico.partial_fit(curr_patches).components_
    dt = time.time() - t0

display_components(V)

plt.show()
