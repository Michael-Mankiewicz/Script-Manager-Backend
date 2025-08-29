to install dependecies, run the following command:

pip install -r requirements.txt

to run, type:

python manage.py runserver

and then run the frontend to use the full project.

If the backend produces a really small zipfile- it is because it didn't find any address corrections. Every month there are always address corrections to be found, so this is almost always an error. If this happens, it is because the column order in the Fedex Invoice is incremented or decremented by 1. To fix this error, go to api > services > AddressCorrectionBot > AddressCorrectionBot.py and adjust the array on line 27. It should look like this-

fedexInvoiceColumns = [
        addressCorrectionFeeIndex,
        2,   # Invoice Date
        3,   # Invoice Number
        9,   # Express or Ground Tracking Number
        14,  # Shipment Date
        33,  # Recipient Name
        35,  # Recipient Address Line 1
        36,  # Recipient Address Line 2
        37,  # Recipient City
        38,  # Recipient State
        39,  # Recipient Zip Code
        40,  # Recipient Country/Territory
        49,  # Original Customer Reference
        50,  # Original Ref#2
        51,  # Original Ref #3/PO Number
        107  # Tracking ID Charge Description,
        ]
Do not change "addressCorrectionFeeIndex", no need to increment that- that index is automatically found already. The other indices are not manually found, and are hardcoded numbers. If the error previously mentioned occurred, a guaranteed fix is to either increment every number by 1 or decrement every number by 1. Some months, I believe there is an additional column that is added, and this code does not automatically adjust for that. So, you must manually increment or decrement all the indices in this array if the code does not properly generate any invoices.

You might open a fedex invoice csv in Excel, and Excel will display the columns with letters, and the rows with numbers. With the format that this code uses, the column letters are assined to indices as numbers in the fedexInvoiceColumn array with the following pattern: A = 0, B = 1, C = 2 ... Z = 25, AA = 26, AB = 27 ...



