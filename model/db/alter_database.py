from sqlalchemy import or_

from model.db.database import Subject, session, User, UserHasSubject, Grade


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
        subjects = session.query(Subject). \
            order_by(Subject.subject_code.asc()) \
            .order_by(Subject.subject_name.asc())

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

    def search_user_subjects(self, user_id: int, query: str):
        """Returns a search result for user subjects"""
        if not isinstance(user_id, int):
            raise TypeError("Invalid datatype for user ID.")

        if not isinstance(query, str):
            raise TypeError("Invalid datatype for query.")

        if len(query) < 3:
            raise ValueError("Please write three or more letters to search.")

        results = session.query(UserHasSubject, User, Subject, Grade) \
            .join(User) \
            .join(Subject) \
            .join(Grade) \
            .filter(User.user_id == user_id) \
            .filter(or_(
            Subject.subject_code.like('%' + query + '%'),
            Subject.subject_name.like('%' + query + '%')
        )) \
            .order_by(Subject.subject_code.asc()) \
            .order_by(Subject.subject_name.asc()) \
            .all()

        results = [result for result in results]
        return results

    def retrieve_user_subjects(self, user_id: int):
        """Returns the subjects the user has added to their database and the grade"""
        if not isinstance(user_id, int):
            raise TypeError("Invalid datatype for user ID.")

        results = session.query(UserHasSubject, User, Subject, Grade) \
            .join(User) \
            .join(Subject) \
            .join(Grade) \
            .filter(User.user_id == user_id) \
            .order_by(Subject.subject_code.asc()) \
            .order_by(Subject.subject_name.asc()) \
            .all()

        results = [result for result in results]

        return results

    def search_subjects(self, query: str):
        """Returns a search result for admin subjects"""
        if not isinstance(query, str):
            raise TypeError("Invalid datatype for query.")

        if len(query) < 3:
            raise ValueError("Please write three or more letters to search.")

        results = session.query(Subject) \
            .filter(or_(
            Subject.subject_code.like('%' + query + '%'), Subject.subject_name.like('%' + query + '%'))) \
            .order_by(Subject.subject_code.asc()) \
            .order_by(Subject.subject_name.asc()) \
            .all()

        results = [result for result in results]
        return results

    def retrieve_user_has_subject(self):
        results = session.query(UserHasSubject).all()
        results = [result for result in results]

        return results

    def retrieve_grades(self):
        grades = session.query(Grade).all()
        grades = [grade for grade in grades]

        return grades

    def retrieve_top_grades(self, user_id: int):
        """The four subjects with the highets grades"""
        grades = session.query(UserHasSubject, User, Subject, Grade) \
            .join(User) \
            .join(Subject) \
            .join(Grade) \
            .filter(User.user_id == user_id) \
            .order_by(Grade.grade_value.asc()) \
            .order_by(Subject.credits.desc()) \
            .limit(4)

        grades = [grade for grade in grades]

        results = []

        for _ in grades:
            link, user, subject, grade = _
            data = {
                'subject_code': subject.subject_code,
                'subject_name': subject.subject_name,
                'credits': subject.credits,
                'grade': grade.grade_value
            }

            results.append(data)

        return results


class Insert:

    def __init__(self):
        self.r = Retrieve()

    def insert_user(self, first_name, surname, dob, email, password, is_admin):
        """
        Adds user to user table as long as the user have an unique email.
        Returns True if data was added successfully
        """
        if not isinstance(email, str):
            # Only need to check email datatype. All the other parameters can be checked adding into the database
            raise TypeError("Invalid datatype for email")

        if len(self.r.retrieve_users_by_email(email)) > 0:
            return False

        user = User(first_name, surname, dob, email, password, is_admin)

        session.add(user)
        session.commit()

        return True

    def insert_subject(self, subject_code: str, subject_name: str, credits: float):
        """
        Inserts subject into database. Checks if a subject with the same subject code has been added.
        Returns True if data was added successfully
        """
        subject_code.upper()

        if len(self.r.retrieve_subject_by_code(subject_code)) > 0:
            return False

        subject = Subject(subject_code, subject_name, credits)

        session.add(subject)
        session.commit()

        return True

    def insert_link(self, user_id: int, subject_id: int, grade_id=1):
        """
        Adds to user_has_subject table. Checks if user already has added the subject to their database.
        Is also possible to add a grade
        Returns True if data was added successfully
        """
        if not isinstance(user_id, int):
            raise TypeError("Invalid datatype for user ID.")

        if not isinstance(subject_id, int):
            raise TypeError("Invalid datatype for subject ID.")

        if not isinstance(grade_id, int):
            raise TypeError("Invalid datatype for grade ID.")

        for link in self.r.retrieve_user_has_subject():
            # Checks if the subject and user combo has already been added to the database
            if link.user_id == user_id and link.subject_id == subject_id:
                return False

        link = UserHasSubject(user_id, subject_id, grade_id)

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

    def user_delete_subject(self, user_id: int, subject_id: int):
        if not isinstance(user_id, int):
            raise TypeError("Invalid datatype for user ID.")

        if not isinstance(subject_id, int):
            raise TypeError("Invalid datatype for subject ID")

        deleted = False
        links = self.r.retrieve_user_has_subject()

        for link in links:
            if link.user_id == user_id and link.subject_id == subject_id:
                session.delete(link)
                session.commit()
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
            # Checks if the cause of link-delete is a deleted user
            if user_id != 0:
                if link.user_id == user_id:
                    session.delete(link)
                    session.commit()
                    deleted = True

            # Checks if the cause of link-delete is a deleted subject
            if subject_id != 0:
                if link.subject_id == subject_id:
                    session.delete(link)
                    session.commit()
                    deleted = True

        return deleted


class Modify:
    def __init__(self):
        self.r = Retrieve()

    def admin_modify_subject(self, subject_id: int, subject_code=None, subject_name=None, credits=float(0)):
        if not isinstance(subject_id, int):
            raise TypeError("Invalid datatype for subject ID.")

        sub = next(filter(lambda subject: subject.subject_id == subject_id, self.r.retrieve_subjects()))

        if subject_code is not None:
            if not isinstance(subject_code, str):
                raise TypeError("Invalid datatype for subject code")

            Subject(subject_code, sub.subject_name, credits)  # Subject code validation

        if subject_name is not None:
            if not isinstance(subject_name, str):
                raise TypeError("Invalid datatype for subject name.")

            Subject(sub.subject_code, subject_name, credits)  # Subject name validation

        if credits is not None:
            if not isinstance(credits, float) or credits is None:
                raise TypeError("Invalid datatype for credits.")

            Subject(sub.subject_code, sub.subject_name, credits)  # Credits validation

        updated = False

        # Checks if the user wants to edit subject code, subject name or both
        if subject_code is not None:
            session.query(Subject) \
                .filter(Subject.subject_id == subject_id) \
                .update({Subject.subject_code: subject_code})

            updated = True

        if subject_name is not None:
            session.query(Subject) \
                .filter(Subject.subject_id == subject_id) \
                .update({Subject.subject_name: subject_name})

            updated = True

        if credits is not None:
            session.query(Subject) \
                .filter(Subject.subject_id == subject_id) \
                .update({Subject.credits: credits})

        session.commit()
        return updated

    def user_modify_subject(self, user_id: int, subject_id: int, grade_id: int):
        if not isinstance(user_id, int):
            raise TypeError("Invalid datatype for user ID.")

        if not isinstance(subject_id, int):
            raise TypeError("Invalid datatype for subject ID.")

        if not isinstance(grade_id, int):
            raise TypeError("Invalid datatype for grade ID.")

        links = self.r.retrieve_user_has_subject()

        for link in links:
            link_user_id = link.user_id
            link_subject_id = link.subject_id

            if link_user_id == user_id and link_subject_id == subject_id:
                session.query(UserHasSubject) \
                    .filter(UserHasSubject.user_id == link_user_id) \
                    .filter(UserHasSubject.subject_id == link_subject_id) \
                    .update({UserHasSubject.grade_id: grade_id})
                return True

        session.commit()
        return False


"""
i = Insert()
print("INSERT")
print(i.insert_user("Jathavaan", "Shankarr", datetime(2001, 7, 12), "jathavaan12@gmail.com", "Jathavaan12", True))
print(i.insert_subject("TDT4100", "Objektorientert programmering"))
print(i.insert_link(1, 1))

print()

d = Delete()
print("DELETE")
print(d.delete_subject("TDT4100"))
print(d.delete_user("jathavaan12@gmail.com"))

print()

r = Retrieve()
print("RETRIEVE")
print(r.retrieve_user_subjects(1))
print(r.retrieve_subject_search_results(1, "obj"))
"""
