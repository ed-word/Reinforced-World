from __future__ import division

import sys

sys.path.append('/home/hudi/anaconda2/lib/python2.7/site-packages/h5py')
sys.path.append('/home/hudi/anaconda2/lib/python2.7/site-packages/Keras-2.0.6-py2.7.egg')


import numpy as np
from numpy.random import seed, randint
from scipy.io import wavfile

from vggish import VGGish
from preprocess_sound import preprocess_sound


def get_wav_data(filename):

    seg_num = 60
    seg_len = 5
    data = np.zeros((seg_num, seg_len, 96, 64, 1))

    sr, wav_data = wavfile.read(filename)
    length = sr * seg_len
    range_high = len(wav_data) - length
    seed(1)
    random_start = randint(range_high, size=seg_num)

    for j in range(seg_num):
        cur_wav = wav_data[random_start[j]:random_start[j] + length]
        cur_wav = cur_wav / 32768.0
        cur_spectro = preprocess_sound(cur_wav, sr)
        cur_spectro = np.expand_dims(cur_spectro, 3)
        data[j, :, :, :, :] = cur_spectro

    return np.reshape(data, (-1, 96, 64, 1))


model = VGGish()

pred = model.predict(get_wav_data('1530408068357.wav'))
print(np.mean(pred, axis=0))
print(np.mean(pred, axis=0).shape)

