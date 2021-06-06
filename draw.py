def draw(df):
    import pandas as pd
    from matplotlib import pyplot as plt 
    import pylab as pyl #使matplotlib可显示中文
    pyl.mpl.rcParams['font.sans-serif'] = ['SimHei'] #使matplotlib可显示中文
    
    date=df.drop_duplicates('indate').loc[:,['indate','inweek']]#去重
    #类型dataframe 两列存不重复的日期和相应的星期
    date=date.sort_values('indate')#按日期排序
    
    for id in date.index: #画九月每天的不同车开始停车时刻与停车时长散点图
        d=date.loc[id,'indate']
        w=date.loc[id,'inweek']
        fig1=df.loc[(df['indate']==d)&(df['type']=='业主')\
                  &(df['length']<24),:]#忽略停车时长大于一天的
        fig2=df.loc[(df['indate']==d)&(df['type']=='临时')\
                  &(df['length']<24),:]
        title=str(d)[:11]+str(w) #日期星期几
        plt.title(title)
        plt.xlabel("开始停车时刻/点(h)") 
        plt.ylabel("停车时长/h") 
        plt.xticks(range(0,24))#横坐标 0:23 步长1
        plt.yticks(range(0,24))
        plt.grid()
        plt.plot(fig1['intimedig'],fig1['length'],'r.',markersize=3)
        plt.plot(fig2['intimedig'],fig2['length'],'b.',markersize=3)
        plt.savefig('./fig开始停车/'+title+'.jpg',dpi=100)#指定分辨率100
        plt.clf()#清空画布
        #plt.show()
    date=df.drop_duplicates('outdate').loc[:,['outdate','outweek']]#去重
    #因为excel表数据本身是根据离开时刻排的，不需要排序日期
    
    for id in date.index: #画九月每天的不同车离开时刻与停车时长散点图
        d=date.loc[id,'outdate']
        w=date.loc[id,'outweek']
        fig1=df.loc[(df['outdate']==d)&(df['type']=='业主')\
                  &(df['length']<24),:]
        fig2=df.loc[(df['outdate']==d)&(df['type']=='临时')\
                  &(df['length']<24),:]
        title=str(d)[:11]+str(w) #日期星期几
        plt.title(title)
        plt.xlabel("离开时刻/点(h)") 
        plt.ylabel("停车时长/h") 
        plt.xticks(range(0,24))
        plt.yticks(range(0,24))
        plt.grid()
        plt.plot(fig1['outtimedig'],fig1['length'],'r.',markersize=3)
        plt.plot(fig2['outtimedig'],fig2['length'],'b.',markersize=3)
        plt.savefig('./fig离开时刻/'+title+'.jpg',dpi=100)#指定分辨率100
        plt.clf()#清空画布
