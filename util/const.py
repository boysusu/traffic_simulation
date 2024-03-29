'''
@File   :   const.py
@Author :   boysusu
@Desc   :   定义常量
'''

bit = 1
Kbit = bit * 10**3
Mbit = Kbit * 10 **3

bps = 1
Kbps = bps * 10**3
Mbps = Kbps * 10 **3

Hz = 1
KHz = Hz * 10**3
MHz = KHz * 10**3
GHz = MHz * 10**3

V2R_channel_bandwidth = 40 * MHz  # V2R通信信道带宽
V2V_channel_bandwidth = 2 * MHz  # V2V通信信道带宽
path_loss_factor = 3  # 路径损耗因子
upload_channel_fading_factor = 4  # 上传链路信道衰落因子
gaussian_noise_power = 3 * 10**-8  # 高斯噪声功率(w)
car_communication_transmission_power = 1.3  # 车载设备通信发射功率(w)
