import sys
import time
from datetime import datetime
import configparser
from pathlib import Path
import pydub
import pydub.playback as playback

def unidades_por_plataforma():
    if sys.platform == 'linux':
        #p = Path('/media/constantino-radio/')
        print('unidades_por_plataforma: ', self._diretorio_usb_linux)
        p = Path(self._diretorio_usb_linux)
        return [str(i) for i in p.iterdir() if i.is_dir()] if p.exists() else []
    # se for windows...
    return ['D:/musicas/', 'E:/musicas/', 'F:/musicas/', 'G:/musicas/']



class Cfg:
    def __init__(self):
        self.sino_ou_musica = None
        self.sino_padrao = None 
        self.pasta_padrao = None 
        self.tempo_musica = None


cfg = Cfg()


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


def gerar_ini():
    pass


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


def ler_ini():
    
    global cfg

    try:
        config = configparser.ConfigParser()
        # colocar direitorio aqui via código
        config.read('/home/jhoonb/proj/pysino/horarios.ini')
    except:
        gerar_ini()
    
    cfg.pasta_padrao = config['configuracao']['pastaPadrao']
    cfg.sino_padrao = config['configuracao']['sinoPadrao']
    cfg.tempo_musica = config['configuracao']['tempoMusica']

    return config


def tocar():
    global cfg
    c = '/home/jhoonb/'
    arquivo = 'sino_padrao.mp3' if cfg.sino_ou_musica == 'sino' else "errare.mp3"
    musica = pydub.AudioSegment.from_file(c+arquivo, format="mp3")
    tempo = cfg.tempo_musica * 1000
    playback.play(musica[:tempo])


if __name__ == '__main__':
    
    config_file = ler_ini()
    dia = dia_hoje()

    hr_musica = config_file[dia]['horarioMusica'].strip().split(",")
    hr_sino = config_file[dia]['horarioSinoPadrao'].strip().split(",")
    hr_musica = [i.replace(" ", "") for i in hr_musica]
    hr_sino = [i.replace(" ", "") for i in hr_sino]

    print("""
    -----------------------------------------------------
                        Pysino 

                        2019 
    ----------------Configurações------------------------
    Hoje é: {}
    Tempo de execução da Música: {} seg(s).
    Diretório das Músicas: {}
    Sino Padrão: {}
    -----------------------------------------------------
    """.format(dia,
    cfg.tempo_musica,
    cfg.pasta_padrao,
    cfg.sino_padrao))

    while hr_musica:
       
        hora_agora = datetime.now()
        _hora = 'Horário: {}:{}'.format(hora_agora.hour, hora_agora.minute)

        print(_hora, end='\r')

        comp = comparar_data(hr_musica[0], hora_agora)
        cfg.sino_ou_musica = 'sino' if hr_musica[0] in hr_sino else 'musica'

        if comp == 0:
            tocar()
            hr_musica.remove(hr_musica[0])
        elif comp == -1:
            hr_musica.remove(hr_musica[0])
        else: # comp == 1:
            pass # ainda nao foi, espera...
        time.sleep(5)

# fim
print("\ttodos os sinos agendados tocados!")