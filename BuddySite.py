#!/usr/bin/python
# Filename : BuddySite.py

import json
import urllib
import urllib2
import cgi
import os.path
import md5
import time
import appkey
class BuddySiteTest :
    __testCases = {}
    __testTargets = []
    __script = '''
     <script type="text/javascript" language="JavaScript" src="../../navi/diff_match_patch.js"></script>
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
            try :
                name = line.split('info:')[0]
                info = line.split('info:')[1]
                case = json.loads(info)
                if(not(isinstance(case['QUERY'], basestring))) :
                    case['QUERY'] = json.dumps(case['QUERY'])
                if(case['method'] == 'POST') :
                    appKey = case['HEADER']['BAPI_APP_KEY']
                    hashKey = case['uri'] + case['QUERY'] + appkey.getSec(appKey)
                    case['HEADER']['BAPI_HASH'] = md5.md5(hashKey).hexdigest()
                self.__testCases[name] = case
            except :
                if(line != '\n') :
                    print "case error"
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
        caseId = 1;
        for name in self.__testCases :
            case = self.__testCases[name]
            fileName = name.replace('/', '|')
            print '''start test ''' + fileName
            if not(os.path.isdir('result')) :
                os.makedirs('result')
            resultFilePath = 'result/' + str(caseId) + fileName[0:200] + '/'
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
                try :
                    if (case['method'] == 'POST') :
                        resp = urllib2.urlopen(req, case['QUERY'])
                    else :
                        resp = urllib2.urlopen(req)
                    content = resp.read()
                except :
                    content = url + " connect failed"
                print content
                self.__writeResult(url, content, resultFilePath, i, caseNum)
                i = i + 1
                time.sleep(0.1)
            cmpFile = file(resultFilePath + 'compare.html', 'a')
            cmpFile.write(self.__script)
            cmpFile.close()
            caseId = caseId + 1
        print 'Test finished!\n'
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
