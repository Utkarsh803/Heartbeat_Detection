# returns the 3 separate colour channels of the image
import cv2
import numpy as np
from scipy import signal
import neurokit2 as nk
from scipy.fftpack import fft, fftshift
from sklearn.decomposition import FastICA
import statistics
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


def calc_avg_col(img):
    """
    this function returns the average colour value of the image or frame

    :param img: takes in an image or frame of video
    :return: the average value of the three colour channels
    """
    if img is None:
        return 0

    red_ch, green_ch, blue_ch = rgb_split(img)

    col = 0
    count = 0

    for i in range(len(red_ch)):
        for j in range(len(red_ch[i])):
            col = col + red_ch[i][j] + blue_ch[i][j] + green_ch[i][j]
            count = count + 3

    if count == 0:
        return 0

    avg = col / count

    return col


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
    row0 = colour_signal[0]
    row1 = colour_signal[1]
    row2 = colour_signal[2]

    new_signal0 = nk.signal_detrend(row0, order=0, method="loess", alpha=1, window=0.059)
    new_signal1 = nk.signal_detrend(row1, order=0, method="loess", alpha=1, window=0.059)
    new_signal2 = nk.signal_detrend(row2, order=0, method="loess", alpha=1, window=0.059)

    return new_signal0, new_signal1, new_signal2


def detrend_signal(colour_signal):
    """
    this function returns the detrended signal over a time period T which will be used to calculate the heart rate
    it is done using a simple detrending library


    :param colour_signal: this is an array of averaged colour values over a time period
            it is a 2d array of the 3 colour channels
    :return: this returns the detrended signal (a 2d array)

    """
    # row0=colour_signal[0]
    # row1=colour_signal[1]
    # row2=colour_signal[2]
    #
    # new_signal0 = signal.detrend(colour_signal[0])
    # new_signal1 = signal.detrend(colour_signal[1])
    # new_signal2 = signal.detrend(colour_signal[2])

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
    new_data0 = ((data - data.mean()) / data.std())
    return new_data0


def removeZero(signal):
    sig0=signal[0]
    sig0.pop(0)

    sig1=signal[1]
    sig1.pop(0)
    
    sig2=signal[2]
    sig2.pop(0)
    
    rows=3
    cols=51
    new_array = [[0]*cols]*rows
    new_array=[sig0,sig1,sig2]
    
    
    return new_array



def hamming_window(detr_signal):
    """
    this function returns the detrended average colour signal after being passed through a hamming window
    in order to reduce the error of the signal to get a more accurate original signal

    :param detr_signal: this is the detrended signal
    :return: the signal after being passed through a hamming window
    """

    window = signal.hamming(len(detr_signal[0]))
    data = [detr_signal[0] * window, detr_signal[1] * window, detr_signal[2] * window]
    return data


def ica(data):
    ica = FastICA(n_components=3)
    ica_signal = ica.fit_transform(data)
    return ica_signal


def bandpassFilter(data, freq=[0.7, 4.5], window='hamming'):
    filt_signal = signal.firwin(128, freq, window=window, pass_zero=False, scale=False)
    return signal.lfilter(filt_signal, 1, data)


def select_component(components):
    largest_psd_peak = -1e10
    best_component = None
    for i in range(components.shape[1]):
        x = components[:, i]
        x = bandpassFilter(x, freq=[0.7, 4.5], window='hamming')
        f, psd = signal.periodogram(x)
        if max(psd) > largest_psd_peak:
            largest_psd_peak = max(psd)
            best_component = components[:, i]
    return x


def fft(data):
    fft_signal = np.fft.rfft(data, n=8 * len(data))
    return fft_signal


def get_means(subframe):
    v1 = np.mean(subframe[:, :, 2])
    v2 = np.mean(subframe[:, :, 0])
    v3 = np.mean(subframe[:, :, 1])
    return v1, v2, v3


def normalize(data):
    new_data = data - data.mean(axis=0) / data.std(axis=0)
    return new_data


def hamming(sig):
    window = signal.hamming(len(sig))
    data = sig * window
    return data


def calc_frequency(signal):
    fft_sig = fft(signal)

    threshold = 0.5 * max(abs(fft_sig))
    freq = fft.fftfreq(len(fft_sig))
    mask = abs(fft_sig) > threshold
    peaks = freq[mask]
    return


def calc_HR(sig):
    print("--signal--", sig)
    dtr_sig = signal.detrend(sig)
    print(dtr_sig)
    norm_sig = z_normalize(dtr_sig)
    print(norm_sig)
    interpolated = np.hamming(len(norm_sig)) * norm_sig
    print(interpolated)
    fft = np.fft.rfft(interpolated, n=8 * len(interpolated))
    print(signal)
    peaks = signal.find_peaks(fft)
    freq = (len(peaks[0]) / (50 / 30))
    return 60 * freq
