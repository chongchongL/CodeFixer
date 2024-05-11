## 实验运行环境

操作系统：ubuntu 64位；

编程语言：python3.9；

数据库：mysql8.0；

API：ChatGPT3.5turbo api；

Java版本：openjdk1.7;

defects4jV1.2;

Pytorch：1.12.0。

## 文件结构

CodeFixer 	  												源代码 

......chatgpt												   大语言模型交互模块

​......config													 配置模块（设置不同的参数值）

​......dao														 数据库模块

​......db														 数据库创建

​......models												 需要保存的结果模型

​......program												程序类

​......strategies									 策略模块（包含上下文的优化、测试用例的选择等）

​......utils														工具模块

result 			 												实验结果

​......gpt_d4j												   defects4J V1.2与大语言模型的交互记录

​......gpt_qx													quixbugs与大语言模型的交互

​......project_d4j											defects4J V1.2的自动化验证

​......project_qx											 quixbugs的自动化验证

......res.xls                          使用思维树的最终修复结果表格（bug名称、补丁、对错误的分析）

......res.html                         使用思维树的最终修复结果表格（bug名称、补丁、对错误的分析）

tests																测试代码



## 持续更新中....................



