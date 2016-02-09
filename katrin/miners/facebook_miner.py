import configparser
import mechanicalsoup

from katrin.dao.human import NormalHuman
from katrin.dao.neo4j import NormalHumanStore
from katrin.miners.abstract_miner import Miner, MinerConfig

from katrin.parsers.facebook_parser import FacebookFriendsParser


class FacebookFriendsMinerConfig(MinerConfig):
    def __init__(self):
        self._mining_depth = 0
        self._username = ""
        self._password = ""
        self._user_agent = ""
        self._human_store = None

    def miner_id(self):
        return "facebook_friends_miner"

    def load(self, filename):
        config = configparser.ConfigParser()
        config.read(filename)
        self._mining_depth = int(config['facebook-friends-miner']['depth'])
        self._username = config['facebook-friends-miner']['username']
        self._password = config['facebook-friends-miner']['password']
        self._user_agent = config['facebook-friends-miner']['ua']
        self._human_store = NormalHumanStore(config['neo4j']['uri'])

    @property
    def mining_depth(self):
        return self._mining_depth

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def user_agent(self):
        return self._user_agent

    @property
    def human_store(self):
        return self._human_store


class FacebookFriendsMiner(Miner):
    def __init__(self, miner_config):
        super().__init__(miner_config)
        self._friends_parser = FacebookFriendsParser()

    def mine(self, suspect):
        target = NormalHuman()
        target.uid = suspect

        http_browser = self.login()
        self.mine_friends(target, 0, http_browser)

    def mine_friends(self, suspect, current_depth, http_browser):
        if current_depth > self.miner_config.mining_depth:
            return

        friend_list_url = "https://m.facebook.com/" + suspect.uid + '/friends'
        unparsed_friends = http_browser.get(friend_list_url)
        parsed_friends = self._friends_parser.parse(unparsed_friends)
        suspect.friends = parsed_friends
        self.update_suspect(suspect)
        for friend in suspect.friends:
            self.mine_friends(friend, current_depth + 1, http_browser)

    def login(self):
        browser = mechanicalsoup.Browser()
        browser.session.headers["User-Agent"] = self.miner_config.user_agent
        login_page = browser.get("https://m.facebook.com/")
        login_form = login_page.soup.select(".mobile-login-form")[0]
        login_form.select("[name=email]")[0]["value"] = self.miner_config.username
        login_form.select("[name=pass]")[0]["value"] = self.miner_config.password
        browser.submit(login_form, "https://m.facebook.com/login")
        return browser

    def update_suspect(self, suspect):
        self.miner_config.human_store.update_human(suspect)
