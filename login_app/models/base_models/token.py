from abc import ABC,abstractmethod


class Token(ABC):

    @abstractmethod
    def encode(self,data):
        raise NotImplementedError

    @abstractmethod
    def decode(self):
        raise NotImplementedError

    @abstractmethod
    def verify(self):
        raise NotImplementedError

    @abstractmethod
    def create(self):
        raise NotImplementedError
