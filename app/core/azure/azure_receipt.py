from typing import Optional
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from app.config.config import Config
from app.core.entities.receipt.receipt import Receipt, ReceiptItem

from app.utils.logger import Log

log = Log("Receipt Function")


def analyze_receipt(file_location):
    try:
        log.info(f"file_location: {file_location}.")

        document_analysis_client = DocumentAnalysisClient(
            endpoint=Config.AZURE_FORM_RECOGNIZER_ENDPOINT,
            credential=AzureKeyCredential(Config.AZURE_FORM_RECOGNIZER_KEY),
        )

        with open(file_location, "rb") as f:
            poller = document_analysis_client.begin_analyze_document("prebuilt-receipt", document=f, locale="ja-JP")

        receipts = poller.result()

        create_receipts: Optional[Receipt] = Receipt()

        for idx, receipt in enumerate(receipts.documents):
            print(f"--------Analysis of receipt #{idx + 1}--------")
            print(f"Receipt type: {receipt.doc_type if receipt.doc_type else 'N/A'}")
            merchant_name = receipt.fields.get("MerchantName")
            if merchant_name:
                print(f"Merchant Name: {merchant_name.value} has confidence: " f"{merchant_name.confidence}")
                create_receipts.merchant_name = merchant_name.value

            transaction_date = receipt.fields.get("TransactionDate")
            if transaction_date:
                print(f"Transaction Date: {transaction_date.value} has confidence: " f"{transaction_date.confidence}")
                create_receipts.transaction_date = transaction_date.value

            transaction_address = receipt.fields.get("MerchantAddress")
            if transaction_address:
                print(
                    f"Transaction Address: {transaction_address.value} has confidence: "
                    f"{transaction_address.confidence}"
                )
                create_receipts.address = transaction_address.value

            merchant_phone_number = receipt.fields.get("MerchantPhoneNumber")
            if merchant_phone_number:
                print(
                    f"Merchant Phone Number: {merchant_phone_number.value} has confidence: "
                    f"{merchant_phone_number.confidence}"
                )
                create_receipts.phone_number = merchant_phone_number.value

            transaction_time = receipt.fields.get("TransactionTime")
            if transaction_time:
                print(f"Transaction Time: {transaction_time.value} has confidence: " f"{transaction_time.confidence}")
                create_receipts.transaction_time = transaction_time.value

            if receipt.fields.get("Items"):
                print("Receipt items:")
                for idx, item in enumerate(receipt.fields.get("Items").value):
                    create_receipt_item: Optional[ReceiptItem] = ReceiptItem()

                    print(f"...Item #{idx + 1}")
                    item_description = item.value.get("Description")
                    if item_description:
                        print(
                            f"......Item Description: {item_description.value} has confidence: "
                            f"{item_description.confidence}"
                        )
                        create_receipt_item.description = item_description.value
                    item_quantity = item.value.get("Quantity")
                    if item_quantity:
                        print(
                            f"......Item Quantity: {item_quantity.value} has confidence: " f"{item_quantity.confidence}"
                        )
                        create_receipt_item.quantity = item_quantity.value

                    item_price = item.value.get("Price")
                    if item_price:
                        print(
                            f"......Individual Item Price: {item_price.value} has confidence: "
                            f"{item_price.confidence}"
                        )
                        create_receipt_item.price = str(item_price.value)

                    item_total_price = item.value.get("TotalPrice")
                    if item_total_price:
                        print(
                            f"......Total Item Price: {item_total_price.value} has confidence: "
                            f"{item_total_price.confidence}"
                        )
                        create_receipt_item.total_price = str(item_total_price.value)

                    create_receipts.add_receipt_item(create_receipt_item)

            subtotal = receipt.fields.get("Subtotal")
            if subtotal:
                print(f"Subtotal: {subtotal.value} has confidence: {subtotal.confidence}")
                create_receipts.subtotal = subtotal.value

            tax = receipt.fields.get("TotalTax")
            if tax:
                print(f"Total tax: {tax.value} has confidence: {tax.confidence}")
                create_receipts.tax = str(tax.value)

            tip = receipt.fields.get("Tip")
            if tip:
                print(f"Tip: {tip.value} has confidence: {tip.confidence}")
                create_receipts.tip = str(tip.value)

            total = receipt.fields.get("Total")
            if total:
                print(f"Total: {total.value} has confidence: {total.confidence}")
                create_receipts.total = str(total.value)

            print("--------------------------------------")

        return create_receipts
    except Exception:
        return Exception
