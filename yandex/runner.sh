#!/bin/bash


QUERY=""

if [ ! -z $1 ]
then
    QUERY=$*
fi

echo "Start with query :: |${QUERY}|"

#/usr/local/bin/scrapy crawl yanews -a keywords="${QUERY}" --logfile='spiders.log'
/usr/local/bin/scrapy crawl yanews -a keywords="${QUERY}"

