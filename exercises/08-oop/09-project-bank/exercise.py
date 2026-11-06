# Fill in every TODO. Transaction, InsufficientFunds, Bank.report and main() are already written.
from dataclasses import dataclass


@dataclass(frozen=True)
class Transaction:
    kind: str  # "deposit" or "withdraw"
    amount: float


class InsufficientFunds(Exception):
    pass


class Account:
    def __init__(self, owner, balance=0):
        # TODO 1: a negative opening balance raises ValueError("opening balance cannot be negative").
        # Store the owner, the balance (privately, as self._balance) and an empty list of transactions.
        ...

    @property
    def balance(self):
        # TODO 2: read-only; return the balance.
        ...

    @property
    def history(self):
        # TODO 3: return a COPY of the list of transactions.
        ...

    def deposit(self, amount):
        # TODO 4: amount <= 0 raises ValueError("amount must be positive").
        # Add it to the balance, record Transaction("deposit", amount) and return the new balance.
        ...

    def withdraw(self, amount):
        # TODO 5: amount <= 0 raises ValueError("amount must be positive").
        # amount > balance raises InsufficientFunds(f"balance is {balance:.2f}, cannot withdraw {amount:.2f}").
        # Otherwise subtract, record Transaction("withdraw", amount) and return the new balance.
        ...

    def __str__(self):
        # TODO 6: "ada: 60.00"
        ...


class SavingsAccount(Account):
    def __init__(self, owner, balance=0, rate=0.02):
        # TODO 7: let Account set up the owner and balance, then store the rate.
        ...

    def add_interest(self):
        # TODO 8: interest = balance * rate rounded to 2 decimals. If it is above 0, deposit it.
        # Return the interest.
        ...

    def __str__(self):
        # TODO 9: "bo (savings): 40.00"
        ...


class Bank:
    def __init__(self):
        self.accounts = {}

    def open_account(self, owner, balance=0, kind="checking"):
        # TODO 10: kind is "checking" (an Account) or "savings" (a SavingsAccount); anything else raises
        # ValueError(f"unknown account type: {kind}"). An owner who already has an account raises
        # ValueError(f"{owner} already has an account"). Store the account in self.accounts and return it.
        ...

    def get(self, owner):
        # TODO 11: return the owner's account. An unknown owner raises KeyError.
        ...

    def transfer(self, source, target, amount):
        # TODO 12: move money between two accounts. Look up BOTH accounts before moving any money,
        # so an unknown name changes nothing. Withdraw first: if it fails, nothing is deposited.
        ...

    def total_deposits(self):
        # TODO 13: the sum of all balances, rounded to 2 decimals.
        ...

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
