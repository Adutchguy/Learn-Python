def _fn(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a function called {name}(). Define it with: def {name}(...):"
    func = getattr(exercise, name)
    assert callable(func), f"{name} should be a function, but it is {func!r}."
    return func


def _cls(name):
    import exercise

    assert hasattr(exercise, name), f"Your program needs a class called {name}. Start it with: class {name}:"
    cls = getattr(exercise, name)
    assert isinstance(cls, type), f"{name} should be a class, but it is {cls!r}."
    return cls


def test_employee():
    Employee = _cls("Employee")
    ann = Employee("Ann", 3000)
    assert ann.annual_pay() == 36000, f"Employee('Ann', 3000).annual_pay() should be 36000 but was {ann.annual_pay()!r}."
    assert ann.describe() == "Ann earns 36000.00 a year", f"describe() should be 'Ann earns 36000.00 a year' but was {ann.describe()!r}."


def test_manager_is_an_employee():
    Employee, Manager = _cls("Employee"), _cls("Manager")
    assert issubclass(Manager, Employee), "Manager should inherit from Employee: class Manager(Employee):"
    assert isinstance(Manager("Bo", 4000), Employee), "A Manager object should also count as an Employee."


def test_manager_pay_includes_a_bonus_per_report():
    Employee, Manager = _cls("Employee"), _cls("Manager")
    team = [Employee("Ann", 3000), Employee("Cy", 2500)]
    boss = Manager("Bo", 4000, team)
    assert boss.annual_pay() == 50000, f"A manager on 4000 a month with 2 reports should earn 48000 + 2000 = 50000 but annual_pay() was {boss.annual_pay()!r}."
    assert Manager("Di", 4000).annual_pay() == 48000, "A manager with no reports gets just the normal pay."


def test_describe_uses_the_managers_pay():
    Employee, Manager = _cls("Employee"), _cls("Manager")
    boss = Manager("Bo", 4000, [Employee("Ann", 3000)])
    assert boss.describe() == "Bo earns 49000.00 a year", f"A manager's describe() should use the manager's pay: 'Bo earns 49000.00 a year' but it was {boss.describe()!r}. Do not copy describe: inherit it."


def test_each_manager_has_their_own_reports_list():
    Manager = _cls("Manager")
    a, b = Manager("A", 1), Manager("B", 1)
    a.reports.append("x")
    assert b.reports == [], f"A second manager should have no reports but has {b.reports!r}. Do not share one list."


def test_manager_still_has_the_employee_attributes():
    Manager = _cls("Manager")
    boss = Manager("Bo", 4000)
    assert (boss.name, boss.monthly_salary) == ("Bo", 4000), "Call super().__init__(name, monthly_salary) so the parent's attributes are set."


def test_total_payroll():
    Employee, Manager = _cls("Employee"), _cls("Manager")
    total_payroll = _fn("total_payroll")
    staff = [Employee("Ann", 3000), Manager("Bo", 4000, [Employee("Cy", 2000)])]
    assert total_payroll(staff) == 36000 + 49000, f"total_payroll should be 85000 but was {total_payroll(staff)!r}."
    assert total_payroll([]) == 0, "No staff means a total of 0."
