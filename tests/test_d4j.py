import os
import time
# import sys
import traceback
from chatgpt.chatgpt_api import ChatGPTInteractive
from d4j.dao import insert_ans, insert_patch, insert_stat, query_add_lines, query_single_chunk, query_single_chunk_del, query_sinle_chunk2, update_patch, query_single_line
from patch.d4jpatch import D4jPatchValidator
# from patch.patch import PatchValidator
from project.project_d4j import D4jBuilder, D4jDirector
from utils.logUtils import setup_logger
from utils.templateUtils import EngAddChunkTemplate, EngAddTemplate, EngChunkTemplate, EngTemplate
from config.cfg import cfg

if __name__ == '__main__':
    root_path = cfg['project_dir']
    print(root_path)
    logger = setup_logger('project', os.path.join(root_path, "log", "tests.log"))
    sigle_line = query_single_line()
    # single_chuck = query_single_chunk()
    chunks_del = query_single_chunk_del()   # 单块删除的
    chunks_add = query_add_lines()
    chunks = []
    # chunks = list(set(single_chuck) - set(sigle_line))
    single_chunks = query_sinle_chunk2()   # 单块补丁（不包含单行）
    for chunk in single_chunks:
        if chunk not in sigle_line and chunk not in chunks_del and chunk not in chunks_add:
            chunks.append(chunk)
    # chunks = query_single_chunk_del()     # 单行删除
    # chunks = query_add_lines()          # 单行添加
    len_chunk = len(chunks)
    print("总共有%s个" %len_chunk)
    chunks = [('Chart', 1)]
    # chunks = [('Closure', 10), ('Closure', 14), ('Closure', 18), ('Lang', 16), ('Lang', 26), ('Math', 27), ('Mockito', 5), ('Time', 4)]
    choose = 24
    for project, bug_id in chunks:
        try:
            print(project, bug_id)
            builder = D4jBuilder(project + "_" + str(bug_id))
            D4jDirector(builder).build()
            p = builder.project
            gpt = ChatGPTInteractive(project, bug_id, p.logger)
            # patch_type = 2
            # 更新模板
            if p.bug_type() == 1:
                # tem = LineTemplate()
                tem  = EngTemplate()
                tem.make_template(p.bug_code, p.error_test_lines, p.test_error_mes, p.method)
            
                logger.info(logger.info(f"{project} {bug_id}b 已生成模板，内容请见对应的日志文件"))
                gpt.send_message(tem)
                # # 对补丁进行校验
                validator = D4jPatchValidator(p)
                validator.test_patchs4singleline()
                if validator.sucess_type != 0:
                    print("修复成功")
                else:
                    print("修复失败")
                insert_patch(bugId=p.bug_id, project=p.project, epoch=validator.batch, step=1, patch=validator.correct_patch, type=validator.sucess_type)
            if p.bug_type() == 2:
                insert_ans(p.bug_id, p.project, 0, 1, "")
                insert_patch(bugId=p.bug_id, project=p.project, epoch=1, step=1, patch="", type=1)
                print("修复成功")
            if p.bug_type() == 3:
                # tem = LineTemplate()
                tem  = EngAddTemplate()
                tem.make_template(p.bug_code, p.error_test_lines, p.test_error_mes, p.method)
            
                logger.info(logger.info(f"{project} {bug_id}b 已生成模板，内容请见对应的日志文件"))
                gpt.send_message(tem)
                # # 对补丁进行校验
                validator = D4jPatchValidator(p)
                validator.test_patchs4singleline()
                if validator.sucess_type != 0:
                    print("修复成功")
                else:
                    print("修复失败")
                insert_patch(bugId=p.bug_id, project=p.project, epoch=validator.batch, step=1, patch=validator.correct_patch, type=validator.sucess_type)
            if p.bug_type() == 4:
                # tem = LineTemplate()
                tem  = EngChunkTemplate()
                tem.make_template(p.bug_code, p.error_test_lines, p.test_error_mes, p.method)
            
                logger.info(logger.info(f"{project} {bug_id}b 已生成模板，内容请见对应的日志文件"))
                gpt.send_message(tem)
                # 对补丁进行校验
                validator = D4jPatchValidator(p)
                validator.test_patchs4singleline()
                if validator.sucess_type != 0:
                    print("修复成功")
                else:
                    print("修复失败")
                insert_patch(bugId=p.bug_id, project=p.project, epoch=validator.batch, step=1, patch=validator.correct_patch, type=validator.sucess_type)
            # time.sleep(10)
            if p.bug_type() == 5:
                # tem = LineTemplate()
                tem  = EngAddChunkTemplate()
                tem.make_template(p.bug_code, p.error_test_lines, p.test_error_mes, p.method)
            
                logger.info(logger.info(f"{project} {bug_id}b 已生成模板，内容请见对应的日志文件"))
                gpt.send_message(tem)
                # 对补丁进行校验
                validator = D4jPatchValidator(p)
                validator.test_patchs4singleline()
                if validator.sucess_type != 0:
                    print("修复成功")
                else:
                    print("修复失败")
                insert_patch(bugId=p.bug_id, project=p.project, epoch=validator.batch, step=1, patch=validator.correct_patch, type=validator.sucess_type)
        except Exception as e:
            # 获取堆栈跟踪信息
            stack_trace = traceback.format_exc()
            logger.error(f"{project} {bug_id}b 出现了异常")
            logger.error(e)
            logger.error("堆栈跟踪信息: %s", stack_trace)
        
        