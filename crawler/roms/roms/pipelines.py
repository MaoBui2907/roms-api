# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
from pprint import pprint
from azure.cosmos import cosmos_client, PartitionKey

from roms.items import RomsItem

class RomsPipeline:
    def process_item(self, item, spider):
        # pprint(item)
        return item

class StoreToDatabase:
    def __init__(self) -> None:
        COSMOSDB_ACCOUNT_URI = os.environ.get("COSMOSDB_ACCOUNT_URI")
        COSMOSDB_ACCOUNT_KEY = os.environ.get("COSMOSDB_ACCOUNT_KEY")
        COSMOSDB_DATABASE_ID = os.environ.get("COSMOSDB_DATABASE_ID")

        self.client = cosmos_client.CosmosClient(
            COSMOSDB_ACCOUNT_URI, {'masterKey': COSMOSDB_ACCOUNT_KEY}
        )
        self.database = self.client.create_database_if_not_exists(COSMOSDB_DATABASE_ID)
        self.roms_container = self.database.create_container_if_not_exists(
            id="roms",
            partition_key=PartitionKey(path="/roms"),
            offer_throughput=400
        )
        self.region_container = self.database.create_container_if_not_exists(
            id="regions",
            partition_key=PartitionKey(path="/regions"),
            offer_throughput=400
        )
        self.categories_container = self.database.create_container_if_not_exists(
            id="categories",
            partition_key=PartitionKey(path="/category"),
            offer_throughput=400
        )

    def process_item(self, item: RomsItem, spider):
        self.roms_container.upsert_item(dict(item))
        self.region_container.upsert_item({
            "id": item["region"],
            "title": item["region"]
        })
        self.categories_container.upsert_item({
            "id": item["category"],
            "title": item["category"]
        })
        return item