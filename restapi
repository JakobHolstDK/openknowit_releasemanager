from flask import Flask, request
from pymongo import MongoClient
import json
import os
import requests

import subprocess

app = Flask(__name__)
client = MongoClient(os.getenv("MONGO"))
db = client['releasemanager']
projects = db['projects']
 

@app.route('/projects', methods=['GET'])
def get_projects():
    return json.dumps(list(packages.find({}, {'_id': False})))

@app.route('/projects', methods=['POST'])
def add_project():
    # Retrieve the project name from the request
    project_name = request.json.get('name')

    # Check if the project exists
    if packages.find_one({'name': project_name}):
        return 'Project already exists', 409

    # Add the project to the database
    packages.insert_one({'name': project_name, 'version': '0.0.0'})
    return 'Project added successfully'



@app.route('/bump-version/project', methods=['POST'])
def bump_version():
    # Retrieve the new version from the request
    bumptype = request.json.get('bumptype')
    project_name = request.json.get('name')
    if not project_name in projects.find_one({'name': project_name}):
        return 'Project does not exist', 404
    old_version = projects.find_one({'name': project_name})['version']
    old_version = old_version.split('.')

        
        
    if bumptype == 'major':
        new_version = str(int(old_version[0]) + 1) + old_version[1] + old_version[2]
    elif bumptype == 'minor':
        new_version = old_version[0] + str(int(old_version[1]) + 1) + old_version[2]
    elif bumptype == 'patch':
        new_version = old_version[0] + old_version[1] + str(int(old_version[2]) + 1)
    else:
        return 'Invalid bump type', 400
    try:
        # Clone the repository
        subprocess.run(['git', 'clone', "request.json.get('url')"])
        # Checkout the main branch
        subprocess.run(['git', 'checkout', 'main'])

        # Bump the version in pyproject.toml
        subprocess.run(['sed', '-i', 's/version = ".*/version = "{}"/'.format(new_version), 'pyproject.toml'])

        # Commit the changes
        subprocess.run(['git', 'commit', '-am', 'Bumped version to {}'.format(new_version)])

        # Push to the main branch
        subprocess.run(['git', 'push', 'origin', 'main'])

        return 'Version bumped successfully'
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5200)

