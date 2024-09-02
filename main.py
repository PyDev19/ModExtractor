import json
import requests
import os

headers = {
    'Accept': 'application/json',
    'x-api-key': '$2a$10$MOIkQlgwiwSh6O10uVZ0B.6IGhDKjnuEOYEgGIeGvG8gH9RxIM1Q.'
}

base_url = 'https://api.curseforge.com'

# Get all mincraft categories
r = requests.get(f'{base_url}/v1/categories', params={'gameId': '432'}, headers = headers)
categories = r.json()['data']

# Specify the path to your JSON file
json_file_path = 'manifest.json'

# Specify the path to your mods folder
mods_folder_path = 'mods'

# Make sure the mods folder exists
os.makedirs(mods_folder_path, exist_ok=True)

# Open the JSON file
with open(json_file_path, 'r') as json_file:
    # Load the JSON data
    data = json.load(json_file)

# get files
files = data['files']

# iterate through files
for file in files:
    # get mod info
    r = requests.get(f'{base_url}/v1/mods/{file["projectID"]}', headers=headers)

    with open('test.json', 'w') as f:
        f.write(json.dumps(r.json(), indent=4))

    # check mod category
    for category in categories:
        for mod_category in r.json()['data']['categories']:
            if category['id'] == mod_category['parentCategoryId']:
                try:
                    parent_category_id = category['parentCategoryId']
                    category_name = [x['name'] for x in categories if x['id'] == parent_category_id][0]
                    break
                except KeyError:
                    category_name = category['name']
                    break
    
    # make sure the category folder exists
    os.makedirs(f'{mods_folder_path}/{category_name}', exist_ok=True)

    # get file info
    r = requests.get(f'{base_url}/v1/mods/{file["projectID"]}/files/{file["fileID"]}', headers=headers)

    # get file name
    file_name = r.json()['data']['fileName']

    # get display name
    display_name = r.json()['data']['displayName']

    # get download url
    download_url = r.json()['data']['downloadUrl']

    if download_url is None:
        with open("error.log", "a") as f:
            f.write(f'Error downloading {display_name} ({file_name})\n')
        continue

    # print info
    print(f'Downloading {category_name} {display_name} ({file_name})')

    # download file
    r = requests.get(download_url)

    # save file
    with open(f'{mods_folder_path}/{category_name}/{file_name}', 'wb') as f:
        f.write(r.content)