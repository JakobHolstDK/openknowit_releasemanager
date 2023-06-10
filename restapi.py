from flask import Flask, request
from pymongo import MongoClient
import json
import os
import requests


import subprocess
import tempfile

temp_dir = tempfile.TemporaryDirectory()
print(temp_dir.name)
# use temp_dir, and when done:
temp_dir.cleanup()

app = Flask(__name__)
client = MongoClient(os.getenv("MONGO"))
db = client['releasemanager']
projects = db['projects']
 
import os
import shutil
import tempfile
from git import Repo

def clone_and_print_pyproject(git_url):
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()

    try:
        # Clone the Git repository
        repo = Repo.clone_from(git_url, temp_dir)

        # Find the pyproject.toml file
        pyproject_path = os.path.join(temp_dir, 'pyproject.toml')

        if os.path.exists(pyproject_path):
            # Read and print the contents of pyproject.toml
            with open(pyproject_path, 'r') as file:
                print(file.read())
        else:
            print("pyproject.toml file not found in the repository.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Cleanup: Remove the temporary directory
        shutil.rmtree(temp_dir)


@app.route('/projects', methods=['GET'])
def get_projects():
    return json.dumps(list(projects.find({}, {'_id': False})))

@app.route('/projects', methods=['POST'])
def add_project():
    # Retrieve the project name from the request
    project_name = request.json.get('name')
    gitrepo = request.json.get('gitrepo')


    # Check if the project exists
    if projects.find_one({'name': project_name}):
        return 'Project already exists', 409

    # Add the project to the database
    clone_and_print_pyproject(gitrepo)

    projects.insert_one({'name': project_name, 'version': '0.0.0', 'gitrepo': gitrepo})

    return 'Project added successfully'

# return my ssh public key
@app.route('/projects/key', methods=['GET'])
def get_key():
    if os.getenv("KEY") is None:
        return 'No key found', 404
    else:
        key = open(os.getenv("KEY"), 'r').read()
        return key


@app.route('/projects/bump', methods=['POST'])
def bump_version():
    print(request.json)
    projects = db['projects']
    print(projects)

    # Retrieve the new version from the request
    bumptype = request.json.get('bumptype')
    project_name = request.json.get('name')
    project =  projects.find_one({'name': project_name})
    if project is None:
        return 'Project does not exist:' + project_name , 404
    old_version = projects.find_one({'name': project_name})['version']
    old_version = old_version.split('.')
    print(old_version)
    

        
        
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
        subprocess.run(['git',  'config',  '--global', 'user.email', "kalm@knowit.dk"])
        subprocess.run(['git',  'config',  '--global', 'user.user', "kalm automation"])
        subprocess.run(['git', 'clone', "request.json.get('url')"])
        subprocess.run(['git', 'checkout', 'main'])
        subprocess.run(['sed', '-i', 's/version = ".*/version = "{}"/'.format(new_version), 'pyproject.toml'])
        subprocess.run(['git', 'commit', '-am', 'Bumped version to {}'.format(new_version)])
        subprocess.run(['git', 'push', 'origin', 'main'])

        return 'Version bumped successfully'
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5200)

