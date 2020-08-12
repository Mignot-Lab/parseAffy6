import gzip
import argparse
from collections import defaultdict
#def parseAffy(affyFile, outPre):
affyFile = 'raw/plate28_29.txt.gz'
outPre ='data/Plates28_29_Processed'
pedF = open(outPre+'.ped', 'w')
mapF = open(outPre+'.map', 'w')
sampleList = ''
sampleOrder = defaultdict(str)
rsidOrder =list()
genoCalls = defaultdict(str)
with gzip.open(affyFile, 'rt') as inFile:
    for n, line in enumerate(inFile):
        if n % 10000 == 0:
            print('PROCESSED {} SNPS'.format(n))
        if n > 3:
            #print(line)
            parseLine = line.strip().split('\t')
            if len(parseLine) == len(sampleList):
                rsidInfo = '{} {} 0 {}'.format(parseLine[chrInd], parseLine[rsId], parseLine[bp])
                mapF.write(rsidInfo+'\n')
                for j, call in enumerate(parseLine):
                    if j >0 and j < len(sampleList)-3: ## retreiive sample key
                        sampleName = sampleOrder.get(j)
                        if call == '---':
                            call = '00'
                        for geno in call:
                            genoCalls[sampleName] += geno+' '
            else:
                print('SKIPPING {}'.format(parseLine[0]))
            
        elif n ==3: ## sampleNames
            sampleList =line.strip().split('\t')
            chrInd = len(sampleList)-2
            rsId = len(sampleList)-3
            bp = len(sampleList)-1
            for j, id in enumerate(sampleList):
                if j > 0 and j < len(sampleList)-3:
                    idParse = '_'.join(id.split('.')[0].split('_')[:4])
                    sampleOrder[j] = idParse
    mapF.close()
