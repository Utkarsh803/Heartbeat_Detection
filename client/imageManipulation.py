# returns the 3 separate colour channels of the image
import cv2
from scipy import signal


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
    signal.detrend(colour_signal, -1, 'linear', 0, True)
    return colour_signal
