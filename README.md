# brightness-conversions
FITS file unit conversions

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
