from snowboy import snowboydecoder
import sys
import signal
#import sys
import base64
import os
from aip import AipSpeech
import json
import requests
from MyEncoder import MyEncoder  # 自定义json序列化
""" 你的 APPID AK SK """
baidu_config = {
    "APP_ID" : '25440803',
    "API_KEY" : 'UZ5lqiTxodXW841lqPQZx0u1',
    "SECRET_KEY" : 'horc2YIgeIN5AsRZzohTQGPlV0nASDa8'
}
client = AipSpeech(baidu_config["APP_ID"],baidu_config["API_KEY"],baidu_config["SECRET_KEY"])

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}  # 请求头

def get_baidu_access():
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=UZ5lqiTxodXW841lqPQZx0u1&client_secret=horc2YIgeIN5AsRZzohTQGPlV0nASDa8"
    response = requests.get(url,headers=headers)
    response = json.loads(response.text)
    accsee_token = response["access_token"]

    return accsee_token

# reload(sys)

# sys.setdefaultencoding('utf-8')

def Speask():

    header = {'Content-Type': 'application/json'}
    url = "https://vop.baidu.com/pro_api"

    WAVE_FILE = "16k.wav"
    f = open(WAVE_FILE, "rb")  # 以二进制读模式打开输入音频
    speech = base64.b64encode(f.read())  # 读音频文件并使用base64编码
    size = os.path.getsize(WAVE_FILE)  # 获取文件大小(字节)

    token = get_baidu_access()
    print(token)
    data_json = json.dumps(
        {"format": "wav", "rate": 16000, "channel": 1, "cuid": "zhl", "token":token,"dev_pid":80001,
         "speech": speech, "len": size}, cls=MyEncoder, indent=4)  # 请求数据格式

    response = requests.post(url, data=data_json,
                             headers=header)
    print(response.text)


def chat(message):

    key = "c49849b470506d680697c9e94bcda286"  #天行机器人密钥
    url = "http://api.tianapi.com/robot/index?key={}&question={}".format(key,message)
    response = requests.get(url)
    response = json.loads(response.text)
    return response["newslist"][0]["reply"]


def baidu_tts(message):
    result = client.synthesis(message, 'zh', 1, {'vol': 5, 'per': 4})  # 请求参数
    if not isinstance(result, dict):  # 识别正确返回语音二进制 错误则返回dict
        with open('audio.mp3', 'wb') as f:  # wb表示二进制写入
            f.write(result)
    else:
        print(result)






def weather():
    pass


def get_song_url(keyword):

    url = "http://maosheng0088.cn:3000/search?limit=1&keywords={}".format(keyword)
    response = requests.get(url)
    response = json.loads(response.text)
    id = response["result"]["songs"][0]["id"]
    print(id)
    song_url = "http://maosheng0088.cn:3000/song/url?id={}".format(id)
    res = requests.get(song_url)
    res = json.loads(res.text)
    result = res["data"][0]["url"]
    print(result)
    try:
        song = requests.get(result,headers=headers,stream=True)
        with open("song.mp3",'wb') as f:
            f.write(song.content)
        print("suceese")
    except:
        print("err")
        print("播放失败")

def callbacks():
    global detector
    print("成功唤醒小派!")
    snowboydecoder.play_audio_file()  # ding
    detector.terminate()  # close
    Speech(access_token)
    wake_up()

def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

def wake_up():
    global detector
    model = '/home/pi/finaldesign/raspi-python/resources/xiaopai.pmdl'
    signal.signal(signal.SIGINT, signal_handler)
    detector = snowboydecoder.HotwordDetector(model, sensitivity=0.6)
    print('我在听...请说唤醒词:小派...')
    # main loop
    detector.start(detected_callback=callbacks,
                   interrupt_check=interrupt_callback, sleep_time=0.03)
    detector.terminate()


if __name__ == "__main__":

    Speask()