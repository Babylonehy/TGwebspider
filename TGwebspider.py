# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
by Lyn from wuhan university
last modified 2017年04月04日17:03:20
三峡水情爬取
"""

import requests
import datetime
import json
import xlwt
import sys
import time


#进度条
def view_bar(num, total):
  rate = num / total
  rate_num = int(rate * 100)
  r = '\r[%s%s]%d%%' % ("="*num, " "*(100-num), rate_num, )
  sys.stdout.write(r)
  sys.stdout.flush()

#生成日期数组
def dateRange(beginDate, endDate):
    dates = []
    dt = datetime.datetime.strptime(beginDate, "%Y-%m-%d")
    date = beginDate[:]
    while date <= endDate:
        dates.append(date)
        dt = dt + datetime.timedelta(1)
        date = dt.strftime("%Y-%m-%d")
    return dates   
    
def get_datafromhtml(posttime):
    flag = True
    global r 
    while flag:
        try:
            params={'time':posttime}
#三峡日单独
            url="http://www.ctg.com.cn/eportal/ui?moduleId=50c13b5c83554779aad47d71c1d1d8d8&&struts.portlet.mode=view&struts.portlet.action=/portlet/waterFront!getDatas.action"
#三峡&葛洲坝日平均
            url2="http://www.ctg.com.cn/eportal/ui?moduleId=4f104da2afbc4bf59babd925d469491b&&struts.portlet.mode=view&struts.portlet.action=/portlet/waterPicFront!getDatas.action"
            headers={
        'Accept':'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Cache-Control':'no-cache',
        'Connection':'keep-alive',
        'Content-Length':'15',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie':'JSESSIONID=77BD9F4DCEBFAE8598A88B64781206DB',
        'Host':'www.ctg.com.cn',
        'Origin':'http://www.ctg.com.cn',
        'Pragma':'no-cache',
        'Referer':'http://www.ctg.com.cn/sxjt/sqqk/index.html',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest'
          }
            
            r = requests.post(url=url2,data=params,headers=headers)
            flag=False
            params.clear()
        except Exception:
            flag = True
            
#--------------------------解析存入execl
book = xlwt.Workbook()
sheet1 = book.add_sheet(u'葛洲坝出入库流量2005-2013')
row0 = [u'日期',u'入库平均',u'出库',u'入库某时刻测',u'上游水位',u'下游水位']
columncount=1
#生成第一行
for i in range(0,len(row0)):
    sheet1.write(0,i,row0[i])
    
for each in dateRange("2011-11-03", "2013-12-31"):
    print (each,)
    get_datafromhtml(each)
   # print (r.content.decode('utf-8'))
    html=r.content.decode('utf-8')
    dic=json.loads(html)
    sheet1.write(columncount,0,each)
    sheet1.write(columncount,1,dic['downList'][2]['avgv'])
    sheet1.write(columncount,2,dic['downList'][3]['avgv'])
    sheet1.write(columncount,3,dic['downList'][2]['v'])
    sheet1.write(columncount,4,dic['downList'][0]['avgv'])
    sheet1.write(columncount,5,dic['downList'][1]['avgv'])
    #print ("入库："+dic['downList'][2]['avgv'])
    #print ("出库："+dic['downList'][3]['avgv'])
    columncount=columncount+1
    book.save('葛洲坝出入库流量数据.xls') #保存文件
print ("done")