import json
import requests
from concurrent.futures import ThreadPoolExecutor

def check_link(module):
    filename = module['filename']
    url = f"https://of-302v.zkitefly.eu.org/file/{filename}"
    try:
        response = requests.head(url, proxies=None)
        if response.status_code == 404:
            print(f"链接 {url} 返回 404，删除模块 {filename}")
            delete_module(module)
        elif response.status_code != 200:
            print(f"链接 {url} 返回状态码: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"连接 {url} 出错: {e}")

def delete_module(module):
    # 根据需要执行删除模块的操作
    # 这里只是简单打印一条消息
    print(f"模块 {module['filename']} 已删除")
    # 删除模块
    index_data['file'].remove(module)

def check_links():
    # 读取 index.json 文件
    with open('index.json', 'r') as f:
        global index_data
        index_data = json.load(f)
    
    # 使用线程池并发检测链接
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(check_link, module) for module in index_data['file']]
        for future in futures:
            future.result()

    # 保存更新后的 JSON 数据
    with open('index.json', 'w') as f:
        json.dump(index_data, f, indent=4)

if __name__ == "__main__":
    check_links()
