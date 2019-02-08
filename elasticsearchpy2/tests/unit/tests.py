#!/usr/bin/env python

"""Test cases for elasticsearch_ss
"""
import httplib
from unittest import TestCase

import elasticsearch_ss.elasticsearch as elasticsearch

class testElasticsearchPackage(TestCase):
    """Test class for Elasticsearch class
    """
    def test_elasticsearch_http(self):
        """Test Elasticsearch class with HTTP host
        """
        es = elasticsearch.Elasticsearch("http://localhost")

        self.assertEqual("localhost", es.host)
        self.assertEqual(False, es.https)
        connection = es.connection()
        self.assertTrue(isinstance(connection, httplib.HTTPConnection))
        connection.close()

    def test_elasticsearch_init_noargs(self):
        """Test Elasticsearch class with HTTPS host
        """
        es = elasticsearch.Elasticsearch("https://localhost")

        self.assertTrue(isinstance(es, elasticsearch.Elasticsearch))
        self.assertEqual("localhost", es.host)
        self.assertEqual(True, es.https)
        connection = es.connection()
        self.assertTrue(isinstance(connection, httplib.HTTPSConnection))
        connection.close()

