import __init__

def dumpList2File(listObj, fn) :
    output = file(fn, 'w')
    for item in listObj :
        if hasattr(item, '__iter__') :
            output.write('\t'.join([str(subitem) for subitem in item]) + '\n')
        else :
            output.write(item + '\n')
    output.close()

def dumpDict2File(dictObj, fn) :
    output = file(fn, 'w')
    format = '%s\x01%s\n'
    for key in dictObj :
        value = dictObj[key]
        if hasattr(value, '__iter__') :
            output.write(format % (key, '\t'.join([str(subitem) for subitem in value])))
        else :
            output.write(format % (key, value))
    output.close()