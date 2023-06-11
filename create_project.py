import requests
import os

def post_data(url, data):
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        print('POST request successful. Response: {}'.format(response.text))
    except requests.exceptions.RequestException as e:
        print('Error: {}'.format(str(e)))


if __name__ == '__main__':
    url = os.getenv('RELEASEMANAGER_URL') + '/projects'


    data = {
        'name': 'test',
        'gitrepo': 'git@github.com:miracle-as/openknowit_kalm.git'
    }
    post_data(url, data)
