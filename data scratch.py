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


path = os.getcwd() + "/total_weiboComments_spider0508.csv"
path1 = os.getcwd() +'/title_weiboComments_spider0508.csv'
path2 = os.getcwd() + '/comment_weiboComments_spider0508.csv'

csvfile = open(path, 'a', newline='', encoding='utf-8-sig')
csvfile1 = open(path1, 'a', newline='', encoding='utf-8-sig')
csvfile2 = open(path2, 'a', newline='', encoding='utf-8-sig')

writer = csv.writer(csvfile)
writer_1 = csv.writer(csvfile1)
writer_2 = csv.writer(csvfile2)

writer.writerow(('article_url', 'title_text', 'title_user_id', 'title_user_NicName', 'title_user_gender', 'add_title_time',
                 'title_created_YMD', 'reposts_count', 'comments_count', 'attitudes_count', 'user_id', 'user_name',
                 'user_gender', 'created_YMD', 'created_time', 'comment_text'))

writer_1.writerow(('article_url', 'title_text', 'title_user_id', 'title_user_NicName', 'title_user_gender', 'add_title_time',
                 'title_created_YMD', 'reposts_count', 'comments_count', 'attitudes_count'))

writer_2.writerow(('user_id', 'user_name','user_gender', 'created_YMD', 'created_time', 'comment_text'))

headers = {
     'cookie':'SUB=_2A25PfMkqDeRhGeNJ71QU-CnIyD2IHXVsntdirDV6PUJbkdANLUjMkW1NS9wfh4O-H7kUuBiX8lMOdamGCchX_ZsO; WEIBOCN_FROM=1110006030; MLOGIN=1; _T_WM=59055409723; XSRF-TOKEN=cd5420; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D100103type%253D38%2526q%253D%25E6%2596%25B0%25E5%2586%25A0%2526t%253D0%26fid%3D100103type%253D38%2526q%253D%25E6%2596%25B0%25E5%2586%25A0%2526t%253D0%26uicode%3D10000011',
     'Referer': 'https://m.weibo.cn/search?containerid=100103type%3D1%26q%3D%E6%96%B0%E5%86%A0',
     'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36',
     'X-Requested-With': 'XMLHttpRequest'
}


comments_ID = []

def get_title_id():
    for page in range(2, 45):
        headers = {
            "User-Agent": UserAgent().chrome
        }
        time.sleep(1)
        api_url='https://m.weibo.cn/api/container/getIndex?containerid=100103type=61&q=#??????#&t=0&page_type=searchall&page='+str(page)
        print(api_url)
        rep1 = requests.get(url=api_url, headers=headers)
        rep=json.loads(rep1.text)
        for json1 in rep['data']['cards']:
            comment_ID = json1["card_group"][0]['mblog']['id']
            comments_ID.append(comment_ID)

def spider_title(comment_ID):

    try:
        article_url = 'https://m.weibo.cn/detail/' + comment_ID
        print("article_url = ", article_url)
        html_text = requests.get(url=article_url, headers=headers).text


        # title_text
        find_title = re.findall('.*?"text": "(.*?)",.*?', html_text)[0]
        title_text = re.sub('<(S*?)[^>]*>.*?|<.*? />', '', find_title)
        print("title_text = ", title_text)

        # title_user_id
        title_user_id = re.findall('.*?"id": (.*?),.*?', html_text)[1]
        print("title_user_id = ", title_user_id)

        # title_user_NicName
        title_user_NicName = re.findall('.*?"screen_name": "(.*?)",.*?', html_text)[0]
        print("title_user_NicName = ", title_user_NicName)

        # title_user_gende
        title_user_gender = re.findall('.*?"gender": "(.*?)",.*?', html_text)[0]
        print("title_user_gender = ", title_user_gender)

        # title_time
        created_title_time = re.findall('.*?"created_at": "(.*?)".*?', html_text)[0].split(' ')

        # title_created_YMD
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
            print('Other_time???URL = ')
            pass
        print("title_created_YMD = ", title_created_YMD)

        # add_title_time
        add_title_time = created_title_time[3]
        print("add_title_time = ", add_title_time)

        # reposts_count
        reposts_count = re.findall('.*?"reposts_count": (.*?),.*?', html_text)[0]
        print("reposts_count = ", reposts_count)

        # comments_count
        comments_count = re.findall('.*?"comments_count": (.*?),.*?', html_text)[0]
        print("comments_count = ", comments_count)

        # attitudes_count
        attitudes_count = re.findall('.*?"attitudes_count": (.*?),.*?', html_text)[0]
        print("attitudes_count = ", attitudes_count)

        # comment_count
        comment_count = int(int(comments_count) / 18)

        position1 = (article_url, title_text, title_user_id, title_user_NicName, title_created_YMD,
                     add_title_time, reposts_count, comments_count, attitudes_count, " ", " ", " ", " ", " ", " ")
        position11 = (article_url, title_text, title_user_id, title_user_NicName, title_created_YMD,
                     add_title_time, reposts_count, comments_count, attitudes_count)

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
        # user_id
        user_id = json['user']['id']
        # user_Name
        user_name = json['user']['screen_name']
        # user_gender,M for male???F for female
        user_gender = json['user']['gender']
        # comments_text
        comments_text = json['text']
        comment_text = re.sub('<(S*?)[^>]*>.*?|<.*? />', '', comments_text)
        # created_times
        created_times = json['created_at'].split(' ')

        if 'May' in created_times:
            created_YMD = "{}/{}/{}".format(created_times[-1], '05', created_times[2])
        elif 'Apr' in created_times:
            created_YMD = "{}/{}/{}".format(created_times[-1], '04', created_times[2])
        else:
            print()
            pass
        created_time = created_times[3]
        # if len(comment_text) != 0:

        position2 = (
        " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", user_id, user_name, user_gender, created_YMD, created_time,
        comment_text)

        position22 = (user_id, user_name, user_gender, created_YMD,created_time,comment_text)
        writer.writerow((position2))
        writer_2.writerow(position22)
        # print (user_id, user_name, user_gender, created_YMD, created_time)


def main():
    count_title = len(comments_ID)
    for count, comment_ID in enumerate(comments_ID):
        print("???????????????%s???????????????????????????%s??????????????????" % (count + 1, count_title))

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
    print("?????????????????????????????????%s??????" % useTime)



