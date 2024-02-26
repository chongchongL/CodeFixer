from abc import ABC, abstractmethod
import re


class ContextStratege(ABC):

    @abstractmethod
    def get_context(self):
        pass


class TestStrategy(ABC):
    """
    选择测试用例
    """
    @abstractmethod
    def get_test(self, failing_tests):
        pass


class TestCodeStratege(ABC):

    @abstractmethod
    def get_test_code(self):
        pass