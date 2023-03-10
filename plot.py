'''
@File   :   plot.py
@Author :   boysusu
@Desc   :   读取仿真结果数据处理并绘制折线图
'''

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt, ticker

import matplotlib as mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['font.serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False
plt.rcParams.update({"font.size":12})
dpi = 100

def plot_V2R_B():
    V2R_B_l = [i for i in range(20, 121, 10)]

    local_delays = []
    V2R_V2V_delays = []
    for i in range(20, 121, 10):
        fileNameStr = f'./result/result(V2R_channel_bandwidth={i}MHz).xlsx'
        xl = pd.read_excel(fileNameStr, usecols=['本地计算处理总时延(s)', '协同节点处理总时延(s)'])
        t1 = xl['本地计算处理总时延(s)']
        t2 = xl['协同节点处理总时延(s)']
        sum_t = 0
        for k in range(len(t2)):
            if pd.isnull(t2[k]):
                sum_t += t1[k]
            else:
                sum_t += t2[k]
        local_delays.append(sum(t1) / len(t1))
        V2R_V2V_delays.append(sum_t / len(t2))

    # 绘图（在一个刻度的两边分别绘制两条柱状图）
    # width = 0.2  # 设置一个固定宽度
    # po_l = [i - width / 2 for i in range(len(V2R_B_l))]
    # po_r = [i + width / 2 for i in range(len(V2R_B_l))]
    # print(po_l,po_r)
    # [-0.15, 0.85, 1.85, 2.85] [0.15, 1.15, 2.15, 3.15]

    # print(local_delays, V2R_V2V_delays)
    # plt.bar(po_l, local_delays, width=width, label='local')
    # plt.bar(po_r, V2R_V2V_delays, width=width, label='xiezuo')

    # plt.plot(local_delays, color='r', linewidth=2, linestyle=':', marker='o', label='本地计算')  # color指定线条颜色，labeL标签内容
    plt.plot(V2R_V2V_delays, color='g', linewidth=2, linestyle=':', marker='o',label='协同计算')  # linewidth指定线条粗细

    # 设置刻度
    plt.xticks(range(len(V2R_B_l)), V2R_B_l)

    # 设置坐标标签
    plt.xlabel('V2R信道带宽(MHz)')
    plt.ylabel('计算任务完成平均时延(s)')

    # 设置图例
    plt.legend()

    # 展示
    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(2))
    plt.title('V2R信道带宽与平均时延关系图')
    plt.savefig('V2R信道带宽与平均时延关系图.png', dpi=dpi)
    plt.show()

def plot_X():
    X_l = [i for i in range(100, 1001, 100)]

    local_delays = []
    V2R_V2V_delays = []
    for i in range(100, 1001, 100):
        fileNameStr = f'./result/result(X={i}).xlsx'
        xl = pd.read_excel(fileNameStr, usecols=['本地计算处理总时延(s)', '协同节点处理总时延(s)'])
        t1 = xl['本地计算处理总时延(s)']
        t2 = xl['协同节点处理总时延(s)']
        sum_t = 0
        for k in range(len(t2)):
            if pd.isnull(t2[k]):
                sum_t += t1[k]
            else:
                sum_t += t2[k]
        local_delays.append(sum(t1) / len(t1))
        V2R_V2V_delays.append(sum_t / len(t2))

    # 绘图（在一个刻度的两边分别绘制两条柱状图）
    # width = 0.2  # 设置一个固定宽度
    # po_l = [i - width / 2 for i in range(len(X_l))]
    # po_r = [i + width / 2 for i in range(len(X_l))]
    # print(po_l,po_r)
    # [-0.15, 0.85, 1.85, 2.85] [0.15, 1.15, 2.15, 3.15]

    # plt.bar(po_l, local_delays, width=width, label='local')
    # plt.bar(po_r, V2R_V2V_delays, width=width, label='xiezuo')
    plt.plot(local_delays, color='r', linewidth=2, linestyle=':', marker='o', label='本地计算')
    plt.plot(V2R_V2V_delays, color='g', linewidth=2, linestyle=':', marker='o', label='协同计算')

    # 设置刻度
    plt.xticks(range(len(X_l)), X_l)

    # 设置坐标标签
    plt.xlabel('计算任务复杂度(cycles/bit)')
    plt.ylabel('计算任务完成平均时延(s)')

    # 设置图例
    plt.legend()

    # 展示
    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(2))
    plt.title('计算任务复杂度与平均时延关系图')
    plt.savefig('计算任务复杂度与平均时延关系图.png', dpi=dpi)
    plt.show()


def plot_data_size():
    data_size_l = np.arange(0.5, 5.01, 0.5)
    for i in range(len(data_size_l)):
        data_size_l[i] = round(data_size_l[i], 2)

    local_delays = []
    V2R_V2V_delays = []
    for data_size in data_size_l:
        fileNameStr = f'./result/result(data_size={data_size}Mbit).xlsx'
        xl = pd.read_excel(fileNameStr, usecols=['本地计算处理总时延(s)', '协同节点处理总时延(s)'])
        t1 = xl['本地计算处理总时延(s)']
        t2 = xl['协同节点处理总时延(s)']
        sum_t = 0
        for k in range(len(t2)):
            if pd.isnull(t2[k]):
                sum_t += t1[k]
            else:
                sum_t += t2[k]
        local_delays.append(sum(t1) / len(t1))
        V2R_V2V_delays.append(sum_t / len(t1))

    # 绘图（在一个刻度的两边分别绘制两条柱状图）
    width = 0.2  # 设置一个固定宽度
    # po_l = [i - width / 2 for i in range(len(data_size_l))]
    # po_r = [i + width / 2 for i in range(len(data_size_l))]
    # print(po_l,po_r)
    # [-0.15, 0.85, 1.85, 2.85] [0.15, 1.15, 2.15, 3.15]

    # plt.bar(po_l, local_delays, width=width, label='local')
    # plt.bar(po_r, V2R_V2V_delays, width=width, label='xiezuo')

    plt.plot(local_delays, color='r', linewidth=2, linestyle=':', marker='o', label='本地计算')
    plt.plot(V2R_V2V_delays, color='g', linewidth=2, linestyle=':', marker='o',label='协同计算')

    # 设置刻度
    plt.xticks(range(len(data_size_l)), data_size_l)

    # 设置坐标标签
    plt.xlabel('计算任务数据量(Mbit)')
    plt.ylabel('计算任务完成平均时延(s)')

    # 设置图例
    plt.legend()

    # 展示
    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(2))
    plt.title('计算任务数据量与平均时延关系图')
    plt.savefig('计算任务数据量与平均时延关系图.png', dpi=dpi)
    plt.show()


def plot_task_release_speed():
    size_l = np.arange(5, 41, 5)

    local_delays = []
    V2R_V2V_delays = []
    for size in size_l:
        fileNameStr = f'./result/result(task_release_speed={size}).xlsx'
        xl = pd.read_excel(fileNameStr, usecols=['本地计算处理总时延(s)', '协同节点处理总时延(s)'])
        t1 = xl['本地计算处理总时延(s)']
        t2 = xl['协同节点处理总时延(s)']
        sum_t = 0
        for k in range(len(t2)):
            if pd.isnull(t2[k]):
                sum_t += t1[k]
            else:
                sum_t += t2[k]
        local_delays.append(sum(t1) / len(t1))
        V2R_V2V_delays.append(sum_t / len(t1))

    print(local_delays)
    print(V2R_V2V_delays)
    #
    # for i in range(len(size_l)):
    #     size_l[i] = size_l[i]
    # 绘图（在一个刻度的两边分别绘制两条柱状图）
    # width = 0.2  # 设置一个固定宽度
    # po_l = [i - width / 2 for i in range(len(size_l))]
    # po_r = [i + width / 2 for i in range(len(size_l))]
    # print(po_l,po_r)
    # [-0.15, 0.85, 1.85, 2.85] [0.15, 1.15, 2.15, 3.15]

    # plt.bar(po_l, local_delays, width=width, label='local')
    # plt.bar(po_r, V2R_V2V_delays, width=width, label='V2V/V2R')
    plt.plot(local_delays, color='r', linewidth=2, linestyle=':', marker='o', label='本地计算')
    plt.plot(V2R_V2V_delays, color='g', linewidth=2, linestyle=':', marker='o', label='协同计算')

    # 设置刻度
    plt.xticks(range(len(size_l)), size_l)

    # 设置坐标标签
    plt.xlabel('任务下发密度')
    plt.ylabel('计算任务完成平均时延(s)')

    # 设置图例
    plt.legend()

    # 展示
    plt.show()

def plot_size():
    size_l = np.arange(10, 40 + 1, 5)

    local_delays = []
    V2R_V2V_delays = []
    for size in size_l:
        fileNameStr = f'./result/result(size={size}).xlsx'
        xl = pd.read_excel(fileNameStr, usecols=['本地计算处理总时延(s)', '协同节点处理总时延(s)'])
        t1 = xl['本地计算处理总时延(s)']
        t2 = xl['协同节点处理总时延(s)']
        sum_t = 0
        for k in range(len(t2)):
            if pd.isnull(t2[k]):
                sum_t += t1[k]
            else:
                sum_t += t2[k]
        local_delays.append(sum(t1) / len(t1))
        V2R_V2V_delays.append(sum_t / len(t1))

    print(local_delays)
    print(V2R_V2V_delays)
    #
    # for i in range(len(size_l)):
    #     size_l[i] = size_l[i]
    # 绘图（在一个刻度的两边分别绘制两条柱状图）
    # width = 0.2  # 设置一个固定宽度
    # po_l = [i - width / 2 for i in range(len(size_l))]
    # po_r = [i + width / 2 for i in range(len(size_l))]
    # print(po_l,po_r)
    # [-0.15, 0.85, 1.85, 2.85] [0.15, 1.15, 2.15, 3.15]

    # plt.bar(po_l, local_delays, width=width, label='local')
    # plt.bar(po_r, V2R_V2V_delays, width=width, label='V2V/V2R')
    # plt.plot(local_delays, color='r', linewidth=2, linestyle=':', marker='o', label='本地计算')
    plt.plot(V2R_V2V_delays, color='g', linewidth=2, linestyle=':', marker='o', label='协同计算')

    # 设置刻度
    plt.xticks(range(len(size_l)), size_l)

    # 设置坐标标签
    plt.xlabel('车流密度(车/车道)')
    plt.ylabel('计算任务完成平均时延(s)')

    # 设置图例
    plt.legend()

    # 展示
    plt.title('车流密度与平均时延关系图')
    plt.savefig('车流密度与平均时延关系图.png', dpi=dpi)
    plt.show()


if __name__ == '__main__':
    # plot_task_release_speed()
    plot_V2R_B()
    plot_X()
    plot_data_size()
    plot_size()
