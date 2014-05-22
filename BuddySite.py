#!/usr/bin/python
# Filename : BuddySite.py

import json
import urllib
import urllib2
import cgi
import os.path
class BuddySiteTest :
    __testCases = []
    __testTargets = []
    __script = '''
     <script type="text/javascript" language="JavaScript" src="../../diff_match_patch.js"></script>
	<script type="text/javascript" language="JavaScript">
		var dmp = new diff_match_patch();
		var textOri = document.getElementById('0');
		var i = 1;
		var textNew = document.getElementById(i);
		while(textNew) {
		dmp.Diff_Timeout = 15;

		var d = dmp.diff_main(textOri.innerText, textNew.innerText);
		var ds = dmp.diff_prettyHtml(d);
		textNew.innerHTML = ds ;
		textNew = document.getElementById(++i)
		}
	</script><style>
		.linkResult{
			border:solid 1px grey;
			float:left;
			overflow: hidden;
			word-wrap: break-word;
			margin-right: 0.5%;
		}
	</style>
    '''
    def __init__(self, logName = 'testcases', target = 'target') :
        self.__setTestCase(logName)
        self.__setTargets(target)
    def __setTestCase(self, logName) :
        f = file(logName, 'r')
        for line in f :
            case = json.loads(line.split('info:')[1])
            self.__testCases.append(case)
        f.close()

    def __setTargets(self, target) :
        f = file(target, 'r')
        for url in f :
            self.__testTargets.append(url.strip())
        f.close()

    def __genTargetUrl(self, host, target) :
        hostParams = host.split('.')
        temp = target.split('//')
        reqType = temp[0]
        targetParams = temp[1].split('.')
        hostParams[-3] = targetParams[-3]
        url = ''
        for param in hostParams :
            url = url + '.' + param
        return reqType + '//' + url[1:]
    def __genRequestHeader(self,headers,req) :
        for key in headers :
            req.add_header(key, headers[key])

    def __genPostData (self, queryString) :
        data = {}
        querys = queryString.split('&')
        for query in querys :
            KeyVal = query.split('=')
            data[KeyVal[0]] = KeyVal[1]
        return data
    def execute(self) :
        caseNum = 1;
        for case in self.__testCases :
            fileName = str(caseNum) + case['HEADER']['HOST'] + case['uri'].replace('/', '|')
            print '''start test ''' + fileName
            if not(os.path.isdir('result')) :
                os.makedirs('result')
            resultFilePath = 'result/' + fileName[0:200] + '/'
            if not(os.path.isdir(resultFilePath)) :
                os.makedirs(resultFilePath)
            i = 0
            caseNum = len(self.__testTargets)
            cmpFile = file(resultFilePath + 'compare.html', 'w')
            cmpFile.truncate()
            cmpFile.close()
            for url in self.__testTargets :
                url = self.__genTargetUrl(case['HEADER']['HOST'], url)
                req = urllib2.Request(url + case['uri'])
                case['HEADER']['HOST'] = url.split('//')[1]
                self.__genRequestHeader(case['HEADER'], req)
                print '    target is ' + url + ' type is ' + case['method']
                try:
                    if (case['method'] == 'POST') :
                        resp = urllib2.urlopen(req, case['QUERY'])
                    else :
                        resp = urllib2.urlopen(req)
                    content = resp.read()
                except:
                    content = 'url connect failed'
                print content
                self.__writeResult(url, content, resultFilePath, i, caseNum)
                i = i + 1
            cmpFile = file(resultFilePath + 'compare.html', 'a')
            cmpFile.write(self.__script)
            cmpFile.close()
            caseNum = caseNum + 1
        print 'Done!'
        #need to add POST type && add post query string
    def __writeResult(self, target, content, refilePath, i, num) :
        cmpFile = file(refilePath + 'compare.html', 'a')
        width = 100/num - 1;
        reContent = '''<div id="''' + str(i) + '''" class='linkResult' style='width:''' + str(width) + '''%'/>''' + cgi.escape(content) + '''</div>''' + '\n'
        cmpFile.write(reContent)
        cmpFile.close()
        resultFile = file(refilePath + target.split('//')[1] + '.html', 'w')
        resultFile.write(content)
        resultFile.close()
    def caseInfo(self) :
        return self.__genRequest(self.__testCases[0]['HEADER'])
