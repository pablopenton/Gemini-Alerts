import argparse
import logging
import statistics as st

from utils.gemini_api import GeminiAPI

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(funcName)s %(message)s',
)


def determine_price_dev(symbol):
    """
    Determines whether current price is greater than standard deviation.

    :param symbol: string. Supplied from CLI args.
    :return: None. Outputs to console.
    """
    logging.info("Running check: pricedev")
    # Get symbol data
    gem_api = GeminiAPI()
    r = gem_api.get_sym_ticker(symbol)
    sym_ticker = r.json()
    # Hourly prices for past 24 hours
    prices = sym_ticker.get('changes')
    if not prices:
        logging.error(f"No prices found via API.")
        return
    # Convert to floats
    prices_num = [float(price) for price in prices]
    # Get average of prices
    avg_price = sum(prices_num) / len(prices_num)
    logging.info(f"Average price: {avg_price}")
    # Calculate standard deviation
    std_dev = st.stdev(prices_num)
    logging.info(f"Standard deviation: {std_dev}")
    # Get last price
    current_price = sym_ticker.get('close')
    current_price = float(current_price)
    logging.info(f"Current price: {current_price}")
    # Determine current deviation
    deviation = abs(current_price - avg_price)
    logging.info(f"Deviation of current price: {deviation}")
    # Determine whether current deviation is greater than standard
    price_dev = deviation > std_dev
    logging.info(f"Price greater than standard deviation: {price_dev}")


def determine_price_change(symbol, per_threshold):
    """
    Determines whether percentage diff from start price to current price is
    greater than threshold.

    :param symbol: string. Supplied from CLI args.
    :param per_threshold: float. Supplied from CLI args
    :return: None. Outputs to console.
    """
    # Create API object
    gem_api = GeminiAPI()
    r = gem_api.get_sym_ticker(symbol)
    sym_ticker = r.json()
    logging.debug(sym_ticker)
    # Get start and current price
    start_price = float(sym_ticker.get('open'))
    logging.info(f"Start price: {start_price}")
    current_price = float(sym_ticker.get('close'))
    logging.info(f"Current price: {current_price}")
    # Calculate percentage difference
    try:
        percent_diff = (abs(current_price - start_price) / start_price) * 100.0
    except ZeroDivisionError as err:
        logging.error(f"Error: {err}")
        return
    logging.info(f"Percentage difference: {percent_diff}")
    # Determine whether greater than threshold
    percent_dev = percent_diff > per_threshold
    logging.info(f"Percentage difference greater than deviation: {percent_dev}")


def determine_vol_deviation(symbol, per_threshold):
    """
    Determines whether volume of last trade is greater than threshold of last 24
    hours.

    :param symbol: string. Supplied from CLI args.
    :param per_threshold: float. Supplied from CLI args.
    :return: None. Output to console.
    """
    # Create API object
    gem_api = GeminiAPI()
    # Get trade info of last 24 hours.
    r = gem_api.get_pub_ticker(symbol)
    pub_ticker = r.json()
    # Volume for the day. Opportunity for better handling of missing data.
    day_volume = pub_ticker.get('volume', {}).get('BTC')
    if day_volume:
        day_volume = float(day_volume)
        logging.info(f"Trading volume last 24 hours: {day_volume}")
        # Exit if no day volume found.
        if day_volume == 0.0:
            logging.error(f"No historical trading volume found.")
            return
    else:
        logging.error(f"No historical trading volume found.")
        return
    # Get last trade info
    last_trade_r = gem_api.get_last_trade(symbol)
    last_trade = last_trade_r.json()
    # Get last trade volume
    try:
        last_trade_volume = float(last_trade[0].get('amount'))
    except IndexError:
        logging.error(f"No historical trading data.")
        return
    logging.info(f"Last trade volume: {last_trade_volume}")
    l_trade_vol_percent = (last_trade_volume / day_volume) * 100
    logging.info(
        f"Last trade volume greater than threshold: {l_trade_vol_percent}"
    )


def args_handler(args):
    """
    Handles args passed from command line to run corresponding task
    functions. Opportunity to refactor this with a better dispatcher.
    :param args: argsparser object
    :return: None. Subtasks print to command line.
    """
    # Exit if deviation threshold not provided for tasks that require it.
    if not args.deviation and args.type != 'pricedev':
        logging.warning('Error: deviation threshold required when checking '
                        'for price change and volume deviation')
        return
    # Output deviation if supplied
    if args.deviation:
        logging.info(f"Using deviation threshold: {args.deviation}")
    # If currency not provided, assume all are wanted.
    if not args.currency:
        # Create API object
        gem_api = GeminiAPI()
        # Get all symbols
        symbols_r = gem_api.get_all_symbols()
        symbols = symbols_r.json()
    # If provided, place in list to simplify iteration logic
    else:
        symbols = [args.currency]
    # Iterate over symbols provided and grab information as type arg dictates
    for sym in symbols:
        logging.info(f"Running checks for symbol: {sym}")
        if args.type == 'pricedev':
            determine_price_dev(sym)
        if args.type == 'pricechange':
            determine_price_change(sym, args.deviation)
        if args.type == 'voldev':
            determine_vol_deviation(sym, args.deviation)
        if args.type == 'ALL':
            determine_price_dev(sym)
            determine_price_change(sym, args.deviation)
            determine_vol_deviation(sym, args.deviation)


if __name__ == '__main__':
    logging.info('Starting main task...')
    logging.info('Parsing args')
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Gemini trade alerts')
    parser.add_argument('-c', '--currency', help='currency symbol')
    parser.add_argument('-t', '--type',
                        help='Type of check to run or all. Required.',
                        choices=['pricedev', 'pricechange', 'voldev', 'ALL'],
                        required=True)
    parser.add_argument('-d', '--deviation',
                        help='percentage threshold for deviation check.',
                        type=float)
    args = parser.parse_args()
    logging.debug(args)
    # Send args to handler function
    args_handler(args)
    logging.info('Main task finished.')



# sym_dev = determine_price_dev('btcusd')
# print(sym_dev)
#
# print(determine_price_change('btcusd', 0.1))
#
# print(determine_vol_deviation('btcusd', 2))



