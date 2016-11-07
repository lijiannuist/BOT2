#encoding=utf-8
import os
import sys
import numpy as np

if __name__ == '__main__':
    root_dir = '/data2/lijian/BOT2/38_Annotations/'
    trainval_file = 'test38_trainval.txt'
    test_file = 'test38_test.txt'
    test_num = 4   # 表示有多少数据用来测试
    all_samples = os.listdir(root_dir)
    new_all_samples = []
    for sample in all_samples:
        cur_sample = sample.replace('.xml', '')
        new_all_samples.append(cur_sample)
    print new_all_samples[:10]
    np.random.shuffle(new_all_samples)
    print new_all_samples[:10]

    trainval_samples = new_all_samples[test_num:]
    test_samples = new_all_samples[:test_num]
    print len(trainval_samples), len(test_samples)
    # 将数据写入文本中
    with open(trainval_file, 'w') as fwrite:
        for train in trainval_samples:
            per_line = str(train) + '\n'
            fwrite.write(per_line)
    with open(test_file, 'w') as fwrite:
        for test in test_samples:
            per_line = str(test) + '\n'
            fwrite.write(per_line)
