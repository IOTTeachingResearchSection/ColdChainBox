from aip import AipSpeech
from playsound import playsound
from pathlib import Path

class Voice:

    def __init__(self,APP_ID, API_KEY, SECRET_KEY) -> None:

        self.client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    def run(self,text:str,name:str,lang='zh'):

        voice = Path(name)

        if not voice.is_file():
            self.result  = self.client.synthesis(text, lang, 1, {
                'vol': 5,
                })

            # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
            if not isinstance(self.result, dict):
                with open(name, 'wb') as f:
                    f.write(self.result)

        playsound(name)

if __name__ == '__main__':
    voice = Voice('26112295','SL4QkrsHkr99SFlIe7aDNFp7','NQs1W4ZvbnFsGmeTRllp0TIv8ECGMMPy')
    voice.run('箱门已开,请及时取餐','LockOpen.mp3')
        

