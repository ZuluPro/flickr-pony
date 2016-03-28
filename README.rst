===========
Flickr Pony 
===========

.. image:: https://api.travis-ci.org/ZuluPro/flickr-pony.svg
        :target: https://travis-ci.org/ZuluPro/flickr-pony

.. image:: https://coveralls.io/repos/ZuluPro/flickr-pony/badge.svg?branch=master&service=github
        :target: https://coveralls.io/github/ZuluPro/flickr-pony?branch=master

This library provides a `Django Storage`_ for use `Flickr`_ in read and write
operations.

With 1To free and a thumbnail system, Flickr is a quite good solution for store
wide pictures in original format and retrieve them in smaller format

As Flickr is dedicated to photos/images, it is not a conventional
object-storge, we consider all pics from all users in the same bucket but
different directories. So what should a be directory path on other storages
will be a user ID in this one.

Install
=======

A classic :::

    pip install flickr-pony

or::

    git clone https://github.com/ZuluPro/flickr-pony.git
    cd flickr-pony
    python setup.py develop

It isn't necessary to include data in ``settings.FLICKR_STORAGE_OPTIONS``, and
settings are explained below.


Settings
========

The storage can be configured with the following parameters, at instanciation or
by set a dictionary named ``FLICKR_STORAGE_OPTIONS`` in your ``settings.py``.

**api_key** : Findable at
https://www.flickr.com/services/apps/create/apply/, it is the only one
mandatory data for read operations.

**api_secret** : Given with the API KEY

**oauth_token_secret** : Oauth access token, not request token

**oauth_token_secret** : Oauth access token secret, not request secret

**user_id** : Your personal User ID, findable at your Flickr web page.
It is the last part of URL example: ``140893176@N07``. This data is useful
if you want to automatize action related to this user.


Info
  Get all authentication info may be really long and boring, we advise you
  this page http://acme.com/flickr/authmap.html

Usage
=====

This storage has a simple usage as define in Django Storage API plus others
method for play more easily with pictures. You can list a user's photos with: ::

    >>> from flickr_pony.storage import FlickrStorage
    >>> storage = FlickrStorage(api_key="myApiKey")
    >>> storage.listdir('140893176@N07')
    ([], ['https://farm2.staticflickr.com/1586/25309081103_518e989396_o.jpg',
     'https://farm2.staticflickr.com/1623/25911906696_84c8cf31ae_o.jpg',
     'https://farm2.staticflickr.com/1617/25637193860_98a08d224f_o.jpg',
     ...
     'https://farm2.staticflickr.com/1671/25794942526_5b54c8a908_o.jpg',
     'https://farm2.staticflickr.com/1653/25820730145_4040532d03_o.jpg'])

It will return image in original if you are allowed to get it, but it could be too
heavy for some usage, so you can use decide get it in "medium" format: ::

    >>> storage.listdir('140893176@N07', original=False)
    ([], ['https://farm2.staticflickr.com/1586/25309081103_d132f2fa3f.jpg',
     ...
     'https://farm2.staticflickr.com/1623/25911906696_cee21c32be.jpg',
     'https://farm2.staticflickr.com/1653/25820730145_ef8db88e60.jpg'])

Or in "small" size: ::

    >>> storage.listdir('140893176@N07', original=False, size='s')
    ([], ['https://farm2.staticflickr.com/1586/25309081103_d132f2fa3f.jpg',
     ...
     'https://farm2.staticflickr.com/1623/25911906696_cee21c32be.jpg',
     'https://farm2.staticflickr.com/1653/25820730145_ef8db88e60.jpg'])

For image gallery, you could also decide to list original and thumbnail: ::

    >>> storage.list_image_and_thumb()
    [('https://farm2.staticflickr.com/1586/25309081103_d132f2fa3f.jpg',
      'https://farm2.staticflickr.com/1586/25309081103_518e989396_o.jpg'),
    ...
     ('https://farm2.staticflickr.com/1623/25911906696_cee21c32be.jpg',
      'https://farm2.staticflickr.com/1623/25911906696_84c8cf31ae_o.jpg')]
        
Uploading and deleting are available: ::

    >>> from django.core.files import File
    >>> with open('myPic', 'rb') as img:
    ...     storage.save('picName', img)
        '25839776716'
    >>> storage.delete('25839776716')

Demo
====

A demo project is available for testing and trying purpose, for use it: ::

    git clone https://github.com/ZuluPro/flickr-pony-demo
    cd flickr-pony-demo
    pip install requirements.txt
    cd demo_project
    export FLICKR_API_KEY="YourFlickrApiKey" # Mandatory
    # export FLICKR_USER_ID="YourFlickrUserId"
    ./manage runserver

You can also deploy it on Heroku:

.. image:: https://www.herokucdn.com/deploy/button.svg
        :target: https://heroku.com/deploy?template=https://github.com/ZuluPro/flickr-pony-demo


Contributing
============

All contribution are very welcomed, propositions, problems, bugs and
enhancement are tracked with `GitHub issues`_ system and patch are submitted
via `pull requests`_.

We use `Travis`_ coupled with `Coveralls`_ as continious integration tools.

.. _`Django Storage`: https://docs.djangoproject.com/en/1.9/ref/files/storage/
.. _`Flickr`: https://www.flickr.com
.. _`GitHub issues`: https://github.com/ZuluPro/flickr-pony/issues
.. _`pull requests`: https://github.com/ZuluPro/flickr-pony/pulls
.. _Travis: https://travis-ci.org/ZuluPro/flickr-pony
.. _Coveralls: https://coveralls.io/github/ZuluPro/flickr-pony
