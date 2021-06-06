def process(s):#输入Series owner_sum 不同时间段业主的在库车数量 本文件与时间段长度相关的为allbar中name
    import pandas as pd
    dfn=pd.DataFrame({'num':s.values,'datetime':s.index})
    dfn['week']=list(map(datetime2week,dfn['datetime']))#星期类型 weekday/weekend
    dfn['time']=[i.time() for i in dfn['datetime']] #每个元素Timestamp类的 time方法返回时间 object类
    maxnum=dfn.groupby([dfn['week'],dfn['time']])['num'].max()
    #Series类 双索引'week','time' 值'num'为相同索引下在库数量最大值
    #print(maxnum['weekday'].values)
    meannum=dfn.groupby([dfn['week'],dfn['time']])['num'].mean()
    allbar('max','weekday',maxnum)
    allbar('max','weekend',maxnum)
    allbar('mean','weekday',meannum)
    allbar('mean','weekend',meannum)
    
    #return dfn

    
def datetime2week(t):#输入Timestamp 2018-09-01 00:10:00 输出weekday/weekend
    import pandas as pd
    date=t.date()#Timestamp date方法返回日期
    interval=(date-pd.to_datetime('2018-09-02').date()).days#2018-09-02为星期日 与其的天数差 
    #.days为Timedelta的属性 天数 int型
    r=interval%7#余数0-6 余数0则为星期日 1为星期一
    dic=[7,1,2,3,4,5,6]
    week=dic[r]
    if week in [6,7]:
        return 'weekend'
    else:
        return 'weekday'
    
def allbar(s1,s2,S):#画统计好的不同时间段业主在库车数量 柱状图
    #s1=mean/max s2=weekday/weekend 分组好处理过的Series S 如maxnum
    #S第一个索引week 第二个索引time
    import matplotlib.pyplot as plt  
    import pylab as pyl #使matplotlib可显示中文
    pyl.mpl.rcParams['font.sans-serif'] = ['SimHei'] #使matplotlib可显示中文
    name=range(24)
    num=S[s2].values #S[s2,:]报错TypeError: ('weekday', slice(0, None, None))
    plt.bar(range(len(num)), num,tick_label=name)  
    title=s2+' '+s1
    plt.title(title)
    plt.xlabel("时刻/点(h)") 
    plt.ylabel('业主在库车数量')
    plt.grid()
    plt.yticks(range(0,560,20))
    plt.savefig('./fig在库车数量统计结果/'+title+'.jpg',dpi=100)#指定分辨率100
    plt.clf()#清空画布