#!/bin/bash


QUERY=""

if [ ! -z $1 ]
then
    QUERY=$*
fi

echo "Start with query :: |${QUERY}|"

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd ${DIR}
/usr/local/bin/scrapy crawl yanews -a keywords="${QUERY}" &> ${DIR}'/logs/out.log'
#/usr/local/bin/scrapy crawl yanews -a keywords="${QUERY}"

