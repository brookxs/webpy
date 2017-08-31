# -*- coding: utf-8 -*-
"""
python相关关键词查询接口
需要安装web.py和Levenshtein
安装方法:
sudo pip install -i https://pypi.douban.com/simple web.py python-Levenshtein
运行脚本: python rskey.py [自定义端口, 默认8080]
使用方法: http://127.0.0.1:8080/?s=关键词&n=3
参数说明: s是要查询的关键词(必填); n是返回相关关键词数量(可选, 默认3)
"""
import web
import Levenshtein


urls = (
    '/', 'Index',
)

# 关键词词库 每行一个关键词
ciku = [w.strip() for w in open("ciku.txt")]

class Index:
    def GET(self):
        web.header('Content-Type','text/html; charset=utf-8')
        key = web.input(s=None)
        num = web.input(n=None)
        if key.s is not None:
            word = key.s.encode("utf-8")
            number = int(num.n) if num.n else 3
            return match_key(word, number, ciku)
        else:
            return "欢迎使用关键词自动匹配系统!"


def match_key(key, num, library):
    """获取固定数量的相关关键词
    key: 要获取的关键词
    num: 要获取相关词的数量
    library: 关键词词库
    return: 由/分割的字符串组成的N个关键词
    """
    simi_dict_list = {lib_key: Levenshtein.jaro(key, lib_key) for lib_key in library}
    simi_list = sorted(simi_dict_list.iteritems(), key=lambda x: x[1], reverse=True)
    return "/".join([w[0] for w in simi_list[:num]])


if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
