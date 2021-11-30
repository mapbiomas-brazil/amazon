

import ee

ASSETS = {
    'classification': 'projects/imazon-simex/LULC/classification',
    'n_observations': 'projects/imazon-simex/LULC/quality',
    'tiles': 'projects/mapbiomas-workspace/AUXILIAR/landsat-mask',
    'samples_folder': 'projects/imazon-simex/LULC/SAMPLES/COLLECTION6/INTEGRATE',
    'output': 'projects/imazon-simex/LULC/classification-itg'
}

NEW_DATA = False

INPUT_VERSION = '2'

OUTPUT_VERSION = '7'

CLASS_IDS = [
    3,  # forest
    4,  # savanna
    12,  # grassland
    15,  # pasture
    19,  # agriculture
    33  # water
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

YEARS = [
    1985, 1986, 1987, 1988,
    1989, 1990, 1991, 1992,
    1993, 1994, 1995, 1996,
    1997, 1998, 1999, 2000,
    2001, 2002, 2003, 2004,
    2005, 2006, 2007, 2008,
    2009, 2010, 2011, 2012,
    2013, 2014, 2015, 2016,
    2017, 2018, 2019, 2020
]

SAMPLES_LIST = [
    "samples-amazon-collection-6-2018-2", "samples-amazon-collection-6-2017-2",
    "samples-amazon-collection-6-2016-2", "samples-amazon-collection-6-2015-2",
    "samples-amazon-collection-6-2014-2", "samples-amazon-collection-6-2013-2",
    "samples-amazon-collection-6-2012-2", "samples-amazon-collection-6-2011-2",
    "samples-amazon-collection-6-2010-2", "samples-amazon-collection-6-2009-2",
    "samples-amazon-collection-6-2008-2", "samples-amazon-collection-6-2007-2",
    "samples-amazon-collection-6-2006-2", "samples-amazon-collection-6-2005-2",
    "samples-amazon-collection-6-2004-2", "samples-amazon-collection-6-2003-2",
    "samples-amazon-collection-6-2002-2", "samples-amazon-collection-6-2001-2",
    "samples-amazon-collection-6-2000-2", "samples-amazon-collection-6-1999-2",
    "samples-amazon-collection-6-1998-2", "samples-amazon-collection-6-1997-2",
    "samples-amazon-collection-6-1996-2", "samples-amazon-collection-6-1995-2",
    "samples-amazon-collection-6-1994-2", "samples-amazon-collection-6-1993-2",
    "samples-amazon-collection-6-1992-2", "samples-amazon-collection-6-1991-2",
    "samples-amazon-collection-6-1990-2", "samples-amazon-collection-6-1989-2",
    "samples-amazon-collection-6-1988-2", "samples-amazon-collection-6-1987-2",
    "samples-amazon-collection-6-1986-2",
]

# landsat tiles
TILE_LIST = [
    "001057", "001058", "001059", "001061",
    "001062", "001063", "001064", "001065",
    "001066", "001067", "001068", "002057",
    "002059", "002060", "002061", "002062",
    "002063", "002064", "002065", "002066",
    "002067", "002068", "221064", "222061",
    "222062", "222063", "222067", "223061",
    "223062", "223063", "223068", "224063",
    "224064", "224070", "225061", "225062",
    "225063", "225064", "225070", "226059",
    "226062", "226063", "226064", "226065",
    "226068", "227058", "227059", "227060",
    "227063", "227064", "227065", "227067",
    "228058", "228060", "228063", "228064",
    "228067", "228068", "228072", "229060",
    "229061", "229063", "229064", "229066",
    "229067", "229068", "230058", "230059",
    "230060", "230061", "230063", "230064",
    "230065", "230066", "230067", "230070",
    "231060", "231061", "231063", "231065",
    "231067", "232062", "232064", "232067",
    "233058", "233062", "233063", "233064",
    "233065", "233067", "003058", "003059",
    "003060", "003061", "003062", "003063",
    "003064", "003065", "003066", "003067",
    "003068", "004058", "004059", "004060",
    "004061", "004062", "004063", "004064",
    "004065", "004066", "004067", "005059",
    "005060", "005063", "005064", "005065",
    "005066", "005067", "006063", "006064",
    "006065", 
    "006066"
]

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

FEATURE_SPACE = [
    'mode',
    'mode_secondary',
    'transitions_total',
    'distinct_total',
    'transitions_year',
    'distinct_year',
    'occurrence_forest_year',
    'occurrence_savanna_year',
    'occurrence_grassland_year',
    'occurrence_pasture_year',
    'occurrence_agriculture_year',
    'occurrence_water_year',
    'occurrence_savanna_total',
    'occurrence_grassland_total',
    'occurrence_agriculture_total',
    'occurrence_water_total',
]

ee.Initialize()


def shuffle(collection, seed=1):
    """
    Adds a column of deterministic pseudorandom numbers to a collection.
    The range 0 (inclusive) to 1000000000 (exclusive).
    """

    collection = collection.randomColumn('random', seed)\
        .sort('random', True)\
        .map(
            lambda feature: feature.set(
                'new_id',
                ee.Number(feature.get('random'))
                .multiply(1000000000)
                .round()
            )
    )

    # list of random ids
    randomIdList = ee.List(
        collection.reduceColumns(ee.Reducer.toList(), ['new_id'])
        .get('list'))

    # list of sequential ids
    sequentialIdList = ee.List.sequence(1, collection.size())

    # set new ids
    shuffled = collection.remap(randomIdList, sequentialIdList, 'new_id')

    return shuffled


#
# collection of all classified images
#
classification = ee.ImageCollection(ASSETS['classification'])

TRASH = list(map(lambda imageid: imageid + '-' + INPUT_VERSION, TRASH))

classification = classification \
    .filter(ee.Filter.inList('system:index', TRASH).Not());

#
#
#
n_observations = ee.ImageCollection(ASSETS['n_observations'])
#
#
# samples
samples = map(
    lambda sampleName:
        ee.FeatureCollection(ASSETS['samples_folder'] + "/" + sampleName),
    SAMPLES_LIST
)

samples = ee.FeatureCollection(list(samples)).flatten()

samples = shuffle(samples, seed=1)

shuffledSamples = map(
    lambda obj: samples.filterMetadata(
        'class', 'equals', obj['class_id']).limit(obj['n_samples']),
    N_SAMPLES
    )

samples = ee.FeatureCollection(list(shuffledSamples)).flatten()
#
#
# iterate
for tile in TILE_LIST:

    try:
        integrated = ee.Image().select()

        tile_mask = ee.Image('{}/{}-2'.format(ASSETS['tiles'], int(tile)))
        centroid = tile_mask.geometry().centroid()

        #
        #
        #
        classification_tile = classification.filterBounds(centroid)

        n_observations_total = n_observations\
            .filterBounds(centroid)\
            .sum()\
            .rename('observations_total')

        transitions_total = classification_tile\
            .reduce(ee.Reducer.countRuns())\
            .divide(n_observations_total)\
            .rename('transitions_total')

        distinct_total = classification_tile\
            .reduce(ee.Reducer.countDistinctNonNull())\
            .rename('distinct_total')

        #
        # occurrence total
        #
        forest_total = classification_tile\
            .map(lambda image: image.eq(3))\
            .reduce(ee.Reducer.sum())\
            .divide(n_observations_total)\
            .rename('occurrence_forest_total')

        savanna_total = classification_tile\
            .map(lambda image: image.eq(4))\
            .reduce(ee.Reducer.sum())\
            .divide(n_observations_total)\
            .rename('occurrence_savanna_total')

        grassland_total = classification_tile\
            .map(lambda image: image.eq(12))\
            .reduce(ee.Reducer.sum())\
            .divide(n_observations_total)\
            .rename('occurrence_grassland_total')

        pasture_total = classification_tile\
            .map(lambda image: image.eq(15))\
            .reduce(ee.Reducer.sum())\
            .divide(n_observations_total)\
            .rename('occurrence_pasture_total')

        agriculture_total = classification_tile\
            .map(lambda image: image.eq(19))\
            .reduce(ee.Reducer.sum())\
            .divide(n_observations_total)\
            .rename('occurrence_agriculture_total')

        water_total = classification_tile\
            .map(lambda image: image.eq(33))\
            .reduce(ee.Reducer.sum())\
            .divide(n_observations_total)\
            .rename('occurrence_water_total')
        
        for year in YEARS:
            #
            classification_year = classification\
                .filterDate(str(year) + '-01-01', str(year) + '-12-31')\
                .filterBounds(centroid)

            if classification_year.size().getInfo() > 0:
                classification_secondary = classification\
                    .filterDate(str(year - 1) + '-11-01', str(year) + '-06-30')\
                    .filterBounds(centroid)

                #
                n_observations_year = ee.Image(
                    '{}/{}-{}'.format(ASSETS['n_observations'], int(tile), year))\
                    .rename('observations_year')

                #
                transitions_year = classification_year\
                    .reduce(ee.Reducer.countRuns())\
                    .divide(n_observations_year)\
                    .rename('transitions_year')

                distinct_year = classification_year\
                    .reduce(ee.Reducer.countDistinctNonNull())\
                    .rename('distinct_year')

                #
                # mode
                #
                mode_year = classification_year\
                    .reduce(ee.Reducer.mode())\
                    .rename('mode')

                if classification_secondary.size().getInfo() > 0:
                    mode_secondary = classification_secondary\
                        .reduce(ee.Reducer.mode())\
                        .rename('mode_secondary')
                else:
                    mode_secondary = mode_year.rename('mode_secondary')

                #
                # occurrence in the year
                #
                forest_year = classification_year\
                    .map(lambda image: image.eq(3))\
                    .reduce(ee.Reducer.sum())\
                    .divide(n_observations_year)\
                    .rename('occurrence_forest_year')

                savanna_year = classification_year\
                    .map(lambda image: image.eq(4))\
                    .reduce(ee.Reducer.sum())\
                    .divide(n_observations_year)\
                    .rename('occurrence_savanna_year')

                grassland_year = classification_year\
                    .map(lambda image: image.eq(12))\
                    .reduce(ee.Reducer.sum())\
                    .divide(n_observations_year)\
                    .rename('occurrence_grassland_year')

                pasture_year = classification_year\
                    .map(lambda image: image.eq(15))\
                    .reduce(ee.Reducer.sum())\
                    .divide(n_observations_year)\
                    .rename('occurrence_pasture_year')

                agriculture_year = classification_year\
                    .map(lambda image: image.eq(19))\
                    .reduce(ee.Reducer.sum())\
                    .divide(n_observations_year)\
                    .rename('occurrence_agriculture_year')

                water_year = classification_year\
                    .map(lambda image: image.eq(33))\
                    .reduce(ee.Reducer.sum())\
                    .divide(n_observations_year)\
                    .rename('occurrence_water_year')

                # image feature space
                image = mode_year\
                    .addBands(mode_secondary)\
                    .addBands(transitions_total)\
                    .addBands(distinct_total)\
                    .addBands(transitions_year)\
                    .addBands(distinct_year)\
                    .addBands(n_observations_total)\
                    .addBands(n_observations_year)\
                    .addBands(forest_year)\
                    .addBands(savanna_year)\
                    .addBands(grassland_year)\
                    .addBands(pasture_year)\
                    .addBands(agriculture_year)\
                    .addBands(water_year)\
                    .addBands(forest_total)\
                    .addBands(savanna_total)\
                    .addBands(grassland_total)\
                    .addBands(pasture_total)\
                    .addBands(agriculture_total)\
                    .addBands(water_total)

                image = image.select(FEATURE_SPACE)

                # traning the classifier
                classifier = ee.Classifier.smileRandomForest(
                    numberOfTrees=50,
                    variablesPerSplit=4,
                    minLeafPopulation=25
                ).train(samples, 'class', FEATURE_SPACE)

                integrated_year = image\
                    .select(FEATURE_SPACE)\
                    .classify(classifier)

                integrated_year = mode_year\
                    .where(integrated_year.neq(0), integrated_year)\
                    .rename(['classification_' + str(year)])

                integrated = integrated.addBands(integrated_year)
            else:
                integrated_year = ee.Image(0)\
                    .rename(['classification_' + str(year)])

                integrated = integrated.addBands(integrated_year)

        integrated = integrated.mask(tile_mask)

        geometry = tile_mask.geometry()

        name = '{}-{}'.format(int(tile), OUTPUT_VERSION)

        task = ee.batch.Export.image.toAsset(
            image=integrated.toByte().set('version', OUTPUT_VERSION).set('tile', tile),
            description=name,
            assetId='{}/{}'.format(ASSETS['output'], name),
            pyramidingPolicy={".default": "mode"},
            region=geometry.getInfo()['coordinates'],
            scale=30,
        )

        print('Exporting {}...'.format(name))
        task.start()
    except Exception as error:
        print(error)
