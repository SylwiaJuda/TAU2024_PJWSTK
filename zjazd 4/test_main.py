import unittest
from unittest.mock import Mock
from main import PurchaseService, BillingService, StockService, MessageService

class TestPurchaseService(unittest.TestCase):

    def setUp(self):
        self.billing_service = Mock(spec=BillingService)
        self.stock_service = Mock(spec=StockService)
        self.message_service = Mock(spec=MessageService)

        self.purchase_service = PurchaseService(
            self.billing_service,
            self.stock_service,
            self.message_service
        )

    def test_purchase_successful(self):
        purchase_id = "PUR101"
        sku = "SKU101"
        count = 4
        billing_info = {"approved": True}

        self.stock_service.is_item_available.return_value = True
        self.billing_service.process_transaction.return_value = True

        result = self.purchase_service.create_purchase(purchase_id, sku, count, billing_info)

        self.assertTrue(result)
        self.stock_service.is_item_available.assert_called_once_with(sku, count)
        self.billing_service.process_transaction.assert_called_once_with(purchase_id, billing_info)
        self.stock_service.hold_item.assert_called_once_with(sku, count)
        self.message_service.send_message.assert_called_once_with(purchase_id, "Purchase completed successfully.")

    def test_purchase_fails_when_item_not_available(self):
        purchase_id = "PUR102"
        sku = "SKU102"
        count = 12
        billing_info = {"approved": True}

        self.stock_service.is_item_available.return_value = False

        result = self.purchase_service.create_purchase(purchase_id, sku, count, billing_info)

        self.assertFalse(result)
        self.stock_service.is_item_available.assert_called_once_with(sku, count)
        self.message_service.send_message.assert_called_once_with(purchase_id, "Purchase failed: Item not available.")
        self.billing_service.process_transaction.assert_not_called()
        self.stock_service.hold_item.assert_not_called()

    def test_purchase_fails_when_transaction_fails(self):
        purchase_id = "PUR103"
        sku = "SKU103"
        count = 6
        billing_info = {"approved": False}

        self.stock_service.is_item_available.return_value = True
        self.billing_service.process_transaction.return_value = False

        result = self.purchase_service.create_purchase(purchase_id, sku, count, billing_info)

        self.assertFalse(result)
        self.stock_service.is_item_available.assert_called_once_with(sku, count)
        self.billing_service.process_transaction.assert_called_once_with(purchase_id, billing_info)
        self.message_service.send_message.assert_called_once_with(purchase_id, "Purchase failed: Payment issue.")
        self.stock_service.hold_item.assert_not_called()

    def test_purchase_handles_transaction_exception(self):
        purchase_id = "PUR104"
        sku = "SKU104"
        count = 3
        billing_info = {"approved": True}

        self.stock_service.is_item_available.return_value = True
        self.billing_service.process_transaction.side_effect = Exception("Transaction error")

        result = self.purchase_service.create_purchase(purchase_id, sku, count, billing_info)

        self.assertFalse(result)
        self.stock_service.is_item_available.assert_called_once_with(sku, count)
        self.billing_service.process_transaction.assert_called_once_with(purchase_id, billing_info)
        self.message_service.send_message.assert_called_once_with(purchase_id, "Purchase failed: Payment issue.")
        self.stock_service.hold_item.assert_not_called()

if __name__ == "__main__":
    unittest.main()
