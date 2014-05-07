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

###结果文件

测试结果会存放在result文件夹中。每一个testcase会有一个文件夹。compare.html文件是字符对比文件，用浏览器打开后可以查看
结果差异。每个target的结果也会存为单独的文件，默认后缀也是html，可以自行修改。
