import streamlit as st
import pandas as pd
import boto3
from decimal import Decimal

ACCESS_KEY_ID = 'AKIA44U6K7NFXCTYWIJB'
SECRET_ACCESS_KEY = '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'
dynamoDB = boto3.resource('dynamodb', aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY)
table = dynamoDB.Table('inventory')
is_first_run = True

#@st.cache(persist=True)
def get_data():
    df = pd.DataFrame(table.scan(Limit=20)['Items'])

    return df

def create_item(pro_id, name, price, quan):
    item = {
        'product_id': pro_id,
        'product_name': name,
        'price': Decimal(price),
        'quantity': Decimal(quan),
    }
    return item

product_id_place = st.sidebar.empty()
product_id = product_id_place.text_input('Product Id (*):', key='1')
product_name = st.sidebar.text_input('Product Name:', key='2')
price = st.sidebar.number_input('Price:', key='1')
quantity = st.sidebar.number_input('Quantity:', key='2')

btn_record = st.sidebar.button('Record', key='1')

df = get_data()

st.write('This is table from AWS DynamoDB')

data_place = st.empty()

if (is_first_run or btn_record):
    data_place.dataframe(df, width=1000, height=200)

st.write(product_id)


if btn_record:
    is_first_run = False


if (product_id != '') and (product_name != '') and (quantity != 0):
    st.write('Ok to add new item')
    if btn_record:
        new_item = create_item(product_id, product_name, price, quantity)
        response = table.put_item(Item=new_item)
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            df = get_data()
            data_place.dataframe(df, width=1000, height=200)
            st.success('New item is added to DB')

