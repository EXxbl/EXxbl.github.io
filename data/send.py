import csv
import re
from config import connect

connect_config = connect.Insert_sql(redis_db='github_io',mysql_db='github_io')

def load_website_list(path):
    """加载网站列表数据"""
    try:
        # 读取 CSV 文件中的链接到列表
        website_list = []
        with open(path, mode='r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            for row in reader:
                # 去除http://或https://前缀
                url = re.sub(r'^https?://', '', row[0])
                website_list.append(url)  # 假设每行只有一个链接
            return website_list
    except Exception as e:
        print(f"加载网站列表文件失败: {e}")
        return []
def add_csv():
    connect_config.redis_del_list('git_url')
    # if connect_config.redis_llen('git_url') <= 0:
    website_list = load_website_list("../data/links.csv")
    for website in website_list:
        connect_config.redis_save('git_url', website)

if __name__ == '__main__':
    add_csv()