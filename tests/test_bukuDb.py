# -*- coding: utf-8 -*-
from genericpath import exists
import imp
import os
from tempfile import TemporaryDirectory
from unittest import TestCase
from os.path import join, expanduser
import sqlite3

buku = imp.load_source('buku', '../buku')

TEST_TEMP_DIR_OBJ = TemporaryDirectory(prefix='bukutest_')
TEST_TEMP_DIR_PATH = TEST_TEMP_DIR_OBJ.name
TEST_TEMP_DBDIR_PATH = join(TEST_TEMP_DIR_PATH, 'buku')
TEST_TEMP_DBFILE_PATH = join(TEST_TEMP_DBDIR_PATH, 'bookmarks.db')

from buku import BukuDb, parse_tags


class TestBukuDb(TestCase):

    def setUp(self):
        os.environ['XDG_DATA_HOME'] = TEST_TEMP_DIR_PATH

    def tearDown(self):
        os.environ['XDG_DATA_HOME'] = TEST_TEMP_DIR_PATH

    def test_get_dbdir_path(self):
        dbdir_expected = TEST_TEMP_DBDIR_PATH
        dbdir_local_expected = join(expanduser('~'), '.local', 'share', 'buku')
        dbdir_relative_expected = join('.', 'buku')

        # desktop linux
        self.assertEqual(dbdir_expected, BukuDb.get_dbdir_path())

        # desktop generic
        os.environ.pop('XDG_DATA_HOME')
        self.assertEqual(dbdir_local_expected, BukuDb.get_dbdir_path())

        # no desktop

        # -- home is defined differently on various platforms.
        # -- keep a copy and set it back once done
        originals = {}
        for env_var in ['HOME', 'HOMEPATH', 'HOMEDIR']:
            try:
                originals[env_var] = os.environ.pop(env_var)
            except KeyError:
                pass
        self.assertEqual(dbdir_relative_expected, BukuDb.get_dbdir_path())
        for key, value in originals.items():
            os.environ[key] = value

    # # not sure how to test this in nondestructive manner
    # def test_move_legacy_dbfile(self):
    #     self.fail()

    def test_initdb(self):
        if exists(TEST_TEMP_DBFILE_PATH):
            os.remove(TEST_TEMP_DBFILE_PATH)
        self.assertIs(False, exists(TEST_TEMP_DBFILE_PATH))
        conn, curr = BukuDb.initdb()
        self.assertIsInstance(conn, sqlite3.Connection)
        self.assertIsInstance(curr, sqlite3.Cursor)
        self.assertIs(True, exists(TEST_TEMP_DBFILE_PATH))
        curr.close()
        conn.close()


    def test_add_and_retrieve_bookmark(self):
        URL = 'http://slashdot.org'
        TITLE = 'SLASHDOT'
        TAGS = ['old', 'news']
        DESC = "News for old nerds, stuff that doesn't matter"

        # start from clean slate
        if exists(TEST_TEMP_DBFILE_PATH):
            os.remove(TEST_TEMP_DBFILE_PATH)

        bdb = BukuDb()
        bdb.add_bookmark(URL,
                         tag_manual=parse_tags(TAGS),
                         title_manual=TITLE,
                         desc=DESC)

        index = bdb.get_bookmark_index(URL)

        self.assertEqual(1, index)
        # TODO: retrieve and compare
        # TODO: tags should be passed to the api as a sequence...

    def test_update_bookmark(self):
        self.fail()

    def test_refreshdb(self):
        self.fail()

    def test_searchdb(self):
        self.fail()

    def test_search_by_tag(self):
        self.fail()

    def test_compactdb(self):
        self.fail()

    def test_delete_bookmark(self):
        self.fail()

    def test_print_bookmark(self):
        self.fail()

    def test_list_tags(self):
        self.fail()

    def test_replace_tag(self):
        self.fail()

    def test_browse_by_index(self):
        self.fail()

    def test_close_quit(self):
        self.fail()

    def test_import_bookmark(self):
        self.fail()