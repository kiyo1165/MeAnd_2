# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/account/apikeys
import stripe

stripe.api_key = "sk_test_51IU2lyEl5zmDEOnOsMwQOoJmXTm1S4j3NmJbg5UTjWnrFu6Wbknj1B2VUnvUT7gZzjvTNK4HY02K68yybCDRsTbT00QXZuYTyC"

stripe.PaymentIntent.create(

    amount=1099,
    currency='jpy',
    payment_method_types=['card'],
)