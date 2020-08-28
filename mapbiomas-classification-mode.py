# -*- coding: utf-8 -*-
import ee
import sys
import os

sys.dont_write_bytecode = True

ee.Initialize()

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

trash = [
    "LT05_231067_19850823", "LT05_231067_19850908", "LT05_231068_19850823", "LT05_231068_19850908",
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
    "LE07_224068_20190201", "LE07_225068_20190208", "LE07_225068_20190312", "LE07_224068_20190422",
    "LC08_224068_20190414", "LC08_224068_20190430", "LE07_224068_20190508", "LE07_224068_20190913",
    "LE07_225068_20190920", "LE07_224068_20191116", "LC08_224068_20191108", "LE07_224068_20191218",
    "LC08_001062_20191029", "LC08_224066_20190905", "LE07_224067_20190828", "LE07_224066_20190913",
    "LC08_224067_20190921", "LC08_224066_20191023", "LC08_224066_20191007", "LE07_224066_20191031",
    "LC08_224066_20191124", "LE07_224066_20191202", "LC08_224067_20191210", "LC08_224066_20191108",
    "LC08_224067_20191023", "LE07_224066_20190828", "LC08_224067_20190804", "LE07_224066_20190812",
    "LE07_224066_20190727", "LC08_224066_20190719", "LE07_224066_20190625", "LC08_224066_20190703",
    "LE07_224066_20190609", "LE07_224067_20190609", "LC08_224066_20190617", "LC08_224066_20190601",
    "LE07_224066_20190524", "LE07_224066_20190508", "LE07_224066_20190422", "LE07_224067_20190422",
    "LC08_224066_20190430", "LC08_224067_20190430", "LC08_233058_20190107", "LE07_233058_20190320",
    "LC08_233058_20190328", "LE07_233058_20190405", "LC08_233058_20190429", "LC08_233058_20191107",
    "LC08_233058_20190819", "LC08_233058_20191006", "LE07_233058_20191014", "LE07_233058_20191030",

]

classification = ee.ImageCollection(assetClassification)\
    .filterMetadata('version', 'equals', version)

alredyInCollection = ee.ImageCollection(assetOutput)\
    .filterMetadata('version', 'equals', outputVersion)\
    .reduceColumns(
        ee.Reducer.toList(),
        ['system:index'])\
    .get('list').getInfo()

biomes = ee.Image(assetBiomes)

nAllObs = classification.reduce(ee.Reducer.count())

# toda a serie
fnnfFrequency = classification.map(
    lambda image: image.eq(13)) \
    .reduce(ee.Reducer.sum()) \
    .divide(nAllObs)\
    .multiply(100)

# toda a serie
allForestFrequency = classification.map(
    lambda image: image.eq(3))\
    .reduce(ee.Reducer.sum())\
    .divide(nAllObs)\
    .multiply(100)

# toda a serie
allPastureFrequency = classification.map(
    lambda image: image.eq(15)) \
    .reduce(ee.Reducer.sum()) \
    .divide(nAllObs) \
    .multiply(100)

scenes = ee.FeatureCollection(assetScenes)

for year in years:
    for pathrow in pathRows:

        name = "{}-{}-{}".format(pathrow.replace('/', ''), year, outputVersion)

        if name not in alredyInCollection:
            scene = scenes \
                .filter(
                    ee.Filter.inList('SPRNOME', [pathrow])
                )

            try:

                sceneCentroid = scene.map(
                    lambda scene:
                        scene.centroid().copyProperties(scene)
                )

                classificationyear = classification \
                    .filterDate(year + '-01-01', year + '-12-31') \
                    .filterBounds(sceneCentroid.geometry()) \
                    .filter(ee.Filter.inList('system:index', trash).Not())

                geometry = ee.Feature(scene.first()).geometry().buffer(1000)

                mode = classificationyear.mode()

                nObs = classificationyear \
                    .filterBounds(sceneCentroid.geometry())\
                    .reduce(ee.Reducer.count())

                agriculFrequency = classificationyear.map(
                    lambda image: image.eq(19)) \
                    .reduce(ee.Reducer.sum())

                pastureFrequency = classificationyear.map(
                    lambda image: image.eq(15)) \
                    .reduce(ee.Reducer.sum())

                forestFrequency = classificationyear.map(
                    lambda image: image.eq(3)) \
                    .reduce(ee.Reducer.sum())

                # frequency (pasture) >= 1 and number of observations <= 7
                modeAdj = mode.where(nObs.lte(7).And(
                    pastureFrequency.gte(2)), 15)

                # frequency (pasture) >= 2 and number of observations <= 10 // tem gerado muito ruido
                # modeAdj = modeAdj.where(nObs.gt(5).and(nObs.lte(20)).and(pastureFrequency.gte(3)), 15);

                # frequency (pasture) >= 10 and number of observations > 20
                modeAdj = modeAdj.where(
                    nObs.gt(20).And(pastureFrequency.gte(10)), 15)

                # mode = mode.where(pastureFrequency.gte(2).and(forestFrequency.gte(12)), 7); // ainda em teste
                # mode = mode.where(allForestFrequency.lte(20).and(fnnfFrequency.gte(50)), 15); // ainda em teste

                # frequency (agriculture) >= 3 and mode == 3
                modeAdj = modeAdj.where(
                    agriculFrequency.gte(3).And(mode.eq(3)), 15)

                # frequency (agriculture) >= 3 and mode == 15
                modeAdj = modeAdj.where(
                    agriculFrequency.gte(3).And(mode.eq(15)), 19)

                # frequency (forest or pasture) >= 50 and mode == 15
                modeAdj = modeAdj.where((allForestFrequency.add(
                    allPastureFrequency).gt(50)).And(mode.eq(13)), 15)

                # frequency (fnnf) >= 50
                modeAdj = modeAdj.where(fnnfFrequency.gt(50), 13)

                modeAdj = modeAdj.mask(biomes.eq(1))

                modeAdj = modeAdj.rename(['classification'])

                modeAdj = modeAdj.set('version', outputVersion).set(
                    'year', int(year))

                task = ee.batch.Export.image.toAsset(
                    image=modeAdj.toByte().selfMask(),
                    description=name,
                    assetId="{}/{}".format(assetOutput, name),
                    pyramidingPolicy={".default": "mode"},
                    region=geometry.getInfo()['coordinates'],
                    scale=30,
                    # maxPixels=1e+13
                )

                task.start()
            except:
                print('error!')
