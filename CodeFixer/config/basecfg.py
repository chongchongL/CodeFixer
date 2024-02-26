__all__ = ["BaseCfg"]



models = [
        # 0: cgpt3.5模型，响应速度快
        "gpt-3.5-turbo",
        # 1: gpt-4模型，更加准确 
        "gpt-4-1106-preview",
        # 微调过的3.5模型 有单块数据集
        "ft:gpt-3.5-turbo-1106:personal::8lwZ1gKT",
        # 微调过的3.5模型 只有单行数据集
        "ft:gpt-3.5-turbo-1106:personal::8lGMm4OF",
]

class BaseCfg:
    # 日志设置  
    log_dir = "/home/chongchong/log"

    # chatgpt设置
    model1 = models[1]  # 分析错误原因的模型
    model2 = models[1]   # 生成补丁的模型

    # 生成补丁的参数
    epochs = 3          # 生成分析的个数
    patch_num = 3       # 生成补丁的个数

    # 标记设置
    marker = [ '// Suspected bug line below\n', '<fill>',]

    # 语言设置
    language = 'java'

