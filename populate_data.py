#Import necessary packages:
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import numpy as np
 
#Connect to the database and read the csv file:
conn_url = 'postgresql://postgres:y6pj86qh@f19server.apan5310.com:50206/h1b_formal'
engine = create_engine(conn_url)
connection = engine.connect()
df = pd.read_csv('H-1B.csv')
df.columns = map(str.lower, df.columns)   #This is because all table names are automatically turned into lower case in codio, so we make sure our code align with that.
 
#Construct prevailing_wages table with columns directly come from original data
prevailing_wages = df[["prevailing_wage", "pw_unit_of_pay", "pw_wage_level","pw_source", "pw_source_year", "pw_source_other"]]
#drop duplicates
prevailing_wages = prevailing_wages.drop_duplicates()
#add id
prevailing_wages.insert(0, 'pw_id', range(1, 1 + len(prevailing_wages)))
#populate the data into table:
prevailing_wages.to_sql(name='prevailing_wages',con=engine, if_exists='append',index=False)
 
#Construct wages table and populate data:
wages = df[["wage_rate_of_pay_from", "wage_rate_of_pay_to", "wage_unit_of_pay"]]
wages = wages.drop_duplicates()
wages.insert(0, 'wage_case_id', range(1, 1 + len(wages)))
wages.to_sql(name='wages',con=engine, if_exists='append',index=False)
 
#Construct soc table:
#In Excel, some soc_code is shown in the date format, the code below is to reverse those columns into the correct form:
 
df['soc_code']=np.where(df['soc_name']=='ADVERTISING AND PROMOTIONS MANAGERS','11-2011',df['soc_code'])
df['soc_code']=np.where(df['soc_name']=='ADMINISTRATIVE SERVICES MANAGERS','11-3012',df['soc_code'])
df['soc_code']=np.where(df['soc_name']=='MEDICAL AND HEALTH SERVICES MANAGERS','11-9111',df['soc_code'])
df['soc_code']=np.where(df['soc_name']=='MARKETING MANAGERS','11-2021',df['soc_code'])
df['soc_code']=np.where(df['soc_name']=='SALES MANAGERS','11-2022',df['soc_code'])
df['soc_code']=np.where(df['soc_name']=='PUBLIC RELATIONS AND FUNDRAISING MANAGERS','11-2030',df['soc_code'])
df['soc_code']=np.where(df['soc_name']=='COMPUTER AND INFORMATION SYSTEMS MANAGERS','11-3021',df['soc_code'])
df['soc_code']=np.where(df['soc_name']=='FINANCIAL MANAGERS','11-3031',df['soc_code'])
df['soc_code']=np.where(df['soc_name']=='INDUSTRIAL PRODUCTION MANAGERS','11-3051',df['soc_code'])
df['soc_code']=np.where(df['soc_name']=='PURCHASING MANAGERS','11-3061',df['soc_code'])
df['soc_code']=np.where(df['soc_name']=='TRANSPORTATION, STORAGE, AND DISTRIBUTION MANAGERS','11-3071',df['soc_code'])
df['soc_code']=np.where(df['soc_name']=='HUMAN RESOURCES MANAGERS','11-3121',df['soc_code'])
df['soc_code']=np.where(df['soc_name']=='TRAINING AND DEVELOPMENT MANAGERS','11-3131',df['soc_code'])
df['soc_code']=np.where(df['soc_name']=='FARMERS, RANCHERS, AND OTHER AGRICULTURAL MANAGERS','11-9013',df['soc_code'])
df['soc_code']=np.where(df['soc_name']=='CONSTRUCTION MANAGERS','11-9021',df['soc_code'])
df['soc_code']=np.where(df['soc_name']=='EDUCATION ADMINISTRATORS, ELEMENTARY AND SECONDARY','11-9032',df['soc_code'])
df['soc_code']=np.where(df['soc_name']=='EDUCATION ADMINISTRATORS, POSTSECONDARY','11-9033',df['soc_code'])
df['soc_code']=np.where(df['soc_name']=='EDUCATION ADMINISTRATORS, PRESCHOOL AND CHILDCARE','11-9031',df['soc_code'])
df['soc_code']=np.where(df['soc_name']=='EDUCATION ADMINISTRATORS, ALL OTHER','11-9039',df['soc_code'])
df['soc_code']=np.where(df['soc_name']=='ARCHITECTURAL AND ENGINEERING MANAGERS','11-9041',df['soc_code'])
df['soc_code']=np.where(df['soc_name']=='FOOD SERVICE MANAGERS','11-9051',df['soc_code'])
df['soc_code']=np.where(df['soc_name']=='LODGING MANAGERS','11-9081',df['soc_code'])
df['soc_code']=np.where(df['soc_name']=='NATURAL SCIENCES MANAGERS','11-9121',df['soc_code'])
df['soc_code']=np.where(df['soc_name']=='PROPERTY, REAL ESTATE, AND COMMUNITY ASSOCIATION','11-9141',df['soc_code'])
df['soc_code']=np.where(df['soc_name']=='SOCIAL AND COMMUNITY SERVICE MANAGERS','11-9151',df['soc_code'])
df['soc_code']=np.where(df['soc_name']=='MANAGERS, ALL OTHER','11-9199',df['soc_code'])
 
#Some of rows of soc_name have typo, for example, missing ‘s’ at the end, so we find out which rows have this problem and then change their names to the correct ones:
df['soc_name']=np.where(df['soc_code']=='15-1121','COMPUTER SYSTEMS ANALYSTS', df['soc_name'])
df['soc_name']=np.where(df['soc_code']=='15-1131','COMPUTER PROGRAMMERS', df['soc_name'])
df['soc_name']=np.where(df['soc_code']=='15-1199','COMPUTER OCCUPATIONS, ALL OTHER', df['soc_name'])
df['soc_name']=np.where(df['soc_code']=='13-1111','MANAGEMENT ANALYSTS', df['soc_name'])
df['soc_name']=np.where(df['soc_code']=='15-1199.02','COMPUTER SYSTEMS ENGINEERS/ARCHITECTS', df['soc_name'])
df['soc_name']=np.where(df['soc_code']=='25-2021','ELEMENTARY SCHOOL TEACHERS, EXCEPT SPECIAL', df['soc_name'])
df['soc_name']=np.where(df['soc_code']=='41-9031','SALES ENGINEERS', df['soc_name'])
df['soc_name']=np.where(df['soc_code']=='17-2072','ELECTRONICS ENGINEERS, EXCEPT COMPUTER', df['soc_name'])
df['soc_name']=np.where(df['soc_code']=='15-1132','SOFTWARE DEVELOPERS, APPLICATIONS', df['soc_name'])
df['soc_name']=np.where(df['soc_code']=='15-1022','COMPUTER PROGRAMMERS, NON R&D', df['soc_name'])
df['soc_name']=np.where(df['soc_code']=='15-1142','NETWORK AND COMPUTER SYSTEMS ADMINISTRATORS', df['soc_name'])
df['soc_name']=np.where(df['soc_code']=='15-1034','SOFTWARE DEVELOPERS, APPLICATIONS, NON R&D', df['soc_name'])
df['soc_name']=np.where(df['soc_code']=='17-3023','ELECTRICAL AND ELECTRONIC ENGINEERING TECHNICIANS', df['soc_name'])
df['soc_name']=np.where(df['soc_code']=='17-2141','MECHANICAL ENGINEERS', df['soc_name'])
 
#Populate data into soc table:
soc = df[["soc_code", "soc_name"]]
soc = soc.drop_duplicates()
soc.to_sql(name='soc',con=engine, if_exists='append',index=False)
 
#Construct job_title table and populate data:
job_title = df[["job_title"]]
job_title = job_title.drop_duplicates()
job_title.insert(0, 'job_title_id', range(1, 1 + len(job_title)))
job_title = job_title.rename(columns = {"job_title": "job_title_name"})
job_title.to_sql(name='job_title',con=engine, if_exists='append',index=False)
 
#Construct & deal with data in cases table:
#In this step we first select all columns, including those in foreign key tables, so that we can join these columns in the future steps:
cases = df[["case_number", "original_cert_date", "employment_start_date",
"employment_end_date", "case_status", "visa_class", "soc_code", "full_time_position", "wage_rate_of_pay_from", "wage_rate_of_pay_to", "wage_unit_of_pay",
"prevailing_wage", "pw_unit_of_pay", "pw_wage_level","pw_source",
"pw_source_year", "pw_source_other", "job_title"]]
 
 #Since we need 'wage_case_id' column in the cases table, and the column has a foreign key to 'wage_case_id' in'wages'table,
 #we merge the two tables based on columns 'wage_rate_of_pay_from', 'wage_rate_of_pay_to', 'wage_unit_of_pay' so that it satisfy 
 #the requirements of foreign key constraint
cases = pd.merge(cases, prevailing_wages,  how='left', on=["prevailing_wage", "pw_unit_of_pay", "pw_wage_level","pw_source", "pw_source_year", "pw_source_other"])
cases = pd.merge(cases, wages,  how='left', on=["wage_rate_of_pay_from", "wage_rate_of_pay_to", "wage_unit_of_pay"])
job_title = job_title.rename(columns = {"job_title_name": "job_title"})
cases = pd.merge(cases, job_title,  how='left', on=["job_title"])
 
#Rename columns to make sure they have aligned names when populating into the database:
cases = cases[["case_number", "original_cert_date", "employment_start_date", "employment_end_date", "case_status", "visa_class", "job_title_id", "soc_code", "full_time_position", "pw_id", "wage_case_id"]]
cases.to_sql(name='cases',con=engine, if_exists='append',index=False)
 
#Construct worksite table and populate data into database:
worksite = df[["worksite_city", "worksite_county", "worksite_state", "worksite_postal_code"]]
worksite = worksite.drop_duplicates()
worksite.insert(0, 'worksite_id', range(1, 1 + len(worksite)))
worksite.to_sql(name='worksite',con=engine, if_exists='append',index=False)
 
#Construct 'worksite_book' table and populate data into database, the merge here is also to make sure 'worksite_book' table
#has correct corresponding 'worksite_id':
worksite_book = df[["case_number", "worksite_city", "worksite_county", "worksite_state", "worksite_postal_code"]]
worksite_book = pd.merge(worksite_book, worksite, how = "left", on = ["worksite_city", "worksite_county", "worksite_state", "worksite_postal_code"])
worksite_book = worksite_book[["case_number", "worksite_id"]]
worksite_book.to_sql(name='worksite_book',con=engine, if_exists='append',index=False)
 
#Construct naics (North American Industry Classification System) table and populate data into database:
naics = df[['naics_code']]
naics = naics.drop_duplicates()
naics.insert(0, 'naics_id', range(1, 1 + len(naics)))
naics.to_sql(name='naics',con=engine, if_exists='append',index=False)
 
#Construct h1b_request_record table and populate data into database:
h1b_request_record = df[['total_workers', 'new_employment', 'continued_employment', 'change_previous_employment', 'new_concurrent_employment', 'change_employer', 'amended_petition']]
h1b_request_record = h1b_request_record.drop_duplicates()
h1b_request_record.insert(0, 'h1b_request_record_id', range(1, 1 + len(h1b_request_record)))
h1b_request_record.to_sql(name='h1b_request_record',con=engine, if_exists='append',index=False)
 
#Construct employer_address table and populate data into database:
employer_address = df[['employer_address', 'employer_city', 'employer_state', 'employer_postal_code', 'employer_country', 'employer_province']]
employer_address = employer_address.drop_duplicates()
employer_address.insert(0, 'employer_address_id', range(1, 1 + len(employer_address)))
employer_address.to_sql(name='employer_address',con=engine, if_exists='append',index=False)
 
#Construct employer table, merge with nacis table to have correct corresponding ‘naics_code’ column:
employer = df[['employer_name', 'employer_business_dba', 'h1b_dependent', 'willful_violator', 'support_h1b', 'labor_con_agree','employer_phone', 'employer_phone_ext', 'naics_code']]
 
#Merge on NAICS:
employer = pd.merge(employer, naics,  how='left', on=['naics_code'])
employer = employer[['employer_name', 'employer_business_dba', 'naics_id',
                    'h1b_dependent', 'willful_violator', 'support_h1b', 'labor_con_agree']]
 
#Populate data:
employer = employer.drop_duplicates()
employer.insert(0, 'employer_id', range(1, 1 + len(employer)))
employer.to_sql(name='employer',con=engine, if_exists='append',index=False)
 
#Construct employer_phone and populate data:
employer_phone = df[['employer_name','employer_phone', 'employer_phone_ext']]
employer_phone = employer_phone.drop_duplicates()
employer_phone = pd.merge(employer_phone, employer, how='left', on=['employer_name'])
employer_phone.insert(0, 'employer_phone_id', range(1, 1 + len(employer_phone)))
employer_phone = employer_phone[["employer_phone_id", "employer_id", "employer_phone", "employer_phone_ext"]]
employer_phone.to_sql(name='employer_phone',con=engine, if_exists='append',index=False)
 
#Construct agent_attorney table and populate data:
agent_attorney = df[["agent_attorney_name", 'agent_attorney_city', 'agent_attorney_state']]
agent_attorney = agent_attorney.drop_duplicates()
agent_attorney.insert(0, 'agent_attorney_id', range(1, 1 + len(agent_attorney)))
agent_attorney.to_sql(name='agent_attorney',con=engine, if_exists='append',index=False)
 
#Construct employer_address_book table and populate data:
employer_address_book = df[['employer_name', 'employer_address', 'employer_city', 'employer_state', 'employer_postal_code', 'employer_country', 'employer_province']]
employer_address_book = pd.merge(employer_address_book, employer, how='left', on=['employer_name'])
employer_address_book = pd.merge(employer_address_book, employer_address, how='left', on=['employer_address', 'employer_city', 'employer_state', 'employer_postal_code', 'employer_country', 'employer_province'])
employer_address_book = employer_address_book.drop_duplicates()
employer_address_book = employer_address_book[["employer_id", "employer_address_id"]]
employer_address_book.to_sql(name='employer_address_book',con=engine, if_exists='append',index=False)
 
#Construct case_submission table:
#Merge with employer and agent_attorney table:
 
case_submission = df[["case_number", 'employer_name', 'employer_business_dba', 'naics_code',  'h1b_dependent', 'willful_violator', 'support_h1b', 'labor_con_agree',  "case_submitted", "decision_date", "agent_representing_employer", "agent_attorney_name", 'agent_attorney_city', 'agent_attorney_state']]
#Merge with employer table to get corresponding id
case_submission = pd.merge(case_submission, employer, how='left', on=['employer_name', 'employer_business_dba', 'h1b_dependent', 'willful_violator', 'support_h1b', 'labor_con_agree'])
case_submission = case_submission.drop_duplicates(subset = ["case_number", "employer_name"])
case_submission = pd.merge(case_submission, agent_attorney, how='left', on=["agent_attorney_name", 'agent_attorney_city', 'agent_attorney_state'])
case_submission = case_submission[["case_number", "employer_id", "case_submitted", "decision_date", "agent_representing_employer", "agent_attorney_id"]]
case_submission = case_submission.rename(columns={"agent_representing_employer": "agent_representing_status", "case_submitted": "case_submitted_date"})
case_submission.to_sql(name='case_submission',con=engine, if_exists='append',index=False)
 
 
#Construct h1b_record_book table:
#Merge with h1b_request_record table to get corresponding h1b_request_record_id:
h1b_record_book = df[['employer_name', 'employer_business_dba',  'h1b_dependent', 'willful_violator', 'support_h1b', 'labor_con_agree', 'total_workers', 'new_employment', 'continued_employment', 'change_previous_employment',
'new_concurrent_employment', 'change_employer', 'amended_petition']]
h1b_record_book = pd.merge(h1b_record_book, h1b_request_record,  how='left', on=['total_workers', 'new_employment', 'continued_employment', 'change_previous_employment', 'new_concurrent_employment', 'change_employer', 'amended_petition'])
h1b_record_book = pd.merge(h1b_record_book, employer,  how='left', on=['employer_name', 'employer_business_dba', 'h1b_dependent', 'willful_violator', 'support_h1b', 'labor_con_agree'])
h1b_record_book = h1b_record_book[["employer_id", "h1b_request_record_id"]]
h1b_record_book = h1b_record_book.drop_duplicates()
h1b_record_book.to_sql(name='h1b_record_book',con=engine, if_exists='append',index=False)
