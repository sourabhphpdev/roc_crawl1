from scrapy.utils import project
from scrapy.utils.project import get_project_settings as Settings
from scrapy.crawler import CrawlerProcess
from scrapy import signals
from scrapy.spiders import CrawlSpider
from pydispatch import dispatcher
import os, json
from collections import defaultdict
from scrapy import spiderloader

import logging

path_to_scraper_output = 'licensed_HMO_Scraper/spider_output/'

class SpiderPostExecution(CrawlSpider):
    def __init__(self):
        dispatcher.connect(self.engine_stopped, signals.engine_stopped)

    def engine_stopped(self, spider_objects=None):
        if not spider_objects:
            json_files = [pos_json
                          for pos_json in os.listdir(path_to_scraper_output)
                          if pos_json.endswith('.json')]
        else:
            json_files = [spider_object + '.json'
                          for spider_object in spider_objects]

        for json_file in json_files:
            data = {}
            file_path = 'licensed_HMO_Scraper/spider_output/{}'.format(json_file)
            district_data = defaultdict(dict)

            with open(file_path) as json_data:
                try:
                    data = json.load(json_data)
                except:
                    continue

                data = sorted(data, key = lambda i: i['property_address'])

                district_name = json_file.split('.')[0].upper()
                district_data[district_name] = data

            with open(file_path, 'w') as f:
                json.dump(district_data, f)

def run_spiders():
    settings = Settings()

    process = CrawlerProcess(settings)

    spider_loader = spiderloader.SpiderLoader.from_settings(settings)
    spiders = spider_loader.list()
    spider_objects = [spider_loader.load(name) for name in spiders]

    exec_report.number_of_scrapers = len(spider_objects)

    for spider in spider_objects:
        process.crawl(spider)

    process.start()

    post_execution = SpiderPostExecution()
    post_execution.engine_stopped(spider_objects)


def run_spider(spider_name):
    settings = Settings()

    process = CrawlerProcess(settings)

    spider_loader = spiderloader.SpiderLoader.from_settings(settings)

    try:
        spider_object = spider_loader.load(spider_name)

        process.crawl(spider_object)

        process.start()

        post_execution = SpiderPostExecution()
        post_execution.engine_stopped([spider_object])
    except Exception as e:
        raise(e)


def run_single_spider(spider_name,cin):
    settings = Settings()

    process = CrawlerProcess(settings)

    spider_loader = spiderloader.SpiderLoader.from_settings(settings)

    try:
        spider_object = spider_loader.load(spider_name,cin=cin)

        process.crawl(spider_object)

        process.start()

        # post_execution = SpiderPostExecution()
        # post_execution.engine_stopped([spider_object])
    except Exception as e:
        raise (e)


if __name__ == '__main__':
    run_spiders()
