data contains the csv file for the survey

read_data contains read.py which can be executed to test the
GenderSurveyQuestions class.  
>> python read_data.py

This GenderSurveyQuestions class is an object that reads in the csv
file when initialized.  
>> GSQ = GenderSurveyQuestions('../data/survey_responses.csv')

The csv file must have no header (data/survey_responses.csv already
has the header removed).

There are methods in GenderSurveyQuestions that allow you to find out
how many respondents provieded a certain answer.