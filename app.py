import urllib.request, urllib.error, urllib.parse, json, webbrowser
def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

def safe_get(url):
    try:
        return urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        print("The server couldn't fulfill the request.")
        print("Error code: ", e.code)
    except urllib.error.URLError as e:
        print("We failed to reach a server")
        print("Reason: ", e.reason)
    return None

import flickr_key as flickr_key

def flickrREST(baseurl='https://api.flickr.com/services/rest/',
               method='flickr.photos.search',
               api_key=flickr_key.key,
               format='json',
               params={},
               printurl=False
               ):
    params['method'] = method  # saves some of the parameters to the dictionary (also a parameter)
    params['api_key'] = api_key
    params['format'] = format
    if format == "json": params["nojsoncallback"] = True
    url = baseurl + "?" + urllib.parse.urlencode(params)
    if printurl:
        print(url)
    return safe_get(url)

def get_photo_ids(tag, n=100):
    flickr_str = flickrREST(params={'tags': tag, 'per_page': n}).read()
    flickr_data = json.loads(flickr_str)
    result = []

    for photo in flickr_data['photos']['photo']:
        result.append(photo['id'])
    if len(result) == 0:
        return None
    return result

def get_photo_info(photo_id):
    flickr_str = flickrREST(method='flickr.photos.getInfo', params={'photo_id': photo_id}).read()
    flickr_data = json.loads(flickr_str)
    if len(flickr_data) == 0:
        return None
    return flickr_data

class FlickrPhoto():
    """A class to represent a photo from Flickr"""

    def __init__(self, photos_dict):
        self.title = photos_dict['photo']['title']['_content']
        self.author = photos_dict['photo']['owner']['username']
        self.userid = photos_dict['photo']['owner']['nsid']
        self.tags = [x['_content'] for x in photos_dict.get('photo').get('tags').get('tag')]
        self.comment_count = int(photos_dict['photo']['comments']['_content'])
        self.num_views = int(photos_dict['photo']['views'])
        self.url = photos_dict.get('photo').get('urls').get('url')[0]['_content']
        self.server = int(photos_dict['photo']['server'])
        self.id = int(photos_dict['photo']['id'])
        self.secret = photos_dict['photo']['secret']

    def make_photo_url(self, size='q'):
        baseURL = 'https://live.staticflickr.com/{server_id_param}/{photo_id_param}_{secret_param}_{size_letter}.jpg' \
            .format(server_id_param=self.server,
                    photo_id_param=self.id,
                    secret_param=self.secret,
                    size_letter=size)
        return baseURL

    def __str__(self):
        result = '~~~ {photo_title_param} ~~~ \n author: {author_param} \n ' \
                 'number of tags: {num_tags_param} \n views: {views_param} \n ' \
                 'comments: {comments_param} \n url: {url_param}' \
            .format(photo_title_param=self.title, author_param=self.author,
                    num_tags_param=len(self.tags), views_param=self.num_views,
                    comments_param=self.comment_count, url_param=self.url)

        return result

if __name__ == '__main__':
    query = input("Enter what kind of photo you're looking for: ")
    print(query)
    query_str = query
    id_list = get_photo_ids(query_str, 100)
    photo_obj_list = [get_photo_info(x) for x in id_list]
    result_list = [FlickrPhoto(x) for x in photo_obj_list]

    views_sorted = sorted(result_list, key=lambda x: x.num_views, reverse=True)

    tags_sorted = sorted(result_list, key=lambda x: len(x.tags), reverse=True)

    comments_sorted = sorted(result_list, key=lambda x: x.comment_count, reverse=True)

    comments_url = comments_sorted[0].make_photo_url()

    with open("flickr_photos.html", "w") as f:
        f.write("<html><head><title>Top Image Results for your Search</title><meta charset=\"UTF-8\"></head>")
        f.write(
            "<style>body{font-family:serif;} .message{margin-top:1em;padding-top:0.75em;border-top:5px #880 solid} .attachment{margin-top:0.5em;font-size:1.2em}</style>")
        f.write("<body><h1>Top Results</h1>\n")
        f.write("<body><h3>By views:</h3>\n")
        for pic in views_sorted[0:10]:
            url = pic.make_photo_url()
            f.write('<img src="{thumbnailURL}" style="width:150px;height:150px;margin:20px 20px 20px 20px">'.format(
                thumbnailURL=url))
        f.write("<body><h3>By tags:</h3>\n")
        for pic in tags_sorted[0:10]:
            url = pic.make_photo_url()
            f.write('<img src="{thumbnailURL}" style="width:150px;height:150px;margin:20px 20px 20px 20px">'.format(
                thumbnailURL=url))
        f.write("<body><h3>By comments:</h3>\n")
        for pic in comments_sorted[0:10]:
            url = pic.make_photo_url()
            f.write('<img src="{thumbnailURL}" style="width:155px;height:150px;margin:20px 20px 20px 20px">'.format(
                thumbnailURL=url))
        f.close()
