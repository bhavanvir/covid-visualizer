from datetime import datetime
from termcolor import colored
from PyInquirer import style_from_dict, Token, prompt, Separator
import pandas as pd
import os
import colorama

colorama.init()

global style 
style = style_from_dict({
    Token.Separator: '#0000ff',
    Token.QuestionMark: '',
    Token.Selected: '#0000ff',
    Token.Pointer: '#0000ff bold',
    Token.Instruction: '',
    Token.Answer: '#0000ff bold',
    Token.Question: '',
})

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_date_list(start, end):
    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")
    if start_date > end_date:
        return pd.date_range(end, start).strftime("%Y-%m-%d").tolist()
    elif start_date < end_date: 
        return pd.date_range(start, end).strftime("%Y-%m-%d").tolist()

def validate_format(date):
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("Error: specified date is not in the correct format (YYYY-MM-DD).\n")
        get_dates()

def get_dates():
    start = input("Enter start date (YYYY-MM-DD): ")
    validate_format(start)
    end = input("Enter end date (YYYY-MM-DD): ")
    validate_format(end)

    return start, end

def get_data(date_list):
    pass

def get_loc(province_codes):
    questions = [
        {
            'type': 'checkbox',
            'qmark': '•',
            'message': 'Please select a province:',
            'name': 'province',
            'choices': [
                {
                    'name': 'Alberta',
                },
                {
                    'name': 'British Columbia',
                },
                {
                    'name': 'Manitoba',
                },
                {
                    'name': 'New Brunswick',
                },
                {
                    'name': 'Newfoundland and Labrador',
                },
                {
                    'name': 'Northwest Territories',
                },
                {
                    'name': 'Nova Scotia',
                },
                {
                    'name': 'Nunavut',
                },
                {
                    'name': 'Ontario',
                },
                {
                    'name': 'Prince Edward Island',
                },
                {
                    'name': 'Quebec',
                },
                {
                    'name': 'Saskatchewan',
                },
                {
                    'name': 'Yukon',
                },
            ],
        }
    ]
    try:
        answers = prompt(questions, style=style)
        answers['province'][0]
        codes = []
        for province in answers['province']:
            codes.append(province_codes[province])
        return codes
    except IndexError:
        print(colored('Error: you must select at least one province.\n', 'red'))
        return get_loc(province_codes)

def get_stat():
    questions = [
        {
            'type': 'checkbox',
            'qmark': '•',
            'message': 'Please select a statistic:',
            'name': 'statistic',
            'choices': [
                Separator('Cases'),
                {
                    'name': 'Cases',
                },
                {
                    'name': 'Cases Daily',
                },
                Separator('Deaths'),
                {
                    'name': 'Deaths',
                },
                {
                    'name': 'Deaths Daily',
                },
                Separator('Hospitalizations'),
                {
                    'name': 'Hospitalizations',
                },
                {
                    'name': 'Hospitalizations Daily',
                },
                Separator('Tests'),
                {
                    'name': 'Tests Completed',
                },
                {
                    'name': 'Tests Completed Daily',
                },
                Separator('Vaccine Administration'),
                {
                    'name': 'Vaccine Administration Dose 1',
                },
                {
                    'name': 'Vaccine Administration Dose 2',
                },
                {
                    'name': 'Vaccine Administration Dose 3',
                },
                {
                    'name': 'Vaccine Administration Total Doses',
                }
            ],
        }
    ]
    try:
        answers = prompt(questions, style=style)
        answers['statistic'][0]
        return answers['statistic']
    except IndexError:
        cls()
        print(colored('Error: you must select at least one statistic.\n', 'red'))
        return get_stat()

def main():
    province_codes = {
        "Alberta": "AB",
        "British Columbia": "BC",
        "Manitoba": "MB",
        "New Brunswick": "NB",
        "Newfoundland and Labrador": "NL",
        "Nova Scotia": "NS",
        "Ontario": "ON",
        "Prince Edward Island": "PE",
        "Quebec": "QC",
        "Saskatchewan": "SK",
        "Northwest Territories": "NT",
        "Nunavut": "NU",
        "Yukon": "YT"
    }

    start, end = get_dates()
    dates = get_date_list(start, end)
    print(dates)

if __name__ == "__main__":
    main()