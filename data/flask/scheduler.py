import os
import sys
import getpass
import argparse
from crontab import CronTab


parser = argparse.ArgumentParser('Schedule your scraper to recrawl at regular intervals.'
                                  + ' Put the optimization parameters that you have selected')
parser.add_argument('-con_req',
                    nargs='?',
                    type=str,
                    default=8,
                    help='Input parameter CONCURRENT_REQUESTS, def: 8')
parser.add_argument('-con_req_dom',
                    nargs='?',
                    type=str,
                    default=100,
                    help='Input parameter CONCURRENT_REQUESTS_PER_DOMAIN, def: 100')
parser.add_argument('-freq',
                    nargs='?',
                    type=int,
                    default=2,
                    help='Number of days; eg, 5 for once in 5 days')
parser.add_argument('-py_path',
                    type=str,
                    help='Absolute path of python from your virtualenv')
args = parser.parse_args()


currdirec = os.getcwd()
username = getpass.getuser()

job_comment = "buzzbang scraper schedule"
cron = CronTab(user=username)
for job in cron:
    if job.comment == job_comment:
        print("Scheduler already working")
        sys.exit()

job = cron.new(command= 'bash ' + currdirec + '/bioschemas_scraper/scheduler.sh ' + str(args.con_req) + ' ' + str(args.con_req_dom) + ' ' + str(args.py_path), comment=job_comment)

job.day.every(args.freq)
cron.write()
