#!/bin/bash

for i in {0..101..1}
do
    scrapy crawl romsmode -a cate_id=$i
done