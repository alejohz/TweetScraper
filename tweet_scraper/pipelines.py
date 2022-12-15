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
            save_path = os.path.join(self.save_tweet_path, 'tweets.json')
            self.save_to_file(item, save_path)
            logger.debug("Add tweet:%s" % item['id_'])

        elif isinstance(item, User):
            save_path = os.path.join(self.save_user_path, 'users.json')
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
        if not s3.exists(fname):
            with s3.open(fname, 'w', region='us-east-1') as file:
                json.dump([{}], file)
        with s3.open(fname, 'r', encoding='utf-8', region='us-east-1') as file:
            org_file = json.load(file)
            org_file.append(dict(item))
        if not any(d.get('id_') == item['id_'] for d in org_file):
            return None
        with s3.open(fname, 'w', encoding='utf-8', region='us-east-1') as file:
            json.dump(org_file, file, ensure_ascii=False)
