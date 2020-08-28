<div>
    <img src='./assets/logo.jpg' height='auto' width='240' align='right'>
    <h1>Amazon Biome</h1>
</div>

Developed by ***Imazon***.

## About

This repository contains the scripts to classify and filter the **Amazon** biome. 

We highly recommend the reading of [Amazon's Appendix of the Algorithm Theoretical Basis Document (ATBD)](https://mapbiomas.org/download-dos-atbds). The fundamental information about the classification and methodology is there. 

## How to use
1. [Create an account](https://developers.google.com/earth-engine/guides/python_install) in Google Earth Engine plataform.

2. Install the python version 3.x.

3. Install the Earth Engine [python API](https://developers.google.com/earth-engine/guides/python_install) and get the credentials. 

4. Download or clone this repository to your local workspace.

### Example of the samples

```javascript
// This script is executed only in the code editor

// asset containing sample points for training
var assetSamples = "projects/mapbiomas-workspace/AMOSTRAS/Amazonia/Colecao4/samples-collection-4-2019-5";

var samples = ee.FeatureCollection(assetSamples);

Map.addLayer(samples, {}, 'samples 2019', true);
```
<a href="https://code.earthengine.google.com/05af09ff13757eb606212e7edb607b19" target="_blank" rel="noopener">Link to script</a>

### Classification

1. Set the configuration parameters and the paths on the script [mapbiomas-classification-amazon.py](./mapbiomas-classification-amazon.py)

2. Define the number of samples to be used in each image classification.

3. Define the area estimated [table](./csv/collection-31-cover-scenes.csv).

4. Set the list of years, period to filter the image collection and satellite id.

```python
params = [
    [2010, '2010-01-01', '2010-12-31', 'l5'],
    [2013, '2013-01-01', '2013-12-31', 'l8'],
    [2019, '2019-01-01', '2019-12-31', 'l7'],
]
```

5. Create a list with some landsat path/row ids.

```python
pathRowsList = [
    "227/68", "225/69",
    "226/69", "224/69",
    "221/65", "222/66",
    "223/65", "223/66",
    "225/68", "226/68",
]
```

6. Define a list of imagens you don't want to use. Some Landsat imagery are faulty or have bad metadata.
```python
trash = [
    "LT05_231068_19850823", "LT05_231068_19850908",
    "LT05_227067_19850827", "LT05_227067_19850912", 
    "LT05_224065_19850822", "LT05_224065_19851025",
    "LT05_227067_19870817", "LT05_226068_19870911",
    "LT05_226068_19870826", "LT05_226068_19870810",
    "LT05_232068_19870921", "LT05_232068_19870905",
    "LT05_232068_19870820", "LT05_232068_19870804",
    "LT05_230069_19880925", "LT05_230069_19880909",
    "LT05_230069_19880824", "LT05_229069_19880902",
    "LT05_227063_19880819", "LT05_227063_19880904",
    "LT05_227063_19881006", "LT05_229069_19890820",
    "LT05_229069_19890921", "LT05_229068_19890921",
    "LT05_231060_19901008", "LT05_233060_19910822",
    "LT05_229069_19910927", "LT05_229069_19910911",
    "LT05_221063_19911106", "LT05_221063_19911021",
    "LT05_221063_19910919", "LT05_221063_19910903",
    "LT05_223067_19940925", "LT05_223067_19940808",
    "LT05_223067_19941027", "LT05_223066_19940925",
    "LT05_229071_19951008", "LT05_229071_19950906",
    "LT05_228071_19951001", "LT05_228071_19950830",
    "LT05_228071_19950814", "LT05_230069_19970902",
]
```

7. Define the Randon Forest parameters

```python
randomForestParams = {
    'numberOfTrees': 50,
    'variablesPerSplit': 4,
    'minLeafPopulation': 25
}

featureSpace = ["gv", "gvs", "soil", "npv", "shade", "ndfi", "csfi"]
```

8. There area some others parameters you can explore.

9. Run the code on the terminal.

```shell
$ python3 mapbiomas-classification-amazon.py
```
### Reduce the collection of classifications
This methodology is processing and classifying every single image of Landsat collection with less than 50% of cloud cover for the Amazon biome region between 1985 and 2019. We are generating tons of data and we need to extract the best information possible for each pixel. For that reason, we reduce the classification collection by year using an adjustment rule.

For set up the script, define the parameters on the script [mapbiomas-classification-mode.py](./mapbiomas-classification-mode.py).

```python
assetClassification = "projects/imazon-simex/LULC/classification"
assetBiomes = "projects/mapbiomas-workspace/AUXILIAR/biomas-raster-41"
assetScenes = 'projects/mapbiomas-workspace/AUXILIAR/cenas-landsat'
assetOutput = 'projects/imazon-simex/LULC/integration-scenes'

version = '2'
outputVersion = '7'

years = [
    '2017',
    '2018',
    '2019',
]

pathRows = [
    "223/63", "223/64",
    "224/63", "224/64",
    "224/65", "227/65",
]
```

By the end, you can extend the `trash` variable with more Landsat images and run the code.

```shell
$ python3 mapbiomas-classification-mode.py
```

### Spatial and temporal filter

In order to reduce the misclassified pixels, inconsistent transitions, or fill the gaps, we apply a spatial and temporal filter.

1. Create a table for temporal filter rules.
```python
rulesTable = './csv/temporal-filter-rules.csv'
```

2. Define the spatial filter params
```python
filterParams = [
    {
        'classValue': 3,
        'maxSize': 5
    },
    {
        'classValue': 4,
        'maxSize': 5
    },
    {
        'classValue': 12,
        'maxSize': 5
    },
    {
        'classValue': 15,
        'maxSize': 5
    },
    {
        'classValue': 19,
        'maxSize': 5
    },
    {
        'classValue': 25,
        'maxSize': 5
    },
    {
        'classValue': 27,
        'maxSize': 5
    },
    {
        'classValue': 33,
        'maxSize': 5
    },
]
```

3. Run the spatial and temporal script.
```shell
$ python3 mapbiomas-classification-filter.py
```