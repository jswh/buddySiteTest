buddySiteTest
=============
###一般运行
1. 将使用HttpRequestLogging::logFullInfo()记录下来的log文件改名为testcases放入程序目录
2. 修改target文件，增加需测试的地址
3. 运行run.py
###自定义文件运行
修改run.py，在建立BuddySiteTest类时传入对应文件的地址

    run = BuddySiteTest('yourTestcasesFile', 'yourTargetFile');
运行run.py
