#!/bin/bash


QUERY=""

if [ ! -z $1 ]
then
    QUERY=$*
fi

echo "Start with query :: |${QUERY}|"

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo ${DIR}

#cd ${DIR}
#/usr/local/bin/scrapy crawl yanews -a keywords="${QUERY}" --logfile='out.log'

