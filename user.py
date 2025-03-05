# Cerificate details
class CertificateDetails:
    name: str = ""
    number: str = ""
    def __init__(self, details: list[str]):
        if details.__len__() == 2:
            if details[0]!="" and details[1]!="":
                self.name = details[0]
                self.number = details[1]
        else:
            raise Exception("Certificate details incorrect format")
    
    def get_default_format(self) -> str:
        return f"{self.name} | {self.number}"
    def get_name(self) -> str:
        return self.name
    def get_number(self) ->str:
        return self.number

    def __str__(self):
        return f"{self.name},{self.number}"
    def __repr__(self):
        return f"CertificateDetails({self.name}, {self.number})"

# User data stored in one structure
class User:
    firstname: str
    lastname: str
    email: str
    country: str
    organization: str

    position: str
    position_other: str
    job_title: str

    industry_sector: str
    industry_other: str

    certificate: bool = False
    certificate_details: list[CertificateDetails]

    gga_community_consent: bool

    attended: bool = False
    attended_time: int = 0

    def __init__(self, userData: list[str] = None):
        self.handleInput(userData)
        self.certificate_details = []


    def __eq__(self, value):
        if type(value) is User:
            return self.email.lower().strip() == value.email.lower().strip()
        else:
            return False

    def __str__(self):
        return( f"{self.firstname}, {self.lastname}, {self.email}, {self.country}, {self.organization}, {self.position}, {self.position_other}, {self.job_title}, {self.industry_sector}, {self.industry_other}, {self.certificate}, {self.certificate_details}, {self.gga_community_consent}, {self.attended}, {self.attended_time}")

    def handleInput(self, userData: list[str]):
        # self.firstname = userData[0]
        pass
    
    def addCertificateDetails(self, certificateDetails: str):
        if certificateDetails.__len__() != 0:
            self.certificate_details.append(CertificateDetails(certificateDetails.split("|")))
    def get_certificate_details(self):
        return self.certificate_details
    
    def compareEmail(self, email: str) -> bool:
        return self.email.lower() == email.lower()
    
    def append_time(self, val: int):
        self.attended_time += val
    def get_attendance_time(self):
        return self.attended_time
    def get_formatted_attendance_time(self):
        return self.attended_time
    def attend_user(self):
        self.attended = True
    def user_attended(self) -> bool:
        return self.attended

    def get_firstname(self) -> str:
        firstname = ""
        for name_part in self.firstname.split(" "):
            firstname += name_part.lower()
        return self.firstname
    
    def set_firstname(self, val: str):
        self.firstname = val

    def get_lastname(self) -> str:
        return self.lastname
    def set_lastname(self, val: str):
        self.lastname = val

    def get_fullname(self) -> str:
        return self.firstname + self.lastname

    def get_email(self) -> str:
        return self.email
    def set_email(self, val: str):
        self.email = val

    def get_country(self) -> str:
        return self.country
    def set_country(self, val: str):
        self.country = val

    def get_organization(self) -> str:
        return self.organization
    def set_organization(self, val: str):
        self.organization = val
        
    def get_position(self) -> str:
        return self.position
    def set_position(self, val: str):
        self.position = val
        
    def get_position_other(self) -> str:
        return self.position_other
    def set_position_other(self, val: str):
        self.position_other = val
    
    def get_job_title(self) -> str:
        return self.job_title
    def set_job_title(self, val: str):
        self.job_title = val
    
    def get_industry_sector(self) -> str:
        return self.industry_sector
    def set_industry_sector(self, val: str):
        self.industry_sector = val
    
    def get_industry_other(self) -> str:
        return self.industry_other
    def set_industry_other(self, val: str):
        self.industry_other = val
    
    def wants_certificate(self) -> bool:
        return self.certificate
    def set_certificate(self, val: str):
        self.certificate = val =="Yes"
    
    
    def is_gga_consenting(self) -> bool:
        return self.gga_community_consent
    def get_gga_community_consent(self) -> str:
        if self.gga_community_consent:
            return "Checked"
        return "Not Checked"
    def set_gga_community_consent(self, val: str):
        self.gga_community_consent = (val == "Checked")

