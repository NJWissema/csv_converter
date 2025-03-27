#**
# Class definitions for user data
#**
import csv
from user import *

#All the user data in a list
class Users:
    panalists : list[User]
    participants : list[User]
    wordpressLoaded: bool
    zoomLoaded: bool

    def __init__(self):
        self.wordpressLoaded = False
        self.zoomLoaded = False

        self.participants = []
        self.panalists = []

    def CheckIfParticipantExists(self, email) -> User:
        for user in self.participants:
            if user.compareEmail(email):
                return user
        return None
    
    def CheckIfPanalistExists(self, email) -> User:
        for user in self.panalists:
            if user.compareEmail(email):
                return user
        return None

    def loadWordpressFile(self, filename) -> bool:
        print("Beginning file loading")
        if not self.wordpressLoaded:
            with open(filename, encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile)
                header_row = next(reader)
                for i in range(header_row.__len__()):
                    header_row[i] = header_row[i].strip("\" \ufeff")
                # Header row must look like:
                correct_header_format = [
                    'First name', 
                    'Last name (surname)', 
                    'Email', 
                    'Country (Country)', 
                    'Organization / Institution', 
                    'Position', 
                    'Position Other', 
                    'Job Title', 
                    'Industry Sector', 
                    'Industry Other', 
                    'Would you like a certificate of attendance?', 
                    'Join the GGA Community (Consent)'
                ]
                opt_header_row = []
                opt_details_found: bool = False
                for line in header_row:
                    if line.__contains__("Optional certificate details"):
                        opt_details_found = True
                    else:
                        opt_header_row.append(line)
                print("Checking correct fields setup")
                if not opt_header_row == correct_header_format:
                    print("Wordpress registration incorrectly formatted: incorrect fields given")
                    print( f"Correct fields: {correct_header_format}")
                    print( f"Given fields: {opt_header_row}")
                    return False
                elif not opt_details_found:
                    print("WARNING. THE 'Optional certificate details' WERE NOT FOUND IN THE CSV FILE!!!")
                    return False
                print("Correct fields found")
                duplicate_count = 0
                for row in reader:
                    for i in range(row.__len__()):
                            row[i] = row[i].strip("\" ")
                    if ( user := self.CheckIfParticipantExists(row[2]) ) == None:
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
                            if(row[i] != ""):
                                user.addCertificateDetails(row[i])

                        user.set_gga_community_consent(row[row.__len__()-1])
                        
                        # Add this new user
                        self.participants.append(user)
                    else:
                        # print( f"Duplicate found for {row[2]}. Ignoring..." )
                        duplicate_count += 1
            self.wordpressLoaded = True
            print(f"Loading successful with {duplicate_count} duplicates")
            return True
        else:
            print("Files must be loaded in correct order!")
        return False
    
    def loadZoomFile(self, filename) -> bool:
        if not self.zoomLoaded and self.wordpressLoaded:
            with open(filename, encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile)
                state = 0
                for row in reader:
                    # Two states. 1 is panalists, 2 is participants
                    if state ==1:
                        if row[0] == "Yes":
                            if ( user := self.CheckIfPanalistExists(row[4]) ) != None:
                                user.attend_user()
                                user.append_time(int(row[5]))
                            else:
                                user = User()
                                user.set_fullname(row[1])
                                user.set_email(row[2])
                                user.attend_user()
                                user.append_time(int(row[5]))
                                user.set_country(row[7])
                                self.panalists.append(user)
                    if state == 2:
                        if ( row[0] == "Yes" and ( user := self.CheckIfParticipantExists(row[4]) ) != None):
                            user.attend_user()
                            user.append_time(int(row[9]))
                        if row[0] == "No":
                            break
                    
                    if row[0] == "Panelist Details":
                        state = 1
                    elif row[0] == "Attendee Details":
                        state = 2

            self.zoomLoaded = True
            return True
        else:
            print("Files must be loaded in correct order!")
        return False
    
    def exportBrevo(self, filename: str):
        if self.wordpressLoaded:
            data = [
                {
                    'firstname': "Firstname",
                    'lastname': "Lastname",
                    'email': "Email",
                    'country': "Country",
                    'organization': "Company",
                    'position': "Position",
                    'jobtitle': "Job Title",
                    'industry': "Industry Sector",
                    'ggaconsent': "Join the GGA Community (Consent)"
                }
            ]
            

            for user in self.participants:
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

            with open(filename, 'w', newline='', encoding="utf-8") as csvfile:
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

    def exportParticipantCertificate(self, filename: str, event_name: str, event_date: str, event_time_hr: int, event_time_min: int, event_time_threshhold: int):
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
            
            for user in self.participants:
                if user.compareEmail("chanwengkhai1@hotmail.com") and user.user_attended() and user.wants_certificate():
                    print ("chan found")
                    certification_details = user.get_certificate_details()
                    for i in range(certification_details.__len__()):
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
                            'duration': user.get_formatted_attendance_time(event_time_threshhold),
                            'opt_cert_1' : certification_details[i].get_default_format(),
                            'pb_name1' : certification_details[i].get_name(),
                            'pb_num1' : certification_details[i].get_number()
                        }

                        data.append(user_data)

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
                            'duration': user.get_formatted_attendance_time(event_time_threshhold),
                        }
                        for j in range(3):
                            if (3*i)+j < certification_details.__len__():
                                user_data[f'opt_cert_{j+1}'] = certification_details[(3*i)+j].get_default_format()
                                user_data[f'pb_name{j+1}'] = certification_details[(3*i)+j].get_name()
                                user_data[f'pb_num{j+1}'] = certification_details[(3*i)+j].get_number()

                        data.append(user_data)


            with open(filename, 'w', newline='', encoding="utf-8") as csvfile:
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
    
    def exportPanalistCertificate(self, filename: str, event_name: str, event_date: str, event_time_hr: int, event_time_min: int):
        if self.wordpressLoaded and self.zoomLoaded:
            data = [
                {
                    "event_name" : "Event_name",
                    "event_date" : "Date",
                    "event_duration_hrs" : "Event_Time",
                    "event_duration_min" : "Event Time in mins",
                    "first_name" : "First name",
                    "email" : "Email (Enter Email)",
                    "time" : "Time",
                    "fullname" : "Fullname",
                }
            ]
            
            for user in self.panalists:
                if user.user_attended():
                    user_data = {
                        'event_name': event_name,
                        'event_date': event_date,
                        'event_duration_hrs': event_time_hr,
                        'event_duration_min': event_time_min,
                        'first_name': user.get_fullname().split(" ")[0],
                        'email': user.get_email(),
                        'time': user.get_attendance_time(),
                        'fullname': user.get_fullname(),
                    }
                    data.append(user_data)

            with open(filename, 'w', newline='', encoding="utf-8") as csvfile:
                fieldnames = [
                    'event_name',
                    'event_date',
                    'event_duration_hrs',
                    'event_duration_min',
                    'first_name',
                    'email',
                    'time',
                    'fullname',
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerows(data)        
            print(f"done {filename}")
        else:
            print("Incorrect order!")
    def findUser(self, user_email) -> User:
        print(user_email)
        for user in self.participants:
            if user.compareEmail(user_email):
                print(user)
                return user
        return None