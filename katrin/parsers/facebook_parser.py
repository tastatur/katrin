from katrin.dao.human import NormalHuman
from katrin.parsers.abstract_parser import AbstractParser
from re import sub, match
from math import floor
import time


def get_number_of_friends(suspect_home_raw):
    friends_span = suspect_home_raw.soup.select("h3.by.i")
    if len(friends_span) is not 0:
        return int(sub(r"[^\d]+(\d+)[^\d]+", r"\1", friends_span[0].text))
    else:
        return 0


# Parse facebook friendslist.
class FacebookFriendsParser(AbstractParser):
    def parse(self, friends_url, number_of_friends, http_browser, request_delay):
        friends = []
        if number_of_friends is 0:
            return friends

        pages = floor(number_of_friends / 24)

        for page in range(0, pages - 1):
            startindex = page * 24
            friends_list_url_with_index = friends_url + "?startindex={}".format(startindex)
            raw_data = http_browser.get(friends_list_url_with_index)
            for friend_url in raw_data.soup.select("a"):
                if "href" in friend_url.attrs and match(r".+\?fref=fr_tab", friend_url["href"]):
                    friend_id = sub(r"\/([^?]+)\?.+", r"\1", friend_url["href"])
                    friend = NormalHuman()
                    friend.uid = friend_id
                    friends.append(friend)
            time.sleep(request_delay)
        return friends
