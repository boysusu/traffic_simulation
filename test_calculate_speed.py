import numpy

Hz = 1
KHz = Hz * 10**3
MHz = KHz * 10**3
GHz = MHz * 10**3

V2R_channel_bandwidth = 40 * MHz  # V2R通信信道带宽
V2V_channel_bandwidth = 20 * MHz  # V2V通信信道带宽
path_loss_factor = 3  # 路径损耗因子
upload_channel_fading_factor = 4  # 上传链路信道衰落因子
gaussian_noise_power = 3 * 10**-6  # 高斯噪声功率(w) 取值暂不确定
car_communication_transmission_power = 1.6  # 车载设备通信发射功率(w)

d = 50
# 信噪比
xzb = 10*numpy.log10(car_communication_transmission_power/gaussian_noise_power)
print(xzb)

# 上传速率(Mbps)
r = V2R_channel_bandwidth*numpy.log2(1+(car_communication_transmission_power*d**-path_loss_factor*upload_channel_fading_factor**2/gaussian_noise_power))
print(r/10**6)