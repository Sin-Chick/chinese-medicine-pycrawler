from bs4 import BeautifulSoup
import os
import sys
import pandas as pd
from tqdm import tqdm
class herb_info:
    zhon_yao = '无'
    chu_fang = '无'
    zheng_zhuang = '无'
    ji_bing = '无'
    wen_xian = '无'
    yi_sheng = '无'
    gui_jing = '无'
    yao_xing = '无'
    bu_wei = '无'
def analyser():
    path = 'output'
    if(not os.path.exists(path)):
        print('no output')
        return
    zhongyaocai_xls = []#用于最后输出
    index = list(os.walk(path))#获得所有目录信息，同时将生成器对象转换为列表
    for filepath,_,filename in tqdm(index, desc='analysing...'):
        if(filename == []):#跳过中间结点
            continue
        type=os.path.split(filepath)
        while(True):#获得类型，尽量使用os库以避免不同操作系统产生的路径读取问题
            if(type[0]==path):
                type=type[1]
                break
            else:
                type=os.path.split(type[0])
        if(type == '中药材'):
            name=os.path.split(filepath)[1]#获得实体名
            file = open(os.path.join(filepath,filename[0]),'rb')
            html = file.read().decode('utf-8')
            be = BeautifulSoup(html,'lxml')
            main = be.find(attrs={'id':'content'})
            sec = main.find_all(attrs={'class':'section'})
            for each in sec:
                info = herb_info()
                info.zhon_yao=name
                ji_bing = each.find(attrs={'class':'item functional_indications'})
                if(not ji_bing == None):
                    info.ji_bing = ji_bing.find(attrs={'class':'item-content'}).text.replace('\n','')
                wen_xian = each.find(attrs={'class':'item excerpt'})
                if(not wen_xian == None):
                    info.wen_xian = wen_xian.find(attrs={'class':'item-content'}).text.replace('\n','')
                gui_jing = each.find(attrs={'class':'item attribution'})
                if(not gui_jing == None):
                    info.gui_jing = gui_jing.find(attrs={'class':'item-content'}).text.replace('\n','')
                yao_xing = each.find(attrs={'class':'item properties_flavor'})
                if(not yao_xing == None):
                    info.yao_xing = yao_xing.find(attrs={'class':'item-content'}).text.replace('\n','')
                zhongyaocai_xls.append(
                    {'中药':info.zhon_yao,
                     '处方':info.chu_fang,
                     '症状':info.zheng_zhuang,
                     '疾病':info.ji_bing,
                     '文献':info.wen_xian,
                     '医生':info.yi_sheng,
                     '归经':info.gui_jing,
                     '药性':info.yao_xing,
                     '部位':info.bu_wei
                     })
        elif(type == '中药方剂'):
            pass
        elif(type == '中医古籍'):
            pass
        elif(type == '中医书籍'):
            pass
    savepath = os.path.dirname(sys.argv[0])+'/anlyse.xlsx'
    df = pd.DataFrame(zhongyaocai_xls)
    df.to_excel(savepath, index=False)
if __name__ == '__main__':
    analyser()