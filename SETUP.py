# download python
# https://www.python.org/downloads/

# chromedriver's version compatible with chrome version

# https://www.google.com/intl/pl_pl/chrome/
# https://chromedriver.chromium.org/downloads

# replace chromedriver exe file in project directory if necessary
import os

#
packages = ["pandas", "numpy", "selenium", "python-csv", "bs4", "urllib3", "collection", "scipy", "tabulate", "openpyxl"]
for package in packages:
    os.system(f"pip install  {package}")


directory = os.getcwd()
os.system(f"cd {directory}")
os.system("python mainframe.py")
