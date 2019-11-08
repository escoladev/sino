import unittest
import pysino
import datetime

class TestPysino(unittest.TestCase):
    
    def test_comparar_data(self):
        date_time_str = '2018-06-29 08:15:27.243860'
        date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')
        data_str = '08:15'
        self.assertEqual(pysino.comparar_data(data_str, date_time_obj), 0)
        data_str = '08:16'
        self.assertEqual(pysino.comparar_data(data_str, date_time_obj), 1)
        data_str = '08:14'
        self.assertEqual(pysino.comparar_data(data_str, date_time_obj), -1)
        data_str = '09:15'
        self.assertEqual(pysino.comparar_data(data_str, date_time_obj), 1)
        data_str = '09:16'
        self.assertEqual(pysino.comparar_data(data_str, date_time_obj), 1)
        data_str = '09:14'
        self.assertEqual(pysino.comparar_data(data_str, date_time_obj), 1)
        data_str = '07:15'
        self.assertEqual(pysino.comparar_data(data_str, date_time_obj), -1)
        data_str = '07:16'
        self.assertEqual(pysino.comparar_data(data_str, date_time_obj), -1)
        data_str = '07:14'
        self.assertEqual(pysino.comparar_data(data_str, date_time_obj), -1)

    def test_dia_hoje(self):
        hr = datetime.datetime.now()
        dia = hr.strftime("%A")
        
        dias = {
        'Monday': 'segunda',
        'Tuesday': 'terca',
        'Wednesday': 'quarta',
        'Thursday': 'quinta',
        'Friday': 'sexta'
        }

        self.assertEqual(pysino.dia_hoje(), dias[dia])
        # dia que não xiste
        resultado = dias['macaco'] if 'macaco' in dias else 'sexta'
        self.assertEqual(resultado, 'sexta')



  
if __name__ == '__main__':
    unittest.main()