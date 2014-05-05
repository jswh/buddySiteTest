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
     <script type="text/javascript" language="JavaScript" src="../diff_match_patch.js"></script>
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
            fileName = str(caseNum) + case['HEADER']['HOST'] + '.html'
            print '''start test ''' + fileName
            resultFile = file('result/' + fileName, 'w')
            resultFile.truncate()
            i = 0
            num = len(self.__testTargets)
            for url in self.__testTargets :
                req = urllib2.Request(url + case['uri'])
                #case['HEADER']['HOST'] = case['HEADER']['HOST'][7:]
                self.__genRequestHeader(case['HEADER'], req)
                print '    target is ' + url + ' type is ' + case['method']
                if (case['method'] == 'POST') :
                    resp = urllib2.urlopen(req, case['QUERY'])
                else :
                    resp = urllib2.urlopen(req)
                content = resp.read()
                self.__writeResult(url, content, resultFile, i, num)
                i = i + 1
            resultFile.write(self.__script)
            resultFile.close()
            caseNum = caseNum + 1
        print 'Done!'
        #need to add POST type && add post query string
    def __writeResult(self, target, content, refile, i, num) :
        width = 100/num - 1;
        reContent = '''<div id="''' + str(i) + '''" class='linkResult' style='width:''' + str(width) + '''%'/>''' + cgi.escape(content) + '''</div>''' + '\n'
        refile.write(reContent)
    def caseInfo(self) :
        return self.__genRequest(self.__testCases[0]['HEADER'])
