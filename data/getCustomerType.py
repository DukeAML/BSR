import requests
import json
import pandas as pd
import time


# Constants for API call
API_KEY = '44ea3bf2fd0d37eb6d39b576846c69187ffe34fd39177373'
headers = {'Content-Type': 'application/json'}


def callCustomers(pageNum):
    """API call for customers
    """
    URL = 'https://app.getsweet.com/api/v1/customers'
    payload = {'token': API_KEY, 'page':pageNum}
    r = requests.get(url=URL, headers=headers, params=payload)
    data = r.json()
    return data


def initCTypeMapping():
    """Create initial CSV for Customer To Customer Type mapping
    """
    start_time = time.time()

    columns = ["Customer Name", "Customer ID", "Customer Type ID"]
    allCustomers = []
    totalPages = callCustomers(1)['meta']['total_pages']

    for pageNum in range(1, totalPages+1):
        data = callCustomers(pageNum)
        while ('customers' not in data):
            print("Pausing execution for API time delay...")
            time.sleep(10)
            data = callCustomers(pageNum)
        print("Integrating page:", data['meta']['current_page'])

        for customer in data['customers']:
            # check if inactive
            if (customer['inactive_date'] is not None):
                print("Customer: " + str(customer['fully_qualified_name']) + " was found to be inactive. Excluding from map. ID:", customer['id'])
                continue

            cname = customer['fully_qualified_name']
            cid = customer['id']
            ctype_id = customer['customer_type_id']
            if cname[:7].lower()=='shopify' and ctype_id is None:
                ctype_id = 324

            values = [cname, cid, ctype_id]
            allCustomers.append(values)

    df = pd.DataFrame(allCustomers, columns=columns)
    df.to_csv(r'customer_type_map.csv', index=False, header=True)

    print("--- %s seconds ---" % (time.time() - start_time))


def addCMap(customerid, pageNum=1):
    """Adds a customer with customerid to mapping CSV
    """
    URL = 'https://app.getsweet.com/api/v1/customers/' + str(customerid)
    payload = {'token': API_KEY, 'page':pageNum}
    r = requests.get(url=URL, headers=headers, params=payload)
    data = r.json()
    return data


def updateCMap(newOrdersdf, date_since_last_update):
    """Cross-checks orders csv to determine if there exist any new customers, if so, add them to the mapping CSV
    """

    return

# def add_new_row(file_name, elements):
#     ''' Appends a list that contains a new order to the csv file '''
#     with open(file_name, 'a+', newline='') as write_obj:
#         # Create a writer object from csv module
#         csv_writer = writer(write_obj)
#         csv_writer.writerow(elements)


def callCType(pageNum):
    """API call for customer types
    """
    URL = 'https://app.getsweet.com/api/v1/customer_types'
    payload = {'token': API_KEY, 'page':pageNum}
    r = requests.get(url=URL, headers=headers, params=payload)
    data = r.json()
    return data


def getCustomerTypes():
    """Get customer types and convert into dictionary
    """
    ctypes = dict()

    # Get total pages and retrieve customer types
    totalPages = callCType(1)['meta']['total_pages']

    for pageNum in range(1, totalPages+1):
        data = callCType(pageNum)

        # Add to dictionary
        for customer_type in data['customer_types']:
            CID = customer_type['id']
            label = customer_type['name']
            ctypes[CID] = label

    return ctypes


def main():
    ctypes = getCustomerTypes()
    initCTypeMapping()


if __name__=="__main__":
    main()
