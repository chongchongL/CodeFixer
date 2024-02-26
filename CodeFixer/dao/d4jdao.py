# -*- coding: utf-8 -*-
# @Time : 2023/12/5 17:57
# @Author : chongchong
# @File : get_bug_info.py
# @Software: PyCharm
# @comments:
from datetime import datetime
import os
import re
from CodeFixer.utils.logutil import setup_logger
import pymysql
from CodeFixer.config.d4jcfg import D4jCfg as cfg


sql_logger = setup_logger("sql_log",os.path.join(cfg.log_dir, 'sql.log'))
# 连接到数据库信息

conn = pymysql.connect(**cfg.db_config)
cursor = conn.cursor()

# SQL 查询语句
sql_query = "SELECT diff FROM bugs WHERE bugId = %s AND project = %s"


def get_dif(project, bug_id):
    # 执行查询
    cursor.execute(sql_query, (bug_id, project))
    # 获取查询结果
    result = cursor.fetchone()
    return result[0]


def get_info(project, bug_id):
    # 执行查询
    cursor.execute(sql_query, (bug_id, project))
    # 获取查询结果
    result = cursor.fetchone()
    flag = 0
    if result:
        return result[0]
    else:
        return ""


# 创建插入命令的SQL语句，使用占位符%s
sql_insert = ("INSERT INTO answer "
              "(bugId, project, time, epoch, step, ans) "
              "VALUES (%s, %s, %s, %s, %s, %s)")


def insert_ans(bugId, project, epoch, step, ans):
    # 准备要插入的数据
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = (bugId, project, current_time, epoch, 1, ans)
    # 执行SQL语句
    sql_logger.info(sql_insert % data)
    cursor.execute(sql_insert, data)
    conn.commit()


# 查找单行修改的补丁
query = "SELECT project, bugId FROM metrics WHERE chunks = 1 and sizeInLines = 1 and linesMod = 1"


def query_single_line():
    cursor.execute(query)
    # 提取结果
    chunks = []
    results = cursor.fetchall()
    for project, bugId in results:
        # print(f"Project: {project}, BugId: {bugId}")
        chunks.append((project, bugId))
    return chunks

# 查询多块补丁
query_chunks_sql = "SELECT project, bugId from metrics WHERE methods = 1 and sizeInLines + spreadAllLines < 11 and chunks>1 and sizeInLines != linesAdd;"

def query_chunks():
    cursor.execute(query_chunks_sql)
    # 提取结果
    chunks = []
    results = cursor.fetchall()
    for project, bugId in results:
        # print(f"Project: {project}, BugId: {bugId}")
        chunks.append((project, bugId))
    return chunks

query_add = "SELECT project, bugId FROM metrics WHERE chunks = 1 and sizeInLines = linesAdd"

# 查找单块添加的补丁
def query_add_lines():
    cursor.execute(query_add)
    # 提取结果
    chunks = []
    results = cursor.fetchall()
    for project, bugId in results:
        # print(f"Project: {project}, BugId: {bugId}")
        chunks.append((project, bugId))
    return chunks



# 查询单块补丁
query_sinle_chunk_sql = "SELECT project, bugId FROM metrics WHERE chunks = 1"

def query_single_chunk():
    cursor.execute(query_sinle_chunk_sql)
    # 提取结果
    chunks = []
    results = cursor.fetchall()
    for project, bugId in results:
        # print(f"Project: {project}, BugId: {bugId}")
        chunks.append((project, bugId))
    return chunks

# # 查询单块修改的补丁
# query_sinle_chunk_dmod_sql = "SELECT project, bugId FROM metrics WHERE chunks = 1 and linesRem = sizeInLines"

# def query_single_chunk_del():
#     cursor.execute(query_sinle_chunk_del_sql)
#     # 提取结果
#     chunks = []
#     results = cursor.fetchall()
#     for project, bugId in results:
#         # print(f"Project: {project}, BugId: {bugId}")
#         chunks.append((project, bugId))
#     return chunks


# 查询单块删除的补丁
query_sinle_chunk_del_sql = "SELECT project, bugId FROM metrics WHERE chunks = 1 and linesRem = sizeInLines"

def query_single_chunk_del():
    cursor.execute(query_sinle_chunk_del_sql)
    # 提取结果
    chunks = []
    results = cursor.fetchall()
    for project, bugId in results:
        # print(f"Project: {project}, BugId: {bugId}")
        chunks.append((project, bugId))
    return chunks


query_sinle_chunk_sql2 = "SELECT project, bugId FROM metrics WHERE chunks = 1 and sizeInLines > 1"

# 查找单行的补丁,不包括单行的
def query_sinle_chunk2():
    cursor.execute(query_sinle_chunk_sql2)
    # 提取结果
    chunks = []
    results = cursor.fetchall()
    for project, bugId in results:
        # print(f"Project: {project}, BugId: {bugId}")
        chunks.append((project, bugId))
    return chunks

# 查找未修复的补丁
query_undone_sql = "SELECT project, bugId FROM fix WHERE type = 0"


def query_undone_chunks():
    cursor.execute(query_undone_sql)
    # 提取结果
    chunks = []
    results = cursor.fetchall()
    for project, bugId in results:
        # print(f"Project: {project}, BugId: {bugId}")
        chunks.append((project, bugId))
    return chunks


query_answer = "SELECT ans FROM answer WHERE project=%s and bugId=%s"


def query_single_answer(project, bugId):
    cursor.execute(query_answer, (project, bugId))
    # 提取结果
    results = cursor.fetchone()
    return results[0]


# 查询补丁修改的粒度信息
query_mtrics_sql = "SELECT chunks, classes, files, linesAdd, linesMod, linesRem, methods, sizeInLines, spreadAllLines FROM metrics WHERE project=%s and bugId=%s"


def query_mtrics(project, bugId):
    cursor.execute(query_mtrics_sql, (project, bugId))
    # 提取结果
    results = cursor.fetchone()
    return results

def query_ans(project, bugId):
    cursor.execute(query_answer, (project, bugId))
    # 提取结果
    results = cursor.fetchall()
    patchs = []
    for patch in results:
        # print(f"Project: {project}, BugId: {bugId}")
        patchs.append(patch[0])
    return patchs

query_path_sql = "select fileName from changedFiles where project = %s and bugId = %s"

def query_path(project, bugId):
    cursor.execute(query_path_sql, (project, bugId))
    # 提取结果
    results = cursor.fetchone()
    return results[0]


query_all_project_sql = "select project,bugId from bugs"

def query_all_project():
    cursor.execute(query_all_project_sql)
    # 提取结果
    chunks = []
    results = cursor.fetchall()
    for project, bugId in results:
        # print(f"Project: {project}, BugId: {bugId}")
        chunks.append((project, bugId))
    return chunks

# 查找需要修改的文件名
query_file_name_sql = "select fileName, changes from changedFiles where project = %s and bugId = %s"

def query_file_name(project, bugId):
    cursor.execute(query_file_name_sql, (project, bugId))
    # 提取结果
    results = cursor.fetchone()
    return results

# 查找需要修改的类型及位置
query_changes_sql = "select changes, inserts, deletes from changedFiles where project = %s and bugId = %s"

def query_changes(project, bugId):
    cursor.execute(query_changes_sql, (project, bugId))
    # 提取结果
    results = cursor.fetchone()
    return results

# 插入正确补丁信息
insert_patch_sql = "INSERT INTO fix (bugId, project, epoch, step, patch, type) VALUES (%s, %s, %s, %s, %s, %s)"

def insert_patch(bugId, project, epoch, step, patch, type):
    # 准备要插入的数据
    data = (bugId, project, epoch, step, patch, type)
    # 执行SQL语句
    sql_logger.info(insert_patch_sql % data)
    cursor.execute(insert_patch_sql, data)
    conn.commit()

# 更新正确补丁信息
update_patch_sql = "update fix set type=%s,patch=%s where project=%s and bugId=%s"

def update_patch(bugId, project, patch, type):
    # 准备要插入的数据
    data = (type, patch, project, bugId)
    # 执行SQL语句
    sql_logger.info(update_patch_sql % data)
    cursor.execute(update_patch_sql, data)
    conn.commit()

# 插入统计信息
insert_stat_sql = "INSERT INTO stats (pb, `repeat`, blank, unchanged, format, compile_error, run_error, res_type, epoch, time_out) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

def insert_stat(pb, repeat, blank, unchanged, format, compile_error, run_error, res_type, epoch, time_out):
    # 准备要插入的数据
    data = (pb, repeat, blank, unchanged, format, compile_error, run_error, res_type, epoch, time_out)
    sql_logger.info(insert_stat_sql % data)
    # 执行SQL语句
    cursor.execute(insert_stat_sql, data)
    conn.commit()