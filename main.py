import pandas
from fpdf import FPDF

df = pandas.read_csv("articles.csv", dtype={"id": str, "in stock":int})


class Item:
    def __init__(self, item_id):
        self.item_id = item_id
        self.name = df.loc[df["id"] == self.item_id, "name"].squeeze()
        self.price = df.loc[df["id"] == self.item_id, "price"].squeeze()

    def buy(self):
        """Buy an item and change its stock"""
        df.loc[df["id"] == self.item_id, "in stock"] = \
            df.loc[df["id"] == self.item_id, "in stock"] - 1
        df.to_csv("articles.csv", index=False)

    def available(self):
        """Check if the item is in stock"""
        in_stock = df.loc[df["id"] == self.item_id, "in stock"].squeeze()
        return in_stock
        # if availability > 0:
        #     return True
        # else:
        #     return False


class Receipt:
    def __init__(self, item_object):
        self.item = item_object

    def generate(self):
        pdf = FPDF(orientation="P", format="A4")
        pdf.add_page()

        pdf.set_font(family="Times", style="B", size=24)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(w=30, h=8, txt=f"Receipt nr: {self.item.item_id}", ln=1)
        pdf.cell(w=30, h=8, txt=f"Item: {self.item.name}", ln=1)
        pdf.cell(w=30, h=8, txt=f"Price: {self.item.price}", ln=1)

        pdf.output("receipt.pdf")


print(df)
item_id = input("Choose an item to buy: ")
item = Item(item_id)

if item.available():
    item.buy()
    receipt = Receipt(item_object=item)
    receipt.generate()
else:
    print("Item not in the inventory")
