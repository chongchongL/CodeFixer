tems = {
  "T1": {
      "system": "You are an Automated Program Repair Tool, please give %s answers in order of probability",
      "user": "The following code contains a buggy line that has been removed:\n```%s```\nThis was the original buggy line which was removed by the infill location:```%s```\nThe code fails on this test:%s\non this test line:```%s```\nwith the following test error:%sPlease provide the correct line at the infill location."
  },
  "T2": {
   "system": "You are an Automated Program Repair Tool, please give %s answers in order of probability",
   "user": "The following code contains a buggy hunk that has been removed:\n```%s```\nThis was the original buggy hunk which was removed by the infill location:```%s```\nThe code fails on this test:%s\non this test line:```%s```\nwith the following test error:%sPlease provide the correct line at the infill location."
  },
  "T3": {
    "system": "你是程序修复领域的专家,接下来我会告诉你三种信息,1:包含了错误行的java代码,2:被移除的错误行(用<buggy line>表示)的内容, 3:断言失败的报错信息,请在<buggy line>处提供正确的代码行",
    "user": "包含错误行的代码:\n%s\n<buggy line>:%s\n报错信息:%s"
  },
  "T4": {
    "system": "你是程序修复领域的专家,接下来我会告诉你四种信息,1:包含了错误行的java代码,2:被移除的错误行(用<buggy line>表示)的内容,3:运行测试用例时断言失败的代码行, 4:断言失败的报错信息,请在<buggy line>处提供正确的代码行",
    "user": "包含错误行的代码:\n%s\n<buggy line>:%s\n断言失败的代码行:%s报错信息:%s"
  },
  "T5": {
    "system": "你是程序修复领域的专家,接下来我会告诉你四种信息,1:包含了错误行的java代码,2:被移除的错误行(用<buggy line>表示)的内容,3:运行测试用例时断言失败的代码行, 4:断言失败的报错信息,请你根据以上信息思考出%s种可能在<buggy line>处的正确代码行,并根据正确修复的概率大小进行回复",
    "user": "包含错误行的代码:\n%s\n<buggy line>:%s\n断言失败的代码行:%s报错信息:%s"
  },
  "T6": {
    "system": "你是程序修复领域的专家,接下来我会告诉你三种信息,1:出错的java代码,2:运行测试用例时断言失败的代码行, 3:断言失败的报错信息,请你根据以上的代码信息和错误信息,思考出%s种可能在<buggy line>处的添加正确的代码行,并根据正确修复的概率大小进行回复",
    "user": "出错的代码:\n%s\n断言失败的代码行:%s报错信息:%s"
  },
  "T7": {
    "system": "你是程序修复领域的专家,接下来我会告诉你四种信息,1:包含了一个错误块的java代码,2:被移除的错误块(用<buggy chunk>表示)的内容,3:运行测试用例时断言失败的代码行, 4:断言失败的报错信息,请你根据以上信息思考出%s种可能在<buggy chunk>处的正确代码块,并根据正确修复的概率大小进行回复",
    "user": "包含错误块的代码:\n%s\n<buggy chunk>:%s\n断言失败的代码行:%s报错信息:%s"
  },
  "T8":{
      "user": "Erroneous Code Snippet:\n```%s\n%s\n```\nSuspected Bug Line:```%s```\nFailing Test Case Name: %s\nFailing Test Code Snippet:```%s```\nFailure Message:%s\nRequest:Please provide a brief analysis of the potential mistake in the code based on the information provided.(Analyze is not more than 300 tokens)"
  },
  "T9":{
      "system": "You are an Automated Program Repair Tool, please give %s answers in order of probability",
      "user": "Erroneous Code Snippet:\n```%s\n%s\n```\nLocation of the Error: The error is located at the <fill> placeholder. The <fill> was ```%s```.\nAnalysis of the Code Error: '''%s'''\nTask:Replace the <fill> placeholder with the correct line of code."
  },
  "T10":{
      "user": "Erroneous Code Snippet:\n```%s\n%s\n```\nSuspected Bug Lines:```%s```\nFailing Test Case Name: %s\nFailing Test Code Snippet:```%s```\nFailure Message:%s\nRequest:Please provide a brief analysis of the potential mistake in the code based on the information provided.(Analyze is not more than 300 tokens)"
  },
  "T11":{
      "system": "You are an Automated Program Repair Tool, please give %s answers in order of probability",
      "user": "Erroneous Code Snippet:\n```%s\n%s\n```\nLocation of the Error: The error is located at the <fill> placeholder. The <fill> was ```%s```.\nAnalysis of the Code Error: '''%s'''\nTask:Replace the <fill> placeholder with the correct lines of code."
  },
  "T12":{
   "user": "Erroneous Code Method:\n```%s\n%s\n```\nFailing Test Case Name: %s\nFailing Test Code Snippet:```%s```\nFailure Message:%s\nRequest:Please provide a brief analysis of the potential mistake in the code based on the information provided.(Analyze is not more than 300 tokens)"
 },
 "T13":{
   "system": "You are an Automated Program Repair Tool",
   "user": "Erroneous Code Method:\n```%s\n%s\n```\n Analysis of the Code Error: '''%s'''\nTask:Provide the correct method source code in Markdown format."
  }
}
