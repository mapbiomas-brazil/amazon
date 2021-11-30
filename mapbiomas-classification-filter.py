# coding: utf-8
import ee
import csv
import sys
import os
import random

from pprint import pprint

sys.dont_write_bytecode = True

ee.Initialize()

rulesTable = './csv/temporal-filter-rules.csv'

assetScenes = 'projects/mapbiomas-workspace/AUXILIAR/cenas-landsat'

version = '5'
outputVersion = '7'
#
# temporal filter parameters
#
params = {
    'biome': "AMAZONIA",

    'version': version,

    "rulesTable": rulesTable,

    "asset": {
        "classificacao": "projects/imazon-simex/LULC/integration-scenes",
        "classificacaoft": "projects/imazon-simex/LULC/integration-scenes-ft",
    },

    'years': [
        '1985','1986','1987','1988',
        '1989','1990','1991','1992',
        '1993','1994','1995','1996',
        '1997','1998','1999','2000',
        '2001','2002','2003','2004',
        '2005','2006','2007','2008',
        '2009','2010','2011','2012',
        '2013','2014','2015','2016',
        '2017','2018','2019'
    ]
}

#
# spatial filter parameters
#

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


pathRows = [
    "233/58",
    "232/58"
]

scenes = ee.FeatureCollection(assetScenes)\
    .filter(
        ee.Filter.inList(
            'SPRNOME',
            pathRows
        )
)


class TemporalFilter(object):

    # default options
    options = {

        "rulesTable": None,

        "asset": {
            "classificacao": None,
            "classificacaoft": None,
        },

        "ft_rules": {},

        'years': []

    }

    def __init__(self, params):

        self.params = params

        self.options.update(params)

        self.loadRules()

    def readTable(self):
        """Read parameters table"""

        table = []

        with open(self.options['rulesTable']) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                table.append({
                    'rule': row['rule'],
                    'type': row['type'],
                    'kernel': int(row['kernel']),
                    'active': int(row['active']),
                    'biome': row['biome'],
                    'notes': row['notes'],
                    'tminus2': row['tminus2'],
                    'tminus1': row['tminus1'],
                    't': row['t'],
                    'tplus1': row['tplus1'],
                    'tplus2': row['tplus2'],
                    'result': row['result'],
                })

        return table

    def loadRules(self):

        table = self.readTable()

        self.options['ft_rules'] = {
            'rpk3': filter(lambda rule:
                           rule['type'] == 'RP' and rule['kernel'] == 3,
                           table
                           ),
            'rgk3': filter(lambda rule:
                           rule['type'] == 'RG' and rule['kernel'] == 3,
                           table
                           ),
            'ruk3': filter(lambda rule:
                           rule['type'] == 'RU' and rule['kernel'] == 3,
                           table
                           ),
            'rpk5': filter(lambda rule:
                           rule['type'] == 'RP' and rule['kernel'] == 5,
                           table
                           ),
            'rgk5': filter(lambda rule:
                           rule['type'] == 'RG' and rule['kernel'] == 5,
                           table
                           ),
            'ruk5': filter(lambda rule:
                           rule['type'] == 'RU' and rule['kernel'] == 5,
                           table
                           )
        }

        # pprint(self.options['ft_rules'])

    def list2multband(self, imageList):

        image = ee.List(imageList) \
            .iterate(
                lambda band, image:
                    ee.Image(image).addBands(band), ee.Image().select()
                )

        return ee.Image(image)

    def noData2NotObserved(self, image):
        """
        Reclassify the no data value to not observed class value
        """
        image = image.unmask()
        image = image.where(image.eq(0), 27)

        return image

    def applyRuleKernel3(self, imageList, rule, kernelIds, ruleId):

        exp = "((img1==%s) and (img2==%s) and (img3==%s))" % (
            rule['tminus1'], rule['t'], rule['tplus1'])
        
        mask = imageList[ruleId].expression(exp, {
            'img1': imageList[kernelIds[0]],
            'img2': imageList[kernelIds[1]],
            'img3': imageList[kernelIds[2]]
        })

        image = imageList[ruleId].where(mask.eq(1), int(rule['result']))

        return image

    def applyRuleKernel5(self, imageList, rule, kernelIds, ruleId):

        exp = "(img1==%s) and (img2==%s) and (img3==%s) and (img4==%s) and (img5==%s)" % (
            rule['tminus2'], rule['tminus1'], rule['t'], rule['tplus1'], rule['tplus2'])

        mask = imageList[ruleId].expression(exp, {
            'img1': imageList[kernelIds[0]],
            'img2': imageList[kernelIds[1]],
            'img3': imageList[kernelIds[2]],
            'img4': imageList[kernelIds[3]],
            'img5': imageList[kernelIds[4]]
        })

        image = imageList[ruleId].where(mask.eq(1), int(rule['result']))

        return image

    def applyRules(self):

        imageList = []

        for year in self.options['years']:

            image = ee.ImageCollection(self.params['asset']['classificacao']) \
                .filterMetadata('year', 'equals', int(year)) \
                .filterMetadata('version', 'equals', version) \
                .filter(ee.Filter.stringContains('system:index', '23258').Not()) \
                .min() \
                .rename('classification_' + year)
            
            image = self.noData2NotObserved(image)

            imageList.append(image)
        
        n = len(self.options['years'])

        # rules kernel 5
        for rule in self.options['ft_rules']['rpk5']:
            imageList[0] = self.applyRuleKernel5(
                imageList,
                rule,
                [0, 1, 2, 3, 4],
                0
            )

        for i in range(2, n-3):
            for rule in self.options['ft_rules']['rgk5']:
                imageList[i] = self.applyRuleKernel5(
                    imageList,
                    rule,
                    [i-2, i-1, i, i+1, i+2],
                    i
                )

        for rule in self.options['ft_rules']['ruk5']:
            imageList[n-1] = self.applyRuleKernel5(
                imageList,
                rule,
                [n-5, n-4, n-3, n-2, n-1],
                n-1
            )

        # rules kernel 3
        for rule in self.options['ft_rules']['rpk3']:
            imageList[0] = self.applyRuleKernel3(
                imageList,
                rule,
                [0, 1, 2],
                0
            )

        for i in range(1, n-2):
            for rule in self.options['ft_rules']['rgk3']:
                imageList[i] = self.applyRuleKernel3(
                    imageList,
                    rule,
                    [i-1, i, i+1],
                    i
                )

        for rule in self.options['ft_rules']['ruk3']:
            imageList[n-1] = self.applyRuleKernel3(
                imageList,
                rule,
                [n-3, n-2, n-1],
                n-1
            )

        filtered = self.list2multband(imageList)

        return filtered

#
#  Classe de pos-classificação para reduzir ruídos na imagem classificada
#
#  @param {ee.Image} image [eeObjeto imagem de classificação]
#
#  @example
#  var image = ee.Image("aqui vem a sua imagem");
#  var filterParams = [
#      {classValue: 1, maxSize: 3},
#      {classValue: 2, maxSize: 5}, // o tamanho maximo que o mapbiomas está usado é 5
#      {classValue: 3, maxSize: 5}, // este valor foi definido em reunião
#      {classValue: 4, maxSize: 3},
#      ];
#  var pc = new PostClassification(image);
#  var filtered = pc.spatialFilter(filterParams);
#


class PostClassification(object):

    def __init__(self, image):

        self.image = ee.Image(image)

    def _majorityFilter(self, params):

        # Generate a mask from the class value
        classMask = self.image.eq(params['classValue'])

        # Labeling the group of pixels until 100 pixels connected
        labeled = classMask.mask(classMask).connectedPixelCount(100, True)

        # Select some groups of connected pixels
        region = labeled.lt(params['maxSize'])

        # Squared kernel with size shift 1
        # [[p(x-1,y+1), p(x,y+1), p(x+1,y+1)]
        # [ p(x-1,  y), p( x,y ), p(x+1,  y)]
        # [ p(x-1,y-1), p(x,y-1), p(x+1,y-1)]
        kernel = ee.Kernel.square(1)

        # Find neighborhood
        neighs = self.image.neighborhoodToBands(kernel).mask(region)

        # Reduce to majority pixel in neighborhood
        majority = neighs.reduce(ee.Reducer.mode())

        # Replace original values for new values
        filtered = self.image.where(region, majority)

        return filtered.byte()

    #
    # Método para reclassificar grupos de pixels de mesma classe agrupados
    # @param  {list<dictionary>} filterParams [{classValue: 1, maxSize: 3},{classValue: 2, maxSize: 5}]
    # @return {ee.Image}  Imagem classificada filtrada
    #
    def spatialFilter(self, filterParams):

        for params in filterParams:
            self.image = self._majorityFilter(params)

        return self.image


def cloudSeriesFilter(image, bandNames):

    bandNames = list(
        map(lambda year: "classification_" + year, bandNames))

    bandNames1 = ee.List(list(reversed(bandNames)))

    # Corrige os primeiros anos. Aplica o filtro de tras pra frente
    filtered = ee.List(bandNames1).slice(1).iterate(
        lambda bandName, previousImage:
            image.select(ee.String(bandName)).where(
                image.select(ee.String(bandName)).eq(27),
                ee.Image(previousImage).select([0])
            ).addBands(ee.Image(previousImage)),
        ee.Image(image.select(['classification_2019']))
    )

    filtered = ee.Image(filtered)

    # Corrige os ultimos anos. Aplica o filtro da frente pra tras
    filtered2 = ee.List(bandNames).slice(1).iterate(
        lambda bandName, previousImage:
            ee.Image(previousImage).addBands(
                filtered.select(ee.String(bandName)).where(
                    filtered.select(ee.String(bandName)).eq(27),
                    ee.Image(previousImage).select(ee.Image(previousImage).bandNames().length().subtract(1)))),
        ee.Image(filtered.select(['classification_1985']))
    )

    filtered2 = ee.Image(filtered2)

    return filtered2


def applySpatialFilter(nextImage, image):

    pc = PostClassification(nextImage)

    spatialFiltered = pc.spatialFilter(filterParams)

    return ee.Image(image).addBands(ee.Image(spatialFiltered))


for pathRow in pathRows:

    imageName = pathRow.replace('/', '').replace('00', '') + '-' + outputVersion
    
    tf = TemporalFilter(params)

    # Temporal filter collection
    filtered = tf.applyRules()
    
    filtered = ee.Image(filtered)

    filtered = cloudSeriesFilter(filtered, params['years'])

    filtered = filtered.set('version', outputVersion)

    geometry = scenes.filterMetadata('SPRNOME', 'equals', pathRow).first().geometry()

    task = ee.batch.Export.image.toAsset(
        filtered.toByte().clip(geometry.buffer(500)),
        description=imageName,
        assetId=params['asset']['classificacaoft'] + '/' + imageName,
        region=geometry.buffer(500).bounds().getInfo()['coordinates'],
        scale=30,
        pyramidingPolicy={".default": "mode"},
        # maxPixels=1e+13
    )

    task.start()
