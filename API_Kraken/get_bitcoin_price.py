import requests, datetime, click, time, logging, csv

logging.basicConfig(level=logging.INFO, format='%(message)s')

def get_price():
    try:
        get_request = requests.get('https://api.kraken.com/0/public/Ticker?pair=XBTUSD')
        price = get_request.json()['result']['XXBTZUSD']['a'][0]
        date = datetime.datetime.now().strftime('%c')
        day_date = datetime.datetime.now().strftime('%x')
    except Exception as e:
        raise Exception(f'An error has occured due to: {e}')
    return price, date, day_date

def append_data_file(data_file, price, date):
    with open(data_file, 'a', newline= '') as file_csv:
        writer = csv.writer(file_csv, delimiter = ';')
        writer.writerow([price, date])

def remove_data_file(data_file, date):
    filename = data_file
    clear = open(filename, 'w')
    clear.truncate()
    clear.close()
    with open(data_file, 'a', newline = '') as file_csv:
        writer = csv.writer(file_csv, delimiter = ';')
        writer.writerow(["Price of Bitcoin for", date])

@click.command()
@click.option('--data_file', help = 'Path to datafile.')
@click.option('--break_time', default = 5, help = 'Time of a break between prices.')
def main(break_time, data_file):
    price, date, day_date = get_price()
    remove_data_file(data_file, day_date)
    while True:
        price, date, day_date = get_price()
        append_data_file(data_file, price, date)
        logging.info(f"Price of Bitcoin for: {date}")
        logging.info(f"{price}")
        logging.info("Waiting " + str(break_time) + " seconds for next fetch.\n")
        time.sleep(int(break_time))

if __name__ == "__main__":
    main()