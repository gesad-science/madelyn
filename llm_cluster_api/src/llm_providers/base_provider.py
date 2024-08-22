from abc import ABC, abstractmethod

class BaseProvider(ABC):
    @abstractmethod
    def list_models(self) -> list[str]:
        raise NotImplementedError
    @abstractmethod
    def has_model(self, model : str) -> bool:
        raise NotImplementedError
    @abstractmethod
    def make_call(self, prompt : str, model : str) -> str:
        raise NotImplementedError