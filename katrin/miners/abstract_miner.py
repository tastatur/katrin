from abc import ABCMeta, abstractmethod, abstractproperty


class MinerConfig(metaclass=ABCMeta):
    @abstractproperty
    def miner_id(self):
        pass


# Abstract class for miner. MinerConfig defines configuration of the miner (e.g. depth, login data or API keys).
class Miner(metaclass=ABCMeta):
    def __init__(self, miner_config):
        self._miner_config = miner_config

    @abstractmethod
    def mine(self, suspect):
        pass

    @property
    def miner_config(self):
        return self._miner_config

    @miner_config.setter
    def miner_config(self, config):
        self._miner_config = config
