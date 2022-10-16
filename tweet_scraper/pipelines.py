import json
import logging
import os
from s3fs import S3FileSystem

from scrapy.utils.project import get_project_settings

from tweet_scraper.items import Tweet, User
from tweet_scraper.utils import mkdirs

logger = logging.getLogger(__name__)
SETTINGS = get_project_settings()


class SaveToFilePipeline(object):
    """ pipeline that save data to disk """

    def __init__(self):
        self.save_tweet_path = SETTINGS['SAVE_TWEET_PATH']
        self.save_user_path = SETTINGS['SAVE_USER_PATH']
        mkdirs(self.save_tweet_path)  # ensure the path exists
        mkdirs(self.save_user_path)

    def process_item(self, item, spider):
        if isinstance(item, Tweet):
            save_path = os.path.join(self.save_tweet_path, item['id_'])
            if os.path.isfile(save_path):
                pass  # simply skip existing items
                # logger.debug("skip tweet:%s"%item['id_'])
                # or you can rewrite the file, if you don't want to skip:
                # self.save_to_file(item,savePath)
                # logger.debug("Update tweet:%s"%item['id_'])
            else:
                self.save_to_file(item, save_path)
                logger.debug("Add tweet:%s" % item['id_'])

        elif isinstance(item, User):
            save_path = os.path.join(self.save_user_path, item['id_'])
            if os.path.isfile(save_path):
                pass  # simply skip existing items
                # logger.debug("skip user:%s"%item['id_'])
                # or you can rewrite the file, if you don't want to skip:
                # self.save_to_file(item,savePath)
                # logger.debug("Update user:%s"%item['id_'])
            else:
                self.save_to_file(item, save_path)
                logger.debug("Add user:%s" % item['id_'])

        else:
            logger.info("Item type is not recognized! type = %s" % type(item))

    @staticmethod
    def save_to_file(item, fname):
        """ input:
                item - a dict like object
                fname - where to save
        """
        s3 = S3FileSystem(anon=False, key=SETTINGS['ACCESS_KEY_ID'], secret=SETTINGS['SECRET_ACCESS_KEY'])
        with s3.open(fname, 'w', region='us-east-1') as file:
            json.dump(dict(item), file, ensure_ascii=False)
