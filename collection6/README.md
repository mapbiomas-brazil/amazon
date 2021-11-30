<div>
    <img src='./assets/logo.png' height='auto' width='240' align='right'>
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
var assetSamples = "projects/imazon-simex/LULC/SAMPLES/COLLECTION6/TRAINED/samples-amazon-collection-6-2020-5";

var samples = ee.FeatureCollection(assetSamples);

Map.addLayer(samples, {}, 'samples 2020', true);
```

### Classification

1. Set the configuration parameters and the paths on the jupyter notebbok [mapbiomas-classification-amazon.ipynb](./mapbiomas-classification-amazon.ipynb)

2. Define the number of samples to be used in each image classification.

3. Define the area estimated [table](./data/areas.csv).

4. Set up the Random Forest parameters.

```python
RF_PARAMS = {
    'numberOfTrees': 50,
    'variablesPerSplit': 4,
    'minLeafPopulation': 25
}

# define the feature space
FEAT_SPACE_BANDS = ["gv", "gvs", "soil", "npv", "shade", "ndfi", "csfi"]
```

5. Define the number of samples per class.

```python
# number of samples
N_SAMPLES = 10000

# percentage of samples within the sample universe
P_SAMPLES = {"global": 0.30, "regional": 0.70}

# minimum number of samples per classe
dfMinSamples = pd.DataFrame([
    {'class':  3, 'min_samples': 4000},
    {'class':  4, 'min_samples': 2000},
    {'class': 12, 'min_samples':  500},
    {'class': 15, 'min_samples': 2000},
    {'class': 19, 'min_samples': 2000},
    {'class': 33, 'min_samples': 2000},
])
```

6. Define a list of imagens you don't want to use (see [json-trash]("./data/trash.json")). Some Landsat imagery are faulty or have bad metadata.
```json
{
    "image_id":[
        "LT05_231068_19850823",
        "LT05_231068_19850908",
        "LT05_227067_19850827",
        "LT05_227067_19850912",
        "LT05_224065_19850822",
        "LT05_224065_19851025",
        "LT05_227067_19870817",
        "LT05_226068_19870911",
        "LT05_226068_19870826",
        "LT05_226068_19870810",
        "LT05_232068_19870921",
        "LT05_232068_19870905",
        "LT05_232068_19870820",
        "LT05_232068_19870804",
        "LT05_230069_19880925",
        "LT05_230069_19880909",
        "LT05_230069_19880824",
        "LT05_229069_19880902",
        "LT05_227063_19880819",
        "LT05_227063_19880904",
        "LT05_227063_19881006",
        "LT05_229069_19890820",
        "LT05_229069_19890921",
        "LT05_229068_19890921",
        "LT05_231060_19901008",
        "LT05_233060_19910822",
        "LT05_229069_19910927",
        "LT05_229069_19910911",
        "LT05_221063_19911106",
        "LT05_221063_19911021",
        "LT05_221063_19910919",
        "LT05_221063_19910903",
        "LT05_223067_19940925",
        "LT05_223067_19940808",
        "LT05_223067_19941027",
        "LT05_223066_19940925",
        "LT05_229071_19951008",
        "LT05_229071_19950906",
        "LT05_228071_19951001",
        "LT05_228071_19950830",
        "LT05_228071_19950814",
        "LT05_230069_19970902"
    ]
}
```

7. There are some others parameters you can explore.

8. Run the notebook.

### Reduce the collection of classifications
This methodology process and classify every single image of Landsat collection with less than 50% of cloud cover for the Amazon biome region between 1985 and 2020. We are generating tons of data and we need to extract the best information possible for each pixel. For that reason, we reduce the classification collection by year using an ancillary random forest classifier.

For set up the script, define the parameters on the script [mapbiomas-classification-mode-rf.py](./mapbiomas-classification-mode-rf.py).

```python
ASSETS = {
    'classification': 'projects/imazon-simex/LULC/classification',
    'n_observations': 'projects/imazon-simex/LULC/quality',
    'tiles': 'projects/mapbiomas-workspace/AUXILIAR/landsat-mask',
    'samples_folder': 'projects/imazon-simex/LULC/SAMPLES/COLLECTION6/INTEGRATE',
    'output': 'projects/imazon-simex/LULC/classification-itg'
}

INPUT_VERSION = '2'

OUTPUT_VERSION = '7'

CLASS_IDS = [
    3,   # forest
    4,   # savanna
    12,  # grassland
    15,  # pasture
    19,  # agriculture
    33   # water
]

# N Samples padrao
N_SAMPLES = [
    {'class_id': 3, 'n_samples': 4000},
    {'class_id': 4, 'n_samples': 1000},
    {'class_id': 12, 'n_samples': 2000},
    {'class_id': 15, 'n_samples': 6000},
    {'class_id': 19, 'n_samples': 2000},
    {'class_id': 33, 'n_samples': 2000},
]
```

By the end, you can extend the `trash` variable with more Landsat images and run the code.

```python
TRASH = [
    "LT05_226062_20010715",
    "LT05_226062_20010731",
    "LE07_233058_20200322",
    "LC08_233058_20200227",
    "LC08_233058_20200126",
    "LE07_233058_20200219",
    "LC08_233058_20200211",
    "LE07_233058_20190320",
    "LC08_233058_20190328",
    "LE07_233058_20190405",
    "LC08_233058_20190429",
    "LC08_233058_20190819",
    "LE07_233058_20191014",
    "LC08_233058_20191107",
    "LC08_232059_20190305",
    "LC08_232059_20190321",
    "LC08_232059_20190406",
    "LE07_232059_20190430",
    "LE07_232059_20190820",
    "LC08_232059_20190828",
    "LE07_232059_20190905",
    "LC08_232059_20190913",
    "LE07_232059_20190921",
    "LC08_232059_20190929",
    "LE07_232059_20191007",
    "LE07_232059_20191124",
    "LC08_232059_20191202",
    "LE07_232059_20191210",
    "LE07_232059_20191226",
    "LC08_232059_20180926",
    "LC08_232059_20180825"
]
```

```shell
$ python3 mapbiomas-classification-mode-rf.py
```

### Spatial and temporal filter

In order to reduce the misclassified pixels, inconsistent transitions, or fill the gaps, we apply a spatial and temporal filter.

1. Create a table for temporal filter rules.
```python
rulesTable = '../csv/temporal-filter-rules-col6.csv'
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
