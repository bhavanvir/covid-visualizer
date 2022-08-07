# COVID-Visualizer

COVID-Visualizer is a command-line interface that allows users to query public COVID-19 records for all Canadian provinces and territories, and receive a plotted graph with their desired information contained in it.

## Installation

Several dependencies are required to run the COVID-Visualizer that are not included in the Python Standard Library. It is imperative that these modules are installed and functional beforehand.

Using the package manager [pip](https://pip.pypa.io/en/stable/) to install external modules:
```bash
pip install termcolor
pip install PyInquirer
pip install matplotlib
pip install pyfiglet
pip install requests
pip install pandas
pip install colorama
```
Once the external modules have been installed, the source code for COVID-Visualizer can then be obtained using the `git clone` command with the public repository's URL as the target, to make a clone or copy of the repository in a new directory, at another location.

## API

COVID-Visualizer uses the [COVID-19 Canada Open Data Working Group API](https://api.opencovid.ca/) to obtain COVID-19 records across all Canadian provinces and territories, namely with the `/summary` endpoint, which returns the following metrics:

- region
- date
- **cases**
- **cases_daily**
- **deaths**
- **deaths_daily**
- **hospitalizations**
- **hospitalizations_daily**
- icu
- icu_daily
- **tests_completed**
- **tests_completed_daily**
- **vaccine_coverage_dose_1**
- vaccine_coverage_dose_1_daily
- **vaccine_coverage_dose_2**
- vaccine_coverage_dose_2_daily
- **vaccine_coverage_dose_3**
- vaccine_coverage_dose_3_daily
- vaccine_coverage_dose_4
- vaccine_coverage_dose_4_daily
- **vaccine_administration_total_doses**
- vaccine_administration_total_doses_daily
- vaccine_administration_dose_1
- vaccine_administration_dose_1_daily
- vaccine_administration_dose_2
- vaccine_administration_dose_2_daily
- vaccine_administration_dose_3
- vaccine_administration_dose_3_daily

The **bolded** text being the metrics offered in the current version of the COVID-Visualizer.

## License
[MIT](https://choosealicense.com/licenses/mit/)