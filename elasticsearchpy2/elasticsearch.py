"""Python package for making requests to an elasticsearch server
"""
import httplib
import json
import logging
import socket
import sys
from urlparse import urlparse

logging.basicConfig(level=logging.INFO)

class Elasticsearch:
    """Class containing methods for making requests to an elasticsearch server

    Args:
        host (str): Elasticsearch host, in standard format <protocol>://<hostname>:<port>
        timeout (int): HTTP connection timeout (default: 60 seconds)
    """
    def __init__(self, host, timeout=60):
        parsed_uri = urlparse(host)
        self.host = parsed_uri.netloc
        self.https = True if parsed_uri.scheme == 'https' else False
        self.timeout = timeout

    def connection(self):
        """Create a new host connection instance via HTTP or HTTPS

        Returns:
            (httplib.HTTPConnection, httplib.HTTPSConnection)
        """
        logging.info("Connecting to %s" % self.host)

        if self.https:
            return httplib.HTTPSConnection(self.host, timeout=self.timeout)
        else:
            return httplib.HTTPConnection(self.host, timeout=self.timeout)

    def get_response(self, method, endpoint, body=None, headers={}):
        """Returns a valid httplib connection request instance or throws an exception

        Args:
            method (str): HTTP request method (GET, POST, PUT, etc.)
            endpoint (str): Host endpoint for the request
            body (str): HTTP request body; default to None
            headers (dict): HTTP request headers; default to empty dict {}

        Returns:
            (dict): JSON response from server
        """
        try:
            connection = self.connection()
            connection.request(method, endpoint, body=body, headers=headers)
            logging.info("Request: %s \"%s%s\"" % (method, self.host, endpoint))
        except Exception as e:
            logging.critical("Target %s actively refused the connection" % self.host)
            logging.critical(e)
            raise

        response = connection.getresponse().read()
        logging.info(response)

        return json.loads(response)

    def get_indices(self, index_pattern='*', reverse=True):
        """GET all Elasticsearch indices matching `index_pattern`

        Args:
            index_pattern (str): elasticsearch index pattern to return;
                default is `*` (wildcard)
            reverse (bool): order to return results in by creation date
                default is True (decending)

        Returns:
            (list): list of indices matching index_pattern sorted by creation_date
        """
        endpoint = '/%s/_settings' % index_pattern
        response = self.get_response('GET', endpoint)

        indices = {}
        for index in response:
            index_settings = response[index]['settings']
            indices[index] = index_settings['index']['creation_date']

        return sorted(indices.iteritems(), reverse=reverse)

    def alias(self, index_pattern, alias, action):
        """Add an alias to an index or all indices matching the specified
        pattern

        Args:
            index_pattern (str): elasticsearch index pattern to return;
                default is `*` (wildcard)
            alias (str): alias name to add to index_pattern
        """
        logging.info('%s alias `%s` to/from index `%s`' % (action, alias, index_pattern))
        endpoint = '/_aliases'
        indices = self.get_indices(index_pattern)
        actions = []
        for index_tuple in indices:
            index = index_tuple[0]
            actions.append('{ "%s" : { "index" : "%s", "alias" : "%s" } }'
                           % (action, index, alias))
        actions = ','.join(actions)
        body = '{"actions" : [%s]}' % actions
        headers = {'Content-Type': 'application/json'}

        response = self.get_response('POST', endpoint, body=body, headers=headers)

        return response
