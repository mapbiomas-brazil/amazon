#!/usr/bin/env python

# Import earthengine API
import ee

# Initialise
ee.Initialize()

LANDSAT_NEW_NAMES = ['blue', 'green', 'red',
                     'nir', 'swir1', 'swir2', 'pixel_qa', 'temp']
SENTINEL_NEW_NAMES = ['blue', 'green', 'red',
                      'nir', 'swir1', 'swir2', 'pixel_qa']

BAND_NAMES = {
    'l5': {
        'bandNames': ['B1', 'B2', 'B3', 'B4', 'B5', 'B7', 'pixel_qa', 'B6'],
        'newNames': LANDSAT_NEW_NAMES
    },
    'l7': {
        'bandNames': ['B1', 'B2', 'B3', 'B4', 'B5', 'B7', 'pixel_qa', 'B6'],
        'newNames': LANDSAT_NEW_NAMES
    },
    'l8': {
        'bandNames': ['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'pixel_qa', 'B11'],
        'newNames': LANDSAT_NEW_NAMES
    },
    'l5toa': {
        'bandNames': ['B1', 'B2', 'B3', 'B4', 'B5', 'B7', 'BQA', 'B6'],
        'newNames': LANDSAT_NEW_NAMES
    },
    'l7toa': {
        'bandNames': ['B1', 'B2', 'B3', 'B4', 'B5', 'B7', 'BQA', 'B6_VCID_1'],
        'newNames': LANDSAT_NEW_NAMES
    },
    'l8toa': {
        'bandNames': ['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'BQA', 'B11'],
        'newNames': LANDSAT_NEW_NAMES
    },
    'sentinel2': {
        'bandNames': ['B2', 'B3', 'B4', 'B8', 'B11', 'B12', 'QA60'],
        'newNames': SENTINEL_NEW_NAMES
    }
}


def getBandNames(key):
    """Create a new list of names for bands

    Parameters:
        key (str): Key indicating the collection name

    Returns:
        dictionary: A dictionry containing the input band names and
            the new band names
    """
    return BAND_NAMES[key]
