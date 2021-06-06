def Gantt(df):#每天的业主车辆在库时间段
    import pandas as pd
    import matplotlib.pyplot as plt  
    import pylab as pyl #使matplotlib可显示中文
    pyl.mpl.rcParams['font.sans-serif'] = ['SimHei'] #使matplotlib可显示中文
    
    date=df.drop_duplicates('indate').loc[:,['indate','inweek']]#去重
    #类型dataframe 两列存不重复的日期和相应的星期
    date=date.sort_values('indate')#按日期排序
    for id in date.index: #画九月每天的业主车辆在库时间段 甘特图
        d=date.loc[id,'indate']
        w=date.loc[id,'inweek']
        fig=df.loc[(df['indate']==d)&(df['type']=='业主')\
                 &(df['length']<24),['length','intimedig']]#忽略停车时长大于一天的
        #选取相应日期 type为业主的行，保留'length','intimedig'两列 构成datafram:fig
        fig=fig.sort_values('intimedig',ascending=False)#按开始停车时间降序排序
        idlist=range(fig.shape[0])#fig行数个id
        title=str(d)[:11]+str(w) #日期星期几
        plt.title(title)
        plt.xlabel("时刻/点(h)") 
        plt.ylabel("业主不同车") 
        plt.grid()
        plt.xticks(range(0,41),list(range(0,24))+list(range(0,17)))
                   #locs labels
        plt.barh(y=idlist,width=fig['length'].values,left=fig['intimedig'].values)
        plt.savefig('./fig甘特图(停车时长小于24h)/'+title+'.jpg',dpi=100)#指定分辨率100
        plt.clf()#清空画布