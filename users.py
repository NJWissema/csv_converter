#**
# Class definitions for user data
#**
import csv
import numpy as np # type: ignore

from user import *

#All the user data in a list
class Users:
    users : list[User]
    wordpressLoaded: bool
    zoomLoaded: bool

    def __init__(self):
        self.wordpressLoaded = False
        self.zoomLoaded = False

        self.users = []

    def CheckIfExists(self, email) -> User:
        for user in self.users:
            if user.compareEmail(email):
                return user
        return None

    def loadWordpressFile(self, filename) -> bool:
        if not self.wordpressLoaded:
            with open(filename, encoding="utf8") as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                for row in reader:
                    for i in range(row.__len__()):
                            row[i] = row[i].strip("\" ")
                    if ( user := self.CheckIfExists(row[2]) ) == None:
                        user = User()
                        user.set_firstname(row[0])
                        user.set_lastname(row[1])
                        user.set_email(row[2])
                        user.set_country(row[3])
                        user.set_organization(row[4])
                        user.set_position(row[5])
                        user.set_position_other(row[6])
                        user.set_job_title(row[7])
                        user.set_industry_sector(row[8])
                        user.set_industry_other(row[9])
                        user.set_certificate(row[10])

                        for i in range(11, row.__len__()-1):
                            user.addCertificateDetails(row[i])

                        user.set_gga_community_consent(row[row.__len__()-1])
                        
                        # Add this new user
                        self.users.append(user)
                    else:
                        print( f"Duplicate found for {row[2]}. Ignoring..." )
            self.wordpressLoaded = True
            return True
        else:
            print("Files must be loaded in correct order!")
        return False
    
    def loadZoomFile(self, filename) -> bool:
        if not self.zoomLoaded and self.wordpressLoaded:
            with open(filename, encoding="utf8") as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                for row in reader:
                    if ( row[0] == "Yes" and ( user := self.CheckIfExists(row[4]) ) != None):
                        user.attend_user()
                        user.append_time(int(row[9]))

            self.zoomLoaded = True
            return True
        else:
            print("Files must be loaded in correct order!")
        return False
    
    def exportBrevo(self, filename: str):
        if self.wordpressLoaded:
            data = [
                {
                    'firstname': "First name",
                    'lastname': "Last name (surname)",
                    'email': "Email",
                    'country': "Country (Country)",
                    'organization': "Organization / Institution",
                    'position': "Position",
                    'jobtitle': "Job Title",
                    'industry': "Industry Sector",
                    'ggaconsent': "Join the GGA Community (Consent)"
                }
            ]
            

            for user in self.users:
                if user.is_gga_consenting():
                    data.append({
                        'firstname': user.get_firstname(),
                        'lastname': user.get_lastname(),
                        'email': user.get_email(),
                        'country': user.get_country(),
                        'organization': user.get_organization(),
                        'position': user.get_position(),
                        'jobtitle': user.get_job_title(),
                        'industry': user.get_industry_sector(),
                        'ggaconsent': user.get_gga_community_consent()
                    })

            with open(filename, 'w', newline='', encoding="utf8") as csvfile:
                fieldnames = [
                    'firstname', 
                    'lastname', 
                    'email', 
                    'country', 
                    'organization', 
                    'position', 
                    'jobtitle', 
                    'industry', 
                    'ggaconsent'
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerows(data)        
            print(f"done {filename}")
        else:
            print("Incorrect order!")

    def exportCertificate(self, filename: str, event_name: str, event_date: str, event_time_hr: int, event_time_min: int, event_time_threshhold: int):
        if self.wordpressLoaded and self.zoomLoaded:
            data = [
                {
                    "event_name" : "Event_name",
                    "event_date" : "Date",
                    "event_duration_hrs" : "Event_Time",
                    "event_duration_min" : "Event Time in mins",
                    "event_threshhold_min" : "Full event threshold mins",
                    "first_name" : "First name",
                    "last_name" : "Last name (surname)",
                    "email" : "Email (Enter Email)",
                    "time" : "Time",
                    "opt_cert_1" : "Optional certificate details 1",
                    "opt_cert_2" : "Optional certificate details 2",
                    "opt_cert_3" : "Optional certificate details 3",
                    "fullname" : "Fullname",
                    "duration" : "Duration",
                    "pb_name1" : "PBName_1",
                    "pb_num1" : "PBNumber_1",
                    "pb_name2" : "PBName_2",
                    "pb_num2" : "PBNumber_2",
                    "pb_name3" : "PBName_3",
                    "pb_num3" : "PBNumber_3"
                }
            ]
            
            for user in self.users:
                if user.user_attended() and user.wants_certificate() and not user.compareEmail("chanwengkhai1@hotmail.com"):
                    certification_details = user.get_certificate_details()
                    for i in range(0, 1+int((certification_details.__len__()-1)/3)):
                        user_data = {
                            'event_name': event_name,
                            'event_date': event_date,
                            'event_duration_hrs': event_time_hr,
                            'event_duration_min': event_time_min,
                            'event_threshhold_min': event_time_threshhold,
                            'first_name': user.get_firstname(),
                            'last_name': user.get_lastname(),
                            'email': user.get_email(),
                            'time': user.get_attendance_time(),
                            'fullname': user.get_fullname(),
                            'duration': user.get_formatted_attendance_time(),
                        }
                        for j in range(3):
                            if (3*i)+j < certification_details.__len__():
                                user_data[f'opt_cert_{j+1}'] = certification_details[(3*i)+j].get_default_format()
                                user_data[f'pb_name{j+1}'] = certification_details[(3*i)+j].get_name()
                                user_data[f'pb_num{j+1}'] = certification_details[(3*i)+j].get_number()

                        data.append(user_data)


            with open(filename, 'w', newline='', encoding="utf8") as csvfile:
                fieldnames = [
                    'event_name',
                    'event_date',
                    'event_duration_hrs',
                    'event_duration_min',
                    'event_threshhold_min',
                    'first_name',
                    'last_name',
                    'email',
                    'time',
                    'opt_cert_1',
                    'opt_cert_2',
                    'opt_cert_3',
                    'fullname',
                    'duration',
                    'pb_name1',
                    'pb_num1',
                    'pb_name2',
                    'pb_num2',
                    'pb_name3',
                    'pb_num3'
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerows(data)        
            print(f"done {filename}")
        else:
            print("Incorrect order!")
    
    def findUser(self, user_email) -> User:
        print(user_email)
        for user in self.users:
            if user.compareEmail(user_email):
                print(user)
                return user
        return None