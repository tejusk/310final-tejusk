import urllib.request, urllib.error, urllib.parse, json
# Authentication
client_id = "EAK6JKrKKJS4OtcGeyrkPZx1s69wQdlxonotqs-fWgM"
client_secret = "zYr7lACVzUtci8JUpHV5EKlSq-M-lx-6zZBpfcxN4-U"
redirect_uri = "urn:ietf:wg:oauth:2.0:oob"

# Returns search results based on a query as a dictionary
def searchPhotos(query):
    baseurl = f"https://api.unsplash.com/search/photos?client_id={client_id}"
    photo_query = {"query": query, "page": 1}
    query_str = urllib.parse.urlencode(photo_query)
    search_photos = baseurl + "&" + query_str
    result = urllib.request.urlopen(search_photos)
    json_result = result.read()
    photo_dict = json.loads(json_result)
    return photo_dict

# Get a photo based on a particular ID
def getPhoto(id):
    baseurl = "https://api.unsplash.com/photos/"
    # search by ID
    get_photo = baseurl + id + "?client_id=" + client_id
    result = urllib.request.urlopen(get_photo)
    json_result = result.read()
    photo_dict = json.loads(json_result)
    return photo_dict


# Safe methods
def safe_searchPhotos(query):
    try:
        return searchPhotos(query)
    except urllib.error.HTTPError as e:
        print("The server couldn't fulfill the request.")
        print("Error code: ", e.code)
    except urllib.error.URLError as e:
        print("We failed to reach a server")
        print("Reason: ", e.reason)
    return None

def safe_getPhoto(id):
    try:
        return getPhoto(id)
    except urllib.error.HTTPError as e:
        print("The server couldn't fulfill the request.")
        print("Error code: ", e.code)
    except urllib.error.URLError as e:
        print("We failed to reach a server")
        print("Reason: ", e.reason)
    return None


# Returns a list of n photo IDs corresponding to the query
def get_photo_ids(query, n=100):
    unsplash_data = safe_searchPhotos(query)
    result = []

    for photo in unsplash_data['results']:
        result.append(photo['id'])
    if len(result) == 0:
        return None
    return result

class UnsplashPhoto():
    # Represents a photo from Unsplash
    def __init__(self, photo_dict):
        self.id = photo_dict['id']
        self.tags = photo_dict['tags']
        self.description = photo_dict['description']
        self.likes = int(photo_dict['likes'])
        self.downloads = int(photo_dict['downloads'])
        self.url = photo_dict['urls']['raw']
        self.url_thumb = photo_dict['urls']['thumb']
        self.userid = photo_dict['user']['id']
        self.username = photo_dict['user']['username']

    def make_photo_url(self, size='q'):
        baseURL = 'https://unsplash.com/photos/{photo_id_param}' \
            .format(photo_id_param=self.id)
        return baseURL

#test code
# print(safe_searchPhotos("NYC"))
# print(get_photo_ids("NYC", 20))
# print(safe_getPhoto("1KPfcPdbWFM"))
# for pic in get_photo_ids("NYC", 5):
#     print(safe_getPhoto(pic))

# user_query = input("What would you like photos of? ")
user_query = input("Enter what kind of photo you're looking for: ")
id_list = get_photo_ids(user_query, 100)
photo_obj_list = [safe_getPhoto(x) for x in id_list]
result_list = [UnsplashPhoto(photo_dict=x) for x in photo_obj_list]

likes_sorted = sorted(result_list, key=lambda x: x.likes, reverse=True)
# print(likes_sorted)

downloads_sorted = sorted(result_list, key=lambda x: x.downloads, reverse=True)
# print(downloads_sorted)

tags_sorted = sorted(result_list, key=lambda x: len(x.tags), reverse=True)
# print(tags_sorted)

def sort_by_likes(n):
    result = []
    for pic in likes_sorted[0:n]:
        url = pic.url_thumb
        result.append(url)
    return result

def sort_by_tags(n):
    result = []
    for pic in tags_sorted[0:n]:
        url = pic.url_thumb
        result.append(url)
    return result

def sort_by_downloads(n):
    result = []
    for pic in downloads_sorted[0:n]:
        url = pic.url_thumb
        result.append(url)
    return result

with open("unsplash_photos.html", "w") as f:
    f.write(f"<html><head><title>Top Image Results for \"{user_query}\"</title><meta charset=\"UTF-8\"></head>")
    f.write(
        "<style>body{font-family:serif;} .message{margin-top:1em;padding-top:0.75em;border-top:5px #880 solid} .attachment{margin-top:0.5em;font-size:1.2em}</style>")
    f.write(f"<body><h1>Top Image Results for \"{user_query}\"</h1>\n")
    f.write("<body><h3>By likes:</h3>\n")
    for pic in likes_sorted[0:20]:
        url = pic.url_thumb
        f.write('<img src="{thumbnailURL}" style="height:150px;margin:20px 20px 20px 20px">'.format(
            thumbnailURL=url))
    f.write("<body><h3>By downloads:</h3>\n")
    for pic in downloads_sorted[0:20]:
        url = pic.url_thumb
        f.write('<img src="{thumbnailURL}" style="height:150px;margin:20px 20px 20px 20px">'.format(
            thumbnailURL=url))

    f.write("<body><h3>By tags:</h3>\n")
    for pic in tags_sorted[0:20]:
        url = pic.url_thumb
        f.write('<img src="{thumbnailURL}" style="height:150px;margin:20px 20px 20px 20px">'.format(
            thumbnailURL=url))

    f.close()