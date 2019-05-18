import random


# print(str(random.randrange(0, 10, step=2)))

# print(list(range(10, -1)))


def print_jpg(n):
    # 打印上半部分
    for i in range(1, n + 1, 2):
        # 空格加上*号
        img = ' ' * ((n - i) // 2) + "*" * i
        print(img)

    if n % 2 == 0:
        s = n - 1
    else:
        s = n - 2

    # 打印下半部分
    for i in range(s, 0, -2):
        img = ' ' * ((n - i) // 2) + "*" * i
        print(img)

print_jpg(6)


"""
传入一个Json串，返回一个字典，字典只取出Json最底层的数据，中间如果有字符串也要进行处理，请以下面的数据为例，请用递归方法实现
Json：{"a":"aa","b":['{"c":"cc","d":"dd"}',{"f":{"e":"ee"}}]}
输出：Dic:{'a':'aa','c':'cc','d':'dd','e':'ee'})
"""

# def find_dict(str):