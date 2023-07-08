Telegram Crypto Liquidity Pool Impermanent Loss Calculator (Calc-2.0)
This Python-based Telegram bot allows users to calculate the impermanent loss in a cryptocurrency liquidity pool. The bot interacts with users conversationally, requesting their initial and final token positions (names and quantities) along with the farmed commission, and then calculates the impermanent loss based on real-time cryptocurrency prices fetched from the CoinGecko API.

New Features in Calc-2.0
Migrated from a terminal-based application to an interactive Telegram bot interface.
The bot fetches real-time cryptocurrency prices from CoinGecko API.
Provided a multi-stage conversational interface for data input.
Allows users to navigate back or cancel the operation at any stage.
Calculates the impermanent loss based on user-provided data.
Requirements
Python 3.x
A valid Telegram bot token.
Usage
Clone the repository or download the calculator_bot.py file to your local machine.
Set your Telegram bot token in the script.
Open a terminal or command prompt and navigate to the directory where calculator_bot.py is located.
Run the following command to execute the script:
bash
Copy code
python calculator_bot.py
Interact with the bot on Telegram:
Enter the tokens' names and quantities before and after liquidity provisioning.
Enter the farmed commission.
The bot will calculate the impermanent loss and display the result.
Please note: For the security of the application, do not share the bot token publicly, as it's hardcoded in the main function. You might want to consider setting it through environment variables or a secure configuration file.

Disclaimer: The information provided by this bot should be used for informational purposes only. The calculation is dependent on current prices which can fluctuate. Always do your own research before making any investment decisions.
Follow the prompts on the terminal to enter the necessary information:

Enter the tokens and quantities in your position.
Enter the current price.
Enter the commissions from the liquidity pool.
The script will calculate the impairment loss based on the provided information and display the result.
