from monitor import CovidCaseMonitor
import time

monitor = CovidCaseMonitor()
while True:
    time.sleep(10)
    time_last_checked = time.time()
    monitor.report_total_case_change()