
# coding: utf-8

# In[1]:

import unicodecsv
import os
path = 'C:\\Users\\aemra\\Documents\\Python\\Nanodegree'
os.chdir(path)
enrollments=[]
f=open('enrollments.csv','rb')
reader=unicodecsv.DictReader(f)

for row in reader:
    enrollments.append(row)
    
f.close()

enrollments[0]


# In[2]:

def read_csv(filename):
    with open(filename, 'rb') as f:
        reader = unicodecsv.DictReader(f)
        return list(reader)

enrollments = read_csv('enrollments.csv')
daily_engagement = read_csv('daily_engagement.csv')
project_submissions = read_csv('project_submissions.csv')


# In[3]:

from datetime import datetime as dt

# Takes a date as a string, and returns a Python datetime object. 
# If there is no date given, returns None
def parse_date(date):
    if date == '':
        return None
    else:
        return dt.strptime(date, '%Y-%m-%d')
    
# Takes a string which is either an empty string or represents an integer,
# and returns an int or None.
def parse_maybe_int(i):
    if i == '':
        return None
    else:
        return int(i)

# Clean up the data types in the enrollments table
for enrollment in enrollments:
    enrollment['cancel_date'] = parse_date(enrollment['cancel_date'])
    enrollment['days_to_cancel'] = parse_maybe_int(enrollment['days_to_cancel'])
    enrollment['is_canceled'] = enrollment['is_canceled'] == 'True'
    enrollment['is_udacity'] = enrollment['is_udacity'] == 'True'
    enrollment['join_date'] = parse_date(enrollment['join_date'])

    
enrollments[0]


# In[4]:

# Clean up the data types in the engagement table
for engagement_record in daily_engagement:
    engagement_record['lessons_completed'] = int(float(engagement_record['lessons_completed']))
    engagement_record['num_courses_visited'] = int(float(engagement_record['num_courses_visited']))
    engagement_record['projects_completed'] = int(float(engagement_record['projects_completed']))
    engagement_record['total_minutes_visited'] = float(engagement_record['total_minutes_visited'])
    engagement_record['utc_date'] = parse_date(engagement_record['utc_date'])
    
daily_engagement[0]


# In[5]:

# Clean up the data types in the submissions table
for submission in project_submissions:
    submission['completion_date'] = parse_date(submission['completion_date'])
    submission['creation_date'] = parse_date(submission['creation_date'])

project_submissions[0]


# In[6]:

def get_unique_students(data):
    unique_students = set()
    for data_point in data:
        unique_students.add(data_point['account_key'])
    return unique_students
len(enrollments)


# In[7]:

unique_enrolled_students = get_unique_students(enrollments)
len(unique_enrolled_students)


# In[8]:

len(enrollments)


# In[9]:

unique_enrolled_students = get_unique_students(enrollments)
len(unique_enrolled_students)


# In[10]:

len(daily_engagement)


# In[11]:

for engagement_record in daily_engagement:
    engagement_record['account_key'] = engagement_record['acct']
    del[engagement_record['acct']]


# In[12]:

unique_engagement_students = get_unique_students(daily_engagement)
len(unique_engagement_students)


# In[13]:

len(project_submissions)



# In[14]:

unique_project_submitters = get_unique_students(project_submissions)
len(unique_project_submitters)


# In[15]:

daily_engagement[0]['account_key']


# In[16]:

for enrollment in enrollments:
    student=enrollment['account_key']
    if student not in unique_engagement_students:
        print (enrollment)
        break


# In[17]:

count=0
for enrollment in enrollments:
    student=enrollment['account_key']
    if student not in unique_engagement_students     and enrollment['join_date']!=enrollment['cancel_date']:
        count+=1
print (count)


# In[18]:

for enrollment in enrollments:
    student=enrollment['account_key']
    if student not in unique_engagement_students     and enrollment['join_date']!=enrollment['cancel_date']:
        print (enrollment)


# In[19]:

udacity_test_accounts = set()
for enrollment in enrollments:
    if enrollment['is_udacity']:
        udacity_test_accounts.add(enrollment['account_key'])
len(udacity_test_accounts)


# In[20]:

def remove_udacity_accounts(data):
    non_udacity_data = []
    for data_point in data:
        if data_point['account_key'] not in udacity_test_accounts:
            non_udacity_data.append(data_point)
    return non_udacity_data


# In[21]:

# Remove Udacity test accounts from all three tables
non_udacity_enrollments = remove_udacity_accounts(enrollments)
non_udacity_engagement = remove_udacity_accounts(daily_engagement)
non_udacity_submissions = remove_udacity_accounts(project_submissions)

print (len(non_udacity_enrollments))
print (len(non_udacity_engagement))
print (len(non_udacity_submissions))


# In[107]:

from collections import defaultdict

def group_data(data, key_name):
    grouped_data = defaultdict(list)
    for data_point in data:
        key = data_point[key_name]
        grouped_data[key].append(data_point)
    return grouped_data


# In[108]:

paid_students = {}
for enrollment in non_udacity_enrollments:
    if (not enrollment['is_canceled'] or
            enrollment['days_to_cancel'] > 7):
        account_key = enrollment['account_key']
        enrollment_date = enrollment['join_date']
        if (account_key not in paid_students or
                enrollment_date > paid_students[account_key]):
            paid_students[account_key] = enrollment_date
len(paid_students)


# In[109]:

def within_one_week(join_date, engagement_date):
    time_delta = engagement_date - join_date
    return time_delta.days < 7 and time_delta.days>=0


# In[110]:

def remove_free_trial_cancels(data):
    new_data = []
    for data_point in data:
        if data_point['account_key'] in paid_students:
            new_data.append(data_point)
    return new_data


# In[111]:

paid_enrollments = remove_free_trial_cancels(non_udacity_enrollments)
paid_engagement = remove_free_trial_cancels(non_udacity_engagement)
paid_submissions = remove_free_trial_cancels(non_udacity_submissions)

print (len(paid_enrollments))
print (len(paid_engagement))
print (len(paid_submissions))


# In[112]:

for engagement_record in paid_engagement:
    if engagement_record['num_courses_visited']>0:
        engagement_record['has_visited']=1
    else:
        engagement_record['has_visited']=0


# In[113]:

paid_engagement_in_first_week = []
for engagement_record in paid_engagement:
    account_key = engagement_record['account_key']
    join_date = paid_students[account_key]
    engagement_record_date = engagement_record['utc_date']

    if within_one_week(join_date, engagement_record_date):
        paid_engagement_in_first_week.append(engagement_record)

len(paid_engagement_in_first_week)


# In[114]:

from collections import defaultdict
engagement_by_account=defaultdict(list)
for engagement_record in paid_engagement_in_first_week:
    account_key=engagement_record['account_key']
    engagement_by_account[account_key].append(engagement_record)


# In[115]:

total_minutes_by_account={}
for account_key,engagement_for_student in engagement_by_account.items():
    total_munite=0
    for engagement_record in engagement_for_student:
        total_munite+=engagement_record['total_minutes_visited']
    total_minutes_by_account[account_key]=total_munite
    


# In[116]:

import numpy as np
# Summarize the data about minutes spent in the classroom
total_minutes =list(total_minutes_by_account.values())
print ('Mean:', np.mean(total_minutes))
print ('Standard deviation:', np.std(total_minutes))
print ('Minimum:', np.min(total_minutes))
print ('Maximum:', np.max(total_minutes))


# In[117]:

student_with_max_minutes = None
max_minutes = 0

for student, total_minutes in total_minutes_by_account.items():
    if total_minutes > max_minutes:
        max_minutes = total_minutes
        student_with_max_minutes = student
        
max_minutes


# In[118]:

max_minutes

for engagement_record in paid_engagement_in_first_week:
    if engagement_record['account_key'] == student_with_max_minutes:
        print (engagement_record)


# In[119]:

total_lessons_by_account={}
for account_key, engagement_for_student in engagement_by_account.items():
    total_lesson=0
    for engagement_record in engagement_for_student:
        total_lesson+=engagement_record['lessons_completed']
    total_lessons_by_account[account_key]=total_lesson


# In[120]:

import numpy as np
# Summarize the data about minutes spent in the classroom
total_lessons =list(total_lessons_by_account.values())
print ('Mean:', np.mean(total_lessons))
print ('Standard deviation:', np.std(total_lessons))
print ('Minimum:', np.min(total_lessons))
print ('Maximum:', np.max(total_lessons))


# In[121]:

def sum_grouped_items(grouped_data, field_name):
    summed_data = {}
    for key, data_points in grouped_data.items():
        total = 0
        data_points=list(data_points)
        for data_point in data_points:
            total += data_point[field_name]
        summed_data[key] = total
    return summed_data


# In[122]:

total_minutes_by_account = sum_grouped_items(engagement_by_account,
                                             'total_minutes_visited')


# In[123]:


def describe_data(data):
    total_values=list(data)
    print ('Mean:', np.mean(total_values))
    print ('Standard deviation:', np.std(total_values))
    print ('Minimum:', np.min(total_values))
    print ('Maximum:', np.max(total_values))
    


# In[124]:

days_visited_by_account = sum_grouped_items(engagement_by_account,'has_visited')


# In[125]:

describe_data(days_visited_by_account.values())


# In[126]:

subway_project_lesson_keys = ['746169184', '3176718735']


# In[127]:

pass_subway_project = set()

for submission in paid_submissions:
    project = submission['lesson_key']
    rating = submission['assigned_rating']    

    if ((project in subway_project_lesson_keys) and
            (rating == 'PASSED' or rating == 'DISTINCTION')):
        pass_subway_project.add(submission['account_key'])

len(pass_subway_project)


# In[128]:

passing_engagement = []
non_passing_engagement = []

for engagement_record in paid_engagement_in_first_week:
    if engagement_record['account_key'] in pass_subway_project:
        passing_engagement.append(engagement_record)
    else:
        non_passing_engagement.append(engagement_record)

print len(passing_engagement)
print len(non_passing_engagement)


# In[130]:

passing_engagement_by_account = group_data(passing_engagement,'account_key')
non_passing_engagement_by_account = group_data(non_passing_engagement,'account_key')


# In[ ]:

print 'non-passing students:'
non_passing_minutes=sum_grouped_items


# In[132]:

print 'non-passing students:'
non_passing_minutes = sum_grouped_items(
    non_passing_engagement_by_account,
    'total_minutes_visited'
)
describe_data(non_passing_minutes.values())


# In[133]:

print 'non-passing students:'
non_passing_minutes = sum_grouped_items(
    non_passing_engagement_by_account,
    'total_minutes_visited'
)
describe_data(non_passing_minutes.values())


# In[134]:


print 'passing students:'
passing_minutes = sum_grouped_items(
    passing_engagement_by_account,
    'total_minutes_visited'
)
describe_data(passing_minutes.values())


# In[135]:


print 'non-passing students:'
non_passing_lessons = sum_grouped_items(
    non_passing_engagement_by_account,
    'lessons_completed'
)
describe_data(non_passing_lessons.values())


# In[138]:

print 'passing students:'
passing_lessons = sum_grouped_items(
    passing_engagement_by_account,
    'lessons_completed'
)
describe_data(passing_lessons.values())


# In[139]:

print 'non-passing students:'
non_passing_visits = sum_grouped_items(
    non_passing_engagement_by_account, 
    'has_visited'
)
describe_data(non_passing_visits.values())


# In[140]:

print 'passing students:'
passing_visits = sum_grouped_items(
    passing_engagement_by_account,
    'has_visited'
)
describe_data(passing_visits.values())


# In[ ]:



