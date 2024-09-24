from typing import List
import matplotlib.pyplot as plt
import matplotlib.colors
import numpy as np


class Visualisation:
    def __init__(self) -> None:
        pass

    @staticmethod
    def chartSpectrum(wavelength, density):
        plt.plot(wavelength, density)
        plt.show()


    @staticmethod
    def wavelength_to_rgb(wavelength, gamma=0.8):
            ''' taken from http://www.noah.org/wiki/Wavelength_to_RGB_in_Python
            '''
            wavelength = float(wavelength)
            if wavelength >= 380 and wavelength <= 750:
                A = 1.
            else:
                A=0.5
            if wavelength < 380:
                wavelength = 380.
            if wavelength >750:
                wavelength = 750.
            if wavelength >= 380 and wavelength <= 440:
                attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
                R = ((-(wavelength - 440) / (440 - 380)) * attenuation) ** gamma
                G = 0.0
                B = (1.0 * attenuation) ** gamma
            elif wavelength >= 440 and wavelength <= 490:
                R = 0.0
                G = ((wavelength - 440) / (490 - 440)) ** gamma
                B = 1.0
            elif wavelength >= 490 and wavelength <= 510:
                R = 0.0
                G = 1.0
                B = (-(wavelength - 510) / (510 - 490)) ** gamma
            elif wavelength >= 510 and wavelength <= 580:
                R = ((wavelength - 510) / (580 - 510)) ** gamma
                G = 1.0
                B = 0.0
            elif wavelength >= 580 and wavelength <= 645:
                R = 1.0
                G = (-(wavelength - 645) / (645 - 580)) ** gamma
                B = 0.0
            elif wavelength >= 645 and wavelength <= 750:
                attenuation = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
                R = (1.0 * attenuation) ** gamma
                G = 0.0
                B = 0.0
            else:
                R = 0.0
                G = 0.0
                B = 0.0
            return (R,G,B,A)

    @staticmethod
    def rainbowSpectrum(wavelengths, spectrum):
        clim=(350,780)
        norm = plt.Normalize(*clim)
        wl = np.arange(clim[0],clim[1]+1,2)
        colorlist = list(zip(norm(wl),[Visualisation.wavelength_to_rgb(w) for w in wl]))
        spectralmap = matplotlib.colors.LinearSegmentedColormap.from_list("spectrum", colorlist)

        fig, axs = plt.subplots(1, 1, figsize=(8,4), tight_layout=True)

        wavelengths = [ln * 1000 for ln in wavelengths]

        plt.plot(wavelengths, spectrum, color='darkred')

        y = np.linspace(0, max(spectrum), 100)
        X,Y = np.meshgrid(wavelengths, y)

        extent=(np.min(wavelengths), np.max(wavelengths), np.min(y), np.max(y))

        plt.imshow(X, clim=clim,  extent=extent, cmap=spectralmap, aspect='auto')
        plt.xlabel('Wavelength (nm)')
        plt.ylabel('Intensity')

        plt.fill_between(wavelengths, spectrum, max(spectrum), color='w')
        plt.savefig('WavelengthColors.png', dpi=200)

        plt.show()

    @staticmethod
    def colormap(wavelangth, density):
        
        plt.xlim(min(wavelangth),max(wavelangth))
        plt.ylim(0.9,1.1)
        plt.hexbin(wavelangth, [1] * len(wavelangth) , C=density, gridsize=(len(wavelangth), 1))
        plt.show()

    @staticmethod
    def colormapAndXY(wavelangth, density):
        fig, axs = plt.subplots(ncols=1, nrows=2)
        axs[0].plot(wavelangth, density)
        axs[1].hexbin(wavelangth, [1] * len(wavelangth), C=density, gridsize=(len(wavelangth), 1))
        axs[1].set_axis_off()
        plt.tight_layout()
        plt.show()

    @staticmethod
    def typeBar(lst: List[str], count):
        plt.bar(lst, count)
        plt.show()
    
    @staticmethod
    def someSpectrumPlot(lstCoord, lstTypes):
        for c,t in zip(lstCoord, lstTypes):
            plt.plot(c[0], c[1], label = "type " + t.__str__())
    
        plt.legend()
        plt.show()
