import re
from CodeFixer.strategies.basestrategies import ContextStratege, TestCodeStratege, TestStrategy
from CodeFixer.config.d4jcfg import D4jCfg as cfg
from CodeFixer.utils import find_method_by_line


# 定义自定义异常
class CovError(Exception):
    """
    词汇量移除异常
    """
    def __init__(self, message="上下文行数过多"):
        # 调用基类的构造器
        super().__init__(message)
        

class ContextDiff(ContextStratege):
    """
    通过diff获取上下文
    """
    def get_context(self, text:str, patch_type: int=2):
        if text != "":
            processed_lines = []
            bug_line = ""
            # 处理文本行
            method_name = ""
            for i, line in enumerate(text.splitlines()):
                if line.startswith('@'):
                    # 使用正则表达式匹配方法名
                    match = re.search(r'\b\w+\s+(\w+)\s*\(', line)
                    if match:
                        method_name = match.group(1)
                elif i < 3:
                    pass
                elif line.lstrip().startswith('*'):
                    pass
                elif line.startswith('-') and not line.startswith('--'):
                    if patch_type == 3:
                        bug_line = bug_line + line[1:] + '\n'
                        processed_lines.append(line[1:])
                elif not line.startswith('+'):
                    processed_lines.append(line)
                else:
                    if patch_type == 2:
                        processed_lines.append('<buggy line>')
            # 合并处理后的文本
            processed_text = '\n'.join(processed_lines)
            return processed_text, bug_line, method_name
        return "", 0, ""


class ContextAround(ContextStratege):
    """
    将单行错误行周围固定行数作为上下文,同时避免超过上下文窗口
    """
    def __init__(self, context_num: int=cfg.max_lines, context_max_tokens:int=cfg.max_tokens):
        self.context_num = context_num
        self.context_max_tokens = context_max_tokens

    def get_context(self, text:str, error_num: int):
        text_list = text.splitlines()
        text_len = len(text_list)
        tokens = 0
        single_bug_line = text_list[error_num-1]
        win = self.context_num
        for num in range(1, self.context_num+1):
            tokens += len(text_list[error_num-1-num])
            if error_num-1+num < text_len:
                tokens += len(text_list[error_num-1+num])
            if tokens > self.context_max_tokens:
                win = num-1
        text_list[error_num-1] = '- ' + single_bug_line
        context_list = text_list[error_num-1-win:error_num+win]
        return '\n'.join(context_list)


class ChunkContextAround(ContextStratege):
    """
    将单块错误周围固定行数作为上下文,同时避免超过上下文窗口
    """
    def __init__(self, context_num: int=cfg.max_lines, context_max_tokens:int=cfg.max_tokens):
        self.context_num = context_num
        self.context_max_tokens = context_max_tokens

    def get_context(self, text:str, error_num: list):
        # error_num.sort()
        text_list = text.splitlines()
        text_len = len(text_list)
        tokens = 0
        bug_lines = ""
        for no in error_num:
            bug_lines += '\n- ' + text_list[no-1]
        bug_lines += '\n'
        win = self.context_num
        for num in range(1, self.context_num+1):
            tokens += len(text_list[error_num[0]-1-num])
            if error_num[-1]-1+num < text_len:
                tokens += len(text_list[error_num[-1]-1+num])
            if tokens > self.context_max_tokens:
                win = num-1
        
        # text_list[error_num-1] = '- ' + single_bug_line
        bug_lines = '\n'.join(text_list[error_num[0]-1-win:error_num[0]-1]) + bug_lines + '\n'.join(text_list[error_num[-1]:error_num[-1] + win])
        return bug_lines
    

class MethodContextAround(ContextStratege):
    """
    定位整个方法
    """
    def __init__(self, context_num: int=12, context_max_tokens:int=2048):
        self.context_num = context_num
        self.context_max_tokens = context_max_tokens

    def get_context(self, text:str, error_num: list):
        methods_codes = find_method_by_line(text, error_num[0])
        if len(methods_codes.split()) < self.context_num * 2 + 2:
            return methods_codes
        else:
            raise CovError
        return ""

class TestFirst(TestStrategy):
    """
    选择第一个测试用例
    """
    def get_test(self, failing_tests):
        if "testParseMonth" not in failing_tests[0]:
            fail_test = failing_tests[0]
        else:
            fail_test = failing_tests[1]
        return fail_test

class TestCodeSingleline(TestCodeStratege):
    def get_test_code(self, src: str, num: int):
        """
        获取失败的测试用例单行代码
        """
        return src[num-1]
