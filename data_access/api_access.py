import requests, os
from urllib.parse import quote

auth = (os.getenv('API_USER'), os.getenv('API_PASSWORD'))
base_url = "http://{0}/".format(os.getenv('API_IP'))
headers = {'Content-type': 'application/json'}


class API(object):

    def __init__(self, **kwargs):

        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_player_by_id(self, objectId):

        req = requests.get("{0}/players/{1}".format(base_url, objectId), auth=auth)

        return req.text

    def get_player_by_handle(self, handle):

        req = requests.get("{0}/players/{1}".format(base_url, handle), auth=auth)

        return req.text

    def get_players(self, sort_key=None, desc=False, count=None, page=1):

        if desc:
            sort_key = "-{0}".format(sort_key)

        req = requests.get("{0}/players?sort={1}&max_results={2}&page={3}"
                           .format(base_url, sort_key, count, page), auth=auth)

        return req.text

    def post_event(self, event_json):

        req = requests.post("{0}/events".format(base_url),
                            auth=auth, headers=headers, data=event_json)

        return req.text

    def post_game(self, game_json):

        req = requests.post("{0}/games".format(base_url),
                            auth=auth, headers=headers, data=game_json)

        return req.text

    def get_player_events(self, player_id):

        query_string = quote('{{"$or" : [{{"batterId" : "{0}"}}, {{"pitcherId" : "{0}"}}]}}'.format(player_id))

        req = requests.get("{0}/events?where={1}".format(base_url, query_string),
                           auth=auth, headers=headers)

        return req.text
