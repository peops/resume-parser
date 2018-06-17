import sys
import json
import pprint
import logging
import pymongo
import hashlib
import requests
import canonicaljson
from six.moves.configparser import ConfigParser


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("indexer")


class Utils:
    def __init__(self, config):
        self.config = config

    @staticmethod
    def get_value_from_jsonld_value(jsonld_value):
        """
        Return the value for the given jsonld_value object.

        If jsonld_value is a primitive value, return that directly
        Else, if it is a value object then return the associated value

        :param jsonld_value:
        :return:
        """
        if not isinstance(jsonld_value, dict):
            return str(jsonld_value)
        elif '@value' in jsonld_value:
            return str(jsonld_value['@value'])
        else:
            return None

    def map_schema_if_necessary(self, schema):
        """
        Get the mapped schema if there is one for this schema

        :param schema:
        :return:
        """
        if 'schema_map' in self.config:
            schema_map = self.config['schema_map']

            if schema in schema_map:
                logger.debug('Mapping schema %s to %s', schema, schema_map[schema])
                schema = schema_map[schema]

        return schema

class SolrIndexer:
    def __init__(self, config):
        self.config = config
        self.utils = Utils(config)

    def index(self, jsonlds):
        headers = {'Content-type': 'application/json'}
        solr_jsons = []
        for jsonld in jsonlds:
            pprint.pprint(jsonld)
            schema = jsonld['@type']
            solr_json = self._create_solr_json(schema, jsonld)
            solr_json['id'] = hashlib.sha256(canonicaljson.encode_canonical_json(solr_json)).hexdigest()
            solr_jsons.append(solr_json)

        # TODO: Use solr de-dupe for this
        # jsonld['id'] = str(uuid.uuid5(namespaceUuid, json.dumps(jsonld)))

        if self.config['post_to_solr']:
            logger.debug('Posting %s', solr_json)
            print(solr_jsons)
            r = requests.post(
                self.config['solr_json_doc_update_url'] + '?commit=true', json=solr_jsons, headers=headers)
            if r.status_code != 200:
                logger.error('Could not post to Solr: %s', r.text)

    def _create_solr_json(self, schema, jsonld):
        """
        Create JSON we can put into Solr from the Bioschemas JSON-LD

        :param schema:
        :param jsonld:
        :return:
        """
        schema = self.utils.map_schema_if_necessary(schema)
        jsonld['@type'] = schema
        return self._create_solr_json_properties(schema, jsonld)

    def _create_solr_json_properties(self, schema, jsonld):
        """
        Create JSON properties we can put into Solr from the Bioschemas JSON-LD

        :param schema: The name of the schema (e.g. 'DataCatalog')
        :param jsonld: The schema JSON-LD
        :return:
        """

        # print('Inspecting schema %s with jsonld size %d' % (schema, len(jsonld)))
        solr_json = {}

        if 'mandatory_properties' in self.config:
            self._process_configured_properties(schema, jsonld, self.config['mandatory_properties'], solr_json)

        if 'optional_properties' in self.config:
            self._process_configured_properties(schema, jsonld, self.config['optional_properties'], solr_json)

        schema_graph = self.config['schema_inheritance_graph']
        # parent_schema = schema_graph[schema]

        # if parent_schema is not None:
        #     solr_json.update(self._create_solr_json_properties(parent_schema, jsonld))

        return solr_json

    def _process_configured_properties(self, schema, jsonld, configured_props, solr_json):
        """
        Process the configured properties, taking them out of jsonld, transforming them where appropriate, and inserting
        into the solr_json

        :param schema:
        :param jsonld:
        :param configured_props:
        :param solr_json:
        :return:
        """

        json_to_solr_map = self.config['jsonld_to_solr_map']

        if schema in configured_props:
            for prop_name in configured_props[schema]:
                # Mandatory checking is done by the parser
                if prop_name not in jsonld:
                    continue

                if prop_name in json_to_solr_map:
                    solr_prop_name = json_to_solr_map[prop_name]
                else:
                    solr_prop_name = prop_name

                prop_value = self.utils.get_value_from_jsonld_value(jsonld[prop_name])

                logger.debug(
                    'Adding key "%s" -> "%s" for %s, value "%s"',
                    prop_name, solr_prop_name, prop_value, schema)

                solr_json[solr_prop_name] = prop_value

def idlimit(collection, page_size, last_id=None):
    if last_id is None:
        cursor = collection.find().limit(page_size)
    else:
        cursor = collection.find({'_id': {'$gt': last_id}}).limit(page_size)

    data = [x for x in cursor]
    if not data:
        return None, None

    last_id = data[-1]['_id']
    return data, last_id

def index_data(data):
    indexer.index(data)


config_file = "config/settings.ini"
parser = ConfigParser()
parser.optionxform = str
parser.read(config_file)
for section_name in parser.sections():
    if section_name == 'MongoDBServer':
        mongodb = {x:y for x,y in parser.items(section_name)}
    if section_name == 'SolrServer':
        solr = {x:y for x,y in parser.items(section_name)}
client = pymongo.MongoClient(
        mongodb['MONGODB_SERVER'],
        int(mongodb['MONGODB_PORT'])
    )
try:
    client.server_info()
except pymongo.errors.ServerSelectionTimeoutError as e:
    logger.error("MongoDB not connected at %s:%s", mongodb['MONGODB_SERVER'], mongodb['MONGODB_PORT'])
    sys.exit()
logger.info("Connected to MongoDB")
db = client[mongodb['MONGODB_DB']]
collection = db[mongodb['MONGODB_COLLECTION']]


solr_endpoint = 'http://' + solr['SOLR_SERVER'] + ':' + solr['SOLR_PORT'] + '/solr/' + solr['SOLR_CORE'] + '/'
logger.info('Indexing at Solr core %s', solr_endpoint)

with open('config/default_schema.json') as f:
    config = json.load(f)
config.update({
    "post_to_solr": True,
    "solr_json_doc_update_url": solr_endpoint + 'update/json/docs',
    "solr_query_url": solr_endpoint +'select'
})

indexer = SolrIndexer(config)

i=0
while i<1:
    data, last_id = idlimit(collection, page_size=,5 last_id=None)
    index_data(data)
    i+=1
