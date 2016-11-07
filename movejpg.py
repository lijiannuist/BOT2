txtfile = open('test.txt' , 'rb')
img = []
for line in txtfile.readlines():
    print type(line) 
    #linedata = line.strip('\n').split(' ')
    print linedata
      data.append(linedata)