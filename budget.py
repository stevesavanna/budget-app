class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []
        self.__balance = 0.0

    def __repr__(self):
        ledger = ""
        for item in self.ledger:
            ledger += "{:<23.23}{:.7}\n".format(item["description"], "{:>7.2f}".format(item["amount"]))

        return "{:*^30}\n{}Total: {:.2f}".format(self.name, ledger, self.__balance)

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})
        self.__balance += amount

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": -1 * amount, "description": description})
            self.__balance -= amount
            return True
        else:
            return False

    def get_balance(self):
        return self.__balance

    def transfer(self, amount, category_instance):
        if self.withdraw(amount, "Transfer to " + category_instance.name):
            category_instance.deposit(amount, "Transfer from " + self.name)
            return True
        else:
            return False

    def check_funds(self, amount):
        if self.__balance >= amount:
            return True
        else:
            return False


def create_spend_chart(categories):
    chart = "Percentage spent by category\n"
    spent_amounts = {}
    for category in categories:
        spent_amounts[category.name] = round(abs(sum(list(map(lambda item: item["amount"] if item["amount"] < 0 else 0, category.ledger)))), 2)
    total_spent = round(sum(spent_amounts.values()), 2)

    for label in reversed(range(0, 101, 10)):
        chart += "{:>3}|".format(str(label))
        for percent in list(map(lambda amount: int(amount / total_spent // 0.1 * 10), spent_amounts.values())):
            if percent >= label:
                chart += " o "
            else:
                chart += "   "
        chart += " \n"

    chart += "    {:-<{}}\n".format("", 3 * len(categories) + 1)

    max_length = max(map(lambda n: len(n), spent_amounts.keys()))
    for name in zip(*list(map(lambda n: n.ljust(max_length), spent_amounts.keys()))):
        chart += "    " + "".join(map(lambda s: " {} ".format(s), name)) + " \n"

    return chart.rstrip("\n")
