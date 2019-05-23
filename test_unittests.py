import unittest
from intership import *
from unittest.mock import patch
from io import StringIO

class OurDataTests(unittest.TestCase):
    def setUp(self):
        self.our_data = OurData('voivodeships')
        my_file = Path(r'file.db')
        if not my_file.is_file():
            self.our_data.reading_file()
        self.our_data.main_for_sql_data()
        
    def test_data_file(self):
        '''Checks if data_file was fully loaded to variable'''
        my_file = Path(r'file.db')
        if not my_file.is_file():
            proper_len = 613
            self.assertEqual(len(self.our_data.data_in_file), proper_len, 'Wrong len of file')
                    
    def run_test_ir(self, given_answer, expected_out):
        '''Function to test input and expected return'''
        with patch('builtins.input',return_value = given_answer), patch('sys.stdout', new=StringIO()) as fake_out:
            self.assertEqual(self.our_data.take_argument(fake_out.getvalue().strip()), expected_out)
            
    def test_take_argument(self):
        self.run_test_ir('Pomorskie 2015', ['Pomorskie', '2015', 'Both'])
        self.run_test_ir('Pomorskie 2015 F', ['Pomorskie', '2015', 'Kobiety'])
        self.run_test_ir('Pomorskie 2015 M', ['Pomorskie', '2015', 'Mężczyźni'])
        self.run_test_ir('Śląskie 2015 M', ['Śląskie', '2015', 'Mężczyźni'])
        
    def test_get_only_number_of_people(self):
        arg = ['Polska', 'Przystąpiło', 'Kobiety', '2011', '192840']
        ans = 192840
        self.assertEqual(self.our_data.get_only_number_of_people(arg), ans, 'Wrong number of people')
        arg = ['Dolnośląskie', 'Zdało', 'Mężczyźni', '2011', '7090']
        ans = 7090
        self.assertEqual(self.our_data.get_only_number_of_people(arg), ans, 'Wrong number of people')
        
    def test_get_specific_information(self):
        arg = ['Pomorskie', '2015', 'Przystąpiło', 'Mężczyźni'] 
        ans = ['Pomorskie', 'Przystąpiło', 'Mężczyźni', '2015', '7054']
        self.assertEqual(self.our_data.get_specific_information(*arg), ans)
        arg = ['Polska', '2011', 'Przystąpiło', 'Kobiety'] 
        ans = ['Polska', 'Przystąpiło', 'Kobiety', '2011', '192840']
        self.assertEqual(self.our_data.get_specific_information(*arg), ans)
        
class TasksOnOurDataTests(unittest.TestCase):
    def setUp(self):
        self.our_data = TasksOnOurData('voivodeships')
        my_file = Path(r'file.db')
        if not my_file.is_file():
            self.our_data.reading_file()
        self.our_data.main_for_sql_data()

    def run_test_average_participation(self, given_answer, expected_out):
        with patch('builtins.input', return_value=given_answer), patch('sys.stdout', new=StringIO()) as fake_out:
            self.our_data.average_participation()
            self.assertEqual(fake_out.getvalue().strip(), expected_out)

    def test_average_participation(self):
        self.run_test_average_participation('Pomorskie 2015', 'Number of people who participated in Pomorskie in 2015 year: 15964')
        self.run_test_average_participation('Pomorskie 2015 F', 'Number of people who participated in Pomorskie in 2015 year: 8910')
        
    def test_procentage_pass_rate_for_specific_year(self):
        self.assertEqual(self.our_data.procentage_pass_rate_for_specific_year(), 81.6533893049659)
        self.assertEqual(f"{self.our_data.procentage_pass_rate_for_specific_year('Both', 'Pomorskie', '2015'):.8f}", '73.20846906')
        
    def test_procentage_pass_rate_thru_years(self):
        self.assertEqual(self.our_data.procentage_pass_rate_thru_years(), {2010: 81.60509656222453, 2011: 76.39889196675901, 2012: 80.5654166397728, 2013: 80.92578354665099, 2014: 71.28119956022363, 2015: 74.80350665054414, 2016: 81.50925335035099, 2017: 80.3309604759881, 2018: 81.18329089234437})
        self.assertEqual(self.our_data.procentage_pass_rate_thru_years('Both', 'Pomorskie'), {2010: 81.6533893049659, 2011: 74.60350260887535, 2012: 80.29719616031238, 2013: 80.80318997436628, 2014: 71.03486037598103, 2015: 73.2084690553746, 2016: 79.45347630577655, 2017: 78.11701412239408, 2018: 77.43526510480888})

    def run_test_procentage_pass_rate(self, given_answer, expected_out):
        with patch('builtins.input', return_value=given_answer), patch('sys.stdout', new=StringIO()) as fake_out:
            self.our_data.procentage_pass_rate()
            self.assertEqual(fake_out.getvalue().strip(), expected_out)

    def test_procentage_pass_rate(self):
        self.run_test_procentage_pass_rate('Pomorskie', 'In 2010: 81.65%\nIn 2011: 74.60%\nIn 2012: 80.30%\nIn 2013: 80.80%\nIn 2014: 71.03%\nIn 2015: 73.21%\nIn 2016: 79.45%\nIn 2017: 78.12%\nIn 2018: 77.44%')
        self.run_test_procentage_pass_rate('Pomorskie F', 'In 2010: 81.62%\nIn 2011: 73.43%\nIn 2012: 79.97%\nIn 2013: 80.84%\nIn 2014: 70.60%\nIn 2015: 72.14%\nIn 2016: 79.02%\nIn 2017: 77.85%\nIn 2018: 77.31%')
 
    def run_test_best_voivodeship_in_year(self, given_answer, expected_out):
        with patch('builtins.input', return_value=given_answer), patch('sys.stdout', new=StringIO()) as fake_out:
            self.our_data.best_voivodeship_in_year()
            self.assertEqual(fake_out.getvalue().strip(), expected_out)
    
    def test_best_voivodeship_in_year(self):
        self.run_test_best_voivodeship_in_year('2015', 'Małopolskie')
        
    def run_test_looking_for_regress(self, given_answer, expected_out):
        with patch('builtins.input', return_value=given_answer), patch('sys.stdout', new=StringIO()) as fake_out:
            self.our_data.looking_for_regress()
            self.assertEqual(fake_out.getvalue().strip(), expected_out)
        
    def test_looking_for_regress(self):
        self.run_test_looking_for_regress('', '''In 2014 there was a regress in: Małopolskie, Wielkopolskie, Pomorskie, Podkarpackie, Warmińsko-Mazurskie, Lubelskie, Świętokrzyskie, Opolskie, Śląskie, Lubuskie, Dolnośląskie, Kujawsko-Pomorskie, Zachodniopomorskie, Łódzkie, Mazowieckie, Podlaskie
In 2011 there was a regress in: Małopolskie, Wielkopolskie, Pomorskie, Podkarpackie, Warmińsko-Mazurskie, Lubelskie, Świętokrzyskie, Opolskie, Śląskie, Lubuskie, Dolnośląskie, Kujawsko-Pomorskie, Zachodniopomorskie, Łódzkie, Mazowieckie, Podlaskie
In 2017 there was a regress in: Wielkopolskie, Pomorskie, Podkarpackie, Warmińsko-Mazurskie, Lubelskie, Świętokrzyskie, Opolskie, Śląskie, Lubuskie, Dolnośląskie, Kujawsko-Pomorskie, Zachodniopomorskie, Łódzkie, Mazowieckie, Podlaskie
In 2018 there was a regress in: Pomorskie, Lubuskie, Łódzkie''')
        
    def run_test_compare_two_voivodeship(self, given_answer, expected_out):
        with patch('builtins.input', return_value=given_answer), patch('sys.stdout', new=StringIO()) as fake_out:
            self.our_data.compare_two_voivodeship()
            self.assertEqual(fake_out.getvalue().strip(), expected_out)
        
    def test_compare_two_voivodeship(self):
        self.run_test_compare_two_voivodeship('Pomorskie Śląskie', '''In 2010: Śląskie
In 2011: Śląskie
In 2012: Śląskie
In 2013: Śląskie
In 2014: Pomorskie
In 2015: Śląskie
In 2016: Pomorskie
In 2017: Pomorskie
In 2018: Śląskie''')
 
def suite_for_ourdata():
    suite = unittest.TestSuite()
    suite.addTest(OurDataTests('test_data_file'))
    suite.addTest(OurDataTests('test_take_argument'))
    suite.addTest(OurDataTests('test_get_only_number_of_people'))
    suite.addTest(OurDataTests('test_get_specific_information'))
    return suite

def suite_for_tasks_on_our_data():
    suite = unittest.TestSuite()
    suite.addTest(TasksOnOurDataTests('test_average_participation'))
    suite.addTest(TasksOnOurDataTests('test_procentage_pass_rate_for_specific_year'))
    suite.addTest(TasksOnOurDataTests('test_procentage_pass_rate_thru_years'))
    suite.addTest(TasksOnOurDataTests('test_procentage_pass_rate'))
    suite.addTest(TasksOnOurDataTests('test_best_voivodeship_in_year'))
    suite.addTest(TasksOnOurDataTests('test_looking_for_regress'))
    suite.addTest(TasksOnOurDataTests('test_compare_two_voivodeship'))
  
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite_for_ourdata())
    runner.run(suite_for_tasks_on_our_data())
    
    