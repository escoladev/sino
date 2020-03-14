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


def is_mp3(i):
    if i.is_file() and i.suffix == ".mp3":
        return True
    return False


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
        self.tipo = None # 'sino' ou 'musica' 
        self.sino_padrao = _config['configuracao']['sinoPadrao'] 
        self.pasta_padrao = _config['configuracao']['pastaPadrao'] 
        self.tempo_musica = int(_config['configuracao']['tempoMusica'])
        self.dia = _dia
        self.comecar_em = int(_config['configuracao']['comecarEm'])


    def tocar(self):
        arquivo_musica = ''
        tempo = int(self.tempo_musica) * 1000

        if self.tipo == 'sino':
            arquivo_musica = self.sino_padrao
            # a musica pode ser tocada de qualquer segundo
            comecar_em = 0
        # [especial]
        elif self.tipo == 'baitaca':
            arquivo_musica = "/".join(self.sino_padrao.split("/")[:-1]) + "/grota.mp3"
            # a musica pode ser tocada de qualquer segundo
            comecar_em = 0
            tempo = 77 * 1000
        else:
            arquivo_musica = self.escolher_musica()
            # a musica pode ser tocada de qualquer segundo
            comecar_em = int(self.comecar_em) * 1000

        musica = pydub.AudioSegment.from_file(arquivo_musica, format="mp3")
        
        # aplica corta na música e faz fade in/out 
        musica = musica[comecar_em:tempo+comecar_em]
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
        Música começa do segundo: {}
        -----------------------------------------------------
        """.format(hora_agora.year,
        self.dia,
        self.tempo_musica,
        self.pasta_padrao,
        self.sino_padrao,
        self.comecar_em))

        while self.hr_musica:
            hora_agora = datetime.now()
            hora = 'Horário: {}:{}    --> [Próximo Sino: {}]'.format(
                hora_agora.hour, 
                hora_agora.minute,
                self.hr_musica[0])

            print(hora, end='\r')

            comp = comparar_data(self.hr_musica[0], hora_agora)
            if self.hr_musica[0] in self.hr_sino:
                self.tipo = 'sino'
            else:
                self.tipo = 'musica'

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

        p = Path(self.pasta_padrao)
        musicas = [i for i in p.iterdir() if is_mp3(i)]
        return random.choice(musicas)


# homenagem especial ao trovador do Rio Grande do Sul da legitima
# música e tradição gaúcha: Baitaca (Antônio César Pereira Jacques)
def baitaca():
    print(
        """
#    ____          _____                _             _          ____           _        
#   |  _ \  ___   |  ___|   _ _ __   __| | ___     __| | __ _   / ___|_ __ ___ | |_ __ _ 
#   | | | |/ _ \  | |_ | | | | '_ \ / _` |/ _ \   / _` |/ _` | | |  _| '__/ _ \| __/ _` |
#   | |_| | (_) | |  _|| |_| | | | | (_| | (_) | | (_| | (_| | | |_| | | | (_) | || (_| |
#   |____/ \___/  |_|   \__,_|_| |_|\__,_|\___/   \__,_|\__,_|  \____|_|  \___/ \__\__,_|
#    ____        _ _                                                                     
#   | __ )  __ _(_) |_ __ _  ___ __ _                                                    
#   |  _ \ / _` | | __/ _` |/ __/ _` |                                                   
#   | |_) | (_| | | || (_| | (_| (_| |                                                   
#   |____/ \__,_|_|\__\__,_|\___\__,_|                                                   
#   
            (Mateando ao pé do borraio
            Conto causos e anedota
            E o fogo véio campeiro
            Me aquenta o bico da bota
            E pra cantar o Brasil inteiro
            Venho do fundo da grota) 

    Fui criado na campanha
    Em rancho de barro e capim
    Por isso é que eu canto assim
    Pra relembrar meu passado
    Eu me criei arremedado
    Dormindo pelos galpão
    Perto de um fogo de chão
    Com os cabelo enfumaçado

    Quando rompe a estrela D'alva
    Aquento a chaleira
    Já quase no clariá o dia
    Meu pingo de arreio
    Relincha na estrebaria
    Enquanto uma saracura
    Vai cantando empoleirada
                                        
        """)


if __name__ == '__main__':
    # -> 'sino' apenas soa o sino da escola
    # -> 'musica' apenas soa uma música da pasta de músicas (aleatoriamente)
    # -> 'padrao' ou sem parametro executa o programa 
    #    para soar os sinos de acordo com a agenda (horarios.ini)
    # -> 'baitaca' toca apenas trecho de "Do Fundo da Grota" do Baitaca. 
    #    (uso de acordo com a lei na L9610, no Cap. IV, Art. 46)
    param = sys.argv[1] if len(sys.argv) > 1 else 'padrao'
    pysino = Pysino()
        
    if param in ('sino', 'musica', 'baitaca'):
        pysino.tipo = param
        if param == 'baitaca':
            baitaca()
        pysino.tocar()
    else:
        pysino.executar()
    print("""
        -----------------------------------------------------
                         Concluído!
        -----------------------------------------------------
    """)