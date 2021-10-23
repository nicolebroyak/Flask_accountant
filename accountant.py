from module.input import inputlist, input_list


# sciezki programu:
# 1. Saldo:
#     - jeżeli saldo mniejsze niż wypłata - "za mało pieniędzy"
# 2. Zakup:
#     - jeżeli brak towaru: - dodaj do słownika wraz z ilością sztuk
#     - jeżeli towar już jest: - zwiększ stan magazynowy
#     - jeżeli koszt zakupu większy od salda - "za mało pieniędzy"
# 3. Sprzedaż:
#     - jeżeli brak towaru lub towaru mniej niż sprzedawane: - błąd "brak towaru"
#     - jeżeli towar jest: zmniejsz stan magazynowy

class Manager():

    def __init__(self):
        self.ALLOWED_COMMANDS = "saldo", "sprzedaż", "zakup", "stop", "end"
        self.actions = {
            'saldo': saldo.saldo_operation,
            'sprzedaż': sprzedaz.sprzedaz_operation,
            'zakup': zakup.zakup_operation,
            'stop': self.stop_operation,
        }
        self.mode = 'start'
        self.index = 0
        self.operations_type = []
        self.operations = []
        self.inputlog = []
        self.operations_number = 0
        for operations in inputlist:
            if operations in self.ALLOWED_COMMANDS:
                self.operations_number += 1
    
    def select_mode(func):
        def inner(self):
            self.mode = input_list()
            while self.mode not in self.ALLOWED_COMMANDS:
                print("Wrong mode")
                self.mode = input_list()
            func(self)
            return func
        return inner

    @select_mode
    def assign(self):
        self.actions[self.mode]()

    def stop_operation(self):
        print("stop operation")
        index_first = int(input_list())
        index_last = int(input_list())
        index = 1
        with open("output.txt", mode="a") as file:
            file.write(f"Account balance: {saldo.account_balance}\n")
            file.write("Items on stock:\n")
            for item_name, item_quantity in products.trade_items.items():
                file.write(f"{item_name}: {item_quantity} pcs\n")
            file.write("\nSummary:\n")
            for i in manager.operations:
                if index >= index_first and index_first <= index_last:
                    file.write(f"Operation nr {index}:\nmode: "
                               f"{manager.operations_type[index - 1]}\n{i}\n\n")
                if index == index_last:
                    break
                index += 1
            file.write("\nCorrect input log:")
            for i in manager.inputlog:
                file.write(str(i) + "\n")
            self.mode = "end"

class Saldo():
    
    def __init__(self):
        self.test_comment = "OK"
        self.test_value = "OK"
        self.index_balance = 0
        self.account_balance = 0
        self.account_value = 0
        self.account_comment = ""
        self.account_values = []
        self.account_comments = []

    def saldo_operation(self):
        print("saldo operation")
        self.input_check = self.input_balance()
        if self.input_check:
            self.account_balance += self.account_value
            self.oper_append_balance()
            self.input_log_extend()
            self.index_balance += 1
            manager.index += 1
            print("saldo operation successful")
    
    def input_balance(self):
        if not self.account_value:
            self.account_value = "ERROR"
        else:
            self.account_value = int(self.account_value)
        if self.account_balance + self.account_value < 0 or not self.account_comment:
            self.account_value = int(self.account_value)
            self.account_comment = "ERROR"
            return False
        return True


    def oper_append_balance(self):
        self.account_values.append(self.account_value)
        self.account_comments.append(self.account_comment)
        manager.operations_type.append("saldo")
        manager.operations.append(f"Operation in mode 'saldo' number"
                            f" {str(self.index_balance + 1)}:"
                            f" {str(self.account_values[self.index_balance])} - "
                            f"description: {self.account_comments[self.index_balance]}")

    def input_log_extend(self):
        manager.inputlog.extend(("saldo", self.account_values[-1], self.account_comments[-1]))

class Products():
    def __init__(self):
        self.trade_items = {
            'ABC': 50,
        }

class Zakup():

    def __init__(self):
        self.index_purch = 0
    
    def zakup_operation(self):
        print("zakup operation")
        self.input_trade()
        self.item_loop_purch()
        self.trade_items_check()
        saldo.account_balance -= self.item_price * self.item_quantity
        self.input_log_extend()
        self.oper_append_purch()
        self.index_purch += 1
        manager.index += 1


    def input_trade(self):
        self.item_name = input_list()
        self.item_price = int(input_list())
        self.item_quantity = int(input_list())
        if not self.account_value:
            self.account_value = "ERROR"
        else:
            self.account_value = int(self.account_value)
        if self.account_balance + self.account_value < 0 or not self.account_comment:
            self.account_value = int(self.account_value)
            self.account_comment = "ERROR"
            return False
        return True

    def item_loop_purch(self):
        while ((self.item_price <= 0) or (self.item_quantity <= 0)):
                self.item_price = int(input_list())
                self.item_quantity = int(input_list())

    def input_check_purch(self):
        self.item_loop_purch()

    def trade_items_check(self):
            if self.item_name not in products.trade_items:
                products.trade_items[self.item_name] = self.item_quantity
            else:
                products.trade_items[self.item_name] += self.item_quantity

    def oper_append_purch(self):
        manager.operations_type.append("zakup")
        manager.operations.append(f"Operation in mode 'zakup'" 
                            f"number {str(self.index_purch + 1)}:"
                            f"Item:{self.item_name} purchased {self.item_quantity}"
                            f" pcs for price {self.item_price}gr")

    def input_log_extend(self):
        manager.inputlog.extend(("zakup", self.item_name, self.item_price, self.item_quantity))


class Sprzedaz():
    
    def __init__(self):
        self.index_sell = 0

    def sprzedaz_operation(self):
        print("sprzedaz operation")
        Zakup.input_trade(self)
        self.input_check_sell()
        self.item_loop_sell()
        self.trade_items_check()
        saldo.account_balance += self.item_price * self.item_quantity
        self.input_log_extend()
        self.oper_append_sell()
        self.index_sell += 1
        manager.index += 1
    
    def item_loop_sell(self):
        while ((self.item_price <= 0) or (self.item_quantity <= 0)
            or (products.trade_items[self.item_name] < self.item_quantity)):
                self.item_price = int(input_list())
                self.item_quantity = int(input_list())

    def input_check_sell(self):
        while self.item_name not in products.trade_items:
            self.item_name = input_list()
        self.item_loop_sell()

    def oper_append_sell(self):
        manager.operations_type.append("sprzedaż")
        manager.operations.append(f"Operation in mode 'sprzedaż' number"
                            f"{str(self.index_sell + 1)}:"
                            f"Item:{self.item_name} sold {self.item_quantity}" 
                            f" pcs for price {self.item_price}gr")

    def trade_items_check(self):
        products.trade_items[self.item_name] -= self.item_quantity

    def input_log_extend(self):
        manager.inputlog.extend(("sprzedaż", self.item_name, self.item_price, self.item_quantity))
        
saldo = Saldo()
sprzedaz = Sprzedaz()
zakup = Zakup()
products = Products()
manager = Manager()