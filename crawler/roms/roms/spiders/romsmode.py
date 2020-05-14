# -*- coding: utf-8 -*-
import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
import toml
from urllib.parse import urlparse
from collections import defaultdict

import azure.cosmos.documents as documents
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.errors as errors


with open('./db.toml', 'r') as f:
    database_config = toml.load(f).get('Database')

with open('./config.toml', 'r') as f:
    config = toml.load(f)


def id_from_url(url: str) -> str:
    out = url.replace(':', '')
    out = out.replace('/', '-')
    return out


def norm_region(region: str) -> str:
    out = region.strip().lower()
    out = out.replace(" ", "")
    return out

class RomsmodeSpider(CrawlSpider):
    name = 'romsmode'

    def __init__(self, cate_id='0', run_config=config.get("Run"), *args, **kwargs):
        super(RomsmodeSpider, self).__init__(*args, **kwargs)
        self.start_urls = run_config["start_urls"]
        self.allowed_domains = run_config["allowed_domains"]
        self.category = run_config["categories"][int(cate_id)]
        self.rm_none = run_config["rm_none"]

        self.client = cosmos_client.CosmosClient(database_config.get("ACCOUNT_URI"), {
            'masterKey': database_config.get("ACCOUNT_KEY")})
        database_id = "Roms"
        roms_container_id = "roms"
        regions_container_id = "regions"
        categories_container_id = "categories"
        self.container_path = "dbs/" + database_id + "/colls/" + roms_container_id
        self.regions_path = "dbs/" + database_id + "/colls/" + regions_container_id

        self.queue_dict = defaultdict(dict)

        RomsmodeSpider.rules = [Rule(LinkExtractor(allow=run_config["allowed_regex"][int(cate_id)],
                                                   deny_extensions=run_config["denied_extensions"]), callback="parse_item", follow=True)]
        super(RomsmodeSpider, self)._compile_rules()

    def parse_item(self, response):
        xpath = config.get('Xpath')
        o = urlparse(response.url)
        record = {
            "id": id_from_url(response.url),
            "link": response.url,
            "category": self.category,
            "title": "".join(response.xpath(xpath['title']).extract()).strip(),
            "region": norm_region("".join(response.xpath(xpath['region']).extract()).strip()),
            "logo": response.xpath(xpath['image']).extract(),
        }
        if self.rm_none:
            if "" in record.values() or [] in record.values():
                return
        download_page = o.scheme + "://" + o.netloc + "/download" + o.path
        self.queue_dict[download_page] = record
        yield Request(download_page, callback=self.parse_file)

    def parse_file(self, response):
        xpath = config.get('Xpath')
        record = self.queue_dict[response.url]
        record.update({
            "file": response.xpath(xpath['download_link']).extract()
        })
        self.client.UpsertItem(self.container_path, record)
        self.client.UpsertItem(self.regions_path, {"id": record.get("region"), "title": record.get("region")})
        del self.queue_dict[response.url]
