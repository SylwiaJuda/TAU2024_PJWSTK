import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, patch
from bank_system import BankSystem, UserAccount, LowBalanceError


@pytest.fixture
def bank_system():
    return BankSystem()


@pytest.fixture
def user1():
    return UserAccount(acct_id="001", holder_name="Alice", funds=150.0)


@pytest.fixture
def user2():
    return UserAccount(acct_id="002", holder_name="Bob", funds=75.0)


# Testy klasy UserAccount
def test_add_funds(user1):
    user1.add_funds(100)
    assert user1.funds == 250.0


def test_withdraw_funds(user1):
    user1.withdraw_funds(50)
    assert user1.funds == 100.0


def test_withdraw_funds_insufficient(user1):
    with pytest.raises(LowBalanceError):
        user1.withdraw_funds(300)


@pytest.mark.asyncio
async def test_send_funds(user1, user2):
    await user1.send_funds(user2, 50)
    assert user1.funds == 100.0
    assert user2.funds == 125.0


@pytest.mark.asyncio
async def test_send_funds_insufficient(user1, user2):
    with pytest.raises(LowBalanceError):
        await user1.send_funds(user2, 200)


# Testy klasy BankSystem
def test_register_account(bank_system):
    bank_system.register_account("001", "Alice", 150.0)
    account = bank_system.retrieve_account("001")
    assert account.holder_name == "Alice"
    assert account.funds == 150.0


def test_register_account_duplicate(bank_system):
    bank_system.register_account("001", "Alice", 150.0)
    with pytest.raises(ValueError):
        bank_system.register_account("001", "Duplicate", 200.0)


def test_retrieve_account(bank_system):
    bank_system.register_account("001", "Alice", 150.0)
    account = bank_system.retrieve_account("001")
    assert account.holder_name == "Alice"


def test_retrieve_account_invalid(bank_system):
    with pytest.raises(ValueError):
        bank_system.retrieve_account("999")


@pytest.mark.asyncio
async def test_handle_transaction(bank_system):
    user1 = UserAccount(acct_id="001", holder_name="Alice", funds=150.0)
    user2 = UserAccount(acct_id="002", holder_name="Bob", funds=75.0)

    async def transaction():
        await user1.send_funds(user2, 50)

    await bank_system.handle_transaction(transaction)

    assert user1.funds == 100.0
    assert user2.funds == 125.0


# Mockowanie zewnętrznych systemów
@pytest.mark.asyncio
async def test_send_funds_with_mock(user1, user2):
    with patch("bank_system.UserAccount.send_funds", new_callable=AsyncMock) as mock_send:
        await user1.send_funds(user2, 50)
        mock_send.assert_called_once_with(user2, 50)
