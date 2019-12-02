# TODO search API

from flask import Blueprint, request, make_response, redirect, jsonify
from project.server import app
from project.server import cb_media
import couchbase.fulltext as FT


search_bp : Blueprint = Blueprint('search', __name__)

@search_bp.route('/api/v1/search', methods=['GET'])
def search():
    q = request.args.get('q')

    query = FT.QueryStringQuery(q)

    results : FT.SearchRequest = cb_media.search(
        'titles_search_idx', 
        query, 
        limit=20,
        facets={
            'genres': FT.TermFacet('genres', limit=10),
            'titleType': FT.TermFacet('titleType', limit=10)
            },
        fields='originalTitle'
        )
    #title = cb_media.get(title_id).value
    hits = []
    for result in results:
        hits.append(result)

    #for f in results.facets['genres']['terms']:
    #    print(f)
    resp = {}
    resp['meta'] = results.meta
    resp['hits'] = hits
    #resp['facets'] = results.facets


    return make_response(jsonify(resp)), 200





    INDEX_DEF : str = """
    {
 "name": "titles_search_idx",
 "type": "fulltext-index",
 "params": {
  "doc_config": {
   "docid_prefix_delim": "",
   "docid_regexp": "",
   "mode": "type_field",
   "type_field": "type"
  },
  "mapping": {
   "default_analyzer": "standard",
   "default_datetime_parser": "dateTimeOptional",
   "default_field": "_all",
   "default_mapping": {
    "dynamic": true,
    "enabled": true
   },
   "default_type": "_default",
   "docvalues_dynamic": true,
   "index_dynamic": true,
   "store_dynamic": false,
   "type_field": "_type",
   "types": {
    "title": {
     "dynamic": true,
     "enabled": true,
     "properties": {
      "genres": {
       "enabled": true,
       "dynamic": false,
       "fields": [
        {
         "analyzer": "keyword",
         "include_in_all": true,
         "include_term_vectors": true,
         "index": true,
         "name": "genres",
         "type": "text"
        }
       ]
      }
     }
    }
   }
  },
  "store": {
   "indexType": "scorch",
   "kvStoreName": ""
  }
 },
 "sourceType": "couchbase",
 "sourceName": "media",
 "sourceUUID": "8323e55f4edd1c7200b28c054b373fc5",
 "sourceParams": {},
 "planParams": {
  "maxPartitionsPerPIndex": 171,
  "numReplicas": 0
 },
 "uuid": "20a75ed751d56ff5"
}
    """