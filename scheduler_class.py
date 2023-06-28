# -*- coding: utf-8 -*-
import re
import pandas as pd
import itertools
from IPython import display as ICD

class CourseScheduleExtractor:
    def __init__(self, schedule_string, courses):
        self.schedule_string = schedule_string
        self.courses = courses
        
    def extract_course_info(self):
        pattern = r'(\b[A-Z]{3} \d{3}-\d+)\s+(.+)\s+([A-Za-zÇçĞğİıÖöŞşÜü\s]+)\s+header'
        matches = re.findall(pattern, self.schedule_string)
        course_info_list = []
        new_str= self.schedule_string.split('header=[Hint] body=[Syllabus]')
        #print(new_str)
        for match in matches:
            #weekdays = []
            #hours = []
            lecture_hours = []
            i = matches.index(match)
            #print(i)
            course = match[0].strip().split('-')
            course_code = course[0].split(' ')[0] + '-' + course[0].split(' ')[1]
            section_number = course[1]
            course_name = match[1].strip()
            instructor_name = match[2].strip()
            parts = re.findall(r'(Mon|Tue|Wed|Thu|Fri) (\d{2}:\d{2}-\d{2}:\d{2})', new_str[i])
            for part in parts:
                #weekdays.append(part[0])
                #hours.append(part[1])
                if part[1] == '13:30-17:20':
                    lecture_hours.append(part[0] + ' ' + '13:30-15:20')
                    lecture_hours.append(part[0] + ' ' + '15:30-17:20')
                elif part[1] == '08:30-12:20':
                    lecture_hours.append(part[0] + ' ' + '08:30-10:20')
                    lecture_hours.append(part[0] + ' ' + '10:30-12:20')
                else:
                    lecture_hours.append(part[0] + ' ' + part[1])
            course_info = {
                "Course Code": course_code,
                "Section Number": section_number,
                "Course Name": course_name,
                "Instructor Name": instructor_name,
                #"Weekdays": weekdays,
                #"Hours": hours,
                "Lecture Hours": lecture_hours
            }
            course_info_list.append(course_info)
        return course_info_list
    
    def get_course_info(self, course_code):
        course_info_list = self.extract_course_info()
        course_codes = list(set(course_info["Course Code"] for course_info in course_info_list))
        course_codes.sort()
        filtered_courses = []
        for course in range(len(course_codes)):
            filtered_courses.append([course_info for course_info in course_info_list if course_info["Course Code"] == str(course_codes[course])])
        return filtered_courses[course_codes.index(course_code)]
    
    def get_courses(self):
        course_info_list = self.extract_course_info()
        course_codes = list(set(course_info["Course Code"] for course_info in course_info_list))
        course_codes.sort()
        print('All courses: ', course_codes, '\n')
    
    def get_course_combinations(self):
        courses = self.courses
        sec_num_lists = []
        for course in courses:
            course_section_list = self.get_course_info(course)
            total_section_number = len(course_section_list)
            #print(course + ' has ' + str(total_section_number) + ' sections')
            sec_num_list = []
            for i in range(total_section_number):
                sec_num_list.append(i+1)
            sec_num_lists.append(sec_num_list)
        course_combinations = list(itertools.product(*sec_num_lists))
        return course_combinations
    
    def get_lecture_hours(self, course, section_num):
        course_section_list = self.get_course_info(course)
        hours = course_section_list[section_num-1]['Lecture Hours']
        return hours
    
    def get_useful_combinations(self):
        combinations = self.get_course_combinations()
        useful_combinations = []
        for combination in combinations:
            lecture_hours = []
            for i in range(len(self.courses)):
                lecture_hour = self.get_lecture_hours(self.courses[i], combination[i])
                for j in range(len(lecture_hour)):
                    lecture_hours.append(lecture_hour[j])
            old_len = len(lecture_hours)
            lecture_hours = list( dict.fromkeys(lecture_hours) )
            if len(lecture_hours) == old_len:
                useful_combinations.append(combination)
        return useful_combinations
    
    def get_schedules(self):
        rows=['1', '2', '3', '4', 'L', '5', '6', '7', '8']
        cols=['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
        useful_combinations = self.get_useful_combinations()
        df = pd.DataFrame(index=rows, columns=cols, data='')
        print('Selected courses: ', self.courses, '\n')
        print('Number of schedules found: ' + str(len(useful_combinations)), '\n')
        schedules = []
        for combination in useful_combinations:
            df = pd.DataFrame(index=rows, columns=cols, data='')
            
            for i in range(len(self.courses)):
                course = self.courses[i]
                print(course + ' Section: ' + str(combination[i]))
                hours = self.get_lecture_hours(self.courses[i], combination[i])
                for j in range(len(hours)):
                    if hours[j].split(' ')[1] == '08:30-10:20':
                        df.loc['1', hours[j].split(' ')[0]] = course + '-' + str(combination[i])
                        df.loc['2', hours[j].split(' ')[0]] = course + '-' + str(combination[i])
                    elif hours[j].split(' ')[1] == '10:30-12:20':
                        df.loc['3', hours[j].split(' ')[0]] = course + '-' + str(combination[i])
                        df.loc['4', hours[j].split(' ')[0]] = course + '-' + str(combination[i])
                    elif hours[j].split(' ')[1] == '13:30-15:20':
                        df.loc['5', hours[j].split(' ')[0]] = course + '-' + str(combination[i])
                        df.loc['6', hours[j].split(' ')[0]] = course + '-' + str(combination[i])
                    elif hours[j].split(' ')[1] == '15:30-17:20':
                        df.loc['7', hours[j].split(' ')[0]] = course + '-' + str(combination[i])
                        df.loc['8', hours[j].split(' ')[0]] = course + '-' + str(combination[i])
            schedules.append(df)            
            ICD.display(df)
        return schedules