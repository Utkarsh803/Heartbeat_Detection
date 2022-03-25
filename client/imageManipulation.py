# returns the 3 separate colour channels of the image
import cv2
import numpy as np
from scipy import signal
from scipy.fftpack import fft, fftshift


def rgb_split(img):
    red_channel = img[:, :, 2]
    blue_channel = img[:, :, 0]
    green_channel = img[:, :, 1]

    return red_channel, green_channel, blue_channel


# returns the average values of the separate colour channels
def calc_avg_rgb(img):
    red_ch, green_ch, blue_ch = rgb_split(img)

    red = 0
    blue = 0
    green = 0
    count = 0

    for i in range(red_ch.shape):
        for j in range(red_ch.shape[i]):
            red = red + red_ch[i][j]
            blue = blue + blue_ch[i][j]
            green = green + green_ch[i][j]
            count = count + 1

    red = red / count
    blue = blue / count
    green = green / count

    return red, green, blue


def sum_rgb_val(red, green, blue):
    return red + green + blue


def detrend_signal(colour_signal):
    new_signal = signal.detrend(colour_signal)
    return new_signal


def hamming_window(detr_signal):
    window = signal.hamming(len(detr_signal))
    data = np.zeros(len(detr_signal))
    for i in range(len(detr_signal)):
        data[i] = detr_signal[i] * window[i]
    return data
