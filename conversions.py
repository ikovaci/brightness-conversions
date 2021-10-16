import numpy as np
import astropy.units as au
from astropy.io import fits
from astropy.utils import data
from astropy.wcs import WCS
import astropy.constants as ac

'''

Jy/pix - Jy/sr
    input cube in Jy/pix
    if no pix value input, takes it from 1/CDELT1
    
Jy/beam - Jy/sr
    input cube in Jy/beam
    beam in sr
    if no beam value input, calculated by BMIN*BMAJ (in rad)

Jy/sr - Jy/beam
    input cube in Jy/sr
    beam in sr
    if no beam value input, calculated by BMIN*BMAJ (in rad)
    
Jy/beam - K
    transforms Jy/beam into brightness temperature
    input wavelength in um

K - Jy/beam
    transforms from brightness temperature to Jy/beam
    input wavelength in um
    
Jy/sr - W/m2/um/sr
    transforms to W/m2/Hz/sr then W/m2/um/sr
    input wavelength in um

'''

## Jy/pix to Jy/sr
def Jy_pix2sr (hdu, pix = None): ## pix = no of pixels in a degree
    if pix == None:
        pix = abs(hdu.header['CDELT1']*hdu.header['CDELT2'])
    conv = pix*(np.pi/180)**2
    hdu.header['BUNIT'] = 'Jy sr-1'
    hdu.data = hdu.data/conv
    return hdu

## Jy/beam to Jy/sr
def Jy_beam2sr (hdu, beam = None): ## beam == abs BMIN*BMAJ
    if beam == None:
        beam = abs(hdu.header['BMIN']*hdu.header['BMAJ'])*(np.pi/180)**2
    beam_area = np.pi*beam/(4*np.log(2))
    hdu.data = hdu.data/beam_area
    hdu.header['BUNIT'] = 'Jy sr-1'
    return hdu

## Jy/sr to Jy/beam
def Jysr2beam (hdu, beam = None):
    if beam == None:
        beam = abs(hdu.header['BMIN']*hdu.header['BMAJ'])*(np.pi/180)**2
    beam_area = np.pi*beam/(4*np.log(2))
    hdu.data = hdu.data*beam_area
    hdu.header['BUNIT'] = 'Jy beam-1'
    return hdu

## Jy/beam to K
def Jy_beam2K (hdu, wavel, beam = None): ## wavel in microns, beam in sr
    if beam == None:
        beam = (abs(hdu.header['BMIN']*hdu.header['BMAJ']))*(np.pi/180)**2
    wavel = wavel*1e-6
    conv = 0.32e23*wavel**2/beam
    hdu.data = hdu.data*1e-26
    hdu.data = hdu.data*conv
    hdu.header['BUNIT'] = 'K'
    return hdu

## K to Jy/beam
def K2Jy_beam (hdu, wavel, beam = None): ## wavel in microns, beam in sr
    if beam == None:
        beam = (abs(hdu.header['BMIN']*hdu.header['BMAJ']))*(np.pi/180)**2
    wavel = wavel*1e-6
    conv = 0.32e23*wavel**2/beam
    hdu.data = hdu.data*1e26
    hdu.data = hdu.data/conv
    hdu.header['BUNIT'] = 'Jy beam-1'
    return hdu

## Jy/sr to W/m2/um/sr
def Jy_Wm2um (hdu, wavel): ## wavel in microns
    hdu.data = hdu.data * 1e-26
    c = ac.c.to('m/s').value
    wavel = wavel*1e-6
    conv = c/wavel**2*1e-6 ## multiply with 1e-6 because um^2 (um and c cancel)
    hdu.data = hdu.data*conv
    hdu.header['BUNIT'] = 'W m-2 um-1 sr-1'
    return hdu
