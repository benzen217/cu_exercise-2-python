# Code Written by Ben Janzen

# Imports
import pandas as pd
import numpy as np
from datetime import datetime

# Load data into dataframes
df_enrollments = pd.read_csv('enrollments.csv')
df_students = pd.read_csv('students.csv')

# 1 - Join datasets together using term and id
df_stu_enrl = df_students.merge(df_enrollments, on=['student_id','term_id'], how='inner')

# 2 - Retain students with more than 90 earned credits
df_stu_enrl = df_stu_enrl.loc[df_stu_enrl['credits_earned'] > 90] 

# 3 - Calculate the student's current age

# Convert date_of_birth to a datetime
df_stu_enrl['date_of_birth'] = pd.to_datetime(df_stu_enrl['date_of_birth'])

def calc_age(dob):
    """Use a date formatted date of birth to calculate a person's age."""
    today = datetime.now()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

# Add age column and run the calc_age function to calculate the student's age
df_stu_enrl['age'] = df_stu_enrl['date_of_birth'].apply(calc_age)

# 4 - Split the class_id into multiple columns

#Create 4 new columns based on splitting the class_id column
df_stu_enrl[['course_subject','placeholder','course_number','course_section']] = df_stu_enrl['class_id'].str.split('-',expand=True)
#drop the placeholder column
df_stu_enrl.drop('placeholder',inplace=True, axis=1)

# 5 - Concat All Student Majors

# Create new dataframe to get students and their major
df_acad_plans = df_students[['student_id','major']].copy()
# Remove any duplicate majors for a student
df_acad_plans = df_acad_plans.drop_duplicates()
# Concat the majors to create the academic plans
df_acad_plans['academic_plans'] = df_acad_plans.groupby('student_id')['major'].transform(';'.join)
# Remove no longer needed major column and remove duplicates
df_acad_plans.drop('major', inplace=True, axis=1)
df_acad_plans = df_acad_plans.drop_duplicates()
# Merge the academic plans dataframe with the student enrollment dataframe
df_stu_enrl = df_stu_enrl.merge(df_acad_plans, on='student_id', how='inner')
# Drop the major column from df_stu_enrl as it is no longer needed
df_stu_enrl.drop('major', inplace=True, axis=1)
# Remove duplicate records from dataset
df_stu_enrl = df_stu_enrl.drop_duplicates()

# 6 - Export the dataframe to a CSV file

#Fix formatting on columns for export
df_stu_enrl['enrollment_id'] = df_stu_enrl['enrollment_id'].astype(np.int64)
df_stu_enrl['student_id'] = df_stu_enrl['student_id'].astype(np.int64)
df_stu_enrl['credits_earned'] = df_stu_enrl['credits_earned'].astype(np.int64)
df_stu_enrl['student_employee'] = df_stu_enrl['student_employee'].astype(np.int64)
# Note: If using Linux convert # to -
df_stu_enrl['date_of_birth'] = df_stu_enrl['date_of_birth'].dt.strftime('%#m/%#d/%y')

#Prepare Order for Export
df_stu_enrl = df_stu_enrl[['enrollment_id','term_id','course_title','class_id','grade','student_id',
                           'first_name','last_name','credits_earned','date_of_birth','student_employee',
                           'gpa','age','course_subject','course_number','course_section','academic_plans']]

def export_csv(out_file, out_frame):
    """export csv file, out_file is the name of the file, do not include .csv. \
        out_frame is the dataframe you wish to export."""
    
    out_file = out_file + '.csv'
    out_frame.to_csv(out_file,index=False)

# Export the data to csv
export_csv('results',df_stu_enrl)