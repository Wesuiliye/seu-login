import requests
import re
import execjs
import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning



def login(sess, uname, pwd):
    #login_url = 'https://newids.seu.edu.cn/authserver/login?goto=http://my.seu.edu.cn/index.portal'
    login_url = "https://authserver.hniu.cn/authserver/login"
    get_login = sess.get(login_url)
    get_login.encoding = 'utf-8'
    lt = re.search('name="lt" value="(.*?)"', get_login.text).group(1)
    salt = re.search('id="pwdDefaultEncryptSalt" value="(.*?)"', get_login.text).group(1)
    #print(salt)
    execution = re.search('name="execution" value="(.*?)"', get_login.text).group(1)
    f = open("encrypt.js", 'r', encoding='UTF-8')
    line = f.readline()
    js = ''
    
    while line:
        js = js + line
        line = f.readline()
    ctx = execjs.compile(js)
    password = ctx.call('_ep', pwd, salt)

    #login_post_url = 'https://newids.seu.edu.cn/authserver/login?goto=http://my.seu.edu.cn/index.portal'
    login_post_url = "https://authserver.hniu.cn/authserver/login"
    personal_info = {'username': uname,
                     'password': password,
                     'lt': lt,
                     'dllt': 'userNamePasswordLogin',
                     'execution': execution,
                     '_eventId': 'submit',
                     'rmShown': '1'}
    post_login = sess.post(login_post_url, personal_info)
    post_login.encoding = 'utf-8'
    #print(post_login.text)
    if re.search("信息", post_login.text):
        print("SUCCESS!")
    else:
        print("FAILED!")


def main():
    username = sys.argv[1]
    password = sys.argv[2]
    sess = requests.session()
    #sess.trust_env = False
    proxies = {'http': 'socks5://localhost:8083', 'https': 'socks5://localhost:8083'}
    sess.proxies = proxies
    # 禁用特定警告
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    sess.verify=False
    login(sess, username, password)
    sess.close()


if __name__ == '__main__':
    main()
