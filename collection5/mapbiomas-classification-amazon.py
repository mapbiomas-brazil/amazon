# -*- coding: utf-8 -*-
from pprint import pprint
from modules.SMA_NDFI import *
from modules.PreProcessing import iluminationCorrection
from modules.CloudAndShadowMask import getMasks
from modules.BandNames import getBandNames
from modules.Collection import setProperties
from modules.Collection import getCollection
import csv
import ee
import sys
import os

sys.dont_write_bytecode = True

# Initialize
ee.Initialize()

outputAsset = 'projects/imazon-simex/LULC/classification'

assetSamplesLapig = 'projects/mapbiomas-workspace/AMOSTRAS/Amazonia/Colecao4'
assetSamplesRefer = 'projects/imazon-simex/LULC/SAMPLES'

assetScenes = 'projects/mapbiomas-workspace/AUXILIAR/cenas-landsat'
tableName = "./csv/collection-31-cover-scenes.csv"

nsamples = 10000

# final classes
selectedClasses = [3, 4, 12, 13, 15, 19, 21, 25, 33]

params = [
    [2019, '2019-01-01', '2019-12-31', 'l8'],
    [2019, '2019-01-01', '2019-12-31', 'l7'],
]

pathRowsList = [
    "227/68", "225/69",
    "226/69", "224/69",
    "221/65", "222/66",
    "223/65", "223/66",
    "225/68", "226/68",
]

scenes = ee.FeatureCollection(assetScenes)\
    .filter(
        ee.Filter.inList(
            'SPRNOME',
            pathRowsList
        )
)

scenesCentroid = scenes.map(
    lambda scene: scene.centroid()
)

trash = [
    "LT05_231068_19850823", "LT05_231068_19850908",
    "LT05_227067_19850827", "LT05_227067_19850912", "LT05_224065_19850822", "LT05_224065_19851025",
    "LT05_227067_19870817", "LT05_226068_19870911", "LT05_226068_19870826", "LT05_226068_19870810",
    "LT05_232068_19870921", "LT05_232068_19870905", "LT05_232068_19870820", "LT05_232068_19870804",
    "LT05_230069_19880925", "LT05_230069_19880909", "LT05_230069_19880824", "LT05_229069_19880902",
    "LT05_227063_19880819", "LT05_227063_19880904", "LT05_227063_19881006", "LT05_229069_19890820",
    "LT05_229069_19890921", "LT05_229068_19890921", "LT05_231060_19901008", "LT05_233060_19910822",
    "LT05_229069_19910927", "LT05_229069_19910911", "LT05_221063_19911106", "LT05_221063_19911021",
    "LT05_221063_19910919", "LT05_221063_19910903", "LT05_223067_19940925", "LT05_223067_19940808",
    "LT05_223067_19941027", "LT05_223066_19940925", "LT05_229071_19951008", "LT05_229071_19950906",
    "LT05_228071_19951001", "LT05_228071_19950830", "LT05_228071_19950814", "LT05_230069_19970902",
]

randomForestParams = {
    'numberOfTrees': 50,
    'variablesPerSplit': 4,
    'minLeafPopulation': 25
}

featureSpace = ["gv", "gvs", "soil", "npv", "shade", "ndfi", "csfi"]

segmentsBands = ["blue", "green", "red", "nir", "swir1", "swir2"]

splitRanges = [0.0, 0.0, 0.0, 1.0]  # 0 % -30 %, 31%-50%, 71%-100%

#
percentGlobal = 0.3
percentRegional = 0.7

pixelSize = 30

samplesBaseNameLapig = '{}/samples-collection-4-{}-{}'
samplesBaseNameRefer = '{}/collection-31-{}'

version = '9'

metadata = 'samples collection 3.1 and collection 4.1'

samplesVersion = '5'

biome = "AMAZONIA"

collectionVersion = 5.0

specCloudBands = [
    "blue", "green", "red", "nir", "swir1", "swir2",
    'cloudFlagMask', 'cloudScoreMask', 'cloudShadowFlagMask', 'cloudShadowTdomMask']

excludedClassesLapig = [
    "Não Observado",
    "Erro",
    "Desmatamento",
    "Regeneração",
    "Mosaico de ocupação",
    "Apicum",
    "Aquicultura"
]

excludedClassesRefer = [
    100,
]

classesLapig = {
    "Formação Florestal": 3,
    "Floresta Plantada": 3,
    "Mangue": 3,
    "Silvicultura": 3,
    "Formação Savânica": 3,
    "Formação Campestre": 13,
    "Outra Formação Natural Não Florestal": 13,
    "Pastagem Cultivada": 15,
    "Pastagem Natural": 15,
    "Pastagem Nativa": 15,
    "Cultura Anual": 19,
    "Cultura Perene": 19,
    "Culturas Perenes": 19,
    "Cultivos Perenes": 19,
    "Culturas Anuais": 19,
    "Culturas Semi-Perene": 19,
    "Cultura Semi-Perene": 19,
    "Infraestrutura Urbana": 25,
    "Outra Área não Vegetada": 25,
    "Praias e Dunas": 25,
    "Mineração": 25,
    "Rio, Lago e Oceano": 33,
    "Rio": 33,
    "Lago e Oceano": 33,
}

classesRefer = {
    '3': 3,
    '10': 13,
    '21': 15,
    '25': 25,
    '33': 33,
}

endmembers = {
    'l5': ENDMEMBERS_L5,
    'l7': ENDMEMBERS_L7,
    'l8': ENDMEMBERS_L8,
}

collectionIds = {
    'l5': 'LANDSAT/LT05/C01/T1_SR',
    'l7': 'LANDSAT/LE07/C01/T1_SR',
    'l8': 'LANDSAT/LC08/C01/T1_SR',
}

classesLapig = ee.Dictionary(classesLapig)
classesRefer = ee.Dictionary(classesRefer)

alredyInCollection = ee.ImageCollection(outputAsset)\
    .filterMetadata('version', 'equals', version)\
    .reduceColumns(
        ee.Reducer.toList(),
        ['system:index'])\
    .get('list').getInfo()

alredyInCollection = map(
    lambda imageid: imageid.replace('-' + version, ''),
    alredyInCollection
)

#
# Use defined functions
#

def calcCsfi(image):

    exp = "(float(b('gv') - b('shade'))/(b('gv') + b('shade')))"

    csfi = image.expression(exp)\
        .multiply(100).add(100).byte()

    return csfi.rename(['csfi'])


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


def getSamplesLapig(year):

    sampleName = samplesBaseNameLapig.format(
        assetSamplesLapig, year, samplesVersion)

    samples = ee.FeatureCollection(sampleName)\
        .filterMetadata('gv', 'not_equals', None)\
        .filter(ee.Filter.inList('CLASS_' + str(year), excludedClassesLapig).Not())\
        .map(
            lambda feature:
                feature.set('year', year)
                .set('reference', classesLapig.get(feature.get('CLASS_' + str(year)))))\
        .select(['year', 'reference'])

    return samples


def getSamplesRefer(year):

    sampleName = samplesBaseNameRefer.format(
        assetSamplesRefer, year)

    samples = ee.FeatureCollection(sampleName)\
        .filterMetadata('median_gv', 'not_equals', None)\
        .filter(ee.Filter.inList('reference', excludedClassesRefer).Not())\
        .select(['year', 'reference'])

    return samples


def splitSamples(samples, ranges=[0, 0.3, 0.5, 1.0]):

    # shuffle the collection
    shuffled = shuffle(samples, seed=1)

    # define range filter for samples
    size = shuffled.size()

    filter1 = ee.Filter.rangeContains('new_id', size.multiply(
        ranges[0]).round().add(1), size.multiply(ranges[1]).round())

    filter2 = ee.Filter.rangeContains('new_id', size.multiply(
        ranges[1]).round().add(1), size.multiply(ranges[2]).round())

    filter3 = ee.Filter.rangeContains('new_id', size.multiply(
        ranges[2]).round().add(1), size.multiply(ranges[3]).round())

    return {
        'test': shuffled.filter(filter1),
        'validation': shuffled.filter(filter2),
        'training': shuffled.filter(filter3)
    }


def readTable(tableName):

    table = []

    with open(tableName) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:

            dictionary = {
                'cena': row['cena'],
                'classe': row['classe']
            }

            for year in range(1985, 2020):
                dictionary[str(year)] = row[str(year)]

            table.append(dictionary)

    return table


def getNumberOfsamples(table, scene, year, classes):

    sceneTable = filter(
        lambda obj:
        obj['cena'] == scene and int(obj['classe']) in classes,
        table
    )

    sceneTable = map(
        lambda obj:
        dict(zip(
            ['classe', 'area'],
            [obj['classe'], obj[year]])),
            sceneTable
    )

    for a in map(lambda obj: obj, sceneTable):
        pprint(a)

    total = sum(map(
        lambda obj: float(list(obj.values())[1]), sceneTable))

    print('total', total)

    nSamplesTable = map(
        lambda obj:
        dict(zip(
            ['classe', 'nsamples'],
            [int(obj.values()[0]), max(round(nsamples * float(obj.values()[1])/total), int(nsamples * 0.20))])),
            sceneTable
    )

    nSamplesTable = filter(
        lambda obj: obj.values()[0] != 0,
        nSamplesTable
    )

    # split the classe 21 in half for 15 and 19
    nsamples21 = filter(lambda obj: obj['classe'] == 21, nSamplesTable)

    if len(nsamples21) > 0:
        half = round(nsamples21[0]['nsamples']/2.0)
        nSamplesTable = map(
            lambda obj:
                obj
                if obj['classe'] != 15 and obj['classe'] != 19 else {
                    'classe': obj['classe'],
                    'nsamples': obj['nsamples'] + half
                },
                nSamplesTable
        )

    # add the classe 4 to 3
    nsamples4 = filter(lambda obj: obj['classe'] == 4, nSamplesTable)

    if len(nsamples4) > 0:
        nSamplesTable = map(
            lambda obj:
                obj
                if obj['classe'] != 4 else {
                    'classe': obj['classe'],
                    'nsamples': obj['nsamples'] + nsamples4[0]['nsamples']
                },
                nSamplesTable
        )

    # add the classe 12 to 13
    nsamples12 = filter(lambda obj: obj['classe'] == 12, nSamplesTable)

    if len(nsamples12) > 0:
        nSamplesTable = map(
            lambda obj:
                obj
                if obj['classe'] != 12 else {
                    'classe': obj['classe'],
                    'nsamples': obj['nsamples'] + nsamples12[0]['nsamples']
                },
                nSamplesTable
        )

    nSamplesTable = filter(lambda obj: obj['classe'] != 4, nSamplesTable)
    nSamplesTable = filter(lambda obj: obj['classe'] != 12, nSamplesTable)
    nSamplesTable = filter(lambda obj: obj['classe'] != 21, nSamplesTable)

    return nSamplesTable


def applyCloudAndShadowMask(collection):

    # Get cloud and shadow masks
    collectionWithMasks = getMasks(collection,
                                   cloudFlag=True,
                                   cloudScore=True,
                                   cloudShadowFlag=True,
                                   cloudShadowTdom=True,
                                   zScoreThresh=-1,
                                   shadowSumThresh=4000,
                                   dilatePixels=2,
                                   cloudHeights=ee.List.sequence(
                                       200, 10000, 500),
                                   cloudBand='cloudFlagMask')

    collectionWithMasks = collectionWithMasks.select(specCloudBands)

    # get collection without clouds
    collectionWithoutClouds = collectionWithMasks.map(
        lambda image: image.mask(
            image.select([
                'cloudFlagMask',
                'cloudScoreMask',
                'cloudShadowFlagMask',
                'cloudShadowTdomMask'
            ]).reduce(ee.Reducer.anyNonZero()).eq(0)
        )
    )

    return collectionWithoutClouds


def getSegments(image, size=16):

    seeds = ee.Algorithms.Image.Segmentation.seedGrid(
        size=size,
        gridType='square'
    )

    snic = ee.Algorithms.Image.Segmentation.SNIC(
        image=image.select(segmentsBands),
        size=size,
        compactness=1,
        connectivity=8,
        neighborhoodSize=2*size,
        seeds=seeds
    )

    snic = ee.Image(
        snic.copyProperties(image)
            .copyProperties(image, ['system:footprint'])
            .copyProperties(image, ['system:time_start']))

    return snic.select(['clusters'], ['segments'])


def getSimilarMask(segments, samples):

    samplesSegments = segments.sampleRegions(
        collection=samples,
        properties=['reference', 'year'],
        scale=30,
        geometries=True
    )

    segmentsValues = ee.List(
        samplesSegments
        .reduceColumns(
            ee.Reducer.toList().repeat(2),
            ['reference', 'segments']
        ).get('list')
    )

    similiarMask = segments.remap(
        segmentsValues.get(1),
        segmentsValues.get(0), 0)

    return similiarMask.rename(['similarMask'])


def getFeatureSpace(collection):

    featureSpaceCollection = collection\
        .map(lambda image: image.addBands(getSMAFractions(image, endmembers[param[3]])))\
        .map(getNDFI)\
        .map(lambda image: image.addBands(calcCsfi(image)))

    return featureSpaceCollection


def classify(image, randomForestParams, samples):

    classifier = ee.Classifier.randomForest(
        numberOfTrees=randomForestParams['numberOfTrees'],
        variablesPerSplit=randomForestParams['variablesPerSplit'],
        minLeafPopulation=randomForestParams['minLeafPopulation'])\
        .train(samples, 'reference', featureSpace)

    return ee.Image(image
                    .select(featureSpace)
                    .classify(classifier)
                    .rename(['classification'])
                    .copyProperties(image)
                    .copyProperties(image, ['system:footprint'])
                    .copyProperties(image, ['system:time_start'])
                    )


#
# script
#
table = readTable(tableName)

# TODO: melhorar esse trecho de script
for param in params:
    
    landsatCollection = ee.ImageCollection(collectionIds[param[3]])\
        .filterBounds(scenesCentroid.geometry())\
        .filterDate(param[1], param[2])\
        .filterMetadata('CLOUD_COVER', 'less_than', 50)\
        .filter(ee.Filter.inList('system:index', trash).Not())

    classificationCollection = ee.ImageCollection(outputAsset)\
        .filterMetadata('version', 'equals', version)\
        .filterBounds(scenesCentroid.geometry())\
        .filterDate(param[1], param[2])

    landsatIds = landsatCollection\
        .reduceColumns(ee.Reducer.toList(), ['system:index'])\
        .get('list')\
        .getInfo()

    classificationIds = classificationCollection\
        .reduceColumns(ee.Reducer.toList(), ['system:index'])\
        .get('list')\
        .getInfo()

    sceneList = []

    # get path/row ids
    for imageid in landsatIds:
        if not imageid + '-' + version in classificationIds:
            s = list(imageid.split('_')[1])
            s[3] = '/'
            sceneList.append(str("".join(s)))

    sceneList.sort()
    sceneList = list(set(sceneList))

    for sceneName in sceneList:

        print(sceneName)

        centroid = scenes.filterMetadata('SPRNOME', 'equals', sceneName)\
            .geometry().centroid()

        samplesRegion = scenes.filterMetadata('SPRNOME', 'equals', sceneName)\
            .geometry()

        # get Lapig samples
        samplesLapig = getSamplesLapig(param[0])

        # get Reference samples
        samplesRefer = getSamplesRefer(param[0])\
            .filter(ee.Filter.inList('reference', [3, 10, 33]))\
            .remap([3, 10, 33], [3, 13, 33], 'reference')

        # samplesSplited = splitSamples(samplesLapig, ranges=splitRanges)

        nSamplesTable = getNumberOfsamples(
            table, sceneName, str(param[0]), selectedClasses)

        print(nSamplesTable)

        # returns a collection containing the specified parameters
        collection = getCollection(collectionIds[param[3]],
                                   dateStart=param[1],
                                   dateEnd=param[2],
                                   cloudCover=50,
                                   geometry=centroid)

        # Alredy in collection or Black list images
        collection = collection\
            .filter(ee.Filter.inList('system:index', alredyInCollection).Not())\
            .filter(ee.Filter.inList('system:index', trash).Not())

        # returns  a pattern of band names
        bands = getBandNames(param[3])

        # Rename collection image bands
        collection = collection.select(
            bands['bandNames'],
            bands['newNames']
        )

        # remove clouds and shadows
        collectionWithoutClouds = applyCloudAndShadowMask(collection)

        # ilumination correction
        # collectionWithoutClouds = collectionWithoutClouds.map(iluminationCorrection)

        # returns a collection with the sma, ndfi and csfi calculated
        featureSpaceCollection = getFeatureSpace(collectionWithoutClouds)

        try:
            imageIdList = collection.reduceColumns(
                ee.Reducer.toList(), ['system:index']).get('list').getInfo()
        except:
            imageIdList = []

        print('{} images found'.format(len(imageIdList)))

        for imageId in imageIdList:
            print('[{}] {} Exporting {}...'.format(
                param[4], param[3], imageId))

            try:

                image = ee.Image(featureSpaceCollection.filterMetadata(
                    'system:index', 'equals', imageId).first())

                samplesInTheRegion = samplesLapig.filterBounds(samplesRegion)

                classValues = map(
                    lambda obj: obj['classe'], nSamplesTable)

                print("classValues", classValues)

                # print("samplesInTheRegion", samplesInTheRegion.size().getInfo())

                if samplesInTheRegion.size().getInfo() > 0:
                    classPoints = map(
                        lambda obj: int(obj['nsamples'] * percentRegional), nSamplesTable)

                    # add samples points from reference maps
                    # TODO: balancear essas amostras
                    samplesInTheRegion = samplesInTheRegion.merge(
                        shuffle(samplesRefer.filterBounds(samplesRegion))
                        .limit(100)
                    )

                    segments = getSegments(
                        image.select(segmentsBands), size=16)

                    similarMask = getSimilarMask(segments, samplesInTheRegion)

                    # 70% of regional samples
                    print("nRegionalSamples:", int(nsamples * percentRegional))

                    similarMask = similarMask.rename(['reference'])

                    samplesRegional = similarMask.selfMask().addBands(image)\
                        .stratifiedSample(
                            numPoints=int(nsamples * percentRegional),
                            classBand='reference',
                            region=samplesRegion,
                            scale=30,
                            classValues=classValues,
                            classPoints=classPoints,
                            geometries=True
                    )

                    samplesList = map(lambda obj:
                                      samplesLapig.filterMetadata(
                                          'reference',
                                          'equals',
                                          obj['classe']).limit(int(obj['nsamples'] * percentGlobal)),
                                      nSamplesTable)

                    # get 30% of global samples
                    samplesGlobal = ee.FeatureCollection(samplesList).flatten()

                    samplesTotal = samplesRegional.merge(samplesGlobal)
                else:
                    classPoints = map(
                        lambda obj: int(obj['nsamples'] * 0.3), nSamplesTable)

                    print("classPoints", classPoints)

                    samplesList = map(lambda obj:
                                      samplesLapig.filterMetadata(
                                          'reference',
                                          'equals',
                                          obj['classe']).limit(int(obj['nsamples'])),
                                      nSamplesTable)

                    # get 100% of global samples
                    samplesGlobal = ee.FeatureCollection(samplesList).flatten()

                    # print('samplesGlobal', samplesGlobal.size().getInfo())

                    samplesInTheRegionRefer = shuffle(
                        samplesRefer.filterBounds(samplesRegion)).limit(100)

                    # print('samplesInTheRegionRefer', samplesInTheRegionRefer.size().getInfo())

                    segments = getSegments(
                        image.select(segmentsBands), size=16)

                    similarMask = getSimilarMask(
                        segments, samplesInTheRegionRefer)

                    print("nRegionalSamplesRefer:", int(nsamples))

                    similarMask = similarMask.rename(['reference'])

                    samplesRegionalRefer = similarMask.selfMask().addBands(image)\
                        .stratifiedSample(
                            numPoints=int(nsamples),
                            classBand='reference',
                            region=samplesRegion,
                            scale=30,
                            classValues=classValues,
                            classPoints=classPoints,
                            geometries=True
                    )

                    # pprint(samplesRegionalRefer.first().getInfo())
                    # add samples points from reference maps
                    # TODO: balancear melhor essas amostras
                    samplesTotal = samplesGlobal.merge(samplesRegionalRefer)

                # remove None values
                samplesTotal = samplesTotal.filterMetadata(
                    'gv', 'not_equals', None)

                # image classification
                classification = classify(
                    image,
                    randomForestParams,
                    samplesTotal)

                # set properties
                classification = classification\
                    .set('version', version)\
                    .set('collection', collectionVersion)\
                    .set('biome', biome)

                # export task
                geometry = ee.Image(collection.filterMetadata(
                    'system:index', 'equals', imageId).first()).geometry()

                task = ee.batch.Export.image.toAsset(
                    image=classification.toByte(),
                    description='{}-{}'.format(imageId, version),
                    assetId='{}/{}-{}'.format(outputAsset, imageId, version),
                    pyramidingPolicy={".default": "mode"},
                    region=geometry.getInfo()['coordinates'],
                    scale=pixelSize,
                    # maxPixels=1e+13
                )

                task.start()
            except Exception as e:
                print(e)
