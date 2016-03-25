import json
from datetime import datetime
import httpretty
from django.test import TestCase
from django.utils.six import BytesIO
from flickr_pony.storage import FlickrStorage, FileNotFound, FileSaveError
from . import fixtures

API_KEY = 'cac50045e7cc97328169ed50602fac4d'
API_SECRET = 'a5aaa065af3900d4'
OAUTH_TOKEN = '72157665729827041199006029242ec38d'
OAUTH_TOKEN_SECRET = '44b83f7ef19c6728'
USER_ID = '06509042@N00'

BAD_FILE_ID = '424242'


class BaseFlickrTestCase(TestCase):
    def setUp(self):
        def _api_callback(request, uri, headers):
            code = 200
            method = request.querystring['method'][0]
            if method == 'flickr.people.getPublicPhotos':
                body = fixtures.GET_PUBLIC_PHOTOS
            elif method == 'flickr.photos.getInfo':
                if request.querystring['photo_id'][0] == BAD_FILE_ID:
                    body = fixtures.GET_PHOTO_NOT_FOUND
                else:
                    body = fixtures.GET_PHOTO
            return (code, headers, body)

        def _upload_callback(request, uri, headers):
            code = 200
            if request.querystring['title'][0] == 'EMPTY_FILE':
                body = fixtures.UPLOAD_FILESIZE_ERROR
            else:
                body = fixtures.UPLOAD_OK
            return (code, headers, body)

        httpretty.enable()
        httpretty.register_uri(httpretty.GET, FlickrStorage.API_ENDPOINT,
                               body=_api_callback,
                               content_type='text/json')
        httpretty.register_uri(httpretty.POST, FlickrStorage.API_POST_URL,
                               body=_upload_callback)
        self.storage = FlickrStorage(api_key=API_KEY,
                                     api_secret=API_SECRET,
                                     oauth_token=OAUTH_TOKEN,
                                     oauth_token_secret=OAUTH_TOKEN_SECRET,
                                     user_id=USER_ID)

    def tearDown(self):
        httpretty.disable()
        httpretty.reset()


class FlickrListdirTest(BaseFlickrTestCase):
    def test_listdir(self):
        urls = self.storage.listdir(USER_ID)
        self.assertFalse(urls[0])
        self.assertTrue(urls[1])
        for url in urls[1]:
            self.assertTrue(url.startswith('https://'))

    def test_no_path_and_user_id(self):
        urls = self.storage.listdir()
        user_urls = self.storage.listdir(USER_ID)
        self.assertEqual(urls, user_urls)

    def test_no_path_and_no_user_id(self):
        self.storage = FlickrStorage(api_key=API_KEY,
                                     api_secret=API_SECRET,
                                     oauth_token=OAUTH_TOKEN,
                                     oauth_token_secret=OAUTH_TOKEN_SECRET)
        self.assertRaises(ValueError, self.storage.listdir)

    def test_original(self):
        urls = self.storage.listdir(USER_ID, original=True)
        for url in urls[1]:
            self.assertTrue(url.endswith('_o.jpg'))

    def test_not_original(self):
        urls = self.storage.listdir(USER_ID, original=False, size='m')
        for url in urls[1]:
            self.assertFalse(url.endswith('_o.jpg'))


class FlickrListImageAndThumbTest(BaseFlickrTestCase):
    def test_list_image_and_thumb(self):
        urls = self.storage.list_image_and_thumb(USER_ID)
        for url, url_o in urls:
            self.assertFalse(url.endswith('_o.jpg'))
            self.assertTrue(url_o.endswith('_o.jpg'))

    def test_path(self):
        urls = self.storage.list_image_and_thumb(USER_ID)

    def test_no_path_and_user_id(self):
        urls = self.storage.list_image_and_thumb()

    def test_no_path_and_no_user_id(self):
        self.storage = FlickrStorage(api_key=API_KEY,
                                     api_secret=API_SECRET,
                                     oauth_token=OAUTH_TOKEN,
                                     oauth_token_secret=OAUTH_TOKEN_SECRET)
        self.assertRaises(ValueError, self.storage.list_image_and_thumb)


class FlickrGetFileInfoTest(BaseFlickrTestCase):
    def test_get_info(self):
        photo = self.storage._get_file_info('06021990')
        self.assertIsInstance(photo, dict)

    def test_file_not_found(self):
        self.assertRaises(FileNotFound, self.storage._get_file_info,
                          BAD_FILE_ID)


class FlickrCreatedTimeTest(BaseFlickrTestCase):
    def test_created_time(self):
        date = self.storage.created_time('06021990')
        self.assertIsInstance(date, datetime)

    def test_file_not_found(self):
        self.assertRaises(FileNotFound, self.storage._get_file_info,
                          BAD_FILE_ID)


class FlickrExistsTest(BaseFlickrTestCase):
    def test_exists(self):
        self.assertTrue(self.storage.exists('06021990'))

    def test_not_exists(self):
        self.assertFalse(self.storage.exists(BAD_FILE_ID))


class FlickrModifiedTimeTest(BaseFlickrTestCase):
    def test_modified_time(self):
        date = self.storage.modified_time('06021990')
        self.assertIsInstance(date, datetime)

    def test_file_not_found(self):
        self.assertRaises(FileNotFound, self.storage._get_file_info,
                          BAD_FILE_ID)


class FlickrSaveTest(BaseFlickrTestCase):
    def test_save(self):
        photo = BytesIO(b"Foo")
        photo_id = self.storage.save('foo', photo)
        self.assertTrue(photo_id.isdigit())

    def test_save_error(self):
        photo = BytesIO()
        self.assertRaises(FileSaveError, self.storage.save,
                          'EMPTY_FILE', photo)


class FlickrFormatUrlTest(BaseFlickrTestCase):
    photo = json.loads(fixtures.GET_PHOTO)['photo']

    def test_format_original(self):
        url = self.storage._format_url(self.photo, original=True)

    def test_format_original_not_owned_error(self):
        photo = json.loads(fixtures.GET_PHOTO_NOT_OWNED)['photo']
        self.assertRaises(ValueError, self.storage._format_url,
                          photo, original=True)

    def test_format_m(self):
        url = self.storage._format_url(self.photo, original=False, size='m')

    def test_bad_size(self):
        self.assertRaises(ValueError, self.storage._format_url,
                          self.photo, original=False, size='&')


class FlickrUrlTest(BaseFlickrTestCase):
    def test_original(self):
        pass

    def test_size_m(self):
        pass

    def test_file_not_found(self):
        self.assertRaises(FileNotFound, self.storage._get_file_info,
                          BAD_FILE_ID)
