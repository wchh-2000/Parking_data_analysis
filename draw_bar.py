def get_cum(df):
    import pandas as pd
    #下面将indatetime outdatetime 按一定采样间隔离散化(分隔成许多时间段，每个时间段给一个时刻标签)
    f='H'#采样间隔 小时 与f有关的为draw_bar中name_list Onum_list Tnum_list
    timediv=pd.date_range(start='2018-09-01',end='2018-10-01',freq=f)
    #timedivide不同分隔时刻 为DatetimeIndex类型 每个元素datetime64[ns]类
    labelnum=timediv.to_series().size-1
    #n个值，切成n-1段，共n-1个标签 eg:[0,1,2] 切分成[0,1),[1,2)
    timelabel=pd.date_range(start='2018-09-01',periods=labelnum,freq=f)
    #periods表示生成labelnum个时刻标签 每个标签为时间段的左端点值
    df['in_dtime']=pd.cut(x=df['indatetime'],bins=timediv,right=False,labels=timelabel)
    #discrete time 离散时间 right=False 区间左闭右开  'in_dtime'列下的数据类型category
    df['out_dtime']=pd.cut(x=df['outdatetime'],bins=timediv,right=False,labels=timelabel)
    #print(df.loc[795:810,['indatetime','in_dtime']])#检验
    
    #下面将分隔后的数据按照时刻标签in_dtime和停车类别type分组
    ingroup=df.groupby([df['in_dtime'],df['type']])#type:DataFrameGroupBy
    in_num=ingroup.count().fillna(0)['num'] #每类计数，空值置0，取任意一列  Series类 
    print(in_num)
    #双重索引：in_dtime type  一列值：数量
    inOwner_num=in_num[:,'业主']#双重索引 业主的不同时间段的停入车数量 
    print(inOwner_num)
    #inOwner_num单索引：不同时间段的时刻标签in_dtime 一列值：数量
    inTemp_num=in_num[:,'临时']#临停车的不同时间段的停入车数量
    #下面out 与 in同理
    outgroup=df.groupby([df['out_dtime'],df['type']])
    out_num=outgroup.count().fillna(0)['num'] #每类计数，空值置0，取任意一列 Series类
    outOwner_num=out_num[:,'业主']#业主的不同时间段的出场车数量 
    outTemp_num=out_num[:,'临时']#临停车的不同时间段的出场车数量 
    
    owner_sum=(inOwner_num-outOwner_num).cumsum()#累加 不同时间段业主的在库车数量
    owner_sum.index=owner_sum.index.rename('ownertime')#索引名由in_dtime 改为ownertime
    owner_sum.index=pd.to_datetime(owner_sum.index)#索引类型从category(由cut产生)转为datetime64[ns]
    #总的索引CategoricalIndex转为DatetimeIndex  便于以后用日期切片索引
    #下面temp_sum同理
    temp_sum=(inTemp_num-outTemp_num).cumsum()#累加 不同时间段临停车的在库车数量
    temp_sum.index=temp_sum.index.rename('temptime')#索引名由in_dtime 改为ownertime
    temp_sum.index=pd.to_datetime(temp_sum.index)
    
    return owner_sum, temp_sum
    
def draw_bar(owner_sum, temp_sum):#画九月每天的不同时间段在库车数量 柱状图
    #横坐标时刻为时间段左端点
    import pandas as pd
    import matplotlib.pyplot as plt  
    import pylab as pyl #使matplotlib可显示中文
    pyl.mpl.rcParams['font.sans-serif'] = ['SimHei'] #使matplotlib可显示中文
    
    date=df.drop_duplicates('indate').loc[:,['indate','inweek']]#去重
    #类型dataframe 两列存不重复的日期和相应的星期
    date=date.sort_values('indate')#按日期排序
    for id in date.index: #画九月每天的不同时间段在库车数量 每个循环画一天
        d=date.loc[id,'indate']#日期 与in无关 9.1-9.30
        w=date.loc[id,'inweek']#星期
        name_list=range(24)
        Onum_list=owner_sum[d:d+pd.Timedelta(hours=23)].values#业主在库车辆数列表
        #d datetime64[ns]类 可加Timedelta类 加23小时   ：构成切片索引 ：前后都含  Series.values返回列表
        plt.bar(range(len(Onum_list)), Onum_list,label='业主',fc='b')  
        Tnum_list=temp_sum[d:d+pd.Timedelta(hours=23)].values#临停车在库车辆数列表
        plt.bar(range(len(Tnum_list)), Tnum_list,bottom=Onum_list,label='临时',tick_label=name_list,fc='r') 
        plt.legend()  
        title=str(d)[:11]+str(w) #日期星期几
        plt.title(title)
        plt.xlabel("时刻/点(h)") #横坐标时刻为时间段左端点
        plt.ylabel('在库车数量')
        plt.savefig('./fig在库车数量/'+title+'.jpg',dpi=100)#指定分辨率100
        plt.clf()#清空画布
        #plt.show() 