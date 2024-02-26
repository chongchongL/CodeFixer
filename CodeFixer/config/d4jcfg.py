from CodeFixer.config.basecfg import BaseCfg


class D4jCfg(BaseCfg):
    
    # 项目配置
    project_dir = "/home/chongchong/CodeFixer"

    # defects4j的路径
    d4j_dir = '/home/chongchong/d4j-project'

    # 上下文窗口的配置
    max_lines = 7
    max_tokens = 1024


    # 编译和运行最大时间，单位：秒
    compile_maxtime = 600
    test_maxtime = 600

    db_config = {
    'user': 'root',
    'password': '335233long',
    'host': 'localhost',
    'database': 'defects4j',
    'port': 3306,
}








