import datetime
from flask import Flask, render_template, request
from accountant import *
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    manager.context['mode'] = None
    if manager.context['last_mode'] == 'zakup':
        manager.context['zakup'].item_name = request.form.get('item_name')
        try:
            manager.context['zakup'].item_price = int(request.form.get('item_price'))
            manager.context['zakup'].item_quantity = int(request.form.get('item_quantity'))
        except:
            manager.context['zakup'].item_price = -1
            manager.context['zakup'].item_quantity = -1
        if manager.context['zakup'].item_name:
            manager.context['zakup'].zakup_operation()
        else:
            manager.context['zakup'].error = "You didn't type item name"
    
    elif manager.context['last_mode'] == "sprzedaz":
        manager.context['sprzedaz'].item_name = request.form.get('item_name')
        try:
            manager.context['sprzedaz'].item_price = int(request.form.get('item_price'))
            manager.context['sprzedaz'].item_quantity = int(request.form.get('item_quantity'))
        except:
            manager.context['sprzedaz'].item_price = -1
            manager.context['sprzedaz'].item_quantity = -1
        if manager.context['sprzedaz'].item_name:
            manager.context['sprzedaz'].sprzedaz_operation()
        else:
            manager.context['sprzedaz'].error = "You didn't type item name"

    elif manager.context['last_mode'] == 'saldo':
        if request.form.get('saldo_comment'):
            manager.context['saldo'].account_comment = request.form.get('saldo_comment')
            manager.context['saldo'].test_comment = 'OK'
        if request.form.get('saldo_amount'):
            try:
                manager.context['saldo'].account_value = int(request.form.get('saldo_amount'))
                if manager.context['saldo'].account_value != 0:
                    manager.context['saldo'].test_value = 'OK'
            except:
                manager.context['saldo'].account_value = None
        if manager.context['saldo'].account_value and saldo.account_comment:
            manager.context['saldo'].saldo_operation()
        else:
            manager.context['saldo'].account_value = 0
            manager.context['saldo'].input_check = None
    return render_template('index.html', context=manager.context, items=get_items())

@app.route("/operations", methods=["GET", "POST"])
def operations():
    manager.context['saldo'].success = None
    manager.context['zakup'].success = None
    manager.context['zakup'].error = None
    manager.context['sprzedaz'].success = None
    manager.context['sprzedaz'].error = None
    saldo.account_comment = ""
    saldo.account_value = 0
    manager.context['mode'] = request.form.get('mode')
    manager.context['last_mode'] = manager.context['mode']
    saldo.test_comment = None
    saldo.test_value = None
    print(manager.context)
    return render_template('operations.html', context=manager.context, items=get_items())

def get_items():
    items = products.trade_items
    return items

@app.route("/history", methods=["GET", "POST"])
def history():
    return render_template('history.html', context=manager.context)


@app.route("/history/<index_first>/<index_last>/", methods=["GET", "POST"])
def history_index(index_first, index_last):
    try:
        index_last = int(index_last)
        index_first = int(index_first)
    except:
        index_first = 1
        index_last = len(manager.context['history'])
    return render_template(
        'historyindex.html',
        context=manager.context,
        index_first=index_first,
        index_last=index_last,
    )