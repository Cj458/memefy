
def extract_path_from_nextcloud(response):
    data = response.json().get('ocs').get('data') if response else None
    path = str(data.get('url')) + "/download" + str(data.get('file_target')) if data else None
    return path
