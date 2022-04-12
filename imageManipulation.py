# returns the 3 separate colour channels of the image
import cv2
import numpy as np
from scipy import signal
import neurokit2 as nk
from scipy.fftpack import fft, fftshift
from sklearn.decomposition import FastICA
import statistics
from sklearn.preprocessing import normalize
from scipy.signal import savgol_filter
from sklearn.preprocessing import normalize

def rgb_split(img):
    """
    this function returns the three separated colour channels of an image or a frame

    :param img: takes in a single frame of a video stream or an image
    :return: extracts all three colour channels of the image / frame
    """
    red_channel = img[:, :, 2]
    blue_channel = img[:, :, 0]
    green_channel = img[:, :, 1]

    return red_channel, green_channel, blue_channel


# returns the average values of the separate colour channels
def calc_avg_rgb(img):
    """
    this function returns the average colour value of the image or frame

    :param img: takes in an image or frame of video
    :return: the average value of the three colour channels
    """
    red_ch, green_ch, blue_ch = rgb_split(img)

    red = 0
    blue = 0
    green = 0
    count = 0

    for i in range(len(red_ch)):
        for j in range(len(red_ch[i])):
            red = red + red_ch[i][j]
            blue = blue + blue_ch[i][j]
            green = green + green_ch[i][j]
            count = count + 1

    red = red / count
    blue = blue / count
    green = green / count
    return red, green, blue


# taking in a 2d array o fthe three colour channels rgb we calculate the mean and sd and normalise the data
def z_normalize(data):
    """
        this function nomralises the colour channels around zero

        :param data; the 3 colour channels over time t
        :return: Xi = (Yi - MUi)/SDi where i = R,G,B signal channels i.e the normalised values of the colour
                channels
        """
    #d=np.asarray_chkfinite(d)
    #norms = normalize(d, axis=1, norm='l1')
    norms = ((data - data.mean()) / data.std())
    return norms

def ica(data):
    ica = FastICA(n_components=3)
    ica_signal = ica.fit_transform(data)
    return ica_signal

def signal_smooth(signa):
    sig0=signa[0]
    sig1=signa[1]
    sig2=signa[2]

    filter_length=20
    box=np.ones((filter_length))/filter_length

    moving_avg0 = savgol_filter(sig0, 5, 3)
    moving_avg1 = savgol_filter(sig1, 5, 3)
    moving_avg2 = savgol_filter(sig2, 5, 3)
    new_array = []
    new_array=np.matrix([moving_avg0[0],moving_avg1[0],moving_avg2[0]])
    
    
    return new_array