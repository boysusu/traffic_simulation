# traffic_simulation

## 橘子洲大桥
橘子洲大桥西起枫林一路，横跨湘江水道及橘子洲，东至芙蓉中路；线路全长1532米，主桥长1156米；桥面为双向四车道城市快速路，设计速度60千米/小时；

主桥宽20米，其中车车行道宽14米，两侧人行道各宽3米；

## 建模
![image.png](https://s2.loli.net/2022/04/06/lL8D6svFdM52OcY.png)

取主桥1000米路段建模
车道宽3.5米，人行道宽3米

### 局部
![image.png](https://s2.loli.net/2022/04/06/FM9fIlcRhVasGAi.png)

### 全局
![image.png](https://s2.loli.net/2022/04/06/w1pNTxF2HdUAELe.png)


## 参数
### road
长度为1000米，车道宽度为3.5m，人行道宽度为3m
### car
1. 车为红色代表有计算任务
2. 车为绿色代表正在协助计算
3. 两车之间的连线代表任务卸载
```python
self.l = 3.8  # 车身长度
self.h = 2  # 车身宽度
self.s0 = 2  # 期望车距
self.T = 0.1  # 驾驶员反应时间
self.v_max = 60.0  # 正常行驶最大车速
self.a_max = 5.0  # 最大加速度
self.b_max = 5.0  # 非紧急制动下的最大减速度
self.max_num_of_channels = 3  # 信道数量
```
### rsu
```python
self.r = 200  # 通信覆盖半径
self.cpu = 5 * GHz  # 边缘服务器计算能力
self.max_num_of_channels = 20  # 信道数量
```

### others
```python
Hz = 1
KHz = Hz * 10**3
MHz = KHz * 10**3
GHz = MHz * 10**3

V2R_channel_bandwidth = 40 * MHz  # V2R通信信道带宽
V2V_channel_bandwidth = 20 * MHz  # V2V通信信道带宽
path_loss_factor = 3  # 路径损耗因子
upload_channel_fading_factor = 4  # 上传链路信道衰落因子
gaussian_noise_power = 3 * 10**-13  # 高斯噪声功率(w)
car_communication_transmission_power = 1.6  # 车载设备通信发射功率(w)

```
## DONE
1. 橘子洲大桥双向四车道两人行道建模 
2. 使用柏松分布在四个车道初始化汽车
3. 完成汽车跟车行驶模型
4. 部署路侧单元
5. 计算车与车、车与RSU的距离
6. 计算车与车、车与RSU的数据传输上行速率
7. 汽车变道
8. 汽车超车
9. rsu及协同车辆选择
10. 多次模拟生成结果数据
11. 数据绘图

## RUN
```bash
pip install -r requirements.txt
python3 main.py
```

