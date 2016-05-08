import configparser
import mechanicalsoup
import time

from katrin.dao.human import NormalHuman
from katrin.dao.neo4j import NormalHumanStore
from katrin.miners.abstract_miner import Miner, MinerConfig

from katrin.parsers.facebook_parser import FacebookFriendsParser, get_number_of_friends


class FacebookFriendsMinerConfig(MinerConfig):
    def __init__(self):
        self._mining_depth = 0
        self._username = ""
        self._password = ""
        self._user_agent = ""
        self._request_delay = 5
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
        self._request_delay = int(config['facebook-friends-miner']['request_delay'])

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
    def request_delay(self):
        return self._request_delay

    @property
    def human_store(self):
        return self._human_store


class FacebookMiner(Miner):
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
        # We need this for pagination
        suspect_home = http_browser.get(friend_list_url)
        number_of_friends = get_number_of_friends(suspect_home)

        parsed_friends = self._friends_parser.parse(friend_list_url, number_of_friends, http_browser, self.miner_config.request_delay)
        suspect.friends = parsed_friends
        self.update_suspect(suspect)
        print("Targets found: {}" .format(len(parsed_friends)))
        time.sleep(self.miner_config.request_delay)
        for friend in suspect.friends:
            time.sleep(self.miner_config.request_delay)
            self.mine_friends(friend, current_depth + 1, http_browser)

    def login(self):
        browser = mechanicalsoup.Browser(soup_config={"features": "lxml"})
        browser.session.headers["User-Agent"] = self.miner_config.user_agent
        login_page = browser.get("https://m.facebook.com/")
        login_form = login_page.soup.select(".mobile-login-form")[0]
        login_form.select("[name=email]")[0]["value"] = self.miner_config.username
        login_form.select("[name=pass]")[0]["value"] = self.miner_config.password
        browser.submit(login_form, "https://m.facebook.com/login")
        return browser

    def update_suspect(self, suspect):
        self.miner_config.human_store.update_human(suspect)
