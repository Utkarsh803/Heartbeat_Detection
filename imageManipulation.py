# returns the 3 separate colour channels of the image
import cv2
import numpy as np
from scipy import signal
import neurokit2 as nk
from scipy.fftpack import fft, fftshift
from sklearn.decomposition import FastICA



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
    print(red_ch)

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
    """
    :param red: the red value of an image
    :param green: the green value
    :param blue:  the blue value
    :return: the summation of all three values
    """

    return red + green + blue


def adv_detrend_signal(colour_signal):
    """
    this function returns the detrended signal over a time period T which will be used to calculate the heart rate
    it is done using an advanced detrending function with more customisable parameters

    :param colour_signal: this is an array of averaged colour values over a time period
    :return: this returns the detrended signal
    """

    new_signal = nk.signal_detrend(colour_signal, order=0, method="loess", alpha=1, window=0.059)
    return new_signal


def detrend_signal(colour_signal):
    """
    this function returns the detrended signal over a time period T which will be used to calculate the heart rate
    it is done using a simple detrending library


    :param colour_signal: this is an array of averaged colour values over a time period
            it is a 2d array of the 3 colour channels
    :return: this returns the detrended signal (a 2d array)
    """

    new_signal = signal.detrend(colour_signal)
    return new_signal

# taking in a 2d array o fthe three colour channels rgb we calculate the mean and sd and normalise the data
def z_normalize(data):
    """
        this function nomralises the colour channels around zero

        :param data; the 3 colour channels over time t
        :return: Xi = (Yi - MUi)/SDi where i = R,G,B signal channels i.e the normalised values of the colour
                channels
        """
    new_data = [((data[0] - data[0].mean(axis=0)) / data[0].std(axis=0)),
                ((data[1] - data[1].mean(axis=0)) / data[1].std(axis=0)),
                ((data[2] - data[2].mean(axis=0)) / data[2].std(axis=0))]
    return new_data

def hamming_window(detr_signal):
    """
    this function returns the detrended average colour signal after being passed through a hamming window
    in order to reduce the error of the signal to get a more accurate original signal

    :param detr_signal: this is the detrended signal
    :return: the signal after being passed through a hamming window
    """

    window = signal.hamming(len(detr_signal))
    data = np.zeros(len(detr_signal))
    for i in range(len(detr_signal)):
        data[i] = detr_signal[i] * window[i]
    return data

def ica(data):
    ica=FastICA(len(data))
    ica_signal=ica.fit_transform(data)
    return ica_signal

def bandpassFilter(data, freq=[0.7, 4.5], window='hamming'):    
    filt_signal = signal.firwin(128, freq, window=window, pass_zero=False, scale=False)
    return signal.lfilter(filt_signal, 1, data)


def select_component(components):
        largest_psd_peak = -1e10
        best_component = None
        for i in range(components.shape[1]):
            x = components[:,i]
            x = bandpassFilter(x, freq=[0.7, 4.5], window='hamming')
            #fft = np.fft.rfft(x)
            #spectrum = np.abs(fft)
            #freqs = np.linspace(0, 1.5 * 60, len(spectrum))
            f, psd = signal.periodogram(x)
            if max(psd) > largest_psd_peak:
                largest_psd_peak = max(psd)
                best_component = components[:,i]             
        return x


def fft(data):
    fft_signal = np.fft.rfft(data, n=8 * len(data))
    return fft_signal



def get_means(subframe):
    v1 = np.mean(subframe[:, :, 0])
    v2 = np.mean(subframe[:, :, 1])
    v3 = np.mean(subframe[:, :, 2])
    return (v1 + v2 + v3) / 3
