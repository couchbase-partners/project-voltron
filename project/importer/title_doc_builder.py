import json, time
from datetime import datetime

from couchbase.admin import Admin
from couchbase.exceptions import HTTPError
from couchbase.cluster import Cluster, Bucket
from couchbase.cluster import PasswordAuthenticator
from couchbase.analytics import AnalyticsQuery


# See https://www.imdb.com/interfaces/ for a full list of files and their contents
class TitleDocBuilder:
    def __init__(self, target_bucket : Bucket, files_dir : str, min_votes_filter : int):
        self.target_bucket = target_bucket
        self.files_dir = files_dir
        self.min_votes_filter = min_votes_filter
        self.title_ids : set = set()

    def row_split(self, line):
        return line.replace('\n','').replace('\\N','').split('\t')

    def start(self):
    
        # Strategy:
        # We will hold an array of title ids in an array, and only import data from the top
        # n movies using the array as a filter

        # start by loading titles with more than min_votes_filter votes        
        f = open(self.files_dir + '/title.ratings.tsv', 'r')
        fw = open(self.files_dir + '/titles.filtered.tsv', 'w')
        '''
        title.ratings.tsv.gz – Contains the IMDb rating and votes information for titles
            tconst (string) - alphanumeric unique identifier of the title
            averageRating – weighted average of all the individual user ratings
            numVotes - number of votes the title has received
        '''
        docs = {}
        f.readline() # skip first row
        counter = 0
        for line in f.readlines():            
            row = self.row_split(line)             
            doc = {}
            doc['id'] = 'title::' + row[0]
            doc['type'] = 'title'
            doc['averageRating'] = float(row[1])            
            votes = int(row[2])
            doc['numVotes'] = int(row[2])
            if votes > self.min_votes_filter:
                fw.write(row[0] + '\n')
                docs[doc['id']] = doc
                counter += 1
                self.title_ids.add(row[0])
            if counter >= 500:
                print('Sending 500 documents')                        
                self.target_bucket.upsert_multi(docs)
                counter = 0
                docs = {}
        self.target_bucket.upsert_multi(docs) # send remainder

        print('Saved filtered titles to titles.filtered.tsv in ' + self.files_dir)
        f.close()
        fw.close()        
        
    def title_ids_to_set(self) -> set:
        f = open(self.files_dir + '/titles.filtered.tsv')
        titles : set = set()
        for line in f.readlines():
            titles.add(line.strip())
        return titles

    def prune_attr(self):
        f = open(self.files_dir + '/title.akas.tsv', 'r')
        fw = open(self.files_dir + '/title.akas-us.tsv', 'w')
        f.readline()
        for line in f.readlines():
            row = line.split('\t')
            if row[3] == 'US':                
                fw.write(line)
        f.close()
        fw.close()
                

    def title_akas(self):
        # todo: load additional attributes
        pass

    def title_basics(self):
        '''
        title.basics.tsv.gz - Contains the following information for titles:
            tconst (string) - alphanumeric unique identifier of the title
            titleType (string) – the type/format of the title (e.g. movie, short, tvseries, tvepisode, video, etc)
            primaryTitle (string) – the more popular title / the title used by the filmmakers on promotional materials at the point of release
            originalTitle (string) - original title, in the original language
            isAdult (boolean) - 0: non-adult title; 1: adult title
            startYear (YYYY) – represents the release year of a title. In the case of TV Series, it is the series start year
            endYear (YYYY) – TV Series end year. ‘\\N’ for all other title types
            runtimeMinutes – primary runtime of the title, in minutes
            genres (string array) – includes up to three genres associated with the title
        '''
        title_ids = self.title_ids_to_set()
        print('There are %d titles to filter' % len(title_ids))
        f = open(self.files_dir + '/title.basics.tsv', 'r')
        docs = {}
        f.readline() # skip first row
        matches = 0
        for line in f.readlines():                      
            row = self.row_split(line)                  
            if row[0] not in title_ids:
                continue
            try:
                matches += 1
                doc = self.target_bucket.get('title::' + row[0]).value
                doc['titleType'] = row[1]
                doc['primaryTitle'] = row[2]
                doc['originalTitle'] = row[3]
                doc['isAdult'] = row[4]
                doc['startYear'] = row[5]
                doc['endYear'] = row[6]
                doc['runtimeMinutes'] = row[7]
                doc['genres'] = row[8].split(',')            
                self.target_bucket.upsert('title::' + row[0], doc)
                #print('%s: title %s found' % (datetime.now(), row[0]))            
                print('Found match %d of %d' % (matches, len(self.title_ids)))
            except:
                print('something bad happened')
                #print('%s: title %s not found' % (datetime.now(), row[0]))
                pass
            
            
            



