from scrapy.pipelines.images import ImagesPipeline
import scrapy
import hashlib
from scrapy.utils.python import to_bytes
from pymongo import MongoClient


class ExerciselinPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client['Leroy']

    def process_item(self, item, spider):
        collections = self.mongobase[f"{spider.name}_{item['name_base']}"]
        collections.update_one({'_id': {'$eq': item['_id']}}, {'$set': item}, upsert=True)
        return item


class ExerciseImgPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        if item['img']:
            for img in item['img']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)
        return item

    def item_completed(self, results, item, info):
        if results:
            item['img'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        image_name = hashlib.sha1(to_bytes(request.url)).hexdigest()
        if item:
            return f'{item["_id"]}/{image_name}.jpg'
        else:
            return f'full/{image_name}.jpg'
