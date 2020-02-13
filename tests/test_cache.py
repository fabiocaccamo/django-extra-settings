# -*- coding: utf-8 -*-

from django.test import TestCase

from extra_settings.cache import (
    del_cached_setting, get_cached_setting, set_cached_setting, )


class ExtraSettingsCacheTestCase(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_cache_del(self):
        set_cached_setting('test_cache_del', 'del')
        val = get_cached_setting('test_cache_del')
        self.assertEqual(val, 'del')
        del_cached_setting('test_cache_del')
        val = get_cached_setting('test_cache_del')
        self.assertEqual(val, None)

    def test_cache_get(self):
        val = get_cached_setting('test_cache_get')
        self.assertEqual(val, None)
        set_cached_setting('test_cache_get', 'get')
        val = get_cached_setting('test_cache_get')
        self.assertEqual(val, 'get')

    def test_cache_set(self):
        set_cached_setting('test_cache_set', 'set')
        val = get_cached_setting('test_cache_set')
        self.assertEqual(val, 'set')
