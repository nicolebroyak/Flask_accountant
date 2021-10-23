import datetime
from flask import Flask, render_template, request
import accountant
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    mode = request.form.get('mode')
    saldo = accountant.saldo
    zakup = accountant.zakup
    sprzedaz = accountant.sprzedaz
    if mode == "zakup":
        zakup.item_name = request.form.get('item_name')
        try:
            zakup.item_price = int(request.form.get('item_price'))
            zakup.item_quantity = int(request.form.get('item_quantity'))
        except:
            zakup.item_price = None
            zakup.item_quantity = None
    elif mode == "sprzedaż":
        sprzedaz.item_name = request.form.get('item_name')
        try:
            sprzedaz.item_price = int(request.form.get('item_price'))
            sprzedaz.item_quantity = int(request.form.get('item_quantity'))
        except:
            sprzedaz.item_price = None
            sprzedaz.item_quantity = None
    if request.form.get('saldo_comment'):
        saldo.account_comment = request.form.get('saldo_comment')
        saldo.test_comment = 'OK'
    if request.form.get('saldo_amount'):
        try:
            saldo.account_value = int(request.form.get('saldo_amount'))
            if saldo.account_value != 0:
                saldo.test_value = 'OK'
        except:
            saldo.account_value = None
    if saldo.account_value and saldo.account_comment:
        saldo.saldo_operation()
    else:
        saldo.account_value = 0
        saldo.input_check = None
    context = {
        'mode': mode,
        'balance': saldo.account_balance,
        'item_name': item_name,
        'item_price': item_price,
        'item_quantity': item_quantity,
        'saldo': saldo,
        'saldo_amount': saldo.account_value,
        'saldo_comment': saldo.account_comment,
        'saldo_input_check': saldo.input_check,
    }
    print(context['saldo_amount'])
    print(context['saldo_comment'])
    print(saldo.test_value)
    print(saldo.test_comment)
    saldo.account_comment = ""
    saldo.account_value = 0
    return render_template('index.html', context=context, items=get_items())

@app.route("/operations", methods=["GET", "POST"])
def operations():
    mode = request.form.get('mode')
    saldo = accountant.saldo
    context = {
        'mode': mode,
        'balance': saldo.account_balance,
        'saldo_amount': saldo.account_value,
        'saldo_comment': saldo.account_comment,
    }
    saldo.test_comment = None
    saldo.test_value = None
    return render_template('operations.html', context=context, items=get_items())

def get_items():
    items = accountant.products.trade_items
    return items