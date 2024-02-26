import os
from CodeFixer.utils.logutil import setup_logger
from abc import ABC, abstractmethod


class Project():
    def __init__(self, name):
        """
        项目信息
        """
        # self.prefix = __package__
        self.name = name
        self.logger = None
        self.fail_type = 0      # 0无错误  1 编译错误  2 执行错误
        self.fail_tests = []    # 未通过的测试用例
        self.fail_test = ""     # 选择使用的测试用例
        self.bug_code = ""    # 错误的源码
        self.test_error_mes = ""     # 测试错误信息
        self.compile_error_mes = ""     # 编译错误信息
        self.error_test_lines = ""   # 出错的测试用例代码
        self.changes = []           # 修改的代码行
        self.changes_type = []      # 修改的类型
        self.metrics = []
    

class ProjectBuilder(ABC):
    
    def __init__(self, name):
        self.project = Project(name)
        self.project.logger = setup_logger(name, os.path.join(__package__, 'log', 'project', name+".log"))  # 日志记录器

    def set_fail_type(self):
        self.project.fail_type = self.get_fail_type()
    
    @abstractmethod
    def get_fail_type(self):
        """
        获取错误类型
        """
        pass

    def set_fail_tests(self):
        self.project.fail_tests = self.get_fail_tests()

    @abstractmethod
    def get_fail_tests(self):
        """
        获取测试用例
        """
        pass
    
    def set_bug_code(self):
        self.project.bug_code = self.get_bug_code()

    @abstractmethod
    def get_bug_code(self):
        """
        获取错误的源码
        """
        pass
    
    def set_test_error_mes(self):
        self.project.test_error_mes = self.get_test_error_mes()

    @abstractmethod
    def get_test_error_mes(self):
        """
        获取测试时错误的信息
        """
        pass

    def set_compile_error_mes(self):
        self.project.compile_error_mes = self.get_compile_error_mes()

    @abstractmethod
    def get_compile_error_mes(self):
        """
        获取编译时错误的信息
        """
        pass

    # def set_error_test_code(self):
    #     self.project.error_test_code = self.get_error_test_code()

    # @abstractmethod
    # def get_error_test_code(self):
    #     """
    #     获取测试的代码信息
    #     """
    #     pass
        
    def set_change_type(self):
        self.project.changes_type, self.project.changes, self.project.metrics = self.get_change_type()

    @abstractmethod
    def get_change_type(self):
        """
        获取修复前后修改的信息
        """
        pass

    def set_error_test_lines(self):
        self.project.error_test_lines = self.get_error_test_lines()

    @abstractmethod
    def get_error_test_lines(self):
        """
        获取测试出错所在的源码
        """
        pass
    
class ProjectDirector:
    def __init__(self, builder: ProjectBuilder):
        self.builder = builder
    
    def build(self):
        self.builder.set_fail_type()
        self.builder.set_fail_tests()
        self.builder.set_compile_error_mes()
        self.builder.set_test_error_mes()
        self.builder.set_bug_code()
        self.builder.set_change_type()
        # self.builder.set_error_test_code()
        self.builder.set_test_error_mes()
        self.builder.set_error_test_lines()