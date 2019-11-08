import os
import sys
import time
import random
import configparser
# audios libs
import pydub
import pydub.playback as playback

from pathlib import Path
from datetime import datetime

def dia_hoje():

    hr = datetime.now()
    dia = hr.strftime("%A")
    dias = {
        'Monday': 'segunda',
        'Tuesday': 'terca',
        'Wednesday': 'quarta',
        'Thursday': 'quinta',
        'Friday': 'sexta'
    }
    return dias[dia] if dia in dias else 'sexta'


def comparar_data(data_str, data_obj):
    h_str, m_str = data_str.split(":")
    h_str, m_str = int(h_str), int(m_str)
    h_obj, m_obj = int(data_obj.hour), int(data_obj.minute)
    if h_str == h_obj and m_str == m_obj:
        return 0
    if h_str == h_obj and m_str > m_obj:
        return 1
    if h_str == h_obj and m_str < m_obj:
        return -1
    if h_str > h_obj:
        return 1
    return -1


class Pysino:

    def __init__(self):
        
        _config = configparser.ConfigParser()
        _p = os.getcwd()
        _arq = Path(_p)
        _arq = _arq / 'horarios.ini'

        _config.read(str(_arq))
        _dia = dia_hoje()

        _hr_musica = _config[_dia]['horarioMusica'].strip().split(",")
        _hr_sino = _config[_dia]['horarioSinoPadrao'].strip().split(",")

        self.hr_musica = [i.replace(" ", "") for i in _hr_musica]
        self.hr_sino = [i.replace(" ", "") for i in _hr_sino]
        self.sino_ou_musica = None
        self.sino_padrao = _config['configuracao']['sinoPadrao'] 
        self.pasta_padrao = _config['configuracao']['pastaPadrao'] 
        self.tempo_musica = int(_config['configuracao']['tempoMusica'])
        self.dia = _dia


    def tocar(self):
        arquivo_musica = ''
        if self.sino_ou_musica == 'sino':
            arquivo_musica = self.sino_padrao
        else:
            arquivo_musica = self.escolher_musica()

        musica = pydub.AudioSegment.from_file(arquivo_musica, format="mp3")
        tempo = int(self.tempo_musica) * 1000
        # aplica corta na música e faz fade in/out 
        musica = musica[:tempo]
        musica = musica.fade_in(5000)
        musica = musica.fade_out(5000)
        print("Música escolhida: ", arquivo_musica)
        playback.play(musica)


    def executar(self):
        hora_agora = datetime.now()
        print("""
        -----------------------------------------------------
                            Pysino 

                             {} 
        ----------------Configurações------------------------
        Hoje é: {}
        Tempo de execução da Música: {} seg(s).
        Diretório das Músicas: {}
        Sino Padrão: {}
        -----------------------------------------------------
        """.format(hora_agora.year,
        self.dia,
        self.tempo_musica,
        self.pasta_padrao,
        self.sino_padrao))

        while self.hr_musica:
            hora_agora = datetime.now()
            hora = 'Horário: {}:{}    --> [Próximo Sino: {}]'.format(
                hora_agora.hour, 
                hora_agora.minute,
                self.hr_musica[0])

            print(hora, end='\r')

            comp = comparar_data(self.hr_musica[0], hora_agora)
            if self.hr_musica[0] in self.hr_sino:
                self.sino_ou_musica = 'sino'
            else:
                self.sino_ou_musica = 'musica'

            if comp == 0:
                self.tocar()
                self.hr_musica.remove(self.hr_musica[0])
            elif comp == -1: #remove porque é horário passado
                self.hr_musica.remove(self.hr_musica[0])
                time.sleep(2)
                continue
            else: # comp == 1:
                pass # ainda nao foi, espera...
            time.sleep(5)


    def escolher_musica(self):

        def is_mp3(i):
            if i.is_file() and str(i).split(".")[-1] == "mp3":
                return True
            return False

        p = Path(self.pasta_padrao)
        
        musicas = [i for i in p.iterdir() if is_mp3(i)]
        return random.choice(musicas)


if __name__ == '__main__':

    pysino = Pysino()
    pysino.executar()
    print("""
        -----------------------------------------------------
                         Concluído!
        -----------------------------------------------------
    """)