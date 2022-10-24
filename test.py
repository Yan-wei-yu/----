import os
from bs4 import BeautifulSoup
from collections import OrderedDict
path = "."  # 資料夾目錄
files = os.listdir(path)  # 得到資料夾下的所有檔名稱
wapiti_c=1
wapiti_sec_num=[]#section的數字
dective=[]
sec_num_get=[]#獲得每個數字
count_times = []#每個數字計數
postion_time=0

for file in files:  # 遍歷資料夾
        if file != "templates":
            if os.path.isdir(file):  # 判斷是否是資料夾，不是資料夾才開啟
                dirfile = os.listdir(path+f"/{file}")
                for dirfile1 in dirfile:
                    if ".htm" in dirfile1 and "report.html" not in dirfile1 :
                        f = open(path+f"/{file}/{dirfile1}", 'r', encoding='utf-8')  # 開啟檔案
                        htmlhandle = f.read()
                        soup = BeautifulSoup(htmlhandle, 'html.parser')
                        vulnerabilities =soup.select('.small')#漏洞圖表
                        page_content=soup.select('#details')#描述的部分
                        title=soup.select('h3')#標題
                        title.remove(title[0])
                        # dective.append("圖表偵測：\n")
                        for part in vulnerabilities:#圖表輸出
                            if wapiti_c %2!=0:
                                dective.append(part.text)
                                wapiti_c+=1
                            else:
                                dective.append(part.text+'\n')
                                wapiti_c+=1
                        dective.remove(dective[-1])
                        for idName in soup.find_all('section',{'class':''}):#section的處理方式
                            wapiti_sec_num.append(idName.get('id'))
                        for ev_wapiti_sec_num in wapiti_sec_num:
                            ev_wapiti_sec_num=ev_wapiti_sec_num[9:]#去除前八個
                            new_num=''
                            for discover in ev_wapiti_sec_num:
                                if discover !="-":
                                    new_num=new_num+discover   
                                else:
                                    sec_num_get.append(int(new_num))
                                    new_num=""
                                    break
                        for num_count in range(len(sec_num_get)):
                            if num_count == (len(sec_num_get)-1):
                                break
                            else:
                                if  sec_num_get[num_count] == sec_num_get[num_count+1] :
                                    continue
                                elif sec_num_get[num_count] != sec_num_get[num_count+1]:
                                    num=sec_num_get.count(sec_num_get[num_count])
                                    count_times.append(num)
                        last_time=(sec_num_get.count(sec_num_get[-1]))
                        old_countimes=count_times
                        old_countimes.append(last_time)
                        count_times = [int(x/2) for x in count_times]
                        count_times[-1]=1
                        for ev_page_content in  page_content:
                            for part_count in range(0,len(title)):
                                part_title=f"標題：{ev_page_content.select('h3')[part_count].text}"
                                part_description=f"\n描述：{ev_page_content.select('dl dd')[part_count*2].text}"
                                part_solution=f"\n解決：{ev_page_content.select('dl dd')[(part_count*2)+1].text}"
                                print(part_count+1,part_title,part_description,part_solution)
                        part_bug=soup.find_all('section',{'class':''})
                        unique = list(OrderedDict.fromkeys(part_bug))
                        print(unique)
                    
                        for evpart in unique:
                            print(f"<br>{evpart.text}")
                        
                                # print(f"\n第{part_count+1}次紀錄<>{record}")

                            
                            
                                
                            # for num in range(len(count_times)):
                            #     if count_times[num]==1:
                                

                        # for ev_page_content in  page_content:
                        #     for part_count in range(0,len(title)):
                        #         print(f"標題：{ev_page_content.select('h3')[part_count].text}\n描述：{ev_page_content.select('dl dd')[part_count*2].text}\n解決：{ev_page_content.select('dl dd')[(part_count*2)+1].text}")
                            # print(f"標題：{ev_page_content.select('h3')[0].text}\n漏洞發現：{ev_page_content.select('section')[0].text}描述：{ev_page_content.select('dl dd')[0].text}\n解決：{ev_page_content.select('dl dd')[2].text}")
                           
                               
                    
        elif ".htm" in file :#testfire
            f = open(path+"/"+file, 'r', encoding='utf-8')  # 開啟檔案
            htmlhandle = f.read()
            soup = BeautifulSoup(htmlhandle, 'html.parser')
            Description=soup.select('.dataTable>tr:nth-child(3)>td:nth-child(2)')
            for part in Description:
                s.append(part.text)
            s.remove(s[-1])
            s=s[::-1]
            # print("您的網站發生的錯誤有：")
            # for num in s:
            #     if num.isdigit():
            #         break
            #     else:
            #         print(num) 
            
# s = ''.join(str(x) for x in s) 
# print(s)