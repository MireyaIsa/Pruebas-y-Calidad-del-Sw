import json
import sys
import time

def load_json_file(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error al cargar {filename}: {e}")
        return {}

def compute_total_cost(price_catalogue, sales_record):
    total_cost = 0.0
    for sale in sales_record:
        product_title = sale.get("Product")
        quantity = sale.get("Quantity")
        product_info = next((item for item in price_catalogue if item["title"] == product_title), None)
        if product_info:
            total_cost += product_info["price"] * quantity
        else:
            print(f"Advertencia: El producto '{product_title}' No existe en el catálogo")
    return total_cost

def main():
    if len(sys.argv) != 3:
        print("Uso: python computeSales.py priceCatalogue.json salesRecord.json")
        return

    price_catalogue_file = sys.argv[1]
    sales_record_file = sys.argv[2]

    price_catalogue = load_json_file(price_catalogue_file)
    sales_record = load_json_file(sales_record_file)
    
    if not price_catalogue or not sales_record:
        print("Invalid data in input files.")
        return

    start_time = time.time()
    total_cost = compute_total_cost(price_catalogue, sales_record)
    elapsed_time = time.time() - start_time

    result_message = f"Total de ventas: ${total_cost:.2f}\nExecution time: {elapsed_time:.2f} seconds"
    
    print(result_message)

    with open("SalesResults.txt", "w") as result_file:
        result_file.write(result_message)

if __name__ == "__main__":
    main()
