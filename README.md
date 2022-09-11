# COVID-Visualizer

COVID-Visualizer is a command-line interface that allows users to query public COVID-19 records for all Canadian provinces and territories and receive a plotted graph with their desired information contained in it. The generated graph includes the local minima and maxima, as well as a 7-day running average of the chosen statistic.

## Installation

The source code for COVID-Visualizer can then be obtained using the `git clone` command with the public repository's URL as the target, to make a clone or copy of the repository in a new directory, at another location.
```bash
git clone https://github.com/bhavanvir/COVID-Visualizer
```

Change your directory to the root of the project.
```bash
cd COVID-Visualizer
```

Several dependencies are required to run COVID-Visualizer that are not included in the Python Standard Library. It is imperative that these modules are installed and functional beforehand.

Using the package manager [pip](https://pip.pypa.io/en/stable/) to install all external modules:
```bash
pip install -r requirements.txt
```

## Usage

Running the COVID-Visualizer application using `python3 main.py` in any terminal shows an interactive list built with the `PyInquirer` library.

A metric is selected using the `Up` or `Down` keyboard arrow keys and chosen using the `Enter` button. A valid start and end date are then enterable; a valid date occurs after 2020-01-01 (YYYY-MM-DD).

A progress bar is then dynamically rendered to inform the user of the time remaining until their graph is generated.

The graph is then automatically zoomed into a new window to optimize the viewing experience.

Entering `Y` in the terminal allows for a new query to be performed and entering `N` exits the application.

## API

COVID-Visualizer uses the [COVID-19 Canada Open Data Working Group API](https://api.opencovid.ca/) to obtain COVID-19 records across all Canadian provinces and territories, namely with the `/summary` endpoint, which returns the following metrics:

- region
- date
- *cases*
- *cases_daily*
- *deaths*
- *deaths_daily*
- *hospitalizations*
- *hospitalizations_daily*
- *icu*
- *icu_daily*
- *tests_completed*
- *tests_completed_daily*
- *vaccine_coverage_dose_1*
- vaccine_coverage_dose_1_daily
- *vaccine_coverage_dose_2*
- vaccine_coverage_dose_2_daily
- *vaccine_coverage_dose_3*
- vaccine_coverage_dose_3_daily
- vaccine_coverage_dose_4
- vaccine_coverage_dose_4_daily
- *vaccine_administration_total_doses*
- *vaccine_administration_total_doses_daily*
- vaccine_administration_dose_1
- vaccine_administration_dose_1_daily
- vaccine_administration_dose_2
- vaccine_administration_dose_2_daily
- vaccine_administration_dose_3
- vaccine_administration_dose_3_daily

*Italicized* text being the metrics offered in the current version of the COVID-Visualizer.

## License
[MIT](https://choosealicense.com/licenses/mit/)
