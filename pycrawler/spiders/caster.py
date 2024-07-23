import scrapy
import os
from pycrawler.items import PycrawlerItem

class IndexItem(scrapy.Item):
    name = scrapy.Field()
    href = scrapy.Field()

class CasterSpider(scrapy.Spider):
    name = "caster"
    allowed_domains = ["www.zysj.com.cn"]
    start_urls = ["https://www.zysj.com.cn/index.html"]
    base_url = 'https://www.zysj.com.cn'
    debug = False

    def NoneStrCheck(self,st):
        if(st==None):
            return ''
        return st

    def parse(self, response):
        if(self.debug):
            debugNum = 0 # 初始化调试计数器
        path = 'debug'  # 调试输出路径
        if(not os.path.exists(path)):
            os.makedirs(path) # 如果路径不存在则创建
        if(self.debug):
            open(path+'/'+'index.html','wb').write(response.body) # 如果处于调试模式，保存网页响应内容为index.html
        # 使用XPath选取特定节点
        con = response.xpath('//*[@id="main"]/div[1<position() and position()<6]/h2/a')
        if(self.debug):
            strs = ''
            for each  in con:
                strs = strs + each.extract() + '\n'
            open(path+'/'+'debug'+str(debugNum)+'.txt','w').write(strs) # 如果处于调试模式，保存选取的节点内容为debug*.txt
            debugNum += 1  # 调试计数器加一
        indexs=[]
        for each in con:
            item=IndexItem()
            item['name'] = each.xpath('@title').extract_first()  # 提取节点的title属性作为item的'name'
            item['href'] = each.xpath('@href').extract_first()  # 提取节点的href属性作为item的'href'
            indexs.append(item)  # 将item添加到indexs列表中
        if(self.debug):
            strs = ''
            for each in indexs:
                strs = strs + each['name'] + ' ' + each['href'] + '\n'
            open(path+'/'+'debug'+str(debugNum)+'.txt','w').write(strs) # 如果处于调试模式，保存每个item的'name'和'href'为debug*.txt
            debugNum += 1  # 调试计数器加一

        # 遍历每个item，发送请求并调用parse2进行进一步处理
        for each in indexs:
            self.debug = True  # 设定为调试模式
            yield scrapy.Request(self.base_url+each['href'],callback=self.parse2,meta={'parse2msg':each['name']})#meta可用于传参
            # 通过Scrapy发送请求，调用parse2处理响应，同时传递meta参数'parse2msg'
            
            # 如果以下代码被取消注释，会在第一个item处理后直接返回，加速调试
            #return#加速调试
    def parse2(self, response):
        if(self.debug):
            debugNum = 0  # 初始化调试计数器
        path = 'debug/'+response.meta['parse2msg']
        if(not os.path.exists(path)):  # 根据传入的'meta'参数构建调试输出路径
            os.makedirs(path)  # 如果路径不存在则创建
        if(self.debug):
            open(path+'/'+response.meta['parse2msg']+'.html','wb').write(response.body)
            # 如果处于调试模式，保存响应的HTML内容为parse2msg.html

        # 使用XPath选取特定节点
        con = response.xpath('//*[@id="filter"]/ul/li')
        if(self.debug):
            strs = ''
            for each in con:
                strs = strs + each.extract() + '\n'
            open(path+'/'+'debug'+str(debugNum)+'.txt','w').write(strs)
            debugNum += 1 # 如果处于调试模式，保存选取的节点内容为debug*.txt
        initial =[]
        # 使用ASCII码遍历选取特定节点
        for i in range(65,91):
            initial.append(con.xpath('//*[text()="'+chr(i)+'"]')[0])
        if(self.debug):
            strs = ''
            for each in initial:
                strs = strs + each.extract() + '\n'
            open(path+'/'+'debug'+str(debugNum)+'.txt','w').write(strs)
            debugNum += 1  # 如果处于调试模式，保存ASCII码选取的节点内容为debug*.txt
        indexs =[]
        temp = 65
        # 遍历选取的初始节点，构建IndexItem对象列表
        for each in initial:
            item=IndexItem()
            item['name'] = chr(temp) # 使用ASCII字符作为'name'
            item['href'] = each.xpath('@href').extract_first()  # 提取节点的href属性作为'href'
            indexs.append(item)
            temp = temp + 1
        if(self.debug):
            strs = ''
            for each in indexs:
                strs = strs + each['name'] + ' ' + self.NoneStrCheck(each['href']) + '\n'
            open(path+'/'+'debug'+str(debugNum)+'.txt','w').write(strs)
            debugNum += 1  # 如果处于调试模式，保存每个item的'name'和'href'为debug*.txt

        # 遍历每个IndexItem对象，发送请求并调用parse3进行进一步处理
        for each in indexs:
            self.debug = True
            if(each['href']!=None):
                yield scrapy.Request(self.base_url+each['href'],callback=self.parse3,meta={'parse2msg':response.meta['parse2msg'],'parse3msg':each['name']})#meta可用于传参
                # 发送请求到each['href']，调用parse3处理响应，并传递'meta'参数'parse2msg'和'parse3msg'

                # 如果需要加速调试，可以取消注释以下return语句
                #return#加速调试
    def parse3(self, response):
        if(self.debug):
            debugNum = 0 # 初始化调试计数器
        path = 'debug/'+response.meta['parse2msg']+'/'+response.meta['parse3msg']
        if(not os.path.exists(path)):
            os.makedirs(path) # 如果路径不存在则创建
        if(self.debug):
            open(path+'/'+response.meta['parse3msg']+'.html','wb').write(response.body)
            # 如果处于调试模式，保存响应的HTML内容为parse3msg.html

        # 使用XPath选取特定节点
        con = response.xpath('//*[@id="list-content"]/ul/li/a')
        if(self.debug):
            strs = ''
            for each in con:
                strs = strs + each.extract() + '\n'
            open(path+'/'+'debug'+str(debugNum)+'.txt','w').write(strs)
            debugNum += 1 # 如果处于调试模式，保存选取的节点内容为debug*.txt
        indexs = []
        # 遍历选取的节点，构建IndexItem对象列表
        for each in con:
            item=IndexItem()
            item['name'] = each.xpath('@title').extract_first() # 提取节点的title属性作为'name'
            item['href'] = each.xpath('@href').extract_first()  # 提取节点的href属性作为'href'
            indexs.append(item)
        if(self.debug):
            strs = ''
            for each in indexs:
                strs = strs + each['name'] + ' ' + each['href'] + '\n'
            open(path+'/'+'debug'+str(debugNum)+'.txt','w').write(strs)
            debugNum += 1 # 如果处于调试模式，保存每个item的'name'和'href'为debug*.txt

        # 遍历每个IndexItem对象，发送请求并调用parse4进行进一步处理
        for each in indexs:
            self.debug = True
            if(each['href']!=None):
                yield scrapy.Request(self.base_url+each['href'],callback=self.parse4,meta={'parse2msg':response.meta['parse2msg'],'parse3msg':response.meta['parse3msg'],'parse4msg':each['name']})#meta可用于传参
                # 发送请求到each['href']，调用parse4处理响应，并传递'meta'参数'parse2msg'、'parse3msg'和'parse4msg'
                
                # 如果需要加速调试，可以取消注释以下return语句
                #return#加速调试
    def parse4(self, response):
        if(self.debug):
            debugNum = 0 # 初始化调试计数器
        path = 'debug/'+response.meta['parse2msg']+'/'+response.meta['parse3msg']+'/'+response.meta['parse4msg']
        if(not os.path.exists(path)):
            os.makedirs(path)  # 如果路径不存在则创建
        if(self.debug):
            open(path+'/'+response.meta['parse4msg']+'.html','wb').write(response.body)
            # 如果处于调试模式，保存响应的HTML内容为parse4msg.html
        outpath = 'output/'+response.meta['parse2msg']+'/'+response.meta['parse3msg']+'/'+response.meta['parse4msg']
        if(not os.path.exists(outpath)):
            os.makedirs(outpath) # 如果输出路径不存在则创建
        open(outpath+'/'+response.meta['parse4msg']+'.html','wb').write(response.body)
        # 无论是否处于调试模式，保存响应的HTML内容到output路径中的parse4msg.html文件
