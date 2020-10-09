# coding=utf-8
import os


def getpath():

    # 当前路径
    path = os.path.join(os.getcwd())

    # # 获取当前目录
    # print(os.getcwd())
    # print(os.path.split(os.path.realpath(__file__))[0])
    # print(os.path.abspath(os.path.dirname(__file__)))
    #
    # # 获取上级目录
    # print(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
    # print(os.path.abspath(os.path.dirname(os.getcwd())))
    # print(os.path.abspath(os.path.join(os.getcwd(), "..")))

    return path


if __name__ == "__main__":
    a = getpath()
    print(a)
