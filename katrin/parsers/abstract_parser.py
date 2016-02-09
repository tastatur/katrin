from abc import ABCMeta, abstractmethod


# Parse input data (e.g. HTML page) into format, which miner can understand
class AbstractParser(metaclass=ABCMeta):
    @abstractmethod
    def parse(self, raw_data):
        pass
