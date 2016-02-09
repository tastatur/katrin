# Base human class, describing abstract mining target
class Human:
    def __init__(self):
        self._uid = ""
        self._name = ""

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, uid):
        self._uid = uid

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name


# Most of humans should have some friends
class NormalHuman(Human):
    def __init__(self):
        super().__init__()
        self._friends = []

    @property
    def friends(self):
        return self._friends

    @friends.setter
    def friends(self, friends):
        self._friends = friends
