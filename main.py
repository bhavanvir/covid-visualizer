from datetime import datetime
from termcolor import colored, cprint
from PyInquirer import style_from_dict, Token, prompt, Separator
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
    Token.Separator: '#00FFFF bold',
    Token.QuestionMark: '',
    Token.Selected: '#00FFFF',
    Token.Pointer: '#00FFFF bold',
    Token.Instruction: '',
    Token.Answer: '',
    Token.Question: '',
})

global province_codes
province_codes = {
    'YT': 'Yukon',
    'NT': 'Northwest Territories',
    'NU': 'Nunavut',
    'BC': 'British Columbia',
    'AB': 'Alberta',
    'SK': 'Saskatchewan',
    'MB': 'Manitoba',
    'ON': 'Ontario',
    'QC': 'Quebec',
    'NB': 'New Brunswick',
    'NS': 'Nova Scotia',
    'PE': 'Prince Edward Island',
    'NL': 'Newfoundland and Labrador'
}

global statistic_codes
statistic_codes = {
    'cases': 'Cases',
    'cases_daily': 'Cases Daily',
    'deaths': 'Deaths',
    'deaths_daily': 'Deaths Daily',
    'hospitalizations': 'Hospitalizations',
    'hospitalizations_daily': 'Hospitalizations Daily',
    'icu': 'ICU',
    'icu_daily': 'ICU Daily',
    'tests_completed': 'Tests Completed',
    'tests_completed_daily': 'Tests Completed Daily',
    'vaccine_administration_dose_1': 'Vaccine Administration Dose 1',
    'vaccine_administration_dose_2': 'Vaccine Administration Dose 2',
    'vaccine_administration_dose_3': 'Vaccine Administration Dose 3',
    'vaccine_administration_total_doses': 'Vaccine Administration Total Doses',
    'vaccine_administration_total_doses_daily': 'Vaccine Administration Total Doses Daily',
}

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def find_local_min(x, y):
    for x_i, y_i in zip(x, y):
        if y_i == min(y):
            return x_i, y_i

def find_local_max(x, y):
    for x_i, y_i in zip(x, y):
        if y_i == max(y):
            return x_i, y_i

def generate_graph(stat, dates, vals, loc):
    x, y = dates, vals
    loc = [v for k, v in province_codes.items() if k == loc][0]
    stat = [v for k, v in statistic_codes.items() if k == stat][0]
    
    ax = plt.axes()
    ax.grid(True)

    plt.title(stat + " in " +  loc + " over " + str(len(dates)) + " days from " + dates[0] + " to " + dates[len(dates) - 1])
    plt.ylabel(stat)
    plt.xlabel('Dates')

    plt.gca().yaxis.set_tick_params(labelsize='medium')
    plt.gca().xaxis.set_tick_params(rotation=45, labelsize='medium')

    locator = ticker.MaxNLocator(60)
    ax.xaxis.set_major_locator(locator)

    ax.plot(x, y, marker='.')
    
    x_min, y_min = find_local_min(x, y)
    plt.plot(x_min, y_min, "gD", label='local min: ' + f'{y_min:,}' + ' on ' + str(x_min))
    x_max, y_max = find_local_max(x, y)
    plt.plot(x_max, y_max, "rD", label='local max: ' + f'{y_max:,}' + ' on ' + str(x_max))
    
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

def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    if iteration == total: 
        print()

def fetch_api_data(stat, loc, dates):
    url = 'https://api.opencovid.ca/summary'
    vals, l = [], len(dates)

    params = {
            'after': min(dates),
            'before': max(dates),
            'stat': stat,
            'loc': loc,
        }
    
    response = requests.get(url, params=params)
    if response.status_code != 200:
        output_string = re.search(r'(?<=\:).*[^}]', response.text)
        cls()
        print(colored('Error: paramaters input ' + '\'' + str(params) + '\'', 'red', attrs=['bold']))
        print(colored('Error: response with code ' + '\'' + str(response.status_code) + '\'' + ' corresponding to ' + '\'' + output_string.group().strip("\"") + '.\'', 'red', attrs=['bold']))
        exit(1)
    else:
        data = response.json()

        print(colored("\nGenerating graph...", 'cyan'))
        print_progress_bar(0, l, prefix='Progress:', suffix='Complete', length=50)
        
        for i, item in enumerate(data['data']):
            if item['date'] in dates:
                wanted_val = int(item[stat])
                vals.append(wanted_val)
                
            print_progress_bar(i + 1, l, prefix='Progress:', suffix='Complete', length=50)

    return vals

def validate_date(date, desc):
    try:
        if date != datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d"):
            raise ValueError
        return date
    except ValueError:
        print((colored('Error: ' + '\'' + date + '\'' + ' is not in the correct format (YYYY-MM-DD).\n', 'red', attrs=['bold'])))
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

def get_loc():
    questions = [
        {
            'type': 'list',
            'qmark': '•',
            'message': 'Please select a province:',
            'name': 'province',
            'choices': [
                Separator('Northern Canada'),
                {
                    'name': '   Yukon',
                    'value': 'YT'
                },
                {
                    'name': '   Northwest Territories',
                    'value': 'NT'
                },
                {
                    'name': '   Nunavut',
                    'value': 'NU'
                },
                Separator('Western Canada'),
                {
                    'name': '   British Columbia',
                    'value': 'BC'
                },
                {
                    'name': '   Alberta',
                    'value': 'AB'
                },
                {
                    'name': '   Saskatchewan',
                    'value': 'SK'
                },
                {
                    'name': '   Manitoba',
                    'value': 'MB'
                },
                Separator('Eastern Canada'),
                {
                    'name': '   Ontario',
                    'value': 'ON'
                },
                {
                    'name': '   Quebec',
                    'value': 'QC'
                },
                {
                    'name': '   New Brunswick',
                    'value': 'NB'
                },
                {
                    'name': '   Nova Scotia',
                    'value': 'NS'
                },
                {
                    'name': '   Prince Edward Island',
                    'value': 'PE'
                },
                {
                    'name': '   Newfoundland and Labrador',
                    'value': 'NL'
                }
            ],
        }
    ]
    try:
        answers = prompt(questions, style=style)
        return answers['province']
    except IndexError:
        cls()
        print(colored('Error: you must select at least one province.\n', 'red', attrs=['bold']))
        return get_loc()

def get_stat():
    questions = [
        {
            'type': 'list',
            'qmark': '•',
            'message': 'Please select a statistic:',
            'name': 'statistic',
            'choices': [
                Separator('Cases'),
                {
                    'name': '   Cases',
                    'value': 'cases'
                },
                {
                    'name': '   Cases Daily',
                    'value': 'cases_daily'
                },
                Separator('Deaths'),
                {
                    'name': '   Deaths',
                    'value': 'deaths'
                },
                {
                    'name': '   Deaths Daily',
                    'value': 'deaths_daily'
                },
                Separator('Hospitalizations'),
                {
                    'name': '   Hospitalizations',
                    'value': 'hospitalizations'
                },
                {
                    'name': '   Hospitalizations Daily',
                    'value': 'hospitalizations_daily'
                },
                Separator('ICU'),
                {
                    'name': '   ICU',
                    'value': 'icu'
                },
                {
                    'name': '   ICU Daily',
                    'value': 'icu_daily'
                },
                Separator('Tests Completed'),
                {
                    'name': '   Tests Completed',
                    'value': 'tests_completed'
                },
                {
                    'name': '   Tests Completed Daily',
                    'value': 'tests_completed_daily'
                },
                Separator('Vaccine Administration'),
                {
                    'name': '   Vaccine Administration Dose 1',
                    'value': 'vaccine_administration_dose_1'
                },
                {
                    'name': '   Vaccine Administration Dose 2',
                    'value': 'vaccine_administration_dose_2'
                },
                {
                    'name': '   Vaccine Administration Dose 3',
                    'value': 'vaccine_administration_dose_3'
                },
                {
                    'name': '   Vaccine Administration Total Doses',
                    'value': 'vaccine_administration_total_doses'
                },
                {
                    'name': '   Vaccine Administration Total Doses Daily',
                    'value': 'vaccine_administration_total_doses_daily'
                }
            ],
        }
    ]
    try:
        answers = prompt(questions, style=style)
        return answers['statistic']
    except IndexError:
        cls()
        print(colored('Error: you must select at least one statistic.\n', 'red', attrs=['bold']))
        return get_stat()

def main():
    loc, stat = get_loc(), get_stat()

    while True:
        start, end = get_start_date(), get_end_date()
        earliest_date = '2020-01-01'
        latest_date = datetime.today().strftime('%Y-%m-%d')
        same_condition, early_condition, late_condition = False, False, False
        try:
            if start == end:
                same_condition = True
                raise Exception
            elif start < earliest_date or end < earliest_date:
                early_condition = True
                raise Exception
            elif start > latest_date or end > latest_date:
                late_condition = True
                raise Exception
        except Exception:
            if same_condition:
                print(colored("Error: start and end dates cannot both be the same.\n", 'red', attrs=['bold']))
            elif early_condition or late_condition:
                if start < earliest_date and end >= earliest_date or start > latest_date and end <= latest_date:
                    print(colored('Error: entered start date ' + '\'' + start + '\'' + ' has no data available.\n', 'red', attrs=['bold']))
                elif end < earliest_date and start >= earliest_date or end > latest_date and start <= latest_date:
                    print(colored('Error: entered end date ' + '\'' + end + '\'' + ' has no data available.\n', 'red', attrs=['bold']))
                else:
                    print(colored('Error: entered start and end dates, ' + '\'' + start + '\'' + " and "  + end +', have no data available. \n', 'red', attrs=['bold']))
            continue

        dates = get_date_list(start, end)
        vals = fetch_api_data(stat, loc, dates)
        generate_graph(stat, dates, vals, loc)

        valid_req = False
        while not valid_req:
            continue_req = input("\nWould you like to continue with a new query (Y/N): ") 

            if continue_req in ['y', 'Y']:
                valid_req = True
                main()
            elif continue_req in ['n', 'N']:
                cls()
                print("\nThank you for using")
                f = Figlet(font='slant')
                print(colored(f.renderText('COVID Visualizer'), 'cyan'), end = "")
                print("Developed by @bhavanvirs on GitHub\n")
                exit(1)
            else:
                print(colored('Error: ' + '\'' + continue_req + '\'' ' is not a valid response.', 'red', attrs=['bold']))
                valid_req = False

if __name__ == "__main__":
    main()