from katrin.dao.human import NormalHuman
from katrin.parsers.abstract_parser import AbstractParser
from re import sub,match


# Parse facebook friendslist.
class FacebookFriendsParser(AbstractParser):
    def parse(self, raw_data):
        friends = []
        for friend_url in raw_data.soup.select("[class=cc]"):
            if "href" in friend_url.attrs and match(r".+\?fref=fr_tab", friend_url["href"]):
                friend_id = sub(r"\/([^?]+)\?.+", r"\1", friend_url["href"])
                friend = NormalHuman()
                friend.uid = friend_id
                friends.append(friend)
        return friends
