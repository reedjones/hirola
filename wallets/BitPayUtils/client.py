from bitpay.exceptions import *
import bitpay.key_utils as bku
from bitpay.client import *
import pprint
import requests
import json
import re
import os.path

dirname = os.path.dirname(__file__)
# API_HOST = "https://bitpay.com" #for production, live bitcoin
API_HOST = "https://test.bitpay.com"  # for testing, testnet bitcoin
KEY_FILE = os.path.join(dirname, "tmp/key.priv")
TOKEN_FILE = os.path.join(dirname, "tmp/token.priv")

# check if there is a preexisting key file
if os.path.isfile(KEY_FILE):
    with open(KEY_FILE, 'r') as f:
        key = f.read()

    print("Creating a bitpay client using existing private key from disk.")
else:
    key = bku.generate_pem()
    with open(KEY_FILE, 'w') as f:
        f.write(key)

client = Client(API_HOST, False, key)


def fetch_token(facade):
    if os.path.isfile(TOKEN_FILE + facade):
        print("Reading " + facade + " token from disk.")
        with open(TOKEN_FILE + facade, 'r') as ft:
            fetched_token = ft.read()
        # global client
        # client = Client(API_HOST, False, key, {facade: token})
        client.tokens[facade] = fetched_token
    else:
        pairing_code = client.create_token(facade)
        print("Creating " + facade + " token.")
        print(
            "Please go to:  %s/dashboard/merchant/api-tokens  then enter \"%s\" then click the \"Find\" button, "
            "then click \"Approve\"" % (
                API_HOST, pairing_code))
        input("When you've complete the above, hit enter to continue...")
        print("token is: %s" % client.tokens[facade])

        with open(TOKEN_FILE + facade, 'w') as ft:
            ft.write(client.tokens[facade])


def get_from_bitpay_api(client, uri, token):
    payload = "?token=%s" % token
    xidentity = bku.get_compressed_public_key_from_pem(client.pem)
    xsignature = bku.sign(uri + payload, client.pem)
    headers = {"content-type": "application/json",
               "X-Identity": xidentity,
               "X-Signature": xsignature, "X-accept-version": "2.0.0"}
    try:
        # pp.pprint(headers)
        print(uri + payload)
        response = requests.get(uri + payload, headers=headers, verify=client.verify)
    except Exception as pro:
        raise BitPayConnectionError(pro.args)
    if response.ok:
        return response.json()['data']
    client.response_error(response)


"""
POST to any resource
Make sure to include the proper token in the params
"""


def post_to_bitpay_api(client, uri, resource, params):
    payload = json.dumps(params)
    uri = uri + "/" + resource
    xidentity = key_utils.get_compressed_public_key_from_pem(client.pem)
    xsignature = key_utils.sign(uri + payload, client.pem)
    headers = {"content-type": "application/json",
               "accept": "application/json", "X-Identity": xidentity,
               "X-Signature": xsignature, "X-accept-version": "2.0.0"}
    try:
        response = requests.post(uri, data=payload, headers=headers,
                                 verify=client.verify)
    except Exception as pro:
        raise BitPayConnectionError(pro.args)
    if response.ok:
        return response.json()['data']
    client.response_error(response)


def grab_existing_invoice(iid):
    """
    this gets an existing invoice
    :param iid: the invoice id
    :return: the response from bitpay api
    """
    fetch_token("merchant")
    token_ = client.tokens['merchant']
    result = get_from_bitpay_api(client, client.uri + "/invoice/" + iid, token_)

    return result


def grab_invoice(price):
    """
    this creates an invoice
    :param price:
    :return:
    """
    fetch_token("merchant")
    result = client.create_invoice({
        "price": price,
        "currency": "EUR",
        "token": client.tokens['merchant']
    })
    invoice_id = result['id']
    token_ = client.tokens['merchant']
    print("**")
    print("Fetching an invoice with invoiceId " + invoice_id)
    print("**")
    invoice_ = get_from_bitpay_api(client, client.uri + "/invoices/" + invoice_id, token_)

    return invoice_


if __name__ == '__main__':
    fetch_token("merchant")
    print(client.tokens)
    # Now we assume that the pairing code that we generated along with the crypto keys is paired with your merchant
    # account
    #
    print("We will create an invoice using the merchant facade")

    invoice = client.create_invoice({"price": 50.00, "currency": "EUR", "token": client.tokens['merchant']})

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(invoice)

    print("hopefully the above looks OK?")

    print("continuing if we can...")

    invoiceId = invoice['id']
    print("**")
    print("Fetching an invoice with invoiceId " + invoiceId)
    print("**")
    token = client.tokens['merchant']
    invoice = get_from_bitpay_api(client, client.uri + "/invoices/" + invoiceId, token)
    pp.pprint(invoice)
