class MessageService:
    def send_message(self, purchase_id, message):
        print(f"Message for purchase {purchase_id}: {message}")


class BillingService:
    def process_transaction(self, purchase_id, billing_info):
        print(f"Processing transaction for purchase {purchase_id}")
        if billing_info.get("approved", False):
            print("Transaction successful.")
            return True
        else:
            print("Transaction failed.")
            return False


class StockService:
    def __init__(self):
        self.inventory = {}

    def add_to_inventory(self, sku, count):
        self.inventory[sku] = self.inventory.get(sku, 0) + count
        print(f"Added {count} of SKU {sku} to inventory.")

    def is_item_available(self, sku, count):
        available = self.inventory.get(sku, 0) >= count
        print(f"Checking availability for SKU {sku}: {'Available' if available else 'Not available'}.")
        return available

    def hold_item(self, sku, count):
        if self.is_item_available(sku, count):
            self.inventory[sku] -= count
            print(f"Held {count} of SKU {sku}.")


class PurchaseService:
    def __init__(self, billing_service, stock_service, message_service):
        self.billing_service = billing_service
        self.stock_service = stock_service
        self.message_service = message_service

    def create_purchase(self, purchase_id, sku, count, billing_info):
        print(f"Creating purchase {purchase_id} for SKU {sku}, quantity {count}")
        if not self.stock_service.is_item_available(sku, count):
            print("SKU not available in requested quantity.")
            self.message_service.send_message(purchase_id, "Purchase failed: Item not available.")
            return False

        try:
            if not self.billing_service.process_transaction(purchase_id, billing_info):
                print("Transaction failed.")
                self.message_service.send_message(purchase_id, "Purchase failed: Payment issue.")
                return False
        except Exception as e:
            print(f"Transaction error: {e}")
            self.message_service.send_message(purchase_id, "Purchase failed: Payment issue.")
            return False

        self.stock_service.hold_item(sku, count)
        self.message_service.send_message(purchase_id, "Purchase completed successfully.")
        print(f"Purchase {purchase_id} completed successfully.")
        return True


if __name__ == "__main__":
    billing_service = BillingService()
    stock_service = StockService()
    message_service = MessageService()

    purchase_service = PurchaseService(billing_service, stock_service, message_service)

    stock_service.add_to_inventory("SKU001", 15)
    stock_service.add_to_inventory("SKU002", 8)

    print("\n--- Purchase 1 ---")
    purchase_service.create_purchase("PUR001", "SKU001", 5, {"approved": True})

    print("\n--- Purchase 2 ---")
    purchase_service.create_purchase("PUR002", "SKU002", 10, {"approved": True})

    print("\n--- Purchase 3 ---")
    purchase_service.create_purchase("PUR003", "SKU001", 3, {"approved": False})
