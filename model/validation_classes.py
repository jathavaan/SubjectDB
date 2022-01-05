import re
from datetime import datetime


class User:
    def __init__(self, first_name: str, surname: str, dob: datetime, email: str, password: str, is_admin=False):
        self.__first_name = None
        self.__surname = None
        self.__dob = None
        self.__email = None
        self.__password = None
        self.__is_admin = is_admin

        self.set_first_name(first_name)
        self.set_surname(surname)
        self.set_dob(dob)
        self.set_email(email)
        self.set_password(password)
        self.set_admin(is_admin)

    def get_first_name(self) -> str:
        return self.__first_name

    def set_first_name(self, first_name: str):
        self.__validate_first_name(first_name)
        self.__first_name = first_name

    def get_surname(self) -> str:
        return self.__surname

    def set_surname(self, surname: str):
        self.__validate_surname(surname)
        self.__surname = surname

    def get_dob(self) -> datetime:
        return self.__dob

    def set_dob(self, dob: datetime):
        self.__validate_dob(dob)
        self.__dob = dob

    def get_email(self) -> str:
        return self.__email

    def set_email(self, email: str):
        self.__validate_email(email)
        self.__email = email

    def get_password(self) -> str:
        return self.__password

    def set_password(self, password: str):
        self.__validate_password(password)
        self.__password = password

    def set_admin(self, is_admin: bool):
        if not isinstance(is_admin, bool):
            raise TypeError("Invalid datatype for admin state.")

        self.__is_admin = is_admin

    def get_admin(self) -> bool:
        return self.__is_admin




    def __validate_first_name(self, first_name: str):
        """Validation for first name"""
        if not isinstance(first_name, str):
            raise TypeError("Invalid datatype for first name")

        if not first_name or first_name is None:
            raise ValueError("First name cannot be empty")

        if len(first_name) < 2:
            raise ValueError("First name has to at least two characters long.")

        pattern = re.compile("^[a-zA-Z](?:[ '\-a-zA-Z]*[a-zA-Z])?$")  # Does not accept norwegian letters

        if not pattern.match(first_name):
            raise ValueError("Invalid first name. First name can only contain letters, hyphens and apostrophes.")

    def __validate_surname(self, surname: str):
        """Validation for surname"""
        if not isinstance(surname, str):
            raise TypeError("Invalid datatype for first name")

        if not surname or surname is None:
            raise ValueError("Surname cannot be empty")

        if len(surname) < 2:
            raise ValueError("Surname has to at least two characters long.")

        pattern = re.compile("^[a-zA-Z](?:[ '\-a-zA-Z]*[a-zA-Z])?$")  # Does not accept norwegian letters

        if not pattern.match(surname):
            raise ValueError("Invalid surname. Surname can only contain letters, hyphens and apostrophes.")

    def __validate_dob(self, dob: datetime):
        """Validation for date of birth"""
        if not isinstance(dob, datetime):
            raise TypeError("Invalid datatype for date of birth.")

        if dob is None:
            raise ValueError("Date of birth cannot be null")

        if not dob <= datetime.now():
            raise ValueError("Date of birth cannot be in the future")

    def __validate_email(self, email: str):
        """Validation for e-mail"""
        if not isinstance(email, str):
            raise TypeError("Invalid datatype for email.")

        if not email or email is None:
            raise ValueError("E-mail cannot be empty")
        """
        pattern = re.compile("^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$")
        if not pattern.match(email):
            raise ValueError("Invalid e-mail.")
        """

    def __validate_password(self, password: str):
        """Validation for password"""
        if not isinstance(password, str):
            raise TypeError("Invalid datatype for password.")

        if not password or password is None:
            raise ValueError("Password cannot be empty.")

        pattern = re.compile("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")

        if not pattern.match(password):
            raise ValueError(
                "Password is not strong enough. Please make sure the password meets the following requirements: "
                "\n=>At least eight characters long. "
                "\n=>At least one letter. "
                "\n=>At least one number"
            )


class Subject:
    def __init__(self, subject_code: str, subject_name: str):
        self.__subject_code = None
        self.__subject_name = None

        self.set_subject_code(subject_code)
        self.set_subject_name(subject_name)

    def get_subject_code(self) -> str:
        return self.__subject_code

    def set_subject_code(self, subject_code: str):
        self.__validate_subject_code(subject_code)
        self.__subject_code = subject_code

    def get_subject_name(self) -> str:
        return self.__subject_name

    def set_subject_name(self, subject_name: str):
        self.__validate_subject_name(subject_name)
        self.__subject_name = subject_name

    def __validate_subject_id(self, subject_id: int):
        if not isinstance(subject_id, int):
            raise TypeError("Invalid datatype for subject ID.")

        if not subject_id <= 1:
            raise ValueError("Subject ID cannot be less than 1.")

    def __validate_subject_code(self, subject_code: str):
        if not isinstance(subject_code, str):
            raise TypeError("Invalid datatype for subject code.")

        if not subject_code or subject_code is None:
            raise ValueError("Subject code cannot be empty.")

        valid_letter_codes = [
            "TDT", "TET", "TFE", "TFY", "TMA", "TTK", "TTM", "TMT", "TTT", "TBA", "TEP", "TGB",
            "TKT", "TME", "TMM", "TMR", "TPD", "TPG", "TPK", "TVM", "TIØ",
            "BK", "AAR", "EXPH", "EXFAC", "HFEL", "AFR", "ALIT", "ANT",
            "ARK", "AVS", "DANS", "DRA", "ENG", "FI", "FFV", "FILM", "FON",
            "FRA", "GRE", "HIST", "ITA", "KULT", "KRL", "KUH", "LAT",
            "LING", "MUSP", "MUST", "MUSV", "MVIT", "NFU", "NORD", "RVI",
            "SAM", "SWA", "TYSK", "RFEL", "IT", "MA", "ST", "GEOL", "AK",
            "BI", "BO", "FY", "KJ", "ZO", "SFEL", "AFR", "FPED", "GEOG",
            "HLS", "IDR", "MVIT", "PED", "POL", "PPU", "PSY", "PSYPRO",
            "SARB", "SAM", "SANT", "SANT", "SOS", "SPED", "SØK", "ØKAD", "MD"
        ]

        letter_code = ""
        number_code = ""

        for char in subject_code:
            if char.isalpha():
                letter_code += char
            elif char.isnumeric():
                number_code += char
            else:
                raise ValueError("Invalid subject code. " + char + " is an invalid character.")

        letter_code = letter_code.upper()  # Sets subject code to upper case letters

        if letter_code not in valid_letter_codes:
            raise ValueError(letter_code + " is not a valid letter code.")

        if len(number_code) != 4:
            raise ValueError("Number code has to be exactly 4 numbers long")

    def __validate_subject_name(self, subject_name: str):
        if not isinstance(subject_name, str):
            raise TypeError("Invalid datatype for subject name.")

        if not subject_name or subject_name is None:
            raise ValueError("Subject name cannot be empty")

        pattern = re.compile("^[\.a-zA-Z0-9,!? ]*$")
        if not pattern.match(subject_name):
            raise ValueError("Invalid subject name.")
