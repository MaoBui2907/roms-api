#!/bin/bash

for i in {89..101..1}
do
    scrapy crawl romsmode -a cate_id=$i
done