import requests, random, re
import time
import os
import csv
import sys
import json
import importlib
from fake_useragent import UserAgent
from lxml import etree


importlib.reload(sys)
startTime = time.time()

# --------------------------------------------document save-----------------------------------------------------


path = os.getcwd() + "/total_weiboComments_spider0508.csv"
path1 = os.getcwd() +'/title_weiboComments_spider0508.csv'
path2 = os.getcwd() + '/comment_weiboComments_spider0508.csv'

csvfile = open(path, 'a', newline='', encoding='utf-8-sig')
csvfile1 = open(path1, 'a', newline='', encoding='utf-8-sig')
csvfile2 = open(path2, 'a', newline='', encoding='utf-8-sig')

writer = csv.writer(csvfile)
writer_1 = csv.writer(csvfile1)
writer_2 = csv.writer(csvfile2)

writer.writerow(('话题链接', '话题内容', '楼主ID', '楼主昵称', '楼主性别', '发布日期',
                 '发布时间', '转发量', '评论量', '点赞量', '评论者ID', '评论者昵称',
                 '评论者性别', '评论日期', '评论时间', '评论内容'))

writer_1.writerow(('话题链接', '话题内容', '楼主ID', '楼主昵称', '楼主性别', '发布日期',
                 '发布时间', '转发量', '评论量', '点赞量'))

writer_2.writerow(('评论者ID', '评论者昵称','评论者性别', '评论日期', '评论时间', '评论内容'))

headers = {
     'cookie':'SUB=_2A25PfMkqDeRhGeNJ71QU-CnIyD2IHXVsntdirDV6PUJbkdANLUjMkW1NS9wfh4O-H7kUuBiX8lMOdamGCchX_ZsO; WEIBOCN_FROM=1110006030; MLOGIN=1; _T_WM=59055409723; XSRF-TOKEN=cd5420; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D100103type%253D38%2526q%253D%25E6%2596%25B0%25E5%2586%25A0%2526t%253D0%26fid%3D100103type%253D38%2526q%253D%25E6%2596%25B0%25E5%2586%25A0%2526t%253D0%26uicode%3D10000011',
     'Referer': 'https://m.weibo.cn/search?containerid=100103type%3D1%26q%3D%E6%96%B0%E5%86%A0',
     'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36',
     'X-Requested-With': 'XMLHttpRequest'
}


comments_ID = []

def get_title_id():
    for page in range(2, 45):  # 每个页面大约有9个话题
        headers = {
            "User-Agent": UserAgent().chrome  # chrome浏览器随机代理
        }
        time.sleep(1)
        api_url='https://m.weibo.cn/api/container/getIndex?containerid=100103type=61&q=#新冠#&t=0&page_type=searchall&page='+str(page)
        print(api_url)
        rep1 = requests.get(url=api_url, headers=headers)
        rep=json.loads(rep1.text)
        # 获取ID值并写入列表comment_ID中
        for json1 in rep['data']['cards']:
            comment_ID = json1["card_group"][0]['mblog']['id']
            comments_ID.append(comment_ID)

def spider_title(comment_ID):

    try:
        article_url = 'https://m.weibo.cn/detail/' + comment_ID
        print("article_url = ", article_url)
        html_text = requests.get(url=article_url, headers=headers).text


        # 话题内容
        find_title = re.findall('.*?"text": "(.*?)",.*?', html_text)[0]
        title_text = re.sub('<(S*?)[^>]*>.*?|<.*? />', '', find_title)  # 正则匹配掉html标签
        print("title_text = ", title_text)

        # 楼主ID
        title_user_id = re.findall('.*?"id": (.*?),.*?', html_text)[1]
        print("title_user_id = ", title_user_id)

        # 楼主昵称
        title_user_NicName = re.findall('.*?"screen_name": "(.*?)",.*?', html_text)[0]
        print("title_user_NicName = ", title_user_NicName)

        # 楼主性别
        title_user_gender = re.findall('.*?"gender": "(.*?)",.*?', html_text)[0]
        print("title_user_gender = ", title_user_gender)

        # 发布时间
        created_title_time = re.findall('.*?"created_at": "(.*?)".*?', html_text)[0].split(' ')

        # 日期
        if 'Jan' in created_title_time:
            title_created_YMD = "{}/{}/{}".format(created_title_time[-1], '01', created_title_time[2])
        elif 'Feb' in created_title_time:
            title_created_YMD = "{}/{}/{}".format(created_title_time[-1], '02', created_title_time[2])
        elif 'Mar' in created_title_time:
            title_created_YMD = "{}/{}/{}".format(created_title_time[-1], '03', created_title_time[2])
        elif 'Apr' in created_title_time:
            title_created_YMD = "{}/{}/{}".format(created_title_time[-1], '04', created_title_time[2])
        elif 'May' in created_title_time:
            title_created_YMD = "{}/{}/{}".format(created_title_time[-1], '05', created_title_time[2])
        elif 'Jun' in created_title_time:
            title_created_YMD = "{}/{}/{}".format(created_title_time[-1], '06', created_title_time[2])
        elif 'July' in created_title_time:
            title_created_YMD = "{}/{}/{}".format(created_title_time[-1], '07', created_title_time[2])
        elif 'Aug' in created_title_time:
            title_created_YMD = "{}/{}/{}".format(created_title_time[-1], '08', created_title_time[2])
        elif 'Sep' in created_title_time:
            title_created_YMD = "{}/{}/{}".format(created_title_time[-1], '09', created_title_time[2])
        else:
            print('发布在其他时间！URL = ')
            pass
        print("title_created_YMD = ", title_created_YMD)

        # 发布时间
        add_title_time = created_title_time[3]
        print("add_title_time = ", add_title_time)

        # 转发量
        reposts_count = re.findall('.*?"reposts_count": (.*?),.*?', html_text)[0]
        print("reposts_count = ", reposts_count)

        # 评论量
        comments_count = re.findall('.*?"comments_count": (.*?),.*?', html_text)[0]
        print("comments_count = ", comments_count)

        # 点赞量
        attitudes_count = re.findall('.*?"attitudes_count": (.*?),.*?', html_text)[0]
        print("attitudes_count = ", attitudes_count)

        # 每个ajax一次加载18条数据
        comment_count = int(int(comments_count) / 18)

        #position1是记录
        position1 = (article_url, title_text, title_user_id, title_user_NicName, title_created_YMD,
                     add_title_time, reposts_count, comments_count, attitudes_count, " ", " ", " ", " ", " ", " ")
        position11 = (article_url, title_text, title_user_id, title_user_NicName, title_created_YMD,
                     add_title_time, reposts_count, comments_count, attitudes_count)

        # 写入数据
        writer.writerow((position1))
        writer_1.writerow(position11)

        return comment_count
    except:
        pass



def get_page(comment_ID, max_id, id_type):
    params = {
        'max_id': max_id,
        'max_id_type': id_type
    }

    url = ' https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id'.format(comment_ID, comment_ID)

    try:
        r = requests.get(url, params=params, headers=headers)
        if r.status_code==200:
            return r.json()
    except requests.ConnectionError as e:
        print('error', e.args)
        pass



def parse_page(jsondata):
    if jsondata:
        items = jsondata.get('data')
        item_max_id = {}
        item_max_id['max_id'] = items['max_id']
        item_max_id['max_id_type'] = items['max_id_type']
        return item_max_id



def write_csv(jsondata):
    for json in jsondata['data']['data']:
        # 用户ID
        user_id = json['user']['id']
        # 用户昵称
        user_name = json['user']['screen_name']
        # 用户性别,m表示男性，表示女性
        user_gender = json['user']['gender']
        # 获取评论
        comments_text = json['text']
        comment_text = re.sub('<(S*?)[^>]*>.*?|<.*? />', '', comments_text)  # 正则匹配掉html标签
        # 评论时间
        created_times = json['created_at'].split(' ')

        if 'May' in created_times:
            created_YMD = "{}/{}/{}".format(created_times[-1], '05', created_times[2])
        elif 'Apr' in created_times:
            created_YMD = "{}/{}/{}".format(created_times[-1], '04', created_times[2])
        else:
            print('发布时间不在四月，五月之间！')
            pass
        created_time = created_times[3]  # 评论时间时分秒
        # if len(comment_text) != 0:

        position2 = (
        " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", user_id, user_name, user_gender, created_YMD, created_time,
        comment_text)

        position22 = (user_id, user_name, user_gender, created_YMD,created_time,comment_text)
        # 写入数据
        writer.writerow((position2))
        writer_2.writerow(position22)
        # print (user_id, user_name, user_gender, created_YMD, created_time)


主函数---------------------------------------------------
def main():
    count_title = len(comments_ID)
    for count, comment_ID in enumerate(comments_ID):
        print("正在爬取第%s个话题，一共找到个%s话题需要爬取" % (count + 1, count_title))

        maxPage = spider_title(comment_ID)
        print('maxPage = ', maxPage)
        m_id = 0
        id_type = 0
        if maxPage != 0:
            try:
                for page in range(0, maxPage):
                    jsondata = get_page(comment_ID, m_id, id_type)
                    write_csv(jsondata)
                    results = parse_page(jsondata)
                    time.sleep(1)
                    m_id = results['max_id']
                    id_type = results['max_id_type']
            except:
                pass
        print()
    csvfile.close()
    csvfile1.close()
    csvfile2.close()


if __name__ == '__main__':

    main()
    endTime = time.time()
    useTime = (endTime - startTime) / 60
    print("该次所获的信息一共使用%s分钟" % useTime)



