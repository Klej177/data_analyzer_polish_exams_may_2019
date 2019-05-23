'''
@author: Kamil Kleina
Zadanie

Na stronie https://dane.gov.pl/dataset/1534/resource/17201 można znaleźć dane dotyczące liczby osób, które przystąpiły oraz zdały maturę w latach 2010-2018 z uwzględnieniem podziału na województwo oraz płeć.

Zadanie polega na napisaniu skryptu, który umożliwiłby przeanalizowanie danych i znalezienie odpowiedzi na następujące pytania:

1) obliczenie średniej liczby osób, które przystąpiły do egzaminu dla danego województwa w danym roku, np.

2015 - 123456

2) obliczenie procentowej zdawalności dla danego województwa na przestrzeni lat, np.

2010 - 50 %
2011 - 52 %
2012 - 57 %
itd. ...
3) podanie województwa o najlepszej zdawalności w konkretnym roku, np.

rok - województwo A

4) wykrycie województw, które zanotowały regresję (mniejszy współczynnik zdawalności w kolejnym roku), jeżeli takowe znajdują się w zbiorze, np.

województwo A: 2012 -> 2013
województwo B: 2017 -> 2018

5) porównanie dwóch województw - dla podanych dwóch województw wypisanie, które z województw miało lepszą zdawalność w każdym dostępnym roku, np. przy porównaniu województwa A i B

2010 - A
2011 - B
2012 - B
2013 - A
itd. ...

Zaprojektowanie interfejsu linii poleceń to część tego zadania. Każdy z tych punktów powinien być zrealizowany jako osobna komenda wywoływana z tego samego skryptu. Dodatkowo dla każdej z komend powinny być dostępne filtry:
- osoby bez rozróżnienia na płeć (domyślny, jeżeli użytkownik nie podał inaczej)
- tylko kobiety
- tylko mężczyźni

Wymagania techniczne:

- Python 3.7
- wykorzystanie tylko modułów dostępnych w standardowej bibliotece (nie dotyczy zadań bonusowych)
- README z opisem jak postawić projekt oraz spisem dostępnych komend
- testy jednostkowe z użyciem pytest
- kod napisany obiektowo
- (bonus) pobieranie danych z API lub pliku znajdującego się na serwerze, zamiast pliku lokalnego
- (bonus) napisanie skryptu, który jednorazowo wgrywałby dane do bazy danych (sqlite) oraz pobieranie ich z bazy przy wywołaniu komend

Prośba o umieszczenie rozwiązania w publicznie dostępnym repozytorium systemu kontroli wersji git (github, bitbucket, gitlab itp.)
'''

import csv #standard library
import sys #standard library
import collections #standard library
import urllib.request #first bonus to read file
import requests #first bonus checks if site is working
import codecs #first bonus faster reading file from server
import json
import sqlite3 #second bonus
from sqlite3 import Error #second bonus
from pathlib import Path #second bonus

class OurData():
    '''Class for csv file'''
    def __init__(self, name):
        self.name = name

    def get_voivodeships(self): #It's a function not a constant, since in data is also Poland so maybe in different tasks we need add/remove some voivodeships 
        '''Function to return all voivodeships in Poland as dict'''
        self.voivodeships = ('Małopolskie', 'Wielkopolskie', 'Pomorskie', 'Podkarpackie', 
                  'Warmińsko-Mazurskie', 'Lubelskie', 'Świętokrzyskie', 'Opolskie',
                  'Śląskie', 'Lubuskie', 'Dolnośląskie', 'Kujawsko-Pomorskie', 
                  'Zachodniopomorskie', 'Łódzkie', 'Mazowieckie', 'Podlaskie')
        return self.voivodeships

    def reading_data_from_api(self):
        '''Function to read data from API'''
        self.data_in_file = [['Terytorium', 'przystapiło/zdało', 'Płeć', 'Rok', 'Liczba osób']]
        for num in range(1, 32):
            link = "http://api.dane.gov.pl/resources/17363/data?page=" + str(num)
            response = requests.get(link)
            data = response.json()
            for elem in data['data']:
                l = (list(elem['attributes'].values()))
                self.data_in_file.append([l[2].title(), l[3].title(), l[4].title(), str(int(l[0])), str(int(l[1]))])
        return self.data_in_file

    def reading_file_from_server(self, url = 'https://gist.githubusercontent.com/Klej177/f886d589761c9b85b431c3476be9ee78/raw/6569363bac54afc96f28ee04d07c9f4f07b07d3c/data_server.csv'):
        '''Function to read cvs file from a server'''
        self.url = url
        response = requests.get(self.url)
        assert response.status_code < 400
        self.ftpstream = urllib.request.urlopen(self.url)
        self.csv_reader = csv.reader(codecs.iterdecode(self.ftpstream, 'utf-8'), delimiter=',')
        self.data_in_file = []
        for row in self.csv_reader:
            self.data_in_file.append(row[0].title().split(';'))
        return self.data_in_file
    
    def reading_file_from_disk(self, file_name = 'data.csv'):
        '''Function to read cvs file from a disk'''
        self.file_name = file_name
        with open(self.file_name, encoding='utf-8') as self.csv_file:
            self.csv_reader = csv.reader(self.csv_file, delimiter=',')
            self.data_in_file = []
            for row in self.csv_reader:
                self.data_in_file.append(row[0].title().split(';'))
        return self.data_in_file

    def reading_file(self):
        '''Function to get data from api>disk>server'''
        try:
            print("Reading data from API. Wait a sec.")
            self.reading_data_from_api()
        except:
            print("Reading data from API failed.\nTrying file from on server.")
            try:
                self.reading_file_from_server()
            except:
                print("Reading data from Server failed.\nReading from Disk.")
                self.reading_file_from_disk()
            finally:
                if len(self.data_in_file) == 613:
                    print("Success")
                else: print("All 3 has failed.")  
        return None
                
    def create_connection(self):
        '''Function to create connection with our data base in SQL'''
        self.db_file = 'file.db'
        try:
            self.conn = sqlite3.connect(self.db_file)
        except Error as e:
            print(e)
        return None
    
    def create_table(self, create_table_sql):
        '''Function to create new table in our SQL Database'''
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)
        return None
            
    def main_creating_table(self):
        '''Main function for creating table in our SQL database'''
        self.create_connection()
        sql_create_voivodeships_table = """ CREATE TABLE IF NOT EXISTS voivodeships(
                                        voivodeship text,
                                        participated_passed text NOT NULL,
                                        gender text,
                                        year text,
                                        number_of_people text
                                    ); """
        if self.conn is not None:
            self.create_table(sql_create_voivodeships_table)
        else:
            print("Error! cannot create the database connection.")
        return None

    def insert_data(self, project):
        '''Function to instert data in SQL Table'''
        sql = ''' INSERT INTO voivodeships(voivodeship, participated_passed, gender, year, number_of_people)
              VALUES(?,?,?,?,?) '''
        cur = self.conn.cursor()
        cur.execute(sql, project)
        return None
            
    def get_specific_information(self, voivodeship = 'Pomorskie', year = '2010',
                                participated_passed = 'Przystąpiło', gender = 'Mężczyźni'): #get specific information new
        '''Function to get specific information from our data based on specific arguments'''
        self.create_connection()
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM voivodeships WHERE voivodeship=? and participated_passed = ? and gender = ? and year = ?",
                     (voivodeship, participated_passed, gender, year))
        rows = cur.fetchall()
        self.conn.close()
        return list(rows[0])
        #return [elem for elem in self.data_in_file if voivodeship in elem and voivodeship_year in elem and type_of_participation in elem and gender in elem][0] while database doesn't work
    
    
    def take_argument(self, text='Write a word: '):
        '''Function to take input from user and to process it'''
        users_words = (input(text)).title().split()
        if len(users_words) == 0: users_words.append('Both') 
        elif users_words[-1] != 'F' and users_words[-1] != 'M' and users_words[-1] != 'Both': users_words.append('Both')
        elif users_words[-1] == 'F': users_words[-1] = 'Kobiety'
        elif users_words[-1] == 'M': users_words[-1] = 'Mężczyźni' 
        return users_words
    
    def main_inserting_data(self):
        '''Main function to put all the data in sql database'''
        with self.conn:
            for line in self.data_in_file:
                project = (line[0], line[1], line[2], line[3], line[4]);
                self.insert_data(project)
        self.conn.close()
        return None

    def main_for_sql_data(self):
        '''Main function for SQL stuff'''
        my_file = Path(r'file.db')
        if not my_file.is_file():
            self.main_creating_table()
            self.main_inserting_data()
        else:
            pass
        return None
    
    def get_only_number_of_people(self, one_row):
        '''Function to get only year as a integer'''
        return int(one_row[-1])
    
class TasksOnOurData(OurData): #Two class so it cannot regress 
    '''Class do to tasks on our data'''
    def __init__(self, name):
        super().__init__(name)
    
    #task1
    def average_participation(self, gender_to_check = 'Both'):
        '''Function to show average participation of people in specific voivodeship'''
        voivodeship_to_check, voivodeship_year_to_check, gender_to_check = self.take_argument("Write a voivodeship year gender(optional F/M): ")
        ans = 0
        if gender_to_check == 'Both':
            ans += self.get_only_number_of_people(self.get_specific_information(voivodeship_to_check, voivodeship_year_to_check, 'Przystąpiło', gender = 'Mężczyźni'))
            ans += self.get_only_number_of_people(self.get_specific_information(voivodeship_to_check, voivodeship_year_to_check, 'Przystąpiło', gender = 'Kobiety'))
        elif gender_to_check != 'Both':
            ans += self.get_only_number_of_people(self.get_specific_information(voivodeship_to_check, voivodeship_year_to_check, 'Przystąpiło', gender = gender_to_check))
        else: print('Something went wrong.')
        print(f'Number of people who participated in {voivodeship_to_check} in {voivodeship_year_to_check} year: {ans}')
        #return f'Number of people who participated in {voivodeship_to_check} in {voivodeship_year_to_check} year: {ans}'
        return None

    def procentage_pass_rate_for_specific_year(self, gender_to_check = 'Both', voivodeship_to_calculate = 'Pomorskie', year_to_check = '2010'):
        '''Function to calculate of procentage of pass rate in specific voivodeship in specific year'''
        participant, participant_who_passed = 0, 0 
        if gender_to_check == 'Both':
            participant += self.get_only_number_of_people(self.get_specific_information(voivodeship_to_calculate, str(year_to_check)))
            participant += self.get_only_number_of_people(self.get_specific_information(voivodeship_to_calculate, str(year_to_check), gender = 'Kobiety'))
            participant_who_passed += self.get_only_number_of_people(self.get_specific_information(voivodeship_to_calculate, str(year_to_check), 'Zdało'))
            participant_who_passed += self.get_only_number_of_people(self.get_specific_information(voivodeship_to_calculate, str(year_to_check), 'Zdało', 'Kobiety'))
        elif gender_to_check != 'Both':
            participant += self.get_only_number_of_people(self.get_specific_information(voivodeship_to_calculate, str(year_to_check), gender = gender_to_check))
            participant_who_passed += self.get_only_number_of_people(self.get_specific_information(voivodeship_to_calculate, str(year_to_check), 'Zdało', gender_to_check))
        else:
            print("Something went wrong.")
        return (participant_who_passed/participant) * 100
    
    def procentage_pass_rate_thru_years(self, gender_to_check = 'Both', voivodeship_to_calculate = 'Mazowieckie'):
        '''Function to calculate procentage of pass rate in specific voivodeship thru years'''
        dict_year_people = {}
        last_year_to_check = 2018 #in case there added new years in data
        for year in range(2010, last_year_to_check+1):
            dict_year_people[year] = self.procentage_pass_rate_for_specific_year(year_to_check = str(year), gender_to_check = gender_to_check, voivodeship_to_calculate = voivodeship_to_calculate)
        return dict_year_people
    
    #task 2
    def procentage_pass_rate(self):
        '''Function to print pass rate in specific voivodeship thru years'''
        voivodeship_to_calculate, gender_to_check = self.take_argument("Write a voivodeship gender(optional F/M): ")
        dict_year_people = self.procentage_pass_rate_thru_years(gender_to_check, voivodeship_to_calculate)
        for key, value in dict_year_people.items():
            print(f'In {key}: {value:.2f}%')
        #return dict_year_people
        return None
    
    #task 3
    def best_voivodeship_in_year(self, gender_to_check = 'Both', year = 2015):
        '''Function to check best voivodeship in specific year'''
        voivodeships = self.get_voivodeships()
        year, gender_to_check = self.take_argument("Write a year gender(optional F/M): ")
        dict_year_people = {}
        for voivodeship in voivodeships:
            dict_year_people[voivodeship] = self.procentage_pass_rate_for_specific_year(year_to_check = str(year), gender_to_check = gender_to_check, voivodeship_to_calculate = voivodeship)
        print(max(dict_year_people, key=dict_year_people.get))
        #return max(dict_year_people, key=dict_year_people.get)
        return None
        
    #task 4
    def looking_for_regress(self):
        '''Function to check for regress in each voivodeship thru years'''
        voivodeships = self.get_voivodeships()
        dict_regres = collections.defaultdict(list)
        gender_to_check = self.take_argument("Write a gender F/M or leave empty for F+M): ")
        for voivodeship in voivodeships:
            dict_thru_years = self.procentage_pass_rate_thru_years(gender_to_check = gender_to_check[0], voivodeship_to_calculate = voivodeship)
            list_thru_years = list(dict_thru_years.keys())[1:] #remove first year since there is nothing to compare it with
            for year in reversed(list_thru_years):
                if dict_thru_years[year] < dict_thru_years[year-1]:
                    dict_regres[year].append(voivodeship)
        for key, value in dict_regres.items():
            print(f"In {key} there was a regress in: {', '.join(value)}")
        #return dict_regres
        return None
    
    #task 5
    def compare_two_voivodeship(self):
        '''Function to compare 2 voivodeship thru years'''
        voivodeship_one, voivodeship_two, gender_to_check = self.take_argument("Write a voivodeship1 voivodeship2 gender(optional F/M): ")
        dict_one = self.procentage_pass_rate_thru_years(gender_to_check, voivodeship_one)
        dict_two = self.procentage_pass_rate_thru_years(gender_to_check, voivodeship_two)
        dict_with_ans = {}
        for key in dict_one:
            if dict_one[key] > dict_two[key]:
                print(f'In {key}: {voivodeship_one}')
                dict_with_ans[key] = dict_one
            elif dict_one[key] < dict_two[key]:
                print(f'In {key}: {voivodeship_two}')
                dict_with_ans[key] = dict_two
            elif dict_one[key] == dict_two[key]:
                print(f'In {key}: They both had the same result.')
                dict_with_ans[key] = 'Same result'
            else:
                print("Something went wrong")
        #return dict_with_ans
        return None
    
    def printing_info(self):
        '''Function to print info about how program works and user's choices'''
        self.info = f"""Tasks to choose:
1: {self.average_participation.__doc__}
2: {self.procentage_pass_rate.__doc__}
3: {self.best_voivodeship_in_year.__doc__}
4: {self.looking_for_regress.__doc__}
5: {self.compare_two_voivodeship.__doc__}
 Voivodeships you can check:
  {', '.join(self.get_voivodeships())}.
 Genders you can check: Males, Females, Mixed"""
        print(self.info)
        #return self.info
        return None
        
    
def data_program():
    our_data = TasksOnOurData('voivodeships')
    my_file = Path(r'file.db')
    if not my_file.is_file():
        our_data.reading_file()
    our_data.printing_info()
    our_data.main_for_sql_data()
    choice = 0
    while choice != 'exit':
        choice = input("Your choice (1,2,3,4,5) or exit: ")
        if choice == '1': our_data.average_participation()
        elif choice == '2': our_data.procentage_pass_rate()
        elif choice == '3': our_data.best_voivodeship_in_year()
        elif choice == '4': our_data.looking_for_regress()
        elif choice == '5': our_data.compare_two_voivodeship()
        elif choice == 'exit': sys.exit(0)
        else: print('Wrong choice')
        print()
    return None
    
     
if __name__ == "__main__":
    try:
        data_program()
    except SystemExit:
        print("Goodbye")
    except:
        print("Wrong input")