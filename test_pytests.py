from intership import *

class TestClass(object):
    def setup(self):
        self.our_data = TasksOnOurData('voivodeships')
        my_file = Path(r'SQLite/file.db')
        if not my_file.is_file():
            self.our_data.reading_file()
        #self.our_data.printing_info()
        self.our_data.main_for_sql_data()
        
    def test_data_file(self):
        my_file = Path(r'SQLite/file.db')
        if not my_file.is_file():
            proper_len = 613
            assert len(self.our_data.data_in_file) == proper_len
        else: assert my_file.is_file() == True
            
    def test_take_argument(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda x: 'Śląskie 2015 M')
        assert self.our_data.take_argument() == ['Śląskie', '2015', 'Mężczyźni']
    
    def test_get_only_number_of_people(self):
        arg = ['Dolnośląskie', 'Zdało', 'Mężczyźni', '2011', '7090']
        ans = 7090
        assert self.our_data.get_only_number_of_people(arg) == ans
        
    def test_get_specific_information(self):
        arg = ['Pomorskie', '2015', 'Przystąpiło', 'Mężczyźni'] 
        ans = ['Pomorskie', 'Przystąpiło', 'Mężczyźni', '2015', '7054']
        assert self.our_data.get_specific_information(*arg) == ans
        
    def test_average_participation(self, monkeypatch, capfd): #Done by Excel
        monkeypatch.setattr('builtins.input', lambda x: 'Pomorskie 2015 F')
        self.our_data.average_participation()
        out, err = capfd.readouterr()
        assert out == 'Number of people who participated in Pomorskie in 2015 year: 8910\n'
    
    def test_procentage_pass_rate_for_specific_year(self): #Done by Calculator
        assert self.our_data.procentage_pass_rate_for_specific_year() ==  81.6533893049659
        assert f"{self.our_data.procentage_pass_rate_for_specific_year('Both', 'Pomorskie', '2015'):.8f}" == '73.20846906'
        
    def test_procentage_pass_rate_thru_years(self):
        assert self.our_data.procentage_pass_rate_thru_years() == {2010: 81.60509656222453, 2011: 76.39889196675901, 2012: 80.5654166397728, 2013: 80.92578354665099, 2014: 71.28119956022363, 2015: 74.80350665054414, 2016: 81.50925335035099, 2017: 80.3309604759881, 2018: 81.18329089234437}
        assert self.our_data.procentage_pass_rate_thru_years('Both', 'Pomorskie') == {2010: 81.6533893049659, 2011: 74.60350260887535, 2012: 80.29719616031238, 2013: 80.80318997436628, 2014: 71.03486037598103, 2015: 73.2084690553746, 2016: 79.45347630577655, 2017: 78.11701412239408, 2018: 77.43526510480888}

    def test_procentage_pass_rate(self, monkeypatch, capfd):
        monkeypatch.setattr('builtins.input', lambda x: 'Pomorskie')
        self.our_data.procentage_pass_rate()
        out, err = capfd.readouterr()
        assert out == 'In 2010: 81.65%\nIn 2011: 74.60%\nIn 2012: 80.30%\nIn 2013: 80.80%\nIn 2014: 71.03%\nIn 2015: 73.21%\nIn 2016: 79.45%\nIn 2017: 78.12%\nIn 2018: 77.44%\n'
    
    def test_procentage_pass_rate_two(self, monkeypatch, capfd):
        monkeypatch.setattr('builtins.input', lambda x: 'Pomorskie F')
        self.our_data.procentage_pass_rate()
        out, err = capfd.readouterr()
        assert out == 'In 2010: 81.62%\nIn 2011: 73.43%\nIn 2012: 79.97%\nIn 2013: 80.84%\nIn 2014: 70.60%\nIn 2015: 72.14%\nIn 2016: 79.02%\nIn 2017: 77.85%\nIn 2018: 77.31%\n'

    def test_best_voivodeship_in_year(self, monkeypatch, capfd):
        monkeypatch.setattr('builtins.input', lambda x: '2015')
        self.our_data.best_voivodeship_in_year()
        out, err = capfd.readouterr()
        assert out == 'Małopolskie\n'
        
    def test_looking_for_regress(self, monkeypatch, capfd):
        monkeypatch.setattr('builtins.input', lambda x: '')
        self.our_data.looking_for_regress()
        out, err = capfd.readouterr()
        assert out == '''In 2014 there was a regress in: Małopolskie, Wielkopolskie, Pomorskie, Podkarpackie, Warmińsko-Mazurskie, Lubelskie, Świętokrzyskie, Opolskie, Śląskie, Lubuskie, Dolnośląskie, Kujawsko-Pomorskie, Zachodniopomorskie, Łódzkie, Mazowieckie, Podlaskie
In 2011 there was a regress in: Małopolskie, Wielkopolskie, Pomorskie, Podkarpackie, Warmińsko-Mazurskie, Lubelskie, Świętokrzyskie, Opolskie, Śląskie, Lubuskie, Dolnośląskie, Kujawsko-Pomorskie, Zachodniopomorskie, Łódzkie, Mazowieckie, Podlaskie
In 2017 there was a regress in: Wielkopolskie, Pomorskie, Podkarpackie, Warmińsko-Mazurskie, Lubelskie, Świętokrzyskie, Opolskie, Śląskie, Lubuskie, Dolnośląskie, Kujawsko-Pomorskie, Zachodniopomorskie, Łódzkie, Mazowieckie, Podlaskie
In 2018 there was a regress in: Pomorskie, Lubuskie, Łódzkie\n'''
        
    def test_compare_two_voivodeship(self, monkeypatch, capfd):
        monkeypatch.setattr('builtins.input', lambda x: 'Pomorskie Śląskie')
        self.our_data.compare_two_voivodeship()
        out, err = capfd.readouterr()
        assert out == '''In 2010: Śląskie
In 2011: Śląskie
In 2012: Śląskie
In 2013: Śląskie
In 2014: Pomorskie
In 2015: Śląskie
In 2016: Pomorskie
In 2017: Pomorskie
In 2018: Śląskie\n'''
        
    