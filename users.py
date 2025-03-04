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
        #Fields are commented!
        '''
        "First name",
        "Last name (surname)",
        "Email",
        "Country (Country)",
        "Organization / Institution",
        "Position",
        "Position Other",
        "Job Title",
        "Industry Sector",
        "Industry Other",
        "Would you like a certificate of attendance?",
        "Optional certificate details 1",
        "Optional certificate details 2",
        "Optional certificate details 3",
        "Optional certificate details 4",
        "Optional certificate details 5",
        "Optional certificate details 6",
        "Optional certificate details 7",
        "Optional certificate details 8",
        "Optional certificate details 9",
        "Optional certificate details 10",
        "Optional certificate details 11",
        "Join the GGA Community (Consent)"
        '''
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
                        user.set_certificate(row[10]=="Yes")

                        for i in range(11, row.__len__()-1):
                            print(row[i])
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
        '''
        Attended,
        User Name (Original Name),
        First Name,
        Last Name,
        Email,
        Registration Time,
        Approval Status,
        Join Time,
        Leave Time,
        Time in Session (minutes),
        Is Guest,Country/Region Name
        '''
        if not self.zoomLoaded and self.wordpressLoaded:
            with open(filename, encoding="utf8") as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                for row in reader:
                    if ( row[0] == "Yes" and ( user := self.CheckIfExists(row[4]) ) != None):
                        user.userAttended()
                        user.appendTime(int(row[9]))

            self.zoomLoaded = True
            return True
        else:
            print("Files must be loaded in correct order!")
        return False
    
    def exportBrevo(self, filename: str):
        if self.wordpressLoaded:
            pass

    def exportCertificate(self, filename: str):
        if self.wordpressLoaded and self.zoomLoaded:
            pass