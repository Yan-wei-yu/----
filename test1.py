import os
from bs4 import BeautifulSoup
from flask import Flask,render_template
from collections import OrderedDict
import numpy as np
app = Flask(__name__)


@app.route('/')
def home():
    path = "."  # 資料夾目錄
    files = os.listdir(path)  # 得到資料夾下的所有檔名稱
    catch1 = []
    catch2= []
    dective=[]
    unique_true=[]
    wapiti_c=1
    chart_title_test=[]
    chart_title=[]
    chart_num=[]
    re_chart_num=[]
    re_chart_title=[]
    find_index=[]
    no_str="\n"
    for file in files:  # 遍歷資料夾
        if file != "templates":
            if os.path.isdir(file):  # 判斷是否是資料夾，不是資料夾才開啟
                dirfile = os.listdir(path+f"/{file}")
                for dirfile1 in dirfile:
                    if ".htm" in dirfile1 and "report.html" not in dirfile1 :
                        f = open(path+f"/{file}/{dirfile1}", 'r', encoding='utf-8')  # 開啟檔案
                        htmlhandle = f.read()
                        soup = BeautifulSoup(htmlhandle, 'html.parser')
                        vulnerabilities =soup.select('.small')
                        page_content=soup.select('#details')
                        Vulner_hideen=soup.select('.is-hidden')#隱藏的部分
                        title=soup.select('h3')#標題
                        title.remove(title[0])
                        dective.append("<div class='main'>偵測項目</div>")
                        for part in vulnerabilities:#圖表
                            if wapiti_c %2!=0:
                                dective.append('<div class="detect_title">'+part.text)
                                chart_title_test.append(str(part.text))#抓文字
                                wapiti_c+=1
                            else:
                                dective.append(part.text+'</div>')
                                chart_num.append(int(part.text))#抓數字
                                wapiti_c+=1
                        for ev_title in chart_title_test:
                            for ev_no_str in no_str:
                                ev_title=ev_title.replace(ev_no_str,"")
                            chart_title.append(ev_title)
                        find_num=np.array(chart_num)#轉array
                        find_num=np.where(find_num!=0)
                        for catch_index in find_num[0]:
                            find_index.append(catch_index)#抓到index
                        chart_title.remove(chart_title[-1])
                        for get_index in find_index:#移除有0的標題、文字
                            re_chart_num.append(chart_num[get_index])
                            re_chart_title.append(str(chart_title[get_index]))
                        dective.remove(dective[-1])
                        for ev_page_content in  page_content:
                            for part_count in range(0,len(title)):
                                part_title=f"{ev_page_content.select('h3')[part_count].text}"
                                part_description=f"\n描述：{ev_page_content.select('dl dd')[part_count*2].text}"
                                part_solution=f"\n解決：{ev_page_content.select('dl dd')[(part_count*2)+1].text}"
                                
                                dective.append(f"<div class='findtitle'>{part_title}</div>")
                                dective.append(f"<div class='finddiscription'>{part_description}</div>")
                                dective.append(f"<div class='findsolution'>{part_solution}</div>")
                        part_bug=soup.find_all('section',{'class':''})
                        unique = list((part_bug))
                        for sp_unique in unique:
                            unique_true.append(sp_unique.text)
                        unique=list(OrderedDict.fromkeys(unique_true))
                        dective.append("<div class='main_title'>Dangerous</div>")
                        for evpart in unique:
                            dective.append(f"{evpart}<br>")
            elif ".htm" in file :#testfire
                f = open(path+"/"+file, 'r', encoding='utf-8')  # 開啟檔案
                print(f)
                htmlhandle = f.read()
                soup = BeautifulSoup(htmlhandle, 'html.parser')
                Description=soup.select('.dataTable>tr:nth-child(3)>td:nth-child(2)')
                for part in Description:
                    catch2.append(part.text)
                catch2.remove(catch2[-1])
                catch2=catch2[::-1]
                dective.append("<div class='main'>您的網站偵測的錯誤</div>")
                for num in catch2:
                    if num.isdigit():
                        break
                    else:
                        dective.append(f"<div class='main_description'>{num}</div>")
    dective = ''.join(str(x) for x in dective) 
    return render_template('index.html', s=dective,char_value= re_chart_num,char_text=re_chart_title)
if __name__ =='__main__':
    app.run(debug=True,port=8000)
