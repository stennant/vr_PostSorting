from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
import vr_process_movement
import matplotlib.pyplot as plt


def plot_spectrogram2(prm, channel_all_data, channel):

    location = np.load(prm.get_filepath() + "Behaviour/Data/location.npy")

    channel_all_data = np.transpose(channel_all_data[0,:1000000])
    #channel_all_data = vr_process_movement.remove_beginning_and_end(prm,channel_all_data)
    fig, ax = plt.subplots()
    #plt.xlim([0, 150])
    #plt.ylim([0, 50000])
    f, t, Sxx = signal.spectrogram(channel_all_data, 30000)
    plt.pcolormesh(t, f, Sxx, cmap = 'RdBu_r')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.ylim(0,150)

    fig.savefig(prm.get_filepath() + 'Electrophysiology/spectrogram/CH' + str(channel) + '_.png', dpi=200)
    plt.close()


def plot_spectrogram1(prm, channel_all_data, channel):

    fig, ax = plt.subplots()
    #plt.xlim([0, 150])
    plt.ylim([0, 10000])
    plt.specgram(channel_all_data, NFFT=30000, Fs=30000, Fc=0, detrend=None,
         window=np.hamming(30000), noverlap=128,
         cmap=None, xextent=None, pad_to=None, sides='default',
         scale_by_freq=None, mode='default', scale='default')
    fig.savefig(prm.get_filepath() + 'Electrophysiology/spectrogram/CH' + str(channel) + '_.png', dpi=200)
    plt.close()



def plot_spectrogram3(prm, channel_all_data, channel):
    channel_all_data = np.transpose(channel_all_data[0,:100000])

    # Define the list of frequencies
    frequencies = np.arange(0,150,1)

    # Sampling Frequency
    samplingFrequency = len(channel_all_data)

    # Create two ndarrays
    s1 = np.empty([0]) # For samples
    s2 = np.empty([0]) # For signal

    # Start Value of the sample
    start = 1
    # Stop Value of the sample
    stop = samplingFrequency+1

    for frequency in frequencies:
        sub1 = np.arange(start, stop, 1) # arange same size as signal
        sub2 = channel_all_data # signal
        s1 = np.append(s1, sub1)
        s2 = np.append(s2, sub2)

        start = stop+1
        stop = start+samplingFrequency

    # Plot the signal
    plt.subplot(211)
    plt.plot(s1,s2)
    plt.xlabel('Sample')
    plt.ylabel('Amplitude')

    # Plot the spectrogram
    plt.subplot(212)
    powerSpectrum, freqenciesFound, time, imageAxis = plt.specgram(s2, Fs=samplingFrequency)
    plt.xlabel('Time')
    plt.ylabel('Frequency')
    plt.ylim([0, 150])

    #plt.subplot(313)
    #plt.pcolormesh(freqenciesFound, time, powerSpectrum, cmap = 'RdBu_r')

    plt.show()






















def plot_spectrogram(prm, channel_all_data, channel):


    data = np.transpose(channel_all_data[0,:600000])

    dt = 0.000033333333333
    t = np.arange(0.0, 20.0, dt)
    s1 = np.sin(2 * np.pi * 100 * t)
    s2 = 2 * np.sin(2 * np.pi * 400 * t)

    x = data  # the signal
    NFFT = 30000       # the length of the windowing segments
    Fs = 30000  # the sampling frequency

    t = np.arange(0.0, len(x), 1)

    # Pxx is the segments x freqs array of instantaneous power, freqs is
    # the frequency vector, bins are the centers of the time bins in which
    # the power is computed, and im is the matplotlib.image.AxesImage
    # instance

    ax1 = plt.subplot(211)
    plt.plot(t, x)
    plt.subplot(212, sharex=ax1)
    Pxx, freqs, bins, im = plt.specgram(x, NFFT=NFFT, Fs=Fs, noverlap=900)
    plt.show()
