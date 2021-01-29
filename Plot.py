import os
import matplotlib.pyplot as plt

from datetime import datetime

class Plot:
    def __init__(self, freqs, data):
        self.H_FREQUENCY = 1420405000
        self.c_speed = 299792.458
        self.freqs = freqs
        self.data = data

    def plot(self, ra, dec):
        start_freq = self.freqs[0]
        stop_freq = self.freqs[-1]
        SNR, doppler = self.SNR_and_doppler()
        name = f'ra={ra}, dec={dec}, SNR={SNR}, doppler={doppler}'

        fig, ax = plt.subplots(figsize=(12,7))
        ax.plot(self.freqs, self.data, color = 'g', label = 'Observed data')

        # Plots theoretical H-line frequency
        ax.axvline(x = self.H_FREQUENCY, color = 'r', linestyle = ':', label = 'Theoretical frequency')
        
        # Sets axis labels and adds legend & grid
        ylabel ='Signal to noise ratio (SNR) / dB'
        xlabel = 'Frequency / Hz'
        ax.set(title = name, xlabel = xlabel, ylabel = ylabel)
        ax.set(xlim = [start_freq, stop_freq])
        ax.legend(prop = {'size': 8})
        ax.grid()

        # Adds top x-axis for doppler
        # TODO Correct doppler from galactical coordinates
        doppler = ax.secondary_xaxis('top', functions =(self.doppler_from_freq, self.freq_from_doppler))
        doppler.set_xlabel('Doppler / km/h')
        
        # Saves plot
        path = f'./Spectrums/{name}.png'
        plt.savefig(path, dpi = 300)
        plt.close()


    # Returns highest SNR and doppler of the highest peak    
    def SNR_and_doppler(self):
        SNR = max(self.data)
        SNR_index = list(self.data).index(SNR)
        doppler = self.doppler_from_freq(self.freqs[SNR_index])
        return round(SNR, 3), round(doppler, 0)


    # Returns doppler from frequency
    def doppler_from_freq(self, freq):
        diff_freq = freq - self.H_FREQUENCY
        v_doppler = self.c_speed*diff_freq/self.H_FREQUENCY
        return v_doppler
    

    # Returns frequency from doppler
    def freq_from_doppler(self, doppler):
        diff_freq = doppler*self.H_FREQUENCY/self.c_speed
        freq = diff_freq+self.H_FREQUENCY
        return freq

