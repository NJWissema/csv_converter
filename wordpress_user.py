#
#
#
import numpy as np # type: ignore
"First name","Last name (surname)","Email","Country (Country)","Organization / Institution","Position","Position Other","Job Title","Industry Sector","Industry Other","Would you like a certificate of attendance?","Optional certificate details 1","Optional certificate details 2","Optional certificate details 3","Optional certificate details 4","Optional certificate details 5","Optional certificate details 6","Optional certificate details 7","Optional certificate details 8","Optional certificate details 9","Optional certificate details 10","Optional certificate details 11","Join the GGA Community (Consent)"
class WordpressUser:
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

    certificate: bool
    certificate_details: np.array

    def __init__(self):
        self.firstname = "TEST"
    
    def test(self):
        print(self.firstname)