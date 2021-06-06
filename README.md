为了保护隐私，停车数据（excel表存储）没有上传

数据格式如下图：

![image](https://user-images.githubusercontent.com/69345371/120926829-05c37880-c711-11eb-97fa-2972875ea8d4.png)


几个文件夹下为画出的各种图
运行get_data.py得到处理后的数据df（dataframe类）
运行其余文件，调用其中的函数，df作为输入参数，画出各种图。（详细方法见报告内）

画图示例：

下图为一个月内开始停车时刻与相应停车时长的散点图，红点为业主车的，蓝点为临时车的

![image](https://user-images.githubusercontent.com/69345371/120926943-9dc16200-c711-11eb-9ac0-53150f91c857.png)

下图为某一天不同时段内在库车数量

![image](https://user-images.githubusercontent.com/69345371/120927113-4e2f6600-c712-11eb-917a-ef3149d93861.png)

下图为一个月内工作日与周末的不同时段内在库车总数最大值

![image](https://user-images.githubusercontent.com/69345371/120927144-6606ea00-c712-11eb-955e-5810fe85714f.png)

下图为不同业主停车时段的甘特图。每一个横条代表一个业主停车记录的在库时间段。起始点为当天入库的时刻，终止点为当次停车的离开时刻（限制停车时长小于24小时）

![image](https://user-images.githubusercontent.com/69345371/120927181-8c2c8a00-c712-11eb-97fe-391cd4d044eb.png)
