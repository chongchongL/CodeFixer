import re
from CodeFixer.utils.templateUtils import AnalysisTemplate, patchTemplate


def find_method_by_line(java_code, line_number):
    lines = java_code.split('\n')
    method_start = -1
    method_end = -1
    bracket_count = 0

    # 从指定行向上查找方法的开始
    for i in range(line_number - 1, -1, -1):
        if '{' in lines[i]:
            bracket_count += lines[i].count('{')
        if '}' in lines[i]:
            bracket_count -= lines[i].count('}')
        if bracket_count > 0 and ('public' in lines[i] or 'private' in lines[i] or 'protected' in lines[i] or 'void' in lines[i] or lines[i].strip().endswith(")")):
            method_start = i
            break

    # 从指定行向下查找方法的结束
    bracket_count = 1  # 方法开始的'{'已经计算过了
    for i in range(line_number, len(lines)):
        if '{' in lines[i]:
            bracket_count += lines[i].count('{')
        if '}' in lines[i]:
            bracket_count -= lines[i].count('}')
        if bracket_count == 0:
            method_end = i
            break

    if method_start != -1 and method_end != -1:
        return '\n'.join(lines[method_start:method_end + 1])
    else:
        return "Method not found or incorrect line number."