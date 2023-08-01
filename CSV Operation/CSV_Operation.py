import csv
FilePath = "./xxx.csv"

#行读取 i的遍历起始值决定是否去除表头
with open(FilePath, newline = '') as csvfile:
    FilePath_Reader = csv.reader(csvfile, delimiter = ',')
    for row in FilePath_Reader:
        for i in range(len(row)):
            print("不去表头逐行单次输出为", row[i])

#列读取 j的遍历起始值决定是否去除表头
with open(FilePath, newline='') as csvfile:
        FilePath_Reader = csv.reader(csvfile, delimiter=',')
        for i in range(len(row)):
            column = [row[i] for row in FilePath_Reader]
            for j in range(1, len(column)):
                print("去表头逐列输出单次为", column[j])

#行/多行写入
with open(FilePath, 'w') as csvfile:
    FilePath_Writer = csv.writer(FilePath)
    FilePath_Writer.writerow()
    FilePath_Writer.writerows()
    