import africastalking
# username='sandbox'
# api_key="28b9b1aadd5235c282a24ec6cd340cc8cbd210eb62fd3c5615a221cf94f3e8bd"
username='dukadiscount'
api_key="e74361a706c79494e79bf20d7916e543f854fa5811c6368258b89633c8c17346"
africastalking.initialize(username, api_key)
payment = africastalking.Payment
sms = africastalking.SMS

# payment.mobile_checkout(
#     product_name: "c2b",
#     phone_number: "+254725328016",
#     currency_code: "KES", amount: 1.00, metadata: dict = {},provider_channel:"123456")
print("done")
sms.send("Buda mathafaka wwe",["+254725328016"])
payment.mobile_checkout('c2b','+254725328016','KES',1.00,{"TransactionId":"12fbfjb"},'123456')
