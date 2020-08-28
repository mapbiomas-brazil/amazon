#!/usr/bin/env python

# Import earthengine API
import ee

# Initialise
ee.Initialize()

# /* Calculates fractional sub-pixel abundance with Spectral Mixture Analysis (SMA)    \
#   LXEndmembers - defines a set of image endmembers for Landsat sensors (5, 7 or 8 for TM, ETM+ or OLI, respectively)
#  getSMAFractions - applies singular value decomposition to calculate fractions.
#  getNDFI - calculates NDFI from fractional images.
#  ndfiColors - defines NDFI color table
#  getCSF - TBD
#  csfColors - TBD define CSF color table
# """

# Define Landsat 5 endmembers
ENDMEMBERS_L5 = [
    [119.0, 475.0, 169.0, 6250.0, 2399.0, 675.0],  # gv
    [1514.0, 1597.0, 1421.0, 3053.0, 7707.0, 1975.0],  # npv
    [1799.0, 2479.0, 3158.0, 5437.0, 7707.0, 6646.0],  # soil
    [4031.0, 8714.0, 7900.0, 8989.0, 7002.0, 6607.0]  # loud
]

# Define Landsat 7 endmembers
ENDMEMBERS_L7 = [
    [119.0, 475.0, 169.0, 6250.0, 2399.0, 675.0],  # gv
    [1514.0, 1597.0, 1421.0, 3053.0, 7707.0, 1975.0],  # npv
    [1799.0, 2479.0, 3158.0, 5437.0, 7707.0, 6646.0],  # soil
    [4031.0, 8714.0, 7900.0, 8989.0, 7002.0, 6607.0]  # cloud
]

# Define Landsat 8 endmembers
ENDMEMBERS_L8 = [
    [119.0, 475.0, 169.0, 6250.0, 2399.0, 675.0],  # gv
    [1514.0, 1597.0, 1421.0, 3053.0, 7707.0, 1975.0],  # npv
    [1799.0, 2479.0, 3158.0, 5437.0, 7707.0, 6646.0],  # soil
    [4031.0, 8714.0, 7900.0, 8989.0, 7002.0, 6607.0]  # cloud
]

# Define Sentinel-2 endmembers
ENDMEMBERS_S2 = [
    [119.0, 475.0, 169.0, 6250.0, 2399.0, 675.0],  # gv
    [1514.0, 1597.0, 1421.0, 3053.0, 7707.0, 1975.0],  # npv
    [1799.0, 2479.0, 3158.0, 5437.0, 7707.0, 6646.0],  # soil
    [4031.0, 8714.0, 7900.0, 8989.0, 7002.0, 6607.0]  # cloud
]


def getSMAFractions(image, endmembers):
    """Uminxing image using SDVC

    Parameters:
        image (ee.Image): Reflectance image containing the bands:
        blue, red, green, nir, swir1, swir2
        endmembers (list): Matrix containing the endmembers following
        this format: [
            [blue_gv, green_gv, red_gv, nir_gv, swir1_gv, swir2_gv],
            [blue_npv, green_npv, red_npv, nir_npv, swir1_npv, swir2_npv],
            [blue_soil, green_soil, red_soil, nir_soil, swir1_soil, swir2_soil],
            [blue_cloud, green_cloud, red_cloud, nir_cloud, swir1_cloud, swir2_cloud]
        ]

    Returns:
        ee.Image: Image unmixed
    """

    outBandNames = ['gv', 'npv', 'soil', 'cloud']

    fractions = ee.Image(image) \
        .select(['blue', 'green', 'red', 'nir', 'swir1', 'swir2']) \
        .unmix(endmembers) \
        .max(0) \
        .multiply(100) \
        .byte() \

    fractions = fractions.rename(outBandNames)

    summed = fractions.expression('b("gv") + b("npv") + b("soil")')

    shade = summed \
        .subtract(100) \
        .abs() \
        .byte() \
        .rename("shade")

    fractions = fractions.addBands(shade)

    return ee.Image(fractions \
                    .copyProperties(image) \
                    .copyProperties(image, [
                        'system:time_start',
                        'system:time_end',
                        'system:footprint'])
                   )


def getNDFI(image):
    """Calculate GVS and NDFI and add them to image fractions

    Parameters:
        image (ee.Image): Fractions image containing the bands:
        gv, npv, soil, cloud

    Returns:
        ee.Image: Fractions image with gvs and ndfi bands
    """

    summed = image.expression('b("gv") + b("npv") + b("soil")')

    gvs = image.select("gv") \
        .divide(summed) \
        .multiply(100) \
        .byte() \
        .rename("gvs")

    npvSoil = image.expression('b("npv") + b("soil")')

    ndfi = ee.Image.cat(gvs, npvSoil) \
        .normalizedDifference() \
        .rename('ndfi')

    # rescale NDFI from 0 to 200 \
    ndfi = ndfi.expression('byte(b("ndfi") * 100 + 100)')

    image = image.addBands(gvs)
    image = image.addBands(ndfi)

    return ee.Image(image \
                    .copyProperties(image) \
                    .copyProperties(image, [
                        'system:time_start',
                        'system:time_end',
                        'system:footprint'])
                   )


# Calculate CSFI and add it to image fractions
def getCSFI(image):
    """Calculate CSFI and add it to image fractions

    Parameters:
        image (ee.Image): Fractions image containing the bands:
        gv, npv, soil, cloud

    Returns:
        ee.Image: Fractions image with csfi bands
    """

    csfi = image.expression(
        "(float(b('gv') - b('shade'))/(b('gv') + b('shade')))")

    csfi = csfi.multiply(100).add(100).byte().rename(['csfi'])

    image = image.addBands(csfi)

    return ee.Image(image.copyProperties(image))
