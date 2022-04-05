from flask import Blueprint, request, flash, redirect, current_app
from werkzeug.utils import secure_filename
import os
from algoliasearch.search_client import SearchClient
from  dotenv import load_dotenv, find_dotenv
from lark import Lark
import json
import re

blueprint = Blueprint('parse', __name__)

load_dotenv(find_dotenv())

ALGOLIA_APP_ID = os.getenv('ALGOLIA_APP_ID')
ALGOLIA_API_KEY = os.getenv('ALGOLIA_API_KEY')
client = SearchClient.create(ALGOLIA_APP_ID, ALGOLIA_API_KEY)

passages_index = client.init_index('passages')
passages_index.set_settings({
    'searchableAttributes': [
        'passage',
        'filename'
    ],
})

passages_exp_index = client.init_index('passages_exp')
passages_exp_index.set_settings({
    'searchableAttributes': [
        'passage',
        'filename'
    ],
})

ALLOWED_EXTENSIONS = {'txt'}
    
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@blueprint.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect("/")
        
        files = request.files.getlist('file')
        if len(files) == 0:
            return redirect("/")

        passages_index.clear_objects().wait()
        passages_exp_index.clear_objects().wait()

        for file in files:
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file and allowed_file(file.filename):
                parse(file, request.form['parse1'], request.form['parse2'])

    return redirect("/")

def parse(file, parse1, parse2):
    
    
    data = file.read().decode('utf-8')
    
    params = [(parse1, passages_index), (parse2, passages_exp_index)]

    for p, index in params:

        # Parse 1
        if p is not None and p != "":
            d = data
            config = json.loads(p)

            if "ignore" in config:
                ignore = config["ignore"]
                d = re.sub(ignore, '', d)
            
            delim = config["delim"]
            d = re.split(delim, d)
            
            if "min_size" in config:
                min_size = config['min_size']
                out = []
                accum = ""
                for rec in d:
                    if len(accum) > min_size:
                        out.append(accum)
                        accum = ""
                    
                    if len(rec) < min_size:
                        accum += rec + '\n'
                    else:
                        if accum != "":
                            out.append(accum)
                            accum = ""
                        out.append(rec)
                d = out

            records = map(lambda x: {'passage': str(x), 'filename': file.filename}, d[0:5000])
            
            try:

                index.save_objects(records, {'autoGenerateObjectIDIfNotExist': True})
            except:
                print("API Index error")
        else:
            records = data.split('\n\n')

            records = map(lambda x: {'passage': str(x), 'filename': file.filename}, records[0:5000])
            

            try:
                index.save_objects(records, {'autoGenerateObjectIDIfNotExist': True})
            except:
                print("API Index error")

    return