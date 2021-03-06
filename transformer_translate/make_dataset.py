import random
import datetime
import re
import time
import os
from itertools import combinations, permutations
from random import shuffle
import config

# 直接根据原始数据做数据集
def def1():
    f = open("data", "r")
    fl = f.readlines()
    f.close()
    fl.reverse()
    lis = []
    # reslis=[]
    for line in fl:
        if not line.startswith("#"):
            temp = line.strip().split(" ")[1].split("+")
            # temp.sort() # 排序
            lis.append(" ".join(temp) + " <tag>")
            # lis.append(" ".join(temp))
        # else:
        #     reslis.append(lis)
        #     lis=[]
    print("合计 %d 期数据" % len(lis))
    # print(lis)
    f = open("./in.txt", "w")
    g = open("./out.txt", "w")
    #f1 = open("./1in.txt", "w")
    #g1 = open("./1out.txt", "w")
    datalis = []
    trainlis = []
    testlis = []
    """
    采用滑动窗口
    """
    i = 0
    while i < len(lis):
        if i >= 5:
            datalis.append((" ".join(lis[i - 5:i]).rstrip(" <tag>"), " ".join(sorted(lis[i].replace(" <tag>", "").split(" ")))))  # 预测五个 输出值不按顺序
            i += 1  # 不平滑 +=1  平滑 +=2
        else:
            i += 1
    """
    for i, line in enumerate(lis):
        if i >= 4:  # 根据前三条预测本条
            datalis.append((" ".join(lis[i - 4:i - 1]).rstrip(" <tag>"), lis[i].replace(" <tag>", ""))) # 预测五个
            # print(list(combinations(lis[i].replace(" <tag>", "").split(" "), 3)))
            # for sums in random.sample(list(combinations(lis[i].replace(" <tag>", "").split(" "), 3)), 5):  # 4个 3个
            #     datalis.append((" ".join(lis[i - 4:i - 1]).rstrip(" <tag>"), " ".join(sums)))
            # datalis.append((" ".join(lis[i - 4:i - 1]).rstrip(" <tag>")," ".join(lis[i].split(" ")[:3]) ))   # 前 三

        # if i >= 5:  # 根据前四条预测本条
        #     datalis.append((" ".join(lis[i-5:i-1]).rstrip(" <tag>"),lis[i].replace(" <tag>","")))
        # if i >= 6:  # 根据前五条预测本条
        #     datalis.append((" ".join(lis[i-6:i-1]).rstrip(" <tag>"),lis[i].replace(" <tag>","")))
        # if i != len(lis) - 1:
        #     datalis.append((line,lis[i + 1]))  # 5个
        #     datalis.append((line," ".join(lis[i+1].split(" ")[:3]))) # 前三
        #     for sums in combinations(lis[i + 1].split(" "), 4):  # 4个 3个
        #         datalis.append((line," ".join(sums)))
        #     for j in lis[i+1].split(" "): # 六个
        #        datalis.append((line,lis[i + 1] + " " + j))
    """
    for i, line in enumerate(datalis):
        if i % 10 == 1:
            testlis.append(line)
        else:
            trainlis.append(line)
    shuffle(trainlis)
    for ins, outs in trainlis:
        f.write(ins + "\n")
        g.write(outs + "\n")
    print("合计 %d 条训练集" % len(trainlis))

    shuffle(testlis)
    for ins, outs in testlis:  # np.random.shuffle(trainlis)
        f.write(ins + "\n")
        g.write(outs + "\n")
    print("合计 %d 条测试集" % len(testlis))
    f.close()
    g.close()
    # f1.close()
    # g1.close()


# 根据是否连续连续制作数据集
def def1_continue():
    f = open('./data/data', "r", encoding='utf-8')
    fl = f.readlines()
    f.close()
    src_sentences = []
    src_sen = []
    record = {}
    for i, line in enumerate(fl):
        if line.startswith("第"):
            if config.tag:
                src_sen.append(" ".join(re.findall(r'.{2}', re.sub("\D", "", fl[i + 1])))+" <tag>")  # 不加 <tag> 每句分界线
            else:
                src_sen.append(" ".join(re.findall(r'.{2}', re.sub("\D", "", fl[i + 1]))))  # 不加 <tag> 每句分界线
            # src_sen.append(" ".join(re.findall(r'.{2}', re.sub("\D", "", fl[i + 1]))) + " <tag>")  # 加 <tag> 每句分界线
            # src_sen.append(" ".join(re.findall(r'.{2}', re.sub("\D", "", fl[i+1])))) # 不加 每句分界线
            if " ".join(sorted(re.findall(r'.{2}', re.sub("\D", "", fl[i + 1])))) not in record:
                record[" ".join(sorted(re.findall(r'.{2}', re.sub("\D", "", fl[i + 1]))))] = 1
            else:
                record[" ".join(sorted(re.findall(r'.{2}', re.sub("\D", "", fl[i + 1]))))] += 1
        if "#" in line or i == len(fl) - 1:
            src_sen.reverse()
            src_sentences.append(src_sen)
            src_sen = []
    datalis = []
    num = config.history
    for reslis in src_sentences:
        i = 0
        while i < len(reslis):
            if i >= num:
                datalis.append((" ".join(reslis[i - num:i]).rstrip(" <tag>"),
                                " ".join(reslis[i].replace(" <tag>", "").split(" ")[-2:])))  # 预测前n个 输出值不按大小顺序
                                # " ".join(random.sample(reslis[i].replace(" <tag>", "").split(" "), 3))))  # 随机三个数
                # datalis.append((" ".join(reslis[i - num:i]).rstrip(" <tag>"),
                #                " ".join(sorted(reslis[i].replace(" <tag>", "").split(" ")))))  # 预测五个 输出值按大小顺序
                i += 1  # 不平滑 +=1  平滑 +=2
            else:
                i += 1
    f = open("./data/in.txt", "w")
    g = open("./data/out.txt", "w")
    trainlis = []
    testlis = []
    for i, line in enumerate(datalis):
        if i % 10 < 3:
            testlis.append(line)
        else:
            trainlis.append(line)
    shuffle(trainlis)
    for ins, outs in trainlis:
        f.write(ins + "\n")
        g.write(outs + "\n")
    print("合计 %d 条训练集" % len(trainlis))

    shuffle(testlis)
    for ins, outs in testlis:  # np.random.shuffle(trainlis)
        f.write(ins + "\n")
        g.write(outs + "\n")
    print("合计 %d 条测试集" % len(testlis))
    f.close()
    g.close()
    # f1.close()
    # g1.close()



def accquiresource(line):
    """
    和值 16-45 30
    跨度 04-10 7
    单双 0:5-5:0  6
    :param line:
    :return:
    """
    Sums = {15: "r", 16: "A", 17: "B", 18: "C", 19: "D", 20: "E", 21: "F", 22: "G", 23: "H", 24: "I", 25: "J",
            26: "K", 27: "L", 28: "M", 29: "N", 30: "O", 31: "P", 32: "Q", 33: "R", 34: "S", 35: "T",
            36: "U", 37: "V", 38: "W", 39: "X", 40: "Y", 41: "Z", 42: "a", 43: "b", 44: "c", 45: "d"}  # 和值
    Span = {4: "e", 5: "f", 6: "g", 7: "h", 8: "i", 9: "j", 10: "k"}  # 跨度
    Parity = {0: "l", 1: "m", 2: "n", 3: "o", 4: "p", 5: "q"}  # 奇
    # 46:"",47:"",48:"",49:"",50:"",51:"",52:"",53:"",54:"",55:"",
    #           56:"",57:"",58:"",59:"",60:"",61:"",:"",:"",:"",:"",:"",:"",:"",:"",
    result = []
    sumvalue = 0
    sumspan = 0
    Paritys = []
    for value in line.split(" "):
        sumvalue += int(value)
        if int(value) % 2 == 0:
            sumspan += 1
        result.append(value)
        Paritys.append(int(value))

    result.append(Sums[sumvalue])
    result.append(Span[max(Paritys) - min(Paritys)])
    result.append(Parity[sumspan])

    return " ".join(result)


def accquireresult(line):
    # result = []
    return line


def def2():
    f = open("data", "r")
    fl = f.readlines()
    f.close()
    fl.reverse()
    lis = []
    for line in fl:
        if "#" not in line:
            lis.append(" ".join(line.strip().split(" ")[1].split("+")))
    print("合计 %d 期数据" % len(lis))
    f = open("./in.txt", "w")
    g = open("./out.txt", "w")
    f1 = open("./1in.txt", "w")
    g1 = open("./1out.txt", "w")
    trainlis = []
    testlis = []
    datalis = []
    for i, line in enumerate(lis):
        if i != len(lis) - 1:
            datalis.append((accquiresource(lis[i]), accquiresource(lis[i + 1])))

    for i, line in enumerate(datalis):
        if i % 10 == 1:
            testlis.append(line)
        else:
            trainlis.append(line)
    shuffle(trainlis)
    for ins, outs in trainlis:
        f.write(ins + "\n")
        g.write(outs + "\n")
    print("合计 %d 条训练集" % len(trainlis))
    shuffle(testlis)
    for ins, outs in testlis:  # np.random.shuffle(trainlis)
        f1.write(ins + "\n")
        g1.write(outs + "\n")
    print("合计 %d 条测试集" % len(testlis))
    f.close()
    g.close()
    f1.close()
    g1.close()


def def3():
    f = open("data", "r")
    fl = f.readlines()
    f.close()
    fl.reverse()
    lis = []
    for line in fl:
        if "#" not in line:
            lis.append(" ".join(line.strip().split(" ")[1].split("+")))
    print("合计 %d 期数据" % len(lis))
    # print(lis)
    f = open("./in.txt", "w")
    g = open("./out.txt", "w")

    f1 = open("./1in.txt", "w")
    g1 = open("./1out.txt", "w")
    datalis = []
    testlis = []
    trainlis = []
    """
    采用滑动窗口
    """
    i = 0
    while i < len(lis):
        if i >= 3:
            data = []
            for j in " ".join(lis[i - 3:i]).split(" "):
                if j not in data:
                    data.append(j)
            datalis.append((" ".join(data), lis[i]))
            i += 1  # 不平滑 +=1  平滑 +=2
        else:
            i += 1

    # for i, line in enumerate(lis):
    #     if i >= 4:  # 根据前三条预测本条
    #         trainlis.append((" ".join(lis[i - 4:i - 1]).rstrip(" <tag>"), lis[i].replace(" <tag>", "")))
    #     # if i >= 5:  # 根据前四条预测本条
    #     #     trainlis.append((" ".join(lis[i-5:i-1]).rstrip(" <tag>"),lis[i].replace(" <tag>","")))
    #     # if i >= 6:  # 根据前五条预测本条
    #     #     trainlis.append((" ".join(lis[i-6:i-1]).rstrip(" <tag>"),lis[i].replace(" <tag>","")))
    #     # if i != len(lis) - 1:
    #     #     trainlis.append((line,lis[i + 1]))  # 5个
    #     #     trainlis.append((line," ".join(lis[i+1].split(" ")[:3]))) # 前三
    #     #     for sums in combinations(lis[i + 1].split(" "), 4):  # 4个 3个
    #     #         trainlis.append((line," ".join(sums)))
    #     #     for j in lis[i+1].split(" "): # 六个
    #     #        trainlis.append((line,lis[i + 1] + " " + j))

    for i, line in enumerate(datalis):
        if i % 10 == 1:
            testlis.append(line)
        else:
            trainlis.append(line)

    shuffle(trainlis)
    for ins, outs in trainlis:
        f.write(ins + "\n")
        g.write(outs + "\n")
    print("合计 %d 条训练集" % len(trainlis))
    shuffle(testlis)
    for ins, outs in testlis:  # np.random.shuffle(trainlis)
        f.write(ins + "\n")
        g.write(outs + "\n")
    print("合计 %d 条测试集" % len(testlis))
    f.close()
    g.close()
    f1.close()
    g1.close()


def make_pre_model_data():
    a = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11"]
    i = 0
    datalis=[]
    lis=[]
    while i < 10000:
        lis.append(" ".join(random.sample(a, 5))+" <tag>")
        i+=1
    i = 0
    while i < len(lis):
        if i >= 5:
            datalis.append((" ".join(lis[i - 5:i]).rstrip(" <tag>"), lis[i].replace(" <tag>", "")))  # 预测五个 输出值不按顺序
            i += 1  # 不平滑 +=1  平滑 +=2
        else:
            i += 1
    f = open("./in.txt", "w")
    g = open("./out.txt", "w")
    shuffle(datalis)
    for ins, outs in datalis:
        f.write(ins + "\n")
        g.write(outs + "\n")
    print("合计 %d 条训练集" % len(datalis))
    f.close()
    g.close()
    print("train 数据制作完成")


def def4():
    f = open("data", "r")
    fl = f.readlines()
    f.close()
    fl.reverse()
    lis = []
    for line in fl:
        if "#" not in line:
            temp = line.strip().split(" ")[1].split("+")
            # temp.sort() # 排序
            lis.append(" ".join(temp) + " <tag>")
            # lis.append(" ".join(temp))
    print("合计 %d 期数据" % len(lis))
    # print(lis)
    f = open("./in.txt", "w")
    g = open("./out.txt", "w")
    f1 = open("./1in.txt", "w")
    g1 = open("./1out.txt", "w")
    datalis = []
    trainlis = []
    testlis = []
    """
    采用滑动窗口
    """
    i = 0
    while i < len(lis):
        if i >= 3:
            # data=[]
            # for j in " ".join(lis[i - 4:i - 1]).split(" "):
            #     if j not in data:
            #         data.append(j)
            # datalis.append((" ".join(data),lis[i]))
            # list(permutations(lis[i].replace(" <tag>", "").split(" "), 5))
            # datalis.append((" ".join(lis[i - 4:i - 1]).rstrip(" <tag>"), lis[i].replace(" <tag>", "")))  # 预测五个
            for lis4 in random.sample(list(permutations(lis[i - 4].replace(" <tag>", "").split(" "), 5)), 5):  # 随机挑5条
                for lis3 in random.sample(list(permutations(lis[i - 3].replace(" <tag>", "").split(" "), 5)),5):  # 随机挑5条
                    for lis2 in random.sample(list(permutations(lis[i - 2].replace(" <tag>", "").split(" "), 5)),5):  # 随机挑5条
                        datalis.append((" ".join(lis4) + " <tag> " + " ".join(lis3) + " <tag> " + " ".join(lis2),lis[i].replace(" <tag>", "")))  # 预测五个
            i += 2  # 不平滑 +=1  平滑 +=2
        else:
            i += 1
    """
    for i, line in enumerate(lis):
        if i >= 4:  # 根据前三条预测本条
            datalis.append((" ".join(lis[i - 4:i - 1]).rstrip(" <tag>"), lis[i].replace(" <tag>", ""))) # 预测五个
            # print(list(combinations(lis[i].replace(" <tag>", "").split(" "), 3)))
            # for sums in random.sample(list(combinations(lis[i].replace(" <tag>", "").split(" "), 3)), 5):  # 4个 3个
            #     datalis.append((" ".join(lis[i - 4:i - 1]).rstrip(" <tag>"), " ".join(sums)))
            # datalis.append((" ".join(lis[i - 4:i - 1]).rstrip(" <tag>")," ".join(lis[i].split(" ")[:3]) ))   # 前 三

        # if i >= 5:  # 根据前四条预测本条
        #     datalis.append((" ".join(lis[i-5:i-1]).rstrip(" <tag>"),lis[i].replace(" <tag>","")))
        # if i >= 6:  # 根据前五条预测本条
        #     datalis.append((" ".join(lis[i-6:i-1]).rstrip(" <tag>"),lis[i].replace(" <tag>","")))
        # if i != len(lis) - 1:
        #     datalis.append((line,lis[i + 1]))  # 5个
        #     datalis.append((line," ".join(lis[i+1].split(" ")[:3]))) # 前三
        #     for sums in combinations(lis[i + 1].split(" "), 4):  # 4个 3个
        #         datalis.append((line," ".join(sums)))
        #     for j in lis[i+1].split(" "): # 六个
        #        datalis.append((line,lis[i + 1] + " " + j))
    """
    for i, line in enumerate(datalis):
        if i % 10 == 1:
            testlis.append(line)
        else:
            trainlis.append(line)
    shuffle(trainlis)
    for ins, outs in trainlis:
        f.write(ins + "\n")
        g.write(outs + "\n")
    print("合计 %d 条训练集" % len(trainlis))

    shuffle(testlis)
    for ins, outs in testlis:  # np.random.shuffle(trainlis)
        f1.write(ins + "\n")
        g1.write(outs + "\n")
    print("合计 %d 条测试集" % len(testlis))
    f.close()
    g.close()
    f1.close()
    g1.close()


if __name__ == '__main__':
    #if not os.path.exists("./train"):
    #    os.makedirs("./train")
    #if not os.path.exists("./test"):
    #    os.makedirs("./test")
    #make_pre_model_data()  # 制作预训练数据，做预训练数据模型 前3预5

    # def1() #直接根据数据集制作
    def1_continue()  # 期数关联 # 后期与此方法多有有关 前5预5

    # def2() # 加入和跨奇偶
    # def3()  # 合并重复字 还可以进行 数据平滑操做
    # def4()  # 数据增强 排列组合 增加数据量

    """
    解析 任五共有462种,排序55440种
    解析 任三共有165种,排序990种 
    """
print("done")
