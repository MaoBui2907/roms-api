

from collections import defaultdict
from urllib.parse import urlparse
import scrapy, toml, hashlib, uuid


from roms.items import RomsItem

with open('./resources/romsgames.toml', 'r') as f:
    config = toml.load(f)

class RomsGamesSpider(scrapy.Spider):
    name = 'romsgames'
    allowed_domains = ['romsgames.net']
    queue_dict = defaultdict(dict)

        
    def start_requests(self):
        start_url = 'http://romsgames.net/roms'
        yield scrapy.Request(start_url, callback=self.parse_category)

    def parse_category(self, response):
        xpath = config.get('Xpath')
        categories = response.xpath(xpath["category_link"]).getall()
        for category in categories:
            yield scrapy.Request(response.urljoin(category), callback=self.parse_rom_list)

    def parse_rom_list(self, response):
        xpath = config.get('Xpath')
        roms = response.xpath(xpath["rom_link"]).getall()
        for rom in roms:
            yield scrapy.Request(response.urljoin(rom), callback=self.parse)

        next_page = response.xpath(xpath["next_page"]).get()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse_rom_list)

    def parse(self, response):
        xpath = config.get('Xpath')
        norm_url = urlparse(response.url)
        item = {
            "id": str(uuid.UUID(hashlib.md5(response.url.encode('utf-8')).hexdigest())),
            "link": response.url,
            "title": response.xpath(xpath["title"]).get().strip(),
            "logo": response.xpath(xpath["logo"]).get().strip(),
            "region": response.xpath(xpath["region"]).get().strip(),
            "category": response.xpath(xpath["category"]).get().strip(),
        }

        if config.get("Run").get("rm_none"):
            if "" in item.values() or [] in item.values() or None in item.values():
                return

        download_url = norm_url.scheme + "://" + norm_url.netloc + '/download' + norm_url.path
        item.update({
            "download_url": download_url
        })
        # self.queue_dict[download_url] = item
        # yield scrapy.Request(download_url, callback=self.parse_download)
        yield RomsItem(**item)

    # def parse_download(self, response):
    #     xpath = config.get('Xpath')
    #     item = self.queue_dict[response.url]
    #     link = response.xpath(xpath["download_link"]).get()
    #     attachment = response.xpath(xpath["download_attachment"]).get()
    #     item.update({
    #         "download_url": "{}?attach={}".format(link, attachment)
    #     })
    #     yield RomsItem(**item)

    