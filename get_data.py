import pandas as pd
def time2dig(t):#输入时间格式'2018-09-18 23:06:51' 输出23.117,单位小时
    t=t[11:]#舍去日期
    hour=int(t[0:2])#首下标含，尾下标不含
    Min=int(t[3:5])
    sec=int(t[6:])
    if sec>=30:
        Min+=1 #超过30秒分钟加1 精确到分钟
    return hour+Min/60
import re
def len2dig(t):#输入'0天2小时19分51秒',输出2.33 单位小时
    t = re.split('[天 小时 分 秒]',t.strip())#多分隔符
    t = [int(i) for i in t if i != '']#去除列表中空值 字符串转化为整数
    day,hour,Min,sec=t
    if sec>=30:
        Min+=1 #超过30秒分钟加1 精确到分钟
    return day*24+hour+Min/60
def num2week(n):#输入n为与星期日间隔的天数 输出星期几
    r=n%7#余数0-6 余数0则为星期日 1为星期一
    dic=['星期日','星期一','星期二','星期三','星期四','星期五','星期六']
    return dic[r]

import os
def get_data():
    fnames = os.listdir('./data/')#./相对目录 返回data文件夹下所有文件名称
    dfall=pd.DataFrame()#创建一个空的dataframe
    for fname in fnames:
        df=pd.read_excel('./data/'+fname,skiprows=3)#跳过前三行，从第四行开始读取
        delid=[0,1,3,4,5,6,7,9,18,19,20]+list(range(11,17))+list(range(22,29))#要删除的列标
        df.drop(df.columns[delid], axis=1, inplace=True)#axis=1,删除指定列 inplace修改原来df
        df.dropna(inplace=True)#去掉空数据，删除一整行
        df.rename(columns={'车牌号码':'num','服务套餐':'type','入场时间':'intime',\
               '出场时间':'outtime','停车时长':'length'}, inplace = True)#替换列名称
        df['type']=df['type'].replace(['纯车牌月卡A','临时车纯车牌识别(小车)'],['业主','临时'])
        df['indatetime']=pd.to_datetime(df['intime'])#开始停车的日期加时刻 转化为datetime64类型
        df['outdatetime']=pd.to_datetime(df['outtime'])#离开的日期加时刻 转化为datetime64类型
        
        delid=df.loc[df['indatetime']<pd.to_datetime('2018-09-01'),:].index
        df=df.drop(delid)#9.1以前开始停车的日期数据删除 删除一整行 相应的indate也删掉了
        #outdatetime 不用删，因为excel表数据本身是根据离开时刻排的
        df['indate']=list(map(lambda s:s[0:10],df['intime']))#lambda创建匿名函数，取前十个字符
        df['indate']=pd.to_datetime(df['indate'])#转化为datetime64类型，方便处理
        df['intimedig']=list(map(time2dig,df['intime']))#数字化的连续时间float64类
        df['intime']=list(map(lambda s:s[11:],df['intime']))#取第11个字符及以后，为一天内停车时刻
        df['intime']=pd.to_datetime(df['intime'])#转化为datetime64类型
        
        df['outdate']=list(map(lambda s:s[0:10],df['outtime']))
        df['outdate']=pd.to_datetime(df['outdate'])
        df['outtimedig']=list(map(time2dig,df['outtime']))
        df['outtime']=list(map(lambda s:s[11:],df['outtime']))#取第11个字符及以后，为一天内停车时刻
        df['outtime']=pd.to_datetime(df['outtime'])#转化为datetime64类型
        
        df['length']=list(map(len2dig,df['length']))      
        
        dfall=pd.concat([dfall,df],ignore_index=True)#竖向拼接 重新分配索引
    
    interval=dfall['indate']-pd.to_datetime('2018-09-02')#2018-09-02为星期日
    #与星期日的日期间隔 Series类 每个元素Timedelta类
    interval=[i.days for i in interval]#.days为Timedelta的属性 天数
    #每个元素（日期间隔）转化为整数,构成列表
    dfall['inweek']=pd.Series([num2week(i) for i in interval])
    #转化为星期 构建Series类型数据 创建为df新的一列week 后来发现不需要转换为Series 列表就可以
    #outweek同理
    interval=dfall['outdate']-pd.to_datetime('2018-09-02')
    interval=[i.days for i in interval]
    dfall['outweek']=pd.Series([num2week(i) for i in interval])
    #print(dfall.head(10))
    return dfall

df=get_data()

