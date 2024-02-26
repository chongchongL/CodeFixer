# import difflib
# import subprocess
# import os
# import traceback
# from d4j.dao import get_dif, query_ans
import timeout_decorator

from CodeFixer.dao import get_dif
from CodeFixer.models import Fix
from CodeFixer.utils import find_method_by_line
# from patch.patch import PatchValidator
# from project.project_d4j import D4j
# from stats import Stats
# # from utils import Template, ans2patchs


# stats = Stats()
# # template = Template()

# def find_previous_line(text: str):
#     """
#     在给定的字符串中查找目标行的前一行。
#     :param text: 要搜索的字符串。
#     :return: 目标行之前的一行内容，如果找不到目标行或目标行是第一行，则返回 None。
#     """
#     lines = text.splitlines()
#     for i, line in enumerate(lines):
#         if "<buggy line>" in line and i > 0:
#             prev = lines[i - 1].strip()
#             if prev.startswith("//"):
#                 return lines[i - 2].strip(),  lines[i + 1].strip()
#             else:
#                 return prev,  lines[i + 1].strip()
#     return None, None

# def get_diff(file1, file2):
#     # 移除字符串中的所有空格
#     pre_line, next_line = find_previous_line(file1)
#     lines = file2.splitlines()
#     add_lines = []
#     add_flag = 0
#     for i, line in enumerate(lines):
#         line = line.split("//")[0].strip()
#         if add_flag == 1:
#             if line != "":
#                 add_lines.append(line)
#         if line.strip() == pre_line:
#             add_flag = 1
#         if line.strip() == next_line:
#             add_flag = 2
#             break
#     if add_flag != 0:
#         if len(add_lines)>0:
#             return add_lines[0]
#         else:
#             return ""
#     return None

def find_lines_starting_with_plus(text):
    """
    在给定的字符串中查找所有以 '+' 开头的行。

    :param text: 要搜索的字符串。
    :return: 一个包含所有以 '+' 开头的行的列表。
    """
    lines = text.splitlines()  # 将文本分割成单独的行
    plus_lines = [line[1:] for line in lines if line.startswith('+')]  # 查找以 '+' 开头的行
    if len(plus_lines)<2:
        return ""
    return '\n'.join(plus_lines[1:])

# def find_remove_lines(text):
#     """
#     在给定的字符串中查找所有以 '-' 开头的行。

#     :param text: 要搜索的字符串。
#     :return: 一个包含所有以 '-' 开头的行的列表。
#     """
#     lines = text.splitlines()  # 将文本分割成单独的行
#     sub_lines = [line.replace('<buggy line>', '').strip() for line in lines if line.startswith('<buggy line>')]  # 查找以 '+' 开头的行
#     return sub_lines[0]


def get_fault_line(text: str, bug_type):
    """
    获取错误行
    """
    text_list = text.splitlines()
    if bug_type == 1:
        for line in text_list:
            if line.startswith('- '):
                return line.replace('- ', '')
    if bug_type == 2:
        fault_lines = ""
        for line in text_list:
            if line.startswith('- '):
                if fault_lines != "":
                    fault_lines += '\n'
                fault_lines += line.replace('- ', '')
        return fault_lines
    return ""


def do_patch(file: str, rem_lines: list, add_lines: str, bug_type: int):
    """
    打补丁操作
    """
    codes = ""
    with open(file, 'r') as f:
        code_list = f.readlines()
    add_lines = add_lines.strip()
    # 增加容错
    if add_lines.split('\n')[-1].strip() == code_list[rem_lines[-1]].strip():
        code_list[rem_lines[-1]] = ""
    elif len(add_lines.splitlines())>2:
        if add_lines.split('\n')[-2].strip() == code_list[rem_lines[-1]].strip() and add_lines.split('\n')[-1].strip() == code_list[rem_lines[-1]+1].strip():
            code_list[rem_lines[-1]] = ""
            code_list[rem_lines[-1]+1] = ""
    elif len(add_lines.splitlines())>3:
        if add_lines.split('\n')[-3].strip() == code_list[rem_lines[-1]].strip() and add_lines.split('\n')[-2].strip() == code_list[rem_lines[-1]+1].strip() \
        and add_lines.split('\n')[-1].strip() == code_list[rem_lines[-1]+2].strip():
            code_list[rem_lines[-1]] = ""
            code_list[rem_lines[-1]+1] = ""
            code_list[rem_lines[-1]+2] = ""
    # 单行错误
    if bug_type == 1:
        code_list[rem_lines[0]-1] = add_lines
    if bug_type == 2 or bug_type == 4:
        for no in rem_lines:
            code_list[no-1] = ""
        code_list[rem_lines[0]-1] = add_lines
    if bug_type == 3:
        code_list[rem_lines[0]-2] += '\n' + add_lines
    # else:
    #     for no in rem_lines:
    #         code_list[no-1] = ""
    #     code_list[rem_lines[0]-1] = add_lines
    for c in code_list:
        if c != "":
            codes += c + '\n'
    # if bug_type == 4:
    #     context = find_method_by_line(file, rem_lines[0])
    #     codes = file.replace(context, add_lines)
    with open(file, 'w') as f:
        f.write(codes)


import os
import subprocess
import traceback
from CodeFixer.models import Answer
from CodeFixer.program.d4jproject import D4j
from CodeFixer.program.patch import PatchValidator
from CodeFixer.db import baseSession


class D4jPatchValidator(PatchValidator):
    def __init__(self, p: D4j):
        super().__init__(p)
        # stats.add_project(self.p.project + str(self.p.bug_id))


    def src_backup(self):
        """
        对文件进行备份
        """
        cmd = ["cp", self.p.src_path, self.p.src_path+'.bak']
        subprocess.run(cmd, capture_output=True, text=True)
    
    def test_patch(self):
        """
        测试单行补丁是否正确
        """
        p = self.p
        logger = p.logger
        self.src_backup()   # 文件备份
        with baseSession() as session:
            query = session.query(Answer).filter(Answer.bug == self.p.name)
            self.anwsers = query.all()
            # 单行错误
            if p.bug_type() == 1 or p.bug_type() == 2 or p.bug_type() == 3 or p.bug_type() == 4:
                fault_line = get_fault_line(p.bug_code, p.bug_type())
                diff = get_dif(p.project, p.bug_id)      # 注意这里是diff原信息
                human_add_line = find_lines_starting_with_plus(diff)
                # bug_name = p.name
                filter_answers = []
                # 进行过滤和检查是否和人工补丁一致的操作
                for index, answer in enumerate(self.anwsers):
                    assert type(answer) == Answer
                    # 过滤重复补丁
                    print(answer.answer)
                    if answer.answer == fault_line:
                        logger.info(f"补丁{answer.analysis_epoch} {answer.epoch}和初始代码相同:")
                        continue
                    # 检测是否与人工补丁一致
                    if answer.answer.strip() == human_add_line.strip:
                        # with baseSession() as session:
                        session.add(Fix(bug=answer.bug, epoch1=answer.analysis_epoch, epoch2=answer.epoch, step=answer.step, type=1))
                        return True
                    filter_answers.append(answer)
                for index, answer in enumerate(filter_answers):
                    try:
                        p.clear()
                        assert type(answer) == Answer
                        patch = answer.answer
                        subprocess.run(['cp', p.src_path+'.bak', p.src_path], check=True)
                        p.logger.info(f"开始验证补丁{answer.analysis_epoch} {answer.epoch}:")
                        p.logger.info(patch)
                        if patch in self.unique:
                            logger.info(f"补丁{answer.analysis_epoch} {answer.epoch}为重复的补丁")
                            continue
                        else:
                            self.unique.append(patch)
                            do_patch(p.src_path, p.error_num, patch, p.bug_type())
                            if p.compile():
                                if p.test():
                                    self.correct_patch = patch
                                    logger.info(f"补丁{answer.analysis_epoch} {answer.epoch} 通过了所有的测试用例")
                                    # with baseSession() as session:
                                    session.add(Fix(bug=answer.bug, epoch1=answer.analysis_epoch, epoch2=answer.epoch, step=answer.step, type=2))
                                    self.sucess_type = 2
                                    return True
                                else:
                                    # stats.run_error[project] += 1
                                    logger.info("选择失败的测试用例为:")
                                    logger.info(p.fail_test)
                                    logger.info("失败的测试代码为:")
                                    logger.info(p.error_test_lines)
                                    logger.info("失败信息为:")
                                    logger.info(p.test_error_mes)
                                    logger.info(f"补丁{answer.analysis_epoch} {answer.epoch}测试失败")
                            else:
                                # stats.compie_error[project] += 1
                                logger.info(f"补丁{answer.analysis_epoch} {answer.epoch} 未成功编译")

                    except timeout_decorator.TimeoutError:
                        logger.info(f"补丁{self.p.project} {self.p.bug_id} 超时")
                        # stats.time_out[project] += 1
                        # 获取堆栈跟踪信息
                        stack_trace = traceback.format_exc()
                        logger.error("堆栈跟踪信息: %s", stack_trace)
                    except Exception as e:
                        logger.info(f"补丁{self.p.project} {self.p.bug_id} 出错，信息如下：")
                        # 获取堆栈跟踪信息
                        stack_trace = traceback.format_exc()
                        logger.error(e)
                        logger.error("堆栈跟踪信息: %s", stack_trace)
            if self.sucess_type == 0:
                logger.info(f"{p.name} 未成功修复")
                # with baseSession() as session:
                session.add(Fix(bug=p.name, epoch1=-1, epoch2=-1, step=answer.step, type=0))
        return False
                    

    