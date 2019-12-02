import os
import sys

from flask_script import Manager
from project.server import app
from project.server import cb_media
from project.importer.importer import TSVImporter
from project.importer.title_doc_builder import TitleDocBuilder

manager = Manager(app)

@manager.command
def import_imdb():

    tdb : TitleDocBuilder = TitleDocBuilder(cb_media, 'data', 400)
    tdb.start()
    tdb.title_basics()
    


    '''    
    title_rat_imp : TSVImporter = TSVImporter(cb_media, 'data/title.ratings.tsv', 'title_rating', [])
    title_rat_imp.start()

    name_imp : TSVImporter = TSVImporter(cb_media, 'data/name.basics.tsv', 'name', ['primaryProfession','knownForTitles'])
    name_imp.start()
    
    title_basics_imp : TSVImporter = TSVImporter(cb_media, 'data/title.basics.tsv', 'title_basic', ['genres'])
    title_basics_imp.start()
    
    title_crew_imp : TSVImporter = TSVImporter(cb_media, 'data/title.crew.tsv', 'title_crew', ['directors','writers'])
    title_crew_imp.start()
    
    title_epi_imp : TSVImporter = TSVImporter(cb_media, 'data/title.episode.tsv', 'title_episode', [])
    title_epi_imp.start()
    
    title_rat_imp : TSVImporter = TSVImporter(cb_media, 'data/title.ratings.tsv', 'title_rating', [])
    title_rat_imp.start()

    title_prin_imp : TSVImporter = TSVImporter(cb_media, 'data/title.principals.tsv', 'title_principal',[])
    title_prin_imp.start()
    '''

    

if __name__ == '__main__':
    manager.run()