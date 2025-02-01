# 简易电子琴 - 上位机
>  2025 寒假 山东大学电子设计 STM32校园比赛作品 - 上位机
>
> #### 本程序的主要目标是实现和单片机之间基于串口通信的数字孪生
>
> #### 本文忽略图形化界面的细节，主要关注串口通信内容



## 串口通信数据包格式规定

#### 基本格式：包头 数据长度 指令类型 数据 包尾

#### 包头：0xFF 0xAA

#### 包尾：0x55 0x00

#### 数据长度：包含 指令类型 (1 字节) 和 数据 的字节数，最大长度不得超过 255

#### 指令类型：有两种类型的指令，读指令(有返回数据包) 0x02 和 写指令(无返回数据包) 0x12

#### 数据： (范围内) 任意长度和值，解释取决于程序

#### *返回数据包的格式基本相同，但是没有 指令类型 这一项*



## 指令表

### 读指令（0x02）

- #### 0x00，握手指令，用于确认成功连接设备，返回 0x66

  



### 写指令（0x12）

- #### 0x00 0x00/0x01 [0x00 ~ 0x0F]，模拟按键输入，第一位 0 表示按键按下，1 表示按键抬起，第二位表示按键编号

- #### 0x01 [0x00 ~ 0x05]，设置音量档位，0 ~ 5

