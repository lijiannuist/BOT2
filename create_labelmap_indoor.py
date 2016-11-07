#encoding=utf-8
if __name__ == '__main__':
    label_start = 153
    label_end = 241 # 比结束的数字+1
    label_dis = label_end - label_start 
    names = []
    labelmap_dir = 'labelmap_indoor.prototxt'
    for i in xrange(1, label_dis):
        name = "P" + str("%04d" %i)
        names.append(name)
    print names
    with open(labelmap_dir, 'w') as fwrite:         
        for i in xrange(1, label_dis):    
            one_line = "item {" + "\n"
            fwrite.write(one_line)
            one_line = "name: " + "\"%s\"" %names[i-1] + '\n'
            fwrite.write(one_line)
            one_line = "label: %d" %(i-1+label_start) + "\n"
            fwrite.write(one_line)
            one_line = "display_name: " + "\"%s\"" %names[i-1] + '\n'
            fwrite.write(one_line)
            one_line = "}" + '\n'
            fwrite.write(one_line)
