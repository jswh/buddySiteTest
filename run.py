from BuddySite import BuddySiteTest
import tree
import os
import shutil
import time
#BuddySiteTest(logName = 'testcases', target = 'target')
run = BuddySiteTest()
run.execute()

print 'wait for generating result view tree...\n'
tree.genTree()
print 'wait for creating history'
if not(os.path.isdir('history')) :
    os.makedirs('history')
timeStamp = str(time.time())
shutil.copytree('navi', 'history/' + timeStamp + '/navi')
shutil.copytree('result', 'history/' + timeStamp + '/result')

print 'Done!Done!Done!'
print 'all results are in result folder,and you can view the differences by opening navi.html in folder "navi"'
