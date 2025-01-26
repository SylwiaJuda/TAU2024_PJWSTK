import asyncio


class LowBalanceError(Exception):
    """Wyjątek dla zbyt niskiego salda."""


class UserAccount:
    def __init__(self, acct_id: str, holder_name: str, funds: float = 0.0):
        self.acct_id = acct_id
        self.holder_name = holder_name
        self.funds = funds

    def add_funds(self, amount: float):
        if amount <= 0:
            raise ValueError("Added amount must be greater than zero.")
        self.funds += amount

    def withdraw_funds(self, amount: float):
        if amount > self.funds:
            raise LowBalanceError("Not enough funds to complete withdrawal.")
        self.funds -= amount

    async def send_funds(self, recipient: "UserAccount", amount: float):
        if amount > self.funds:
            raise LowBalanceError("Not enough funds to complete transfer.")
        await asyncio.sleep(0.1)  # Symulacja asynchronicznego opóźnienia
        self.funds -= amount
        recipient.add_funds(amount)


class BankSystem:
    def __init__(self):
        self.user_accounts = {}

    def register_account(self, acct_id: str, holder_name: str, initial_funds: float = 0.0):
        if acct_id in self.user_accounts:
            raise ValueError("Account ID already exists.")
        self.user_accounts[acct_id] = UserAccount(acct_id, holder_name, initial_funds)

    def retrieve_account(self, acct_id: str) -> UserAccount:
        if acct_id not in self.user_accounts:
            raise ValueError("Account not found.")
        return self.user_accounts[acct_id]

    async def handle_transaction(self, transaction_fn):
        """Obsługuje asynchroniczne przetwarzanie transakcji."""
        await transaction_fn()
