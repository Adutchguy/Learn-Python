---
title: "Project: A Small Bank"
minutes: 45
prereqs: ["08-oop/08-abstract-classes-and-protocols"]
concepts: ["project", "classes", "inheritance", "composition", "properties", "dataclass", "custom exception", "error handling"]
local_only: false
hints:
  - "Account: store owner, self._balance and self._history = []. balance and history are @property methods (history returns list(self._history)). In deposit and withdraw, validate first, then change the balance, append a Transaction and return the new balance. __str__ is f\"{self.owner}: {self.balance:.2f}\"."
  - "SavingsAccount(Account): __init__ calls super().__init__(owner, balance) and then stores self.rate. add_interest works out round(self.balance * self.rate, 2), deposits it only when it is above 0, and returns it. __str__ is f\"{self.owner} (savings): {self.balance:.2f}\"."
  - "Bank.open_account: check the duplicate owner and the kind first, create an Account or a SavingsAccount, store it in self.accounts[owner] and return it. transfer: src = self.get(source) and dst = self.get(target) first, then src.withdraw(amount), then dst.deposit(amount). total_deposits: round(sum(a.balance for a in self.accounts.values()), 2)."
---

## Why this matters

Time to design with objects. A small **bank** is a classic: it has several kinds of account, rules that must never be broken (no overdrafts, no negative deposits) and one object (the bank) that holds many others. It uses everything in this module: classes, properties, inheritance, composition, a dataclass and a custom exception.

## The idea

You will complete these pieces. The starter has numbered `TODO`s:

| Class | Role |
|---|---|
| `Transaction` | a frozen dataclass recording `"deposit"` or `"withdraw"` and an amount (given) |
| `InsufficientFunds` | your own error type (given) |
| `Account` | an owner, a private balance, a history; `deposit`, `withdraw`, `__str__` |
| `SavingsAccount(Account)` | adds a `rate` and `add_interest()`; its own `__str__` |
| `Bank` | **has** many accounts; opens them, finds them and moves money between them |

Two design rules to notice: the balance can only change through `deposit` and `withdraw` (so every change is checked and recorded), and a failed operation must leave everything exactly as it was.

## Try it

Before coding, read `main()` at the bottom of the starter and work out by hand what it should print. Which line triggers the `InsufficientFunds` error?

## Your turn

Complete all thirteen `TODO`s. The error messages are exact, because the checks compare them. When you are done, running the program prints:

```text
ada: 60.00
bo (savings): 40.00
Transfer failed: balance is 60.00, cannot withdraw 500.00
```

## Recap

- Put the rules next to the data they protect (private balance, checked methods).
- Inheritance for "is a" (`SavingsAccount`), composition for "has a" (`Bank` holds accounts).
- Validate before you change anything, so failures leave no half-done work.

## Common mistakes

- **Changing the balance before checking** it, so a rejected withdrawal still removes money.
- **Returning the real history list**, which lets callers rewrite it.
- **Withdrawing before looking up the target account** in `transfer`, so money disappears when the target is unknown.
