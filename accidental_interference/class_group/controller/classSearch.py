'''
查询工作辊全生命周期

'''
'''
数据存放在数据库里面 数据不完整
根据甲乙丙丁四个班组 返回sum/len
分离时间，对数据进行统计归类 
绘图
'''
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['FangSong']  # 设置matplotlib可以显示汉语
mpl.rcParams['axes.unicode_minus'] = False
import pymysql
import pymysql.cursors

pymysql.install_as_MySQLdb()


# mysql连接
def connect(my_reg):
    try:
        connect = pymysql.Connect(
            host=str(my_reg[0]),
            port=int(my_reg[1]),
            user=str(my_reg[2]),
            passwd=str(my_reg[3]),
            db=str(my_reg[4]),
            charset=str(my_reg[5])
        )
        cursor = connect.cursor()  # 获取一个cursor对象 执行数据库相关操作，cursor.execute()执行,接收返回值
        flag = 2
        return cursor, flag
    except:
        n = 0
        flag = 1
        return n, flag


def inquiryClass(shijian_shang, shijian_xia, my_reg):
    # 连接数据库
    cursor = connect(my_reg)[0]

    # shijian_shang = '2019-8-01 00:00:00'
    # shijian_xia = '2019-10-01 00:00:00'
    # select_banci = "SELECT * FROM all_wr_csv WHERE 下机班次 = '%s'  ORDER BY 下机时间;"%(banci)
    # select_shijian = "SELECT * FROM all_wr_csv WHERE  下机班次 = '%s' And ('%s' < 下机时间  AND 下机时间 <= '%s') And ('%s' <= 上机时间 AND 上机时间 < '%s') ORDER BY 下机时间;"%(banci,shijian_shang,shijian_xia,shijian_shang,shijian_xia)
    # select_banci_shijian = "SELECT * FROM all_wr_csv WHERE 下机班次 = '%s' And ('%s' < 下机时间  AND 下机时间 <= '%s') And ('%s' <= 上机时间 AND 上机时间 < '%s') ORDER BY 下机时间;"%(banci,shijian_shang,shijian_xia,shijian_shang,shijian_xia)
    # select_xianglingun = "SELECT * FROM all_wr_csv WHERE 下机班次 = '%s' And ('%s' < 下机时间  AND 下机时间 <= '%s') And ('%s' <= 上机时间 AND 上机时间 < '%s') ORDER BY 下机时间;"%(banci,shijian_shang,shijian_xia,shijian_shang,shijian_xia)
    # print(select)
    # cursor.execute(select_banci_shijian)

    everyclassIUlist = []

    # 返回len/sum
    def everyclassIU(select_shijian):
        cursor.execute(select_shijian)
        results = cursor.fetchall()  # 返回多个元组，返回多个行记录 二维元组
        # print(results,len(results))
        # for i in results:
        #     print(i)

        all = {}  # 字典 轧辊对应IU
        fenjuanming = []
        zhijing = []  # 直径
        weight = []  # 轧制重量
        hight = []  # 轧制长度
        quanjuanhao = []
        for i in results:
            # print(i)
            zhijing.append(round(float(i[2]), 4))  # round返回 浮点数四舍五入值 4 代表保存四位小数
            weight.append(round(float(i[-2]), 4))
            if i[-1] != None:
                hight.append(round(float(i[-1]), 4))
            else:
                hight.append(0.0)
            # 命名方式 辊号+直径+机架+_+下机原因+_csv
            name = i[1].lower() + '_' + str(i[2]).replace('.', '_') + '_' + str(i[4]) + '机架' + '_' + i[9] + '_csv'
            quanjuanhao.append(name[:15])
            # print(name[:15])
            # 在数据库中查询表名
            select2 = 'SELECT Table_name FROM information_schema.tables where TABLE_NAME = \'%s\';' % (name)
            cursor.execute(select2)
            # 数组数据
            results2 = cursor.fetchall()
            # print('*********************')
            # # print(results2)
            # print('*********************')
            if list(results2) != []:
                fenjuanming.append(list(results2)[0][0])
        # print(zhijing)
        # print(fenjuanming)
        # print(quanjuanhao)

        iu = []
        zhagun = []
        sum = 0
        len = 0  # 分卷名中存在生产数据
        # 根据分卷名 统计IU 轧辊信息 sum len
        for j in fenjuanming:
            inf = []
            iu_sum = 0
            # select3 = 'SELECT 均值 FROM workroll.%s;'%(j)

            # select3 = "SELECT 均值, 开始生产时刻, 结束生产时刻 FROM workroll.%s;"%(j)
            # 对分卷名的数据所有生产数据 avg取均值
            select3 = 'SELECT avg(均值) FROM workroll.%s;' % (j)
            # select3 = 'SELECT avg(均值), 开始生产时刻, 结束生产时刻 FROM workroll.%s;'%(j)
            cursor.execute(select3)
            results3 = cursor.fetchall()
            #
            # print('j:',j)
            flag = True
            for k in results3:
                # iu_sum += k[0]
                # all.append(list(k))
                inf.append(list(k)[0])
                # avg = sum(inf)/len(inf)
                if k[0] != None:
                    len += 1
                    sum += k[0]
                    # print(k)
                    iu.append(k[0])
                else:
                    flag = False
            if flag:
                all[j] = k[0]
                zhagun.append(j[0:15].upper())
        # print(sum/len)
        # print(len)
        # print(iu)
        # print(zhagun)
        if len == 0:
            return 0
        else:
            return sum / len  # 方法 返回平均值，每个班组的IU均值信息

    for i in ['甲', '乙', '丙', '丁']:  # 分别对甲乙丙丁四个班组信息进行查询
        # select后面表示筛选的内容，from后面表示筛选内容来自的位置，where后面表示筛选的条件。 order by 按顺序排列
        select_shijian = "SELECT * FROM all_wr_csv WHERE  下机班次 = '%s' And ('%s' < 下机时间  AND 下机时间 <= '%s') And ('%s' <= 上机时间 AND 上机时间 < '%s') ORDER BY 下机时间;" % (
            i, shijian_shang, shijian_xia, shijian_shang, shijian_xia)  # Mysql语句
        everyclassIUlist.append(everyclassIU(select_shijian))
        print('everyclassIUlist', everyclassIUlist)
    # 分别存储甲乙丙丁四个班组的数据
    jiaClassIUList = []
    jiaClassIUListZhaGun = []
    jiaClassIUListIU = []

    yiClassIUList = []
    yiClassIUListZhaGun = []
    yiClassIUListIU = []

    bingClassIUList = []
    bingClassIUListZhaGun = []
    bingClassIUListIU = []

    dingClassIUList = []
    dingClassIUListZhaGun = []
    dingClassIUListIU = []

    # 获取甲乙丙丁组的 classIU roller iu值
    def eachclassIU(select_shijian):
        cursor.execute(select_shijian)
        results = cursor.fetchall()
        # for i in results:
        #     print(i)

        all = {}
        fenjuanming = []
        zhijing = []
        weight = []
        hight = []
        quanjuanhao = []
        for i in results:
            # print(i)
            zhijing.append(round(float(i[2]), 4))
            weight.append(round(float(i[-2]), 4))
            if i[-1] != None:
                hight.append(round(float(i[-1]), 4))
            else:
                hight.append(0.0)
            name = i[1].lower() + '_' + str(i[2]).replace('.', '_') + '_' + str(i[4]) + '机架' + '_' + i[9] + '_csv'
            quanjuanhao.append(name[:15])
            # print(name[:15])
            select2 = 'SELECT Table_name FROM information_schema.tables where TABLE_NAME = \'%s\';' % (name)
            cursor.execute(select2)
            results2 = cursor.fetchall()
            # print('*********************')
            # # print(results2)
            # print('*********************')
            if list(results2) != []:
                fenjuanming.append(list(results2)[0][0])
        # print(zhijing)
        # print(fenjuanming)
        # print(quanjuanhao)

        iu = []
        zhagun = []
        sum = 0
        len = 0
        for j in fenjuanming:
            inf = []
            iu_sum = 0
            # select3 = 'SELECT 均值 FROM workroll.%s;'%(j)
            # select3 = "SELECT 均值, 开始生产时刻, 结束生产时刻 FROM workroll.%s;"%(j)
            select3 = 'SELECT avg(均值) FROM workroll.%s;' % (j)
            # select3 = 'SELECT avg(均值), 开始生产时刻, 结束生产时刻 FROM workroll.%s;'%(j)
            cursor.execute(select3)
            results3 = cursor.fetchall()
            #
            # print('j:',j)
            flag = True
            for k in results3:
                # iu_sum += k[0]
                # all.append(list(k))
                inf.append(list(k)[0])
                # avg = sum(inf)/len(inf)
                if k[0] != None:
                    len += 1
                    sum += k[0]
                    # print(k)
                    iu.append(k[0])
                else:
                    flag = False
            if flag:
                all[j] = k[0]
                zhagun.append(j[0:15].upper())
        import pandas as pd

        if len == 0:
            return 0, 0, 0
        else:
            # print(sum/len)
            # print(len)
            # print(iu)
            # print(zhagun)
            return sum / len, zhagun, iu
        # 分割时间

    def splittime(shijian_shang, shijian_xia):
        start = shijian_shang.split(' ')[0][:-3]  # 2019-7
        end = shijian_xia.split(' ')[0][:-3]
        timelist = []
        # print(int(shijian_xia.split('-')[0])-int(shijian_shang.split('-')[0])+int(shijian_xia.split('-')[1])-int(shijian_shang.split('-')[1]))
        for i in range(0, (int(shijian_xia.split('-')[0]) - int(shijian_shang.split('-')[0])) * 12 + int(
                shijian_xia.split('-')[1]) - int(shijian_shang.split('-')[1]) + 2):  # 时间间隔一共多少个月
            day = i + int(shijian_shang.split('-')[1]) - 1
            time = day // 12
            timelist.append(str(int(shijian_shang.split('-')[0]) + time) + '-' + str(day - 12 * time + 1))
            # print(str(int(shijian_shang.split('-')[0])+time)+'-'+str(day-12*time+1))
        finaltimelist = []
        for i in range(1, len(timelist)):
            finaltimelist.append([timelist[i - 1], timelist[i]])
            # finaltimelist.append(timelist[i])
        return finaltimelist

    timelist = splittime(shijian_shang, shijian_xia)
    for i in timelist:
        shijian_shang = i[0] + '-01 00:00:00'
        shijian_xia = i[1] + '-01 00:00:00'
        print(shijian_shang, shijian_xia)

        select_shijian = "SELECT * FROM all_wr_csv WHERE  下机班次 = '%s' And ('%s' < 下机时间  AND 下机时间 <= '%s') And ('%s' <= 上机时间 AND 上机时间 < '%s') ORDER BY 下机时间;" % (
            '甲', shijian_shang, shijian_xia, shijian_shang, shijian_xia)
        a1, b1, c1 = eachclassIU(select_shijian)
        jiaClassIUList.append(a1)
        jiaClassIUListZhaGun.append(b1)
        jiaClassIUListIU.append(c1)

        select_shijian = "SELECT * FROM all_wr_csv WHERE  下机班次 = '%s' And ('%s' < 下机时间  AND 下机时间 <= '%s') And ('%s' <= 上机时间 AND 上机时间 < '%s') ORDER BY 下机时间;" % (
            '乙', shijian_shang, shijian_xia, shijian_shang, shijian_xia)

        a2, b2, c2 = eachclassIU(select_shijian)
        yiClassIUList.append(a2)
        yiClassIUListZhaGun.append(b2)
        yiClassIUListIU.append(c2)

        select_shijian = "SELECT * FROM all_wr_csv WHERE  下机班次 = '%s' And ('%s' < 下机时间  AND 下机时间 <= '%s') And ('%s' <= 上机时间 AND 上机时间 < '%s') ORDER BY 下机时间;" % (
            '丙', shijian_shang, shijian_xia, shijian_shang, shijian_xia)

        a3, b3, c3 = eachclassIU(select_shijian)
        bingClassIUList.append(a3)
        bingClassIUListZhaGun.append(b3)
        bingClassIUListIU.append(c3)

        select_shijian = "SELECT * FROM all_wr_csv WHERE  下机班次 = '%s' And ('%s' < 下机时间  AND 下机时间 <= '%s') And ('%s' <= 上机时间 AND 上机时间 < '%s') ORDER BY 下机时间;" % (
            '丁', shijian_shang, shijian_xia, shijian_shang, shijian_xia)

        a4, b4, c4 = eachclassIU(select_shijian)
        dingClassIUList.append(a4)
        dingClassIUListZhaGun.append(b4)
        dingClassIUListIU.append(c4)

    print('jiaClassIUListZhaGun', jiaClassIUListZhaGun)
    print('jiaClassIUListIU', jiaClassIUListIU)
    return everyclassIUlist, jiaClassIUList, yiClassIUList, bingClassIUList, dingClassIUList, timelist, jiaClassIUListZhaGun, jiaClassIUListIU, yiClassIUListZhaGun, yiClassIUListIU, bingClassIUListZhaGun, bingClassIUListIU, dingClassIUListZhaGun, dingClassIUListIU

    # return everyclassIUlist,jiaClassIUList,yiClassIUList,bingClassIUList,dingClassIUList,timelist,jiaClassIUListZhaGun,jiaClassIUListIU,yiClassIUListZhaGun,yiClassIUListIU,bingClassIUListZhaGun,bingClassIUListIU,dingClassIUListZhaGun,dingClassIUListIU


shijian_shang = '2019-8-01 00:00:00'
shijian_xia = '2019-12-01 00:00:00'
# inquiryClass(shijian_shang, shijian_xia)

# print(list(all.keys())[0])
# name = str(list(all.keys())[0])
# for i in all.values():
# print(i)

# print(pd.DataFrame(all[list(all.keys())[0]]))
# x = pd.DataFrame(all[list(all.keys())[0]]).values[:,1]
# y = pd.DataFrame(all[list(all.keys())[0]]).values[:,0]
import matplotlib.pyplot as plt
# plt.bar(x,y,0.001)
# # plt.plot(x,y,'-*')
# plt.title("%s"%(name))

# plt.show()

# plt.figure(figsize=(15*2, 12*2))
# plt.subplots_adjust(left=0.074, right=0.929, top=0.88, bottom=0.22)
# x = np.arange(1,15)
# x = np.arange(1,weight.__len__()+1)
# y = zhijing
# plt.title('%s轧辊全生命周期轧辊直径变化图'%gunhao, fontsize=15)
# plt.step(x,y,where="post")
# plt.xticks(rotation=300, fontsize=12)
# plt.yticks(fontsize=12)
# plt.xlabel('轧辊号——直径',fontsize=14)
# plt.xticks(x,quanjuanhao)
# plt.ylim([540,562])
# for a, b in zip(x, y):
#     plt.text(a, b+0.5, b, ha='center', va='bottom', fontsize=10)
#
#
# x = np.arange(1,15)
# x = np.arange(1,weight.__len__()+1)
# plt.figure(figsize=(15, 12))
# plt.subplots_adjust(left=0.074, right=0.929, top=0.88, bottom=0.188)
# plt.xticks(rotation=300)
# plt.xticks(x+0.3,quanjuanhao)
# axes1 = plt.subplot(111)
# axes1.bar(x,hight,width=0.4,color = 'orange')
# axes2 = axes1.twinx()
# axes2.bar(x+0.4,weight,width=0.4)
# axes1.legend(("轧制里程",),loc='upper left')
# axes2.legend(("轧制重量",),loc='upper right')
# plt.title('%s轧辊全生命周期轧制长度重量图'%gunhao,fontsize=15)
# axes1.set_ylabel('轧制长度(m)',fontsize=14)
# axes2.set_ylabel('轧制重量(t)',fontsize=14)
# axes1.set_xlabel('轧辊号——直径',fontsize=14)
# # plt.show()

# '甲','乙','丙','丁'四个班组的IU均值统计绘图
# 1.7196507506714174 1.7739367663941867  1.7073045197553938  1.7169737270347527
# x = ['甲','乙','丙','丁']
# y = [1.7196507506714174, 1.7739367663941867 , 1.7073045197553938 , 1.7169737270347527]
# plt.bar(x,y,0.5)
# plt.title('不同班组IU均值统计',fontsize=15)
# plt.ylim([1.7,1.8])
# plt.ylabel('IU均值',fontsize=15)
# plt.xlabel('class_group',fontsize=15)
# for a, b in zip(x, y):
#     plt.text(a, b+0.004, round(b,3), ha='center', va='bottom', fontsize=12)
# plt.show()

# 乙班组'7月','8月','9月','10月'月份IU均值统计
# # 1.6419673308386433 1.771724181652735 1.905561256631907 1.7930501510241303
# x = ['7月','8月','9月','10月']
# y = [1.6419673308386433, 1.771724181652735, 1.905561256631907, 1.7930501510241303]
# plt.bar(x,y,0.5)
# plt.title('乙班组各月份IU均值统计',fontsize=15)
# plt.ylim([1.6,1.95])
# plt.ylabel('IU均值',fontsize=15)
# plt.xlabel('月份',fontsize=15)
# for a, b in zip(x, y):
#     plt.text(a, b+0.004, round(b,3), ha='center', va='bottom', fontsize=12)
# plt.show()


# 1.6419673308386433 1.771724181652735 1.905561256631907 1.7930501510241303
# x = zhagun
# y = iu
# print(zhagun.__len__())
# print(iu.__len__())
# plt.subplots_adjust(left=0.107, right=0.980, top=0.915, bottom=0.3, hspace=0.470)
# plt.bar(x,y,0.5)
# plt.title('乙班组10月份IU均值统计',fontsize=15)
# plt.ylim([1,2.9])
# plt.ylabel('IU均值',fontsize=15)
# plt.xlabel('轧辊号_直径',fontsize=15)
# plt.xticks(rotation=270)
# for a, b in zip(x, y):
#     plt.text(a, b+0.004, round(b,3), ha='center', va='bottom', fontsize=10)
#     # plt.text(a, b+0.004, ha='center', va='bottom', fontsize=12)
#
# plt.show()
