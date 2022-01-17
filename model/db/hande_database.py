from model.db.alter_database import Retrieve


class Calculate:
    def __init__(self):
        self.r = Retrieve()

    def calculate_user_average_grade(self, user_id: int):
        """Calculates a users average grade."""
        if not isinstance(user_id, int):
            raise TypeError("Invalid datatype for user ID")

        results = self.r.retrieve_user_subjects(user_id)
        results = [result for result in results]

        average_grade = 0
        total_credits = 0

        if len(results) == 0:
            return average_grade  # Returns 0 if there are no subjects registered for this user

        total_points = 0
        for result in results:
            # In the case of a grade that is ongoing, passed or failed; the average grade should not be affected
            grade = result.Grade
            credits = result.Subject.credits

            match grade.grade_value:
                case 'A':
                    total_points += 5 * credits
                    total_credits += credits
                case 'B':
                    total_points += 4 * credits
                    total_credits += credits
                case 'C':
                    total_points += 3 * credits
                    total_credits += credits
                case 'D':
                    total_points += 2 * credits
                    total_credits += credits
                case 'E':
                    total_points += 1 * credits
                    total_credits += credits

        # Creating a list of all the grades the user has except 'Ongoing', 'Pass' and 'Fail'
        grades_for_calculation = list(filter(
            lambda result:
            result.Grade.grade_value != 'Pass'
            and result.Grade.grade_value != 'Fail'
            and result.Grade.grade_value != 'Ongoing',
            results
        ))

        if len(grades_for_calculation) == 0:
            return average_grade  # Returns 0 if all the subjects are 'Ongoing', 'Pass' or 'Fail'

        average_grade = total_points / total_credits
        return round(average_grade, 2)
