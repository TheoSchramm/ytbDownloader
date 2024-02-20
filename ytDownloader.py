from datetime import datetime
from os import path
from re import sub
from webbrowser import open
from pytube import YouTube, Playlist


def getTime():
    return f"[{datetime.now().strftime('%H:%M')}]"

def cleanse(string: str):
    chars = r'<>:"/\|?*'
    return sub(f'[{chars}]', '', string)

class Main:
    def __init__(self):
        self.funcs = {
        '1' : self.video,
        '2' : self.playlist,
        '3' : self.thumbnail,
        '4' : self.sair
        }

    def baixar(self, video: YouTube, diret: str = None):
        if not path.exists(fr"{diret}\{cleanse(video.title)}.mp3"):
            video.bypass_age_gate()
            print(f'{getTime()} Iniciando download: {video.title}.', end='\r')
            try:
                file = video.streams.filter(only_audio = True)[0].download(output_path = diret, filename = f"{cleanse(video.title)}.mp3")
            except Exception as err:
                print(f'{getTime()} Erro ao baixar o vídeo: {video.title}. | {err.__class__.__name__}: {err}')
            else:
                self.baixados += 1
                print(f'{getTime()} Vídeo baixado com sucesso: {video.title}.')
        else:
            self.baixados += 1

    def video(self):
        yt = YouTube(input(f"{getTime()} Digite o link do vídeo: "))
        self.baixar(video = yt)
        print(f"{getTime()} Terminei! Baixei {self.baixados}/1 vídeo(s) com sucesso.")

    def playlist(self):
        yt = Playlist(input(f"{getTime()} Digite o link da playlist: "))
        
        for video in yt.videos: 
            self.baixar(video = video, diret = cleanse(yt.title))
        print(f"{getTime()} Terminei! Baixei {self.baixados}/{len(yt.videos)} vídeo(s) com sucesso.")

    def thumbnail(self):
        yt = YouTube(input(f"{getTime()} Digite o link do vídeo: "))
        open(yt.thumbnail_url)
        print(f"{getTime()} {yt.title}: \n{yt.thumbnail_url}")

    def sair(self):
        print(f"{getTime()} Saindo...")
        exit()

    def run(self):
        while True:
            self.baixados = 0 
            try:
                self.funcs[input(f"{getTime()} Digite ({'/'.join(self.funcs.keys())}) para baixar ({'/'.join([i.__name__ for i in self.funcs.values()])}): ").strip()]()
            except Exception as err:
                print(f"{getTime()} Erro! | {err.__class__.__name__}: {err}")
            print()

Main().run()