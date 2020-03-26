from config import FREQUENCY_IN_SEC
from monitor import CovidCaseMonitor
import time

monitor = CovidCaseMonitor()
while True:
    time.sleep(FREQUENCY_IN_SEC)
    monitor.report_total_case_change()