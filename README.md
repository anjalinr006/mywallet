# Mini Wallet
This site was built using [GitHub Pages](https://pages.github.com/).

## Dependencies
- Python 3.6+
- Django 3.1+
- For the API module, Django REST Framework 3.12+ is required.

## Setup

1.git clone https://github.com/anjalinr006/mywallet.git
2.virtualenv env
3.source env/bin/activate
4.pip install -r requirements.txt
5.python manage.py makemigrations
6.python manage.py runserver

### Initialize my account for wallet

  curl --location --request POST 'http://localhost/api/v1/wallet/init' --form 'customer_xid="{{customer_xid}}"'
  
  Eg:customer_xid = "ea0212d3-abd6-406f-8c67-868e814a2436"

### Enable my wallet

 curl --location --request POST 'http://127.0.0.1:8000/api/v1/wallet/' --header 'Authorization: Token {{token}} }'


### Disable my wallet

curl --location --request PATCH 'http://127.0.0.1:8000/api/v1/wallet/' --header 'Authorization: Token {{token}}' --form 'is_disabled="true"'

### View my wallet balance

 curl --location --request GET 'http://127.0.0.1:8000/api/v1/wallet/' --header 'Authorization: Token {{token}} }'


### Add virtual money to my wallet

 curl --location --request GET 'http://127.0.0.1:8000/api/v1/wallet/deposits' --header 'Authorization: Token {{token}} }' --form 'amount="60000"' --form 'reference_id="4b01c9bb-3acd-47dc-87db-d9ac483d20b2"'
 
 note: reference_id shoukd be unique

### Use virtual money from my wallet

 curl --location --request GET 'http://127.0.0.1:8000/api/v1/wallet/withdrawals' --header 'Authorization: Token {{token}} }' --form 'amount="60000"' --form 'reference_id="4b01c9bb-3acd-47dc-87db-d9ac483d20b2"'







