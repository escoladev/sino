# pysino


pysino é um pequeno programa que ajuda no controle do sino
da escola.

Na nossa escola, cada sino tocado para a troca das salas
é executado no nosso sistema de som.

Na volta dos intervalos soa um sino, enquanto nas trocas
de sala soa uma música (escolhida de maneira aleatória).

Com esse pequeno programa escrito em Python, podemos
configurar através do arquivo ```horarios.ini```
alguns parâmetros, como:

```
[configuracao]
sinoPadrao = caminho até o arquivo .mp3 do sino
pastaPadrao = caminho até a pasta onde tem as músicas
tempoMusica = 50  
```

e

```
[segunda]
horarioMusica = os horários no formato(hora:minuto) que tocará música, separados por vígula
horarioSinoPadrao = os horários formato(hora:minuto) que tocará sino, separados por vírgula
```

## dependência

Esse programa requer a biblioteca: [pydub](https://github.com/jiaaro/pydub) instalada e as libs para se usar o playback (veja na página do github da lib).
Observação: formato de aúdio, apenas **.mp3**




***Feito com :heart: para a Escola Padre Constantino de Monte - Maracaju/MS***

*Jhonathan P. Banczek*