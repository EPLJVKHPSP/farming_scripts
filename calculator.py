from pycoingecko import CoinGeckoAPI

def get_price(crypto_name):
    cg_client = CoinGeckoAPI()
    data = cg_client.get_price(ids = crypto_name, vs_currencies = 'usd')
    return data[crypto_name]['usd']

def calculate_il():
    # Get inputs
    crypto1_name = input("Enter the name of the first cryptocurrency: ")
    crypto1_qty_before = float(input(f"Enter the quantity of {crypto1_name} before: "))
    crypto1_qty_after = float(input(f"Enter the quantity of {crypto1_name} after: "))

    crypto2_name = input("Enter the name of the second cryptocurrency: ")
    crypto2_qty_before = float(input(f"Enter the quantity of {crypto2_name} before: "))
    crypto2_qty_after = float(input(f"Enter the quantity of {crypto2_name} after: "))

    while True:
        try:
            commission = float(input("Enter the commission: "))
            break
        except ValueError:
            print("Invalid input. Please enter a numeric value for the commission.")

    # Calculate impermanent loss
    if crypto1_qty_before > crypto1_qty_after:
        changed_crypto_qty = crypto1_qty_before - crypto1_qty_after
        changed_crypto_price = get_price(crypto1_name)
        changed_amount_usd = changed_crypto_qty * changed_crypto_price
        crypto2_price = get_price(crypto2_name)
        changed_amount_crypto2 = changed_amount_usd / crypto2_price
        il = (crypto2_qty_after - crypto2_qty_before - changed_amount_crypto2) * crypto2_price + commission
    else:
        changed_crypto_qty = crypto2_qty_before - crypto2_qty_after
        changed_crypto_price = get_price(crypto2_name)
        changed_amount_usd = changed_crypto_qty * changed_crypto_price
        crypto1_price = get_price(crypto1_name)
        changed_amount_crypto1 = changed_amount_usd / crypto1_price
        il = (crypto1_qty_after - crypto1_qty_before - changed_amount_crypto1) * crypto1_price + commission

    return round(il, 2)

il = calculate_il()
print(f"The impermanent loss is: {il}$")
