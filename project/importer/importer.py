import json, time

from couchbase.admin import Admin
from couchbase.exceptions import HTTPError
from couchbase.cluster import Cluster, Bucket
from couchbase.cluster import PasswordAuthenticator
from couchbase.analytics import AnalyticsQuery


def create_bucket(name:str, memory:int, admin:Admin) -> int:
    try:
        admin.bucket_create(name, ram_quota=memory)
    except HTTPError as err:
        v = err.__dict__['all_results'][None]
        if v.value['errors'] and 'name' in v.value['errors'] and 'already exists' in v.value['errors']['name']:    
            print('%s bucket already exists, not creating.' % name)
        else:
            print(err)
        return 1
    return 0


class TSVImporter:
    def __init__(self, target_bucket : Bucket, file_path : str, doc_type: str, array_cols: list):
        print('Initializing TSV importer, loading file: %s, target bucket: %s' % (file_path, target_bucket))
        self.file_path = file_path
        self.target_bucket = target_bucket
        self.doc_type = doc_type
        self.array_cols = array_cols
    

    def print_first_row(self):
        f = open(self.file_path, 'r')
        f1 = f.readline()
        f1 = f1.replace('\n','')
        cols : list = f1.split('\t')
        print(cols)
        f2 = f.readline()
        print(f2)
        f.close()

    def start(self):
        # first row has columns names
        f = open(self.file_path, 'r')
        f1 = f.readline()
        f1 = f1.replace('\n','')
        cols : list = f1.split('\t')
        print(cols)
        print('now read remaining lines:')
        fi = f.readlines()

        doc_count = 0
        docs = {}
        for line in fi:
            row = line.replace('\n','').replace('\\N','').split('\t')
            # not a valid row unless it has the same columns
            if len(row) == len(cols):
                doc = {}
                doc['id'] = self.doc_type + '::' + row[0]
                doc['type'] = self.doc_type
                for i in range(len(cols)):
                    # is this column an array of values?
                    if cols[i] in self.array_cols:
                        doc[cols[i]] = row[i].split(',')
                    else:
                        doc[cols[i]] = row[i]       
                docs[doc['id']] = doc
                doc_count += 1
                # upsert multi
                if doc_count >= 500:
                    print('upserting 500 documents...')
                    self.target_bucket.upsert_multi(docs)
                    # empty docs for the next batch
                    docs = {}
                    doc_count = 0
                #self.target_bucket.upsert(doc['id'],doc)                
                #time.sleep(1)
        # upsert any remaining docs
        self.target_bucket.upsert_multi(docs)
        f.close()
