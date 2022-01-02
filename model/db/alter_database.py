from datetime import datetime

from model.db.database import Subject, session, User, UserHasSubject


class Retrieve:
    def retrieve_users(self):
        """Gets all users from user table"""
        users = session.query(User)
        users = [user for user in users]
        return users

    def retrieve_users_by_email(self, email: str):
        """Gets all users with the same e-mail as the parameter"""
        if not isinstance(email, str):
            raise TypeError("Invalid datatype for e-mail.")

        users = session.query(User).filter(User.email == email)
        users = [user for user in users]

        return users

    def retrieve_subjects(self):
        """Gets all subjects from the subject table"""
        subjects = session.query(Subject)
        subjects = [subject for subject in subjects]

        return subjects

    def retrieve_subject_by_code(self, subject_code: str):
        """Gets all subjects with the same subject code as the parameter"""
        if not isinstance(subject_code, str):
            raise TypeError("Invalid datatype for subject code")

        subject_code.upper()

        subjects = session.query(Subject).filter(Subject.subject_code == subject_code)
        subjects = [subject for subject in subjects]

        return subjects

    def retrieve_user_has_subject(self):
        results = session.query(UserHasSubject)
        results = [result for result in results]

        return results


class Insert:

    def __init__(self):
        self.r = Retrieve()

    def insert_user(self, first_name, surname, dob, email, password):
        """
        Adds user to user table as long as the user have an unique email.
        Returns True if data was added successfully
        """
        if not isinstance(email, str):
            # Only need to check email datatype. All the other parameters can be checked adding into the database
            raise TypeError("Invalid datatype for email")

        if len(self.r.retrieve_users_by_email(email)) > 0:
            return False

        user = User(first_name, surname, dob, email, password)

        session.add(user)
        session.commit()

        return True

    def insert_subject(self, subject_code: str, subject_name: str):
        """
        Inserts subject into database. Checks if a subject with the same subject code has been added.
        Returns True if data was added successfully
        """
        subject_code.upper()

        if len(self.r.retrieve_subject_by_code(subject_code)) > 0:
            return False

        subject = Subject(subject_code, subject_name)

        session.add(subject)
        session.commit()

        return True

    def insert_link(self, user_id: int, subject_id):
        """
        Adds to user_has_subject table. Checks if user already has added the subject to their database
        Returns True if data was added successfully
        """
        if not isinstance(user_id, int):
            raise TypeError("Invalid datatype for user ID.")

        if not isinstance(subject_id, int):
            raise TypeError("Invalid datatype for subject ID.")

        for link in self.r.retrieve_user_has_subject():
            # Checks if the subject and user combo has already been added to the database
            if link.user_id == user_id and link.subject_id == subject_id:
                return False

        link = UserHasSubject(user_id, subject_id)

        session.add(link)
        session.commit()

        return True


class Delete:
    def __init__(self):
        self.r = Retrieve()

    def delete_user(self, email):
        """Deletes a user from the users table. Returns True if the user was successfully deleted"""
        if not isinstance(email, str):
            raise TypeError("Invalid datatype for e-mail.")

        deleted = False
        users = self.r.retrieve_users_by_email(email)

        if len(users) <= 0:
            return deleted

        for user in users:
            session.delete(user)
            session.commit()
            self.delete_link(user_id=user.user_id)
            deleted = True

        return deleted

    def delete_subject(self, subject_code: str):
        """Deletes a subject from the subjects table. Returns True if the subject was successfully deleted"""
        if not isinstance(subject_code, str):
            raise TypeError("Invalid datatype for subject code.")

        deleted = False
        subjects = self.r.retrieve_subject_by_code(subject_code)

        if len(subjects) <= 0:
            return deleted

        for subject in subjects:
            session.delete(subject)
            session.commit()
            self.delete_link(subject_id=subject.subject_id)
            deleted = True

        return deleted

    def delete_link(self, user_id=0, subject_id=0):
        """Deletes link from user_has_subject table. Returns True if link was successfully deleted"""
        if not isinstance(user_id, int):
            raise TypeError("Invalid datatype for user ID.")

        if not isinstance(subject_id, int):
            raise TypeError("Invalid datatype for subject ID.")

        deleted = False
        links = self.r.retrieve_user_has_subject()
        if len(links) <= 0:
            return deleted

        for link in links:
            # Checks if the cause of link delete is a deleted user
            if user_id != 0:
                if link.user_id == user_id:
                    session.delete(link)
                    session.commit()
                    deleted = True

            # Checks if the cause of link delete is a deleted subject
            if subject_id != 0:
                if link.subject_id == subject_id:
                    session.delete(link)
                    session.commit()
                    deleted = True

        return deleted

"""
i = Insert()
print("INSERT")
print(i.insert_subject("TDT4100", "Objektorientert programmering"))
print(i.insert_user("Jathavaan", "Shankarr", datetime(2001, 7, 12), "jathavaan12@gmail.com", "Jathavaan12"))
print(i.insert_link(1, 1))

print()

d = Delete()
print("DELETE")
print(d.delete_subject("TDT4100"))
print(d.delete_user("jathavaan12@gmail.com"))

print()
"""
