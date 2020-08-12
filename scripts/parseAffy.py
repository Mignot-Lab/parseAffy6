import gzip
import argparse

def gzipHandle(fileName):
    if '.gz' in fileName:
        fileOut = gzip.open(fileName, 'rt')
    else:
        fileOut = open(fileName, 'rt')
    return fileOut

def parseAffy(affyFile, outPre):
    pedF = open(outPre+'.tped', 'w')
    famF = open(outPre+'.tfam', 'w')
    posSeen =set()
    sampleList = ''
    inFile = gzipHandle(affyFile)
    for n, line in enumerate(inFile):
        if n % 100000 == 0:
            print('PROCESSED {} SNPS'.format(n))
        if n > 3:
            #print(line)
            parseLine = line.strip().split('\t')
            if len(parseLine) == len(sampleList):
                rsidInfo = '{} {} 0 {}'.format(parseLine[chrInd], parseLine[rsId], parseLine[bp])
                chrPos = '{}_{}'.format(parseLine[chrInd],parseLine[bp])
                rsid = parseLine[rsId]
            if chrPos not in posSeen and rsid not in posSeen:
                pedOut = [rsidInfo]
                for j, call in enumerate(parseLine):
                    if j >0 and j < len(sampleList)-3: ## retreiive sample key
                        if call == '---':
                            call = '00'
                        pedOut.append(' '.join(list(call)))
                pedF.write(' '.join(pedOut).strip()+'\n')
                posSeen.add(chrPos)
                posSeen.add(rsid)
        elif n ==3: ## sampleNames
            sampleList =line.strip().split('\t')
            chrInd = len(sampleList)-2
            rsId = len(sampleList)-3
            bp = len(sampleList)-1
            for j, id in enumerate(sampleList):
                if j > 0 and j < len(sampleList)-3:
                    idParse = '_'.join(id.split('.')[0].split('_')[:4])
                    famF.write('{} {} {} {} {} {}\n'.format(idParse, idParse, 0, 0, 0, 0))
            famF.close()
    pedF.close()
    print('PROCESSED {} GENOS AND {}.tped WRITTEN'.format(n, outPre))

def main():
    parser = argparse.ArgumentParser(description='A script to convert affy export to tped plink')
    parser.add_argument('-A', help='Affymetrix SNP report', required=True)
    parser.add_argument('-O', help='Output prefix', required=True)
    args =parser.parse_args()
    affyFile = args.A
    outPre =args.O
    parseAffy(affyFile, outPre)

if __name__ == "__main__":main()