"""Compare our transformation stats against OSQ for graddb queries."""

from tabulate import tabulate
import pandas as pd

def avg(seq):
    return sum(seq)/len(seq)

# From OSQ, Table 3.
osq_data = [
    ['Current Students', '0.43', '11', '526', '3976'],
    ['New Students', '0.42', '11', '524', '3853'],
    ['TAs and Instructors', '0.51', '16', '689', '4657'],
    ['New TA Emails', '0.26', '11', '412', '2478'],
    ['TA Waitlist', '0.36', '12', '528', '3423'],
    ['Good TAs', '0.18', '8', '267', '1726'],
    ['Qual Exam Results', '0.46', '13', '614', '4723'],
    ['Advisors by Student', '0.43', '12', '558', '4236'],
    ['Advisor Overdue', '0.41', '11', '522', '3764'],
    ['Prelim Exam Overdue', '0.24', '9', '340', '2274'],
]

osq_time = [float(row[1]) for row in osq_data]
osq_loc = [int(row[3]) for row in osq_data]
osq_nodes = [int(row[4]) for row in osq_data]

# python experiments/view_stats.py graddb --format csv
incoq_text = '''
Current Students,12,2.515625,509,5089,5.015625,851,7615
New Students,12,2.515625,509,5107,5.03125,851,7633
TAs and Instructors,18,2.953125,652,6193,7.15625,1194,10179
New TA Emails,10,1.421875,422,3257,3.21875,754,5671
TA Waitlist,10,1.640625,480,3855,3.9375,878,6755
Good TAs,8,1.03125,278,2429,2.140625,516,4171
Qual Exam Results,18,2.9375,680,6131,5.9375,1069,9035
Advisors by Student,14,2.703125,576,5547,5.46875,945,8273
Advisor Overdue,12,2.546875,508,4993,5.046875,850,7511
Prelim Exam Overdue,10,1.34375,350,3077,2.84375,638,5179
'''
incoq_data = [row.rsplit(',')
              for row in incoq_text.split('\n')
              if row]

incoq_inc_time = [float(row[2]) for row in incoq_data]
incoq_inc_loc = [int(row[3]) for row in incoq_data]
incoq_inc_nodes = [int(row[4]) for row in incoq_data]
incoq_filt_time = [float(row[5]) for row in incoq_data]
incoq_filt_loc = [int(row[6]) for row in incoq_data]
incoq_filt_nodes = [int(row[7]) for row in incoq_data]

data = [
    ['Time', avg(osq_time), avg(incoq_inc_time), avg(incoq_filt_time)],
    ['Lines', avg(osq_loc), avg(incoq_inc_loc), avg(incoq_filt_loc)],
    ['Nodes', avg(osq_nodes), avg(incoq_inc_nodes), avg(incoq_filt_nodes)],
]
data = pd.DataFrame(data, columns=['', 'OSQ', 'inc', 'filt'])
data.insert(3, 'inc norm', data['inc']/data['OSQ'])
data.insert(5, 'filt norm', data['filt']/data['OSQ'])
pd.options.display.float_format = '{:.2f}'.format
print(data)
