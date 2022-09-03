# Output Formatting
import colorama
colorama.init()
from termcolor import colored
from pyfiglet import Figlet

# Input Formatting 
from PyInquirer import style_from_dict, Token, prompt, Separator

# Time Tracking
import time
from datetime import datetime

# Progress Bar
from tqdm import tqdm

# API Data
import requests

# Data Manipulation
import pandas as pd

# Data Plotting
from matplotlib import pyplot as plt, ticker

# String Validation
import re

global bolded_colour, colour
bolded_colour = '#FFFF00 bold'
colour = 'yellow'

global style 
style = style_from_dict({
    Token.Separator: bolded_colour,
    Token.QuestionMark: '',
    Token.Selected: bolded_colour,
    Token.Pointer: bolded_colour,
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

def find_minimum(x, y):
    for x_i, y_i in zip(x, y):
        if y_i == min(y):
            return x_i, y_i

def find_maximum(x, y):
    for x_i, y_i in zip(x, y):
        if y_i == max(y):
            return x_i, y_i

def get_location_name(location):
    location = [value for key, value in province_codes.items() if key == location][0]

    return location 

def get_statistic_name(statistic):
    statistic = [value for key, value in statistic_codes.items() if key == statistic][0]

    return statistic

def generate_rolling_average(x, y, window):
    data_frame = pd.DataFrame({'col1': x, 'col2': y})
    plt.plot(data_frame['col2'].rolling(window).mean(), color='blue', label='Rolling average: ' + str(window) + ' days')
    plt.fill_between(x, data_frame['col2'].rolling(window).mean(), color='blue', alpha=0.1)

def generate_minimum_maximum(x, y):
    x_minimum, y_minimum = find_minimum(x, y)
    plt.plot(x_minimum, y_minimum,'rv', label='Minimum: ' + f'{y_minimum:,}' + ' on ' + str(x_minimum))
    x_maximum, y_maximum = find_maximum(x, y)
    plt.plot(x_maximum, y_maximum,'r^', label='Maximum: ' + f'{y_maximum:,}' + ' on ' + str(x_maximum))

def zoom_plot_window():
    manager = plt.get_current_fig_manager()
    manager.window.state('zoomed')

def generate_main_graph(statistic, dates, values, location):
    x, y = dates, values
    location_name, statistic_name = get_location_name(location), get_statistic_name(statistic)
    
    ax = plt.axes()
    ax.grid(True, linestyle=':')

    plt.title(statistic_name + ' in ' +  location_name + ' from ' + dates[0] + ' to ' + dates[len(dates) - 1])
    plt.ylabel(statistic_name)
    plt.xlabel('Date')

    plt.gca().yaxis.set_tick_params(labelsize='medium')
    plt.gca().xaxis.set_tick_params(rotation=45, labelsize='medium')

    locator = ticker.MaxNLocator(60)
    ax.xaxis.set_major_locator(locator)
    ax.plot(x, y, color='black', label='Original: ' + str(len(dates)) +  ' days')

    generate_rolling_average(x, y, 7)
    
    generate_minimum_maximum(x, y)

    plt.tight_layout()
    plt.legend()

    zoom_plot_window()
    
    plt.show()

def get_date_list(start, end):
    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")
    if start_date > end_date:
        return pd.date_range(end, start).strftime("%Y-%m-%d").tolist()
    elif start_date < end_date: 
        return pd.date_range(start, end).strftime("%Y-%m-%d").tolist()

def fetch_api_data(statistic, location, dates):
    url = 'https://api.opencovid.ca/summary'
    values, l = [], len(dates)
    paramaters = {
            'after': min(dates),
            'before': max(dates),
            'stat': statistic,
            'loc': location,
        }
    
    response = requests.get(url, params=paramaters)
    if response.status_code != 200:
        output_string = re.search(r'(?<=\:).*[^}]', response.text)
        print(colored('Error: paramaters input ' + '\'' + str(paramaters) + '\'', 'red', attrs=['bold']))
        print(colored('Error: response with code ' + '\'' + str(response.status_code) + '\'' + ' corresponding to ' + '\'' + output_string.group().strip("\"") + '.\'', 'red', attrs=['bold']))
        exit(1)
    else:
        data = response.json()

        print(colored("\nSucess: generating graph...", 'green', attrs=['bold']))
        for index, item in enumerate(tqdm(data['data'], total=l, desc='Progress', bar_format='{desc}: {percentage:.1f}% Complete |{bar:75}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]')):
            if item['date'] in dates:
                values.append(int(item[statistic]))
            if index % 5 == 0:
                time.sleep(0.01)
        print(colored('Success: graph generated, now displaying...\n', 'green', attrs=['bold']))

    return values

def validate_date(date, description):
    try:
        if date != datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d"):
            raise ValueError
        return date
    except ValueError:
        print((colored('Error: ' + '\'' + date + '\'' + ' is not in the correct format (YYYY-MM-DD).\n', 'red', attrs=['bold'])))
        if description == 'start':
            return get_start_date()
        else:
            return get_end_date()

def get_start_date():
    while True:
        questions = [
            {
                'type': 'input',
                'qmark': '•',
                'name': 'start_date',
                'message': 'Please enter a valid start date or enter \'today\' for the current date (YYYY-MM-DD):',
            }
        ]
        answers = prompt(questions, style=style)
        if answers['start_date'].lower() == 'today': 
            answers['start_date'] = datetime.today().strftime("%Y-%m-%d")

        return validate_date(answers['start_date'], 'start')

def get_end_date():
    while True:
        questions = [
            {
                'type': 'input',
                'qmark': '•',
                'name': 'end_date',
                'message': 'Please enter a valid end date or enter \'today\' for the current date (YYYY-MM-DD):',
            }
        ]

        answers = prompt(questions, style=style)
        if answers['end_date'].lower() == 'today':
            answers['end_date'] = datetime.today().strftime("%Y-%m-%d")

        return validate_date(answers['end_date'], 'end')

def get_location():
    questions = [
        {
            'type': 'checkbox',
            'qmark': '•',
            'message': 'Please select a province:',
            'name': 'province',
            'choices': [
                Separator('Northern Canada'),
                {
                    'name': 'Yukon',
                    'value': 'YT'
                },
                {
                    'name': 'Northwest Territories',
                    'value': 'NT'
                },
                {
                    'name': 'Nunavut',
                    'value': 'NU'
                },
                Separator('Eastern Canada'),
                {
                    'name': 'Ontario',
                    'value': 'ON'
                },
                {
                    'name': 'Quebec',
                    'value': 'QC'
                },
                {
                    'name': 'New Brunswick',
                    'value': 'NB'
                },
                {
                    'name': 'Nova Scotia',
                    'value': 'NS'
                },
                {
                    'name': 'Prince Edward Island',
                    'value': 'PE'
                },
                {
                    'name': 'Newfoundland and Labrador',
                    'value': 'NL'
                },
                Separator('Western Canada'),
                {
                    'name': 'British Columbia',
                    'value': 'BC'
                },
                {
                    'name': 'Alberta',
                    'value': 'AB'
                },
                {
                    'name': 'Saskatchewan',
                    'value': 'SK'
                },
                {
                    'name': 'Manitoba',
                    'value': 'MB'
                }
            ],
        }
    ]

    try:
        answers = prompt(questions, style=style)
        assert len(answers['province']) == 1
        return answers['province'][0]
    except AssertionError:
        if len(answers['province']) == 0:
            print(colored('Error: ' + '\'' + str(answers['province']) + '\'' + ' is not a valid province.\n', 'red', attrs=['bold']))
        else:
            print(colored('Error: ' + '\'' + str(answers['province']) + '\'' + ' too many provinces, only one must be selected.\n', 'red', attrs=['bold']))
        return get_location()

def get_statistic():
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
                    'value': 'cases'
                },
                {
                    'name': 'Cases Daily',
                    'value': 'cases_daily'
                },
                Separator('Deaths'),
                {
                    'name': 'Deaths',
                    'value': 'deaths'
                },
                {
                    'name': 'Deaths Daily',
                    'value': 'deaths_daily'
                },
                Separator('Hospitalizations'),
                {
                    'name': 'Hospitalizations',
                    'value': 'hospitalizations'
                },
                {
                    'name': 'Hospitalizations Daily',
                    'value': 'hospitalizations_daily'
                },
                Separator('ICU'),
                {
                    'name': 'ICU',
                    'value': 'icu'
                },
                {
                    'name': 'ICU Daily',
                    'value': 'icu_daily'
                },
                Separator('Tests Completed'),
                {
                    'name': 'Tests Completed',
                    'value': 'tests_completed'
                },
                {
                    'name': 'Tests Completed Daily',
                    'value': 'tests_completed_daily'
                },
                Separator('Vaccine Administration'),
                {
                    'name': 'Vaccine Administration Dose 1',
                    'value': 'vaccine_administration_dose_1'
                },
                {
                    'name': 'Vaccine Administration Dose 2',
                    'value': 'vaccine_administration_dose_2'
                },
                {
                    'name': 'Vaccine Administration Dose 3',
                    'value': 'vaccine_administration_dose_3'
                },
                {
                    'name': 'Vaccine Administration Total Doses',
                    'value': 'vaccine_administration_total_doses'
                },
                {
                    'name': 'Vaccine Administration Total Doses Daily',
                    'value': 'vaccine_administration_total_doses_daily'
                }
            ],
        }
    ]

    try:
        answers = prompt(questions, style=style)
        assert len(answers['statistic']) == 1
        return answers['statistic'][0]
    except AssertionError:
        if len(answers['statistic']) == 0:
            print(colored('Error: ' + '\'' + str(answers['statistic']) + '\'' + ' is not a valid statistic.\n', 'red', attrs=['bold']))
        else:
            print(colored('Error: ' + '\'' + str(answers['statistic']) + '\'' + ' too many statistics, only one must be selected.\n', 'red', attrs=['bold']))
        return get_statistic()

def new_query():
    questions = [
            {
                'type': 'input',
                'qmark': '•',
                'message': 'Would you like to continue with a new query? (Y/N):',
                'name': 'continue',
            }
        ]

    answers = prompt(questions, style=style)
    if answers['continue'] in ['Y', 'y']:
        main()
    elif answers['continue'] in ['N', 'n']:
        print()
        f = Figlet(font='slant')
        print(colored(f.renderText('COVID Visualizer'), colour), end = "")
        print(colored("Developed by @bhavanvirs on GitHub\n", colour, attrs=['bold']))
        exit(1)
    else:
        print(colored('Error: ' + '\'' + str(answers['continue']) + '\'' + ' is not in the correct format (Y/N).\n', 'red', attrs=['bold']))
        new_query()

def main():
    location, statistic = get_location(), get_statistic()

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
        values = fetch_api_data(statistic, location, dates)
        generate_main_graph(statistic, dates, values, location)

        new_query()

if __name__ == "__main__":
    main()