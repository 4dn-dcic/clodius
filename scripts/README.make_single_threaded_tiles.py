TEST_NAME=tiles_test

##### Create a directory that will store the tiles and download some datasets to it
mkdir -p ~/data/encode/${TEST_NAME}
cd ~/data/encode/${TEST_NAME}
wget https://s3.amazonaws.com/pkerp/data/encode/hg19/E116-DNase.fc.signal.bigwig.bedGraph.genome.sorted.short.gz
wget https://s3.amazonaws.com/pkerp/data/encode/hg19/wgEncodeCrgMapabilityAlign36mer.bw.genome.sorted.short.gz
wget https://s3.amazonaws.com/pkerp/data/coolers/hg19/Rao2014-GM12878-MboI-allreps-filtered.1kb.cool.reduced.genome.5M.gz

# Go back to the clodius directory
cd -


# Where the tiles will be saved
AWS_ES_DOMAIN=52.23.237.226:9872
#AWS_ES_DOMAIN=127.0.0.1:9872
#TEST_NAME=hg19

# Make sure we're not indexing the directory fields for searching
curl -XDELETE "${AWS_ES_DOMAIN}/${TEST_NAME}"
curl -XPUT "http://${AWS_ES_DOMAIN}/${TEST_NAME}" -d '
{
  "settings": {
    "index.codec": "best_compression"
  },
  "mappings": {
    "_default_": {
        "dynamic_templates": [
            { "notanalyzed": {
                  "match":              "*", 
                  "mapping": {
                      "index":       "no"
                  }
               }
            }
          ]
       }
   }
}'

#########################
# A 1D dataset
#########################


DATASET_NAME=${TEST_NAME}/E116-DNase.fc.signal.bigwig.bedGraph.genome.sorted.short.gz
FILEPATH=~/data/encode/${DATASET_NAME}
curl -XDELETE "${AWS_ES_DOMAIN}/${DATASET_NAME}"

    zcat ${FILEPATH} | /usr/bin/time pypy scripts/make_single_threaded_tiles.py --min-pos 1 --max-pos 5000000 -b 256 -r 1 --expand-range 1,2 --ignore-0 -k 1 -v 3 --elasticsearch-url ${AWS_ES_DOMAIN}/${DATASET_NAME}


########################
# Another 1D dataset
########################
DATASET_NAME=${TEST_NAME}/wgEncodeCrgMapabilityAlign36mer.bw.genome.sorted.short.gz
FILEPATH=~/data/encode/${DATASET_NAME}
curl -XDELETE "${AWS_ES_DOMAIN}/${DATASET_NAME}"

    zcat ${FILEPATH} | pypy scripts/make_single_threaded_tiles.py --min-pos 1 --max-pos 5000000 -b 256 -r 1 --expand-range 1,2 --ignore-0 -k 1 -v 3 --elasticsearch-url ${AWS_ES_DOMAIN}/${DATASET_NAME}


####################################
# A 2D dataset
####################################
    DATASET_NAME=${TEST_NAME}/Rao2014-GM12878-MboI-allreps-filtered.1kb.cool.reduced.genome.5M.gz
    FILENAME=coolers/${DATASET_NAME}
    FILEPATH=~/data/${FILENAME}
    curl -XDELETE "${AWS_ES_DOMAIN}/${DATASET_NAME}"

    zcat ${FILEPATH} | /usr/bin/time pypy scripts/make_single_threaded_tiles.py --min-pos 0,0 --max-pos 5000000,5000000 -b 256 -r 1000 --elasticsearch-url ${AWS_ES_DOMAIN}/${DATASET_NAME}


### End example



AWS_ES_DOMAIN=52.23.165.123:9872
#AWS_ES_DOMAIN=52.23.237.226:9872
TEST_NAME=hg19
# Make sure we're not indexing the directory fields for searching
curl -XDELETE "${AWS_ES_DOMAIN}/${TEST_NAME}"
curl -XPUT "http://${AWS_ES_DOMAIN}/${TEST_NAME}" -d '
{
  "settings": {
    "index.codec": "best_compression"
  },
  "mappings": {
    "_default_": {
        "dynamic_templates": [
            { "notanalyzed": {
                  "match":              "*",
                  "mapping": {
                      "index":       "no"
                  }
               }
            }
          ]
       }
   }
}'

#################################
######################################
######################################
    DATASET_NAME=hg19/Rao2014-GM12878-MboI-allreps-filtered.1kb.cool.reduced.genome.5M.gz
    FILENAME=coolers/${DATASET_NAME}
    FILEPATH=~/data/${FILENAME}
    curl -XDELETE "${AWS_ES_DOMAIN}/${DATASET_NAME}"

    zcat ${FILEPATH} | /usr/bin/time pypy scripts/make_single_threaded_tiles.py --min-pos 0,0 --max-pos 5000000,5000000 -b 256 -r 1000 --elasticsearch-url ${AWS_ES_DOMAIN}/${DATASET_NAME} --triangular


DATASET_NAME=Rao2014-GM12878-MboI-allreps-filtered.1kb.cool.reduced.genome.gz #2,220,472,930 lines
INDEX_NAME=hg19/${DATASET_NAME}
#INDEX_NAME=${DATASET_NAME,,}/tiles
echo $INDEX_NAME
FILENAME=coolers/hg19/${DATASET_NAME}
FILEPATH=~/data/${FILENAME}
#curl -XDELETE "http://${AWS_ES_DOMAIN}/${DATASET_NAME,,}"
zcat ${FILEPATH} | /usr/bin/time pypy scripts/make_single_threaded_tiles.py --min-pos 0,0 --max-pos 3137161264,3137161264 -b 256 -r 1000 --elasticsearch-url ${AWS_ES_DOMAIN}/${INDEX_NAME} --num-threads 4 --triangular --log-file clodius.log # 16:48:26

###############################
    DATASET_NAME=hg19/Dixon2015-H1hESC_ES-HindIII-allreps-filtered.1kb.cool.reduced.genome.5M.gz
    FILENAME=coolers/${DATASET_NAME}
    FILEPATH=~/data/${FILENAME}
    curl -XDELETE "${AWS_ES_DOMAIN}/${DATASET_NAME}"
    zcat ${FILEPATH} | head -n 2 | /usr/bin/time pypy scripts/make_single_threaded_tiles.py --min-pos 0,0 --max-pos 5000000,5000000 -b 256 -r 1000 --elasticsearch-url ${AWS_ES_DOMAIN}/${DATASET_NAME} --triangular

    DATASET_NAME=hg19/Dixon2015-H1hESC_ES-HindIII-allreps-filtered.1kb.cool.reduced.genome.mmmili.gz
    FILENAME=coolers/${DATASET_NAME}
    FILEPATH=~/data/${FILENAME}
    curl -XDELETE "${AWS_ES_DOMAIN}/${DATASET_NAME}"

    zcat ${FILEPATH} | /usr/bin/time pypy scripts/make_single_threaded_tiles.py --min-pos 0,0 --max-pos 3137161264,3137161264 -b 256 -r 1000 --elasticsearch-url ${AWS_ES_DOMAIN}/${DATASET_NAME} --triangular

DATASET_NAME=hg19/Dixon2015-H1hESC_ES-HindIII-allreps-filtered.1kb.cool.reduced.genome.gz
FILENAME=coolers/${DATASET_NAME}
FILEPATH=~/data/${FILENAME}
curl -XDELETE "${AWS_ES_DOMAIN}/${DATASET_NAME}"
zcat ${FILEPATH} | /usr/bin/time pypy scripts/make_single_threaded_tiles.py --min-pos 0,0 --max-pos 3137161264,3137161264 -b 256 -r 1000 --elasticsearch-url ${AWS_ES_DOMAIN}/${DATASET_NAME} --num-threads 4 --triangular

curl -XGET "${AWS_ES_DOMAIN}/hg19/_optimize"

##########################
DATASET_NAME=hg19/Rao2014-HUVEC-MboI-allreps-filtered.5kb.cool.reduced.genome.gz # 239159696 lines
FILENAME=coolers/${DATASET_NAME}
FILEPATH=~/data/${FILENAME}
curl -XDELETE "${AWS_ES_DOMAIN}/${DATASET_NAME}"
zcat ${FILEPATH} | /usr/bin/time pypy scripts/make_single_threaded_tiles.py --min-pos 0,0 --max-pos 3137161264,3137161264 -b 256 -r 1000 --elasticsearch-url ${AWS_ES_DOMAIN}/${DATASET_NAME} --num-threads 4 --triangular

curl -XGET "${AWS_ES_DOMAIN}/hg19/_optimize"

##########################
DATASET_NAME=hg19/Rao2014-HMEC-MboI-allreps-filtered.5kb.cool.reduced.genome.gz # 239159696 lines
FILENAME=coolers/${DATASET_NAME}
FILEPATH=~/data/${FILENAME}
curl -XDELETE "${AWS_ES_DOMAIN}/${DATASET_NAME}"
zcat ${FILEPATH} | /usr/bin/time pypy scripts/make_single_threaded_tiles.py --min-pos 0,0 --max-pos 3137161264,3137161264 -b 256 -r 1000 --elasticsearch-url ${AWS_ES_DOMAIN}/${DATASET_NAME} --num-threads 4 --triangular

curl -XGET "${AWS_ES_DOMAIN}/hg19/_optimize"


#####################
DATASET_NAME=hg19/wgEncodeSydhTfbsGm12878Ctcfsc15914c20StdSig.bigWig.bedGraph.genome.sorted.5M.gz    #42938336
FILEPATH=~/data/encode/${DATASET_NAME}
INDEX_NAME=${DATASET_NAME}

zcat ${FILEPATH} | /usr/bin/time pypy scripts/make_single_threaded_tiles.py --min-pos 1 --max-pos 5000000 -b 256 -r 1 --expand-range 1,2 --ignore-0 -k 1 -v 3 --elasticsearch-url ${AWS_ES_DOMAIN}/${INDEX_NAME}

DATASET_NAME=hg19/wgEncodeSydhTfbsGm12878Ctcfsc15914c20StdSig.bigWig.bedGraph.genome.sorted.gz    #42938336
FILEPATH=~/data/encode/${DATASET_NAME}
INDEX_NAME=${DATASET_NAME}

    #zcat ${FILEPATH} | head -n 100000 | pypy scripts/make_single_threaded_tiles.py --min-pos 1 --max-pos 3137161264 -b 64 -r 1 --expand-range 1,2 --ignore-0 -k 1 -v 3 --elasticsearch-url ${AWS_ES_DOMAIN}/${DATASET_NAME}.5M

zcat ${FILEPATH} | /usr/bin/time pypy scripts/make_single_threaded_tiles.py --min-pos 1 --max-pos 3137161264 -b 256 -r 1 --expand-range 1,2 --ignore-0 -k 1 -v 3 --elasticsearch-url ${AWS_ES_DOMAIN}/${INDEX_NAME}

######################
DATASET_NAME=hg19/E116-DNase.fc.signal.bigwig.bedGraph.genome.sorted.gz #112984973
FILEPATH=~/data/encode/${DATASET_NAME}

zcat ${FILEPATH} | /usr/bin/time pypy scripts/make_single_threaded_tiles.py --min-pos 1 --max-pos 3137161264 -b 256 -r 1 --expand-range 1,2 --ignore-0 -k 1 -v 3 --elasticsearch-url ${AWS_ES_DOMAIN}/${DATASET_NAME}

#####################
DATASET_NAME=hg19/wgEncodeSydhTfbsGm12878Pol2s2IggmusSig.bigWig.bedGraph.genome.sorted.gz
FILEPATH=~/data/encode/${DATASET_NAME}

    #zcat ${FILEPATH} | head -n 100000 | pypy scripts/make_single_threaded_tiles.py --min-pos 1 --max-pos 3137161264 -b 256 -r 1 --expand-range 1,2 --ignore-0 -k 1 -v 3 --elasticsearch-url ${AWS_ES_DOMAIN}/${DATASET_NAME}

zcat ${FILEPATH} | /usr/bin/time pypy scripts/make_single_threaded_tiles.py --min-pos 1 --max-pos 3137161264 -b 256 -r 1 --expand-range 1,2 --ignore-0 -k 1 -v 3 --elasticsearch-url ${AWS_ES_DOMAIN}/${DATASET_NAME}
#####################
DATASET_NAME=hg19/wgEncodeSydhTfbsGm12878InputStdSig.bigWig.bedGraph.genome.sorted.gz
FILEPATH=~/data/encode/${DATASET_NAME}
curl -XDELETE "${AWS_ES_DOMAIN}/${DATASET_NAME}"

    #zcat ${FILEPATH} | tail -n 100 >  /tmp/x
    #cat /tmp/x
    #cat /tmp/x | pypy scripts/make_single_threaded_tiles.py --min-pos 1 --max-pos 3137161264 -b 64 -r 1 --expand-range 1,2 --ignore-0 -k 1 -v 3 --elasticsearch-url ${AWS_ES_DOMAIN}/${DATASET_NAME}

zcat ${FILEPATH} | /usr/bin/time pypy scripts/make_single_threaded_tiles.py --min-pos 1 --max-pos 3137161264 -b 64 -r 1 --expand-range 1,2 --ignore-0 -k 1 -v 3 --elasticsearch-url ${AWS_ES_DOMAIN}/${DATASET_NAME}


###### Gene Annotations

INPUT_FILE=~/data/hg19/genbank-output/refgene-count-minus
DATASET_NAME=hg19/refgene-tiles-minus
OUTPUT_DIR=~/data/${DATASET_NAME}
/usr/bin/time python scripts/make_tiles.py --elasticsearch-nodes ${AWS_ES_DOMAIN} --elasticsearch-path $DATASET_NAME -v count --position genomeTxStart --end-position genomeTxEnd  -c refseqid,chr,strand,txStart,txEnd,genomeTxStart,genomeTxEnd,cdsStart,cdsEnd,exonCount,exonStarts,exonEnds,geneName,count,uid --max-zoom 18 -i count --importance --reverse-importance --max-entries-per-tile 16 $INPUT_FILE 

    #rsync -a --delete blank/ $OUTPUT_DIR; mkdir -p $OUTPUT_DIR; /usr/bin/time python scripts/make_tiles.py -o $OUTPUT_DIR -v count --position genomeTxStart --end-position genomeTxEnd  -c refseqid,chr,strand,txStart,txEnd,genomeTxStart,genomeTxEnd,cdsStart,cdsEnd,exonCount,exonStarts,exonEnds,geneName,count,uid --max-zoom 5 -i count --importance --reverse-importance --max-entries-per-tile 16 $INPUT_FILE 
    #rsync -avzP $OUTPUT_DIR/ ~/projects/goomba/.tmp/jsons/${DATASET_NAME}

INPUT_FILE=~/data/hg19/genbank-output/refgene-count-plus
DATASET_NAME=hg19/refgene-tiles-plus
OUTPUT_DIR=~/data/${DATASET_NAME}

/usr/bin/time python scripts/make_tiles.py --elasticsearch-nodes ${AWS_ES_DOMAIN} --elasticsearch-path $DATASET_NAME -v count --position genomeTxStart --end-position genomeTxEnd  -c refseqid,chr,strand,txStart,txEnd,genomeTxStart,genomeTxEnd,cdsStart,cdsEnd,exonCount,exonStarts,exonEnds,geneName,count,uid --max-zoom 18 -i count --importance --reverse-importance --max-entries-per-tile 16 $INPUT_FILE 

















#####################
DATASET_NAME=hg19/wgEncodeSydhTfbsGm12878Rad21IggrabSig.bigWig.bedGraph.genome.sorted.gz
FILEPATH=~/data/encode/${DATASET_NAME}
curl -XDELETE "${AWS_ES_DOMAIN}/${DATASET_NAME}"

    zcat ${FILEPATH} | head -n 10000 | pypy scripts/make_single_threaded_tiles.py --min-pos 1 --max-pos 3137161264 -b 64 -r 1 --expand-range 1,2 --ignore-0 -k 1 -v 3 --elasticsearch-url ${AWS_ES_DOMAIN}/${DATASET_NAME}

zcat ${FILEPATH} | /usr/bin/time pypy scripts/make_single_threaded_tiles.py --min-pos 1 --max-pos 3137161264 -b 64 -r 1 --expand-range 1,2 --ignore-0 -k 1 -v 3 --elasticsearch-url search-higlass-ssxwuix6kow3sekyeresi7ay5e.us-east-1.es.amazonaws.com/${DATASET_NAME}        # 7:42:23

#####################
DATASET_NAME=hg19/wgEncodeCrgMapabilityAlign36mer.bw.genome.sorted.gz
FILEPATH=~/data/encode/${DATASET_NAME}
curl -XDELETE "${AWS_ES_DOMAIN}/${DATASET_NAME}"

    #zcat ${FILEPATH} | head -n 1000 | pypy scripts/make_single_threaded_tiles.py --min-pos 1 --max-pos 3137161264 -b 64 -r 1 --expand-range 1,2 --ignore-0 -k 1 -v 3 --elasticsearch-url ${AWS_ES_INSTANCE}/${DATASET_NAME}

zcat ${FILEPATH} | /usr/bin/time pypy scripts/make_single_threaded_tiles.py --min-pos 1 --max-pos 3137161264 -b 256  -r 1 --expand-range 1,2 --ignore-0 -k 1 -v 3 --elasticsearch-url search-higlass-ssxwuix6kow3sekyeresi7ay5e.us-east-1.es.amazonaws.com/${DATASET_NAME}        # 5:52:04

curl -XGET "http://${AWS_ES_DOMAIN}/hg19/_mapping"

curl -XDELETE "http://${AWS_ES_DOMAIN}/hg19"
curl -XPUT "http://${AWS_ES_DOMAIN}/hg19" -d '
{
  "settings": {
    "index.codec": "best_compression"
  },
  "mappings": {
    "_default_": {
        "dynamic_templates": [
            { "notanalyzed": {
                  "match":              "*", 
                  "mapping": {
                      "index":       "no"
                  }
               }
            }
          ]
       }
   }
}'
