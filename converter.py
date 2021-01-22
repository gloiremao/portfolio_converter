import json
import argparse
import csv
from dataclasses import dataclass

@dataclass
class Portfolio:
    
    records: list
    mapping: dict

    def __init__(self, mapping):
        self.mapping = mapping
        self.records = []

    def export(self, to="yahoo"):
        table = {}
        for record in self.records:
            if record.get("symbol") not in table:
                table[record.get("symbol")] = float(record.get("quantity"))
            else:
                table[record.get("symbol")] += float(record.get("quantity"))
            
        print("Symbol,Current Price,Date,Time,Change,Open,High,Low,Volume,Trade Date,Purchase Price,Quantity,Commission,High Limit,Low Limit,Comment")
        for record in self.records:
            if table[record.get("symbol")] != 0:
                print("%s,,,,,,,,,%s,%s,%s,,,," % (record.get("symbol"),record.get("tradeDate"),record.get("price"),record.get("quantity")))
    

def firsttrade_reader(input_file_path, portfolio):
    with open(input_file_path, 'r', encoding="utf-8") as fp:
        rows = csv.reader(fp)
        next(rows, None)
        for row in rows:
            symbol = row[0].strip()
            if not symbol:
                continue
            record = {
                "symbol": symbol,
                "tradeDate": row[5].replace("-",""),
                "price": row[2],
                "quantity": row[1],
                "commission": row[9],
                "comment": None
            }
            portfolio.records.append(record)



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=' args')
    parser.add_argument(
        "-f", '--from-source', help='source name of input file', required=True)
    parser.add_argument(
        "-i", '--input', help='input file path', required=True)
    parser.add_argument(
        "-t", '--to', help='source name of output file', required=False, default="yahoo")

    args = parser.parse_args()
    input_path = args.input
    source = args.from_source

    config = {}
    with open("./config/mapping.json", "r" ,encoding="utf-8") as fp:
        config = json.load(fp)

    # read input file
    portfolio = Portfolio(config.get("fields"))
    firsttrade_reader(input_path,portfolio)
    portfolio.export()

    pass