from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def make_noise(self) -> None:
        raise NotImplementedError

class Dog(Animal):
    pass

d = Dog()
