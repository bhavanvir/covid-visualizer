from datetime import datetime
from termcolor import colored
from PyInquirer import style_from_dict, Token, prompt
from matplotlib import pyplot as plt, ticker
from pyfiglet import Figlet
import requests
import re
import pandas as pd
import os
import colorama

colorama.init()

global style 
style = style_from_dict({
    Token.Separator: '#00FFFF',
    Token.QuestionMark: '',
    Token.Selected: '#00FFFF',
    Token.Pointer: '#00FFFF bold',
    Token.Instruction: '',
    Token.Answer: '',
    Token.Question: '',
})

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def find_local(x, y, desc):
    x_cord, y_cord = [], []

    for x_pos, y_pos in zip(x, y):
        if desc == 'max' and y_pos == max(y):
            x_cord.append(x_pos)
            y_cord.append(y_pos)
        elif desc == 'min' and y_pos == min(y):
            x_cord.append(x_pos)
            y_cord.append(y_pos)
    return x_cord[0], y_cord[0]

def generate_graph(title, dates, vals, key):
    x, y = dates, vals
    
    ax = plt.axes()
    ax.grid(True)

    plt.title(title + " in " +  key + " over " + str(len(dates)) + " days from " + dates[0] + " to " + dates[len(dates) - 1])
    plt.ylabel(title)
    plt.xlabel('Dates')

    plt.gca().yaxis.set_tick_params(labelsize='medium')

    plt.gca().xaxis.set_tick_params(rotation=45, labelsize='medium')
    locator = ticker.MaxNLocator(60)
    ax.xaxis.set_major_locator(locator)

    ax.plot(x, y, marker = '.', markersize = 10)
    
    x_max, y_max = find_local(x, y, 'max')
    plt.plot(x_max, y_max, "gD", label = 'local max: ' + f'{y_max:,}' + ' on ' + str(x_max))
    x_min, y_min = find_local(x, y, 'min')
    plt.plot(x_min, y_min, "rD", label = 'local min: ' + f'{y_min:,}' + ' on ' + str(x_min))
    
    plt.tight_layout()
    plt.legend()

    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')
    plt.show()

def get_date_list(start, end):
    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")
    if start_date > end_date:
        return pd.date_range(end, start).strftime("%Y-%m-%d").tolist()
    elif start_date < end_date: 
        return pd.date_range(start, end).strftime("%Y-%m-%d").tolist()

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    if iteration == total: 
        print()

def API_fetch(stat, loc, dates):
    url = 'https://api.opencovid.ca/summary'
    vals, l = [], len(dates)

    params = {
            'after': min(dates),
            'stat': stat.replace(" ", "_").lower(),
            'loc': loc,
        }
    
    response = requests.get(url, params=params)
    if response.status_code != 200:
            output_string = re.search(r'(?<=\:).*[^}]', response.text)
            print("An error has occured with code: ", response)
            print("Corresponding to: ", output_string.group()) 
            print("Paramaters input: ", params)
    else:
        data = response.json()
        wanted_stat = stat.replace(" ", "_").lower()

        try:
            print(colored("\nGenerating graph...", 'cyan'))
            printProgressBar(0, l, prefix='Progress:', suffix='Complete', length=50)
            for i, item in enumerate(data['data']):
                if item['date'] in dates:
                    wanted_val = int(item[wanted_stat])
                    vals.append(wanted_val)
                printProgressBar(i + 1, l, prefix='Progress:', suffix='Complete', length=50)
        except IndexError:
            if item['date'] == datetime.today().strftime('%Y-%m-%d'):
                    print(colored('Error: no cases have been reported for ' + item['date'] + ' yet, please try again later.', 'red'))
            else:
                print(colored('Error: entered date has no data available.', 'red'))

    return vals

def validate_date(date, desc):
    try:
        if date != datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d"):
            raise ValueError
        return date
    except ValueError:
        print((colored('Error: ' + date + ' is not in the correct format (YYYY-MM-DD).\n', 'red')))
        if desc == 'start':
            return get_start_date()
        else:
            return get_end_date()

def get_start_date():
    while(True):
        start = input("• Enter a valid start date or enter 'today' for the current date (YYYY-MM-DD): ")
        if start.lower() == 'today': 
            start = datetime.today().strftime("%Y-%m-%d")

        return validate_date(start, 'start')

def get_end_date():
    while(True):
        end = input("• Enter a valid end date or enter 'today' for the current date (YYYY-MM-DD): ")
        if end.lower() == 'today':
            end = datetime.today().strftime("%Y-%m-%d")

        return validate_date(end, 'end')

def get_loc(province_codes):
    questions = [
        {
            'type': 'list',
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
        return province_codes[answers['province']]
    except IndexError:
        print(colored('Error: you must select at least one province.\n', 'red'))
        return get_loc(province_codes)

def get_stat():
    questions = [
        {
            'type': 'list',
            'qmark': '•',
            'message': 'Please select a statistic:',
            'name': 'statistic',
            'choices': [
                {
                    'name': 'Cases',
                },
                {
                    'name': 'Cases Daily',
                },
                {
                    'name': 'Deaths',
                },
                {
                    'name': 'Deaths Daily',
                },
                {
                    'name': 'Hospitalizations',
                },
                {
                    'name': 'Hospitalizations Daily',
                },
                {
                    'name': 'Tests Completed',
                },
                {
                    'name': 'Tests Completed Daily',
                },
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

    while True:
        loc, stat = get_loc(province_codes), get_stat()
        start, end = get_start_date(), get_end_date()

        try:
            if start == datetime.today().strftime("%Y-%m-%d") and end == datetime.today().strftime("%Y-%m-%d"):
                raise Exception
        except Exception:
            print(colored("Error: start and end dates cannot both be 'today'.\n", 'red'))
            start, end = get_start_date(), get_end_date()

        dates = get_date_list(start, end)
        vals = API_fetch(stat, loc, dates)
        key = [k for k, v in province_codes.items() if v == loc][0]
        title = stat.replace("_", " ")
        generate_graph(title, dates, vals, key)

        valid_req = False

        while not valid_req:
            continue_req = input("\nWould you like to continue with a new query (Y/N): ") 

            if continue_req in ['y', 'Y']:
                valid_req = True
            elif continue_req in ['n', 'N']:
                cls()
                print("\nThank you for using the")
                f = Figlet(font='slant')
                print(colored(f.renderText('COVID Visualizer'), 'cyan'), end = "")
                print("Developed by @bhavanvirs on GitHub\n")
                exit(1)
            else:
                print(colored("Error: not a valid response, please try again.", 'red'))
                valid_req = False

if __name__ == "__main__":
    main()