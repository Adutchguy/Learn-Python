class Employee:
    def __init__(self, name, monthly_salary):
        self.name = name
        self.monthly_salary = monthly_salary

    def annual_pay(self):
        return self.monthly_salary * 12

    def describe(self):
        return f"{self.name} earns {self.annual_pay():.2f} a year"


class Manager(Employee):
    def __init__(self, name, monthly_salary, reports=None):
        super().__init__(name, monthly_salary)
        self.reports = list(reports) if reports else []

    def annual_pay(self):
        return super().annual_pay() + 1000 * len(self.reports)


def total_payroll(people):
    return sum(person.annual_pay() for person in people)
