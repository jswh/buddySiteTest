import os

def getFile(rootDir, temp) :
    for lists in os.listdir(rootDir):
        temp.append(lists)
    return temp
def genTree() :
    folder = []
    folder = getFile('result', folder)
    treeFile = file('navi/tree.js', 'w')
    treeFile.write('''var getTree = function() { return "''')
    treeFile.write('<div class=\'folderTree\'>')
    for fd in folder :
        files = []
        files = getFile('result/' + fd, files)
        treeFile.write('<a id=\'folder\' onclick=\'changeView(this)\'>' + fd +'</a>')
        treeFile.write('<div class=\'fileTree\'>')
        for f in files :
            treeFile.write('<a id=\'file\' onclick=\'changeView(this)\'>' + f +'</a>')
        treeFile.write('</div>')
    treeFile.write('</div>')

    treeFile.write('''";}''')
    treeFile.close()
