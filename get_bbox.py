#encoding=utf-8
import os
import json     # read json file
import sys
import xlrd     # read excel file

def get_category_id(input, csv_fname='/data2/lijian/BOT2/code/ProductCategoryInfo.xlsx'):
    '''
    通过输入的中文商品类别，获取其ID
    :return:
    '''
    id = 0
    myWorkbook = xlrd.open_workbook(csv_fname)  # 这是整个excel文件，里面可以包含多个sheet
    table = myWorkbook.sheet_by_name(u'Sheet1') # 这里相当于取出其中的一个工作表
    nrows = table.nrows  # 行数
    for rownum in range(1, nrows):
        row = table.row_values(rownum)
        if input == row[3]:
            id = str(row[0])
            break
    return id

if __name__ == '__main__':
    [{"filename": "Sfff177acc094443eb5f20c0b2bd188be", "width": 3264, "heigth": 2448, "products": [
        {"category": "飘柔|焗油护理洗发露",
         "segm": ["2819, 1720", "2801, 1810", "2867, 1852", "2825, 2008", "2861, 2283", "2879, 2325", "3034, 2319",
                  "3076, 2265", "3100, 2319", "3262, 2331", "3256, 1876", "3220, 1822", "3220, 1762", "3214, 1696",
                  "3160, 1750", "2986, 1654", "2843, 1696", "2819, 1720"],
         "bbox": {"MaxX": 3262, "MaxY": 2331, "MinX": 2801, "MinY": 1654}}, {"category": "飘柔|滋润去屑洗发露",
                                                                             "segm": ["1908, 1738", "1908, 1846",
                                                                                      "1860, 2008", "1848, 2241",
                                                                                      "1872, 2325", "2058, 2325",
                                                                                      "2088, 2253", "2088, 2074",
                                                                                      "2058, 1870", "2022, 1846",
                                                                                      "2016, 1750", "1908, 1738"],
                                                                             "bbox": {"MaxX": 2088, "MaxY": 2325,
                                                                                      "MinX": 1848, "MinY": 1738}}]},
     {"filename": "Sffc875a69f7c450ba3892198fcfeab5f", "width": 3264, "heigth": 2448, "products": [
         {"category": "丝蕴|无硅修护系列",
          "segm": ["2998, 1636", "2998, 1636", "3208, 1630", "3256, 1636", "3264, 1229", "3226, 1211", "3220, 1097",
                   "3076, 1109", "3082, 1199", "2998, 1235", "2998, 1636"],
          "bbox": {"MaxX": 3264, "MaxY": 1636, "MinX": 2998, "MinY": 1097}}, {"category": "丝蕴|无硅水润系列",
                                                                              "segm": ["3064, 840", "3064, 840",
                                                                                       "3064, 432", "3154, 396",
                                                                                       "3154, 277", "3256, 271",
                                                                                       "3244, 828", "3250, 828",
                                                                                       "3064, 840"],
                                                                              "bbox": {"MaxX": 3256, "MaxY": 840,
                                                                                       "MinX": 3064, "MinY": 271}}]}]
    root_dir = '/data2/lijian/BOT2/code/'
    os.chdir(root_dir)
    shampoo_json = 'test_Shampoo.json'
    f = open(shampoo_json, 'r')
	
    # potato_json = 'potatoTags.json'
    # f = open(potato_json, 'r')
    
	# noodle_json = 'noodle_final.json'
    # noodle_json = 'check_noodle.json'
    # f = open(noodle_json, 'r')
    json_list = json.load(fp=f, encoding='utf-8')

    # 定义关于文件存储的相关变量，每一个的filename都对应一个txt文件
    txt_count = 0
    txt_root_dir = os.path.join(root_dir, 'newLabels/3')
    if not os.path.exists(txt_root_dir):
        os.mkdir(txt_root_dir)

    # 整个json文件的目录都是以filename构成的list文件一个个组成
    for per_json in json_list:
        # print per_json.keys()
        print per_json['filename']
        product_lists = per_json['products']
        # 每个文件都会对其拥有的products进行分割和bbox，如果当前区域不包含任何类别，则整个products属性为空
        product_count = 0
        cur_bboxes = []
        cur_categories = []
        # 自动过滤掉product_lists = NULL的情形
        if product_lists == []:
            continue
        else:
            for per_product in product_lists:
                product_count += 1
                print per_product['category'], per_product['bbox']
                #category = get_category_id((per_product['category']).split('|')[1])
                category = per_product['category']
				# Get the bbox 4 position
                xmin = per_product['bbox']['MinX']
                ymin = per_product['bbox']['MinY']
                xmax = per_product['bbox']['MaxX']
                ymax = per_product['bbox']['MaxY']
                # print xmin, ymin, xmax, ymax
                bbox = [xmin, ymin, xmax, ymax]
                cur_bboxes.append(bbox)
                cur_categories.append(category)
        # 将获取的bboxes信息写入文本
        cur_txt_name = per_json['filename'] + '.txt'
        # print cur_categories
        with open(os.path.join(txt_root_dir, cur_txt_name), 'w') as fwrite:
            fwrite.write(( str(product_count) + '\n'))
            print cur_categories
            for i in xrange(product_count):
                per_line = cur_categories[i] + ' ' + str(cur_bboxes[i][0]) + ' ' + str(cur_bboxes[i][1]) + ' ' + str(cur_bboxes[i][2]) + ' ' + str(cur_bboxes[i][3]) + '\n'
                fwrite.write(per_line)

