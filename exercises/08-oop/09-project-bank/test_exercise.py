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


import pytest


def _bank():
    Bank = _cls("Bank")
    return Bank()


def test_account_basics():
    Account = _cls("Account")
    ada = Account("ada", 100)
    assert (ada.owner, ada.balance) == ("ada", 100), f"Account('ada', 100) should have owner 'ada' and balance 100 but has {(ada.owner, ada.balance)!r}."
    assert Account("bo").balance == 0, "The opening balance defaults to 0."


def test_negative_opening_balance():
    Account = _cls("Account")
    with pytest.raises(ValueError) as info:
        Account("bo", -5)
    assert str(info.value) == "opening balance cannot be negative", f"The message should be 'opening balance cannot be negative' but was {str(info.value)!r}."


def test_balance_is_read_only():
    Account = _cls("Account")
    acc = Account("ada", 10)
    with pytest.raises(AttributeError):
        acc.balance = 1000000


def test_deposit():
    Account = _cls("Account")
    acc = Account("ada", 100)
    assert acc.deposit(25.5) == 125.5, "deposit should return the new balance."
    assert acc.balance == 125.5, f"The balance should be 125.5 but is {acc.balance!r}."


def test_deposit_must_be_positive():
    Account = _cls("Account")
    acc = Account("ada", 100)
    for amount in [0, -5]:
        with pytest.raises(ValueError) as info:
            acc.deposit(amount)
        assert str(info.value) == "amount must be positive", f"deposit({amount}) should raise ValueError('amount must be positive') but the message was {str(info.value)!r}."
    assert acc.balance == 100, "A rejected deposit must not change the balance."


def test_withdraw():
    Account = _cls("Account")
    acc = Account("ada", 100)
    assert acc.withdraw(40) == 60, "withdraw should return the new balance."
    assert acc.balance == 60, f"The balance should be 60 but is {acc.balance!r}."


def test_withdraw_too_much_raises_insufficient_funds():
    Account = _cls("Account")
    InsufficientFunds = _cls("InsufficientFunds")
    acc = Account("ada", 60)
    with pytest.raises(InsufficientFunds) as info:
        acc.withdraw(500)
    assert str(info.value) == "balance is 60.00, cannot withdraw 500.00", f"The message should be 'balance is 60.00, cannot withdraw 500.00' but was {str(info.value)!r}."
    assert acc.balance == 60, "A rejected withdrawal must not change the balance."
    assert acc.history == [], "A rejected withdrawal must not be recorded."


def test_withdraw_must_be_positive():
    Account = _cls("Account")
    acc = Account("ada", 100)
    with pytest.raises(ValueError) as info:
        acc.withdraw(-1)
    assert str(info.value) == "amount must be positive", f"withdraw(-1) should raise ValueError('amount must be positive') but the message was {str(info.value)!r}."


def test_history_records_transactions():
    import exercise

    Account = _cls("Account")
    acc = Account("ada", 100)
    acc.deposit(10)
    acc.withdraw(30)
    assert acc.history == [exercise.Transaction("deposit", 10), exercise.Transaction("withdraw", 30)], f"history should list a deposit of 10 then a withdrawal of 30 but is {acc.history!r}."


def test_history_is_a_copy():
    Account = _cls("Account")
    acc = Account("ada", 100)
    acc.deposit(10)
    acc.history.clear()
    assert len(acc.history) == 1, "Changing the list you get from .history must not change the account's real history. Return a copy."


def test_account_text():
    Account = _cls("Account")
    assert str(Account("ada", 60)) == "ada: 60.00", f"str(Account('ada', 60)) should be 'ada: 60.00' but was {str(Account('ada', 60))!r}."


def test_savings_account_is_an_account():
    Account, SavingsAccount = _cls("Account"), _cls("SavingsAccount")
    assert issubclass(SavingsAccount, Account), "SavingsAccount should inherit from Account."
    s = SavingsAccount("bo", 100)
    assert s.rate == 0.02, f"The default rate should be 0.02 but is {s.rate!r}."
    assert s.deposit(10) == 110, "A savings account should deposit just like an Account."
    assert str(s) == "bo (savings): 110.00", f"str(SavingsAccount('bo', 110)) should be 'bo (savings): 110.00' but was {str(s)!r}."


def test_add_interest():
    import exercise

    SavingsAccount = _cls("SavingsAccount")
    s = SavingsAccount("bo", 100)
    assert s.add_interest() == 2.0, "add_interest should return the interest earned (2.0 on 100 at 2%)."
    assert s.balance == 102.0, f"The balance should be 102.0 after interest but is {s.balance!r}."
    assert s.history == [exercise.Transaction("deposit", 2.0)], f"The interest should be recorded as a deposit but history is {s.history!r}."
    empty = SavingsAccount("cy")
    assert empty.add_interest() == 0 and empty.history == [], "No balance earns no interest and records no transaction."


def test_open_account_kinds():
    Account, SavingsAccount = _cls("Account"), _cls("SavingsAccount")
    bank = _bank()
    plain = bank.open_account("ada", 100)
    saver = bank.open_account("bo", kind="savings")
    assert type(plain) is Account and plain.balance == 100, f"open_account('ada', 100) should return an Account holding 100 but returned {plain!r}."
    assert type(saver) is SavingsAccount and saver.balance == 0, "open_account('bo', kind='savings') should return a SavingsAccount."
    assert bank.get("ada") is plain, "get('ada') should return the same account object."


def test_open_account_errors():
    bank = _bank()
    bank.open_account("ada")
    with pytest.raises(ValueError) as info:
        bank.open_account("ada")
    assert str(info.value) == "ada already has an account", f"The message should be 'ada already has an account' but was {str(info.value)!r}."
    with pytest.raises(ValueError) as info:
        bank.open_account("cy", kind="gold")
    assert str(info.value) == "unknown account type: gold", f"The message should be 'unknown account type: gold' but was {str(info.value)!r}."
    assert "cy" not in bank.accounts, "A rejected account must not be stored."


def test_get_unknown_owner():
    bank = _bank()
    with pytest.raises(KeyError):
        bank.get("nobody")


def test_transfer_moves_money():
    bank = _bank()
    bank.open_account("ada", 100)
    bank.open_account("bo", 5)
    bank.transfer("ada", "bo", 40)
    assert bank.get("ada").balance == 60 and bank.get("bo").balance == 45, f"After transferring 40, ada should have 60 and bo 45 but they have {bank.get('ada').balance!r} and {bank.get('bo').balance!r}."


def test_failed_transfer_changes_nothing():
    InsufficientFunds = _cls("InsufficientFunds")
    bank = _bank()
    bank.open_account("ada", 60)
    bank.open_account("bo", 0)
    with pytest.raises(InsufficientFunds):
        bank.transfer("ada", "bo", 500)
    assert bank.get("ada").balance == 60 and bank.get("bo").balance == 0, "A failed transfer must leave both balances unchanged."


def test_transfer_to_an_unknown_account_changes_nothing():
    bank = _bank()
    bank.open_account("ada", 60)
    with pytest.raises(KeyError):
        bank.transfer("ada", "ghost", 10)
    assert bank.get("ada").balance == 60, f"Money must not leave ada when the target does not exist, but her balance is {bank.get('ada').balance!r}. Look up both accounts before withdrawing."


def test_total_deposits():
    bank = _bank()
    assert bank.total_deposits() == 0, "An empty bank holds 0."
    bank.open_account("ada", 60.25)
    bank.open_account("bo", 40.5, kind="savings")
    assert bank.total_deposits() == 100.75, f"total_deposits should be 100.75 but was {bank.total_deposits()!r}."


def test_report():
    bank = _bank()
    assert bank.report() == "No accounts yet.", "An empty bank reports 'No accounts yet.'"
    bank.open_account("bo", 40, kind="savings")
    bank.open_account("ada", 60)
    assert bank.report() == "ada: 60.00\nbo (savings): 40.00", f"The report should list accounts by owner name but was {bank.report()!r}."


def test_main_program(capsys):
    import exercise

    capsys.readouterr()
    exercise.main()
    out = capsys.readouterr().out
    expected = "ada: 60.00\nbo (savings): 40.00\nTransfer failed: balance is 60.00, cannot withdraw 500.00\n"
    assert out == expected, f"main() should print:\n{expected}\nbut printed:\n{out}"
