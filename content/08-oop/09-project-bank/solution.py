from dataclasses import dataclass


@dataclass(frozen=True)
class Transaction:
    kind: str
    amount: float


class InsufficientFunds(Exception):
    pass


class Account:
    def __init__(self, owner, balance=0):
        if balance < 0:
            raise ValueError("opening balance cannot be negative")
        self.owner = owner
        self._balance = balance
        self._history = []

    @property
    def balance(self):
        return self._balance

    @property
    def history(self):
        return list(self._history)

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("amount must be positive")
        self._balance += amount
        self._history.append(Transaction("deposit", amount))
        return self._balance

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("amount must be positive")
        if amount > self._balance:
            raise InsufficientFunds(f"balance is {self._balance:.2f}, cannot withdraw {amount:.2f}")
        self._balance -= amount
        self._history.append(Transaction("withdraw", amount))
        return self._balance

    def __str__(self):
        return f"{self.owner}: {self.balance:.2f}"


class SavingsAccount(Account):
    def __init__(self, owner, balance=0, rate=0.02):
        super().__init__(owner, balance)
        self.rate = rate

    def add_interest(self):
        interest = round(self.balance * self.rate, 2)
        if interest > 0:
            self.deposit(interest)
        return interest

    def __str__(self):
        return f"{self.owner} (savings): {self.balance:.2f}"


class Bank:
    def __init__(self):
        self.accounts = {}

    def open_account(self, owner, balance=0, kind="checking"):
        if owner in self.accounts:
            raise ValueError(f"{owner} already has an account")
        if kind == "checking":
            account = Account(owner, balance)
        elif kind == "savings":
            account = SavingsAccount(owner, balance)
        else:
            raise ValueError(f"unknown account type: {kind}")
        self.accounts[owner] = account
        return account

    def get(self, owner):
        return self.accounts[owner]

    def transfer(self, source, target, amount):
        src = self.get(source)
        dst = self.get(target)
        src.withdraw(amount)
        dst.deposit(amount)

    def total_deposits(self):
        return round(sum(account.balance for account in self.accounts.values()), 2)

    def report(self):
        if not self.accounts:
            return "No accounts yet."
        return "\n".join(str(self.accounts[owner]) for owner in sorted(self.accounts))


def main():
    bank = Bank()
    bank.open_account("ada", 100)
    bank.open_account("bo", kind="savings")
    bank.transfer("ada", "bo", 40)
    print(bank.report())
    try:
        bank.transfer("ada", "bo", 500)
    except InsufficientFunds as err:
        print("Transfer failed:", err)


if __name__ == "__main__":
    main()
