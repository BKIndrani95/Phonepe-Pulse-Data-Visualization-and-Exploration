#*****************************************PhonePe Pulse Data Visualization and Exploration*****************************
#------------------------------------------------------------------------------------------------------------------

#Import necessary packages
import streamlit as st
import json
import locale
import mysql.connector
import os
import plotly.graph_objects as go
import pandas as pd
import pymysql
import matplotlib.pyplot as plt
import plotly.express as px
from streamlit_option_menu import option_menu

#clone data from github and convert it as a DataFrame
def get_agg_transaction():
    path = r'C:\Users\HP\PycharmProjects\pulse\data\aggregated\transaction\country\india\state'
    agg_state_list = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]  # Filter out non-directory files
    agg_trans_data = {"state": [], "year": [], "quarter": [], "transaction_type": [], "transaction_count": [],
                      "transaction_amount": []}

    for state in agg_state_list:
        path1 = os.path.join(path, state)
        year_list = os.listdir(path1)

        for year in year_list:
            path2 = os.path.join(path1, year)
            quarter_list = os.listdir(path2)

            for quarter in quarter_list:
                path3 = os.path.join(path2, quarter)
                with open(path3, "r") as data_file:
                    d = json.load(data_file)

                for i in d["data"]["transactionData"]:
                    Name = i['name']
                    count = i['paymentInstruments'][0]['count']
                    amount = i['paymentInstruments'][0]['amount']
                    agg_trans_data["transaction_type"].append(Name)
                    agg_trans_data["transaction_count"].append(count)
                    agg_trans_data["transaction_amount"].append(amount)
                    agg_trans_data["state"].append(state)
                    agg_trans_data["year"].append(year)
                    agg_trans_data["quarter"].append(quarter.strip(".json"))

    agg_trans = pd.DataFrame(agg_trans_data)
    agg_trans["state"] = agg_trans["state"].astype("str").str.replace("-", " ").str.title()
    return agg_trans

def get_agg_user():
    path = r'C:\Users\HP\PycharmProjects\pulse\data\aggregated\user\country\india\state'
    agg_state_list = os.listdir(path)
    agg_user_data = {"state": [], "year": [], "quarter": [], "Registered_users": [], "App_opens": []}

    for state in agg_state_list:
        path1 = path + "/" + state
        year_list = os.listdir(path1)

        for year in year_list:
            path2 = path1 + "/" + year
            quarter_list = os.listdir(path2)

            for quarter in quarter_list:
                path3 = path2 + "/" + quarter
                data = open(path3, "r")
                d = json.load(data)

                for i in d['data'].items():
                    aggregated_data = d['data'].get('aggregated', {})
                    reg_use = aggregated_data.get('registeredUsers')
                    appOpens = aggregated_data.get('appOpens')
                    agg_user_data["Registered_users"].append(reg_use)
                    agg_user_data["App_opens"].append(appOpens)
                    agg_user_data["state"].append(state)
                    agg_user_data["year"].append(year)
                    agg_user_data["quarter"].append(quarter.strip(".json"))

    agg_user = pd.DataFrame(agg_user_data)
    agg_user_data["state"] = [state.replace("-", " ").title() for state in agg_user_data["state"]]
    return agg_user
def get_map_transaction():
  path = r'C:\Users\HP\PycharmProjects\pulse\data\map\transaction\hover\country\india\state'
  agg_state_list= os.listdir(path)
  map_trans_data = {"state": [], "year": [], "quarter": [], "district": [], "transaction_count": [], "transaction_amount": []}

  for state in agg_state_list:
    path1 = path + "/" + state
    year_list = os.listdir(path1)

    for year in year_list:
      path2 = path1 + "/" + year
      quarter_list = os.listdir(path2)

      for quarter in quarter_list:
        path3 = path2 + "/" + quarter
        with open(path3, "r") as data_file:
          d = json.load(data_file)
          for i in d["data"]:
            hovD = d['data'].get('hoverDataList', {})
            for j in hovD:
              map_trans_data["district"].append(j.get("name"))
              map_trans_data["transaction_count"].append(j['metric'][0]['count'])
              map_trans_data["transaction_amount"].append(j['metric'][0]['count'])
              map_trans_data["state"].append(state)
              map_trans_data["year"].append(year)
              map_trans_data["quarter"].append(quarter.strip(".json"))

  map_transaction = pd.DataFrame(map_trans_data)
  map_transaction["state"] = [state.replace("-", " ").title() for state in map_trans_data["state"]]
  return map_transaction

mapping_transaction = get_map_transaction()
def get_map_user():
  path = r'C:\Users\HP\PycharmProjects\pulse\data\map\user\hover\country\india\state'
  agg_state_list= os.listdir(path)

  map_user_data = {"state": [], "year": [], "quarter": [], "district": [], "Registered_users": [], "App_opens": []}

  for state in agg_state_list:
    path1 = path + "/" + state
    year_list = os.listdir(path1)

    for year in year_list:
      path2 = path1 + "/" + year
      quarter_list = os.listdir(path2)

      for quarter in quarter_list:
        path3 = path2 + "/" + quarter
        data = open(path3, "r")
        d = json.load(data)

        for j in d["data"]["hoverData"].items():
            map_user_data["district"].append(j[0])
            map_user_data["Registered_users"].append(j[1]["registeredUsers"])
            map_user_data["App_opens"].append(j[1]["appOpens"])
            map_user_data["state"].append(state)
            map_user_data["year"].append(year)
            map_user_data["quarter"].append(quarter.strip(".json"))

  map_user = pd.DataFrame(map_user_data)
  map_user["state"] = [state.replace("-", " ").title() for state in map_user_data["state"]]
  return map_user
mapping_users = get_map_user()

def get_top_transaction():
    path = r'C:\Users\HP\PycharmProjects\pulse\data\top\transaction\country\india\state'
    agg_state_list = os.listdir(path)
    top_trans_data = {"state": [], "year": [], "quarter": [], "pincode": [], "transaction_count": [], "transaction_amount": []}

    for state in agg_state_list:
        path1 = path + "/" + state
        year_list = os.listdir(path1)

    for year in year_list:
        path2 = path1 + "/" + year
        quarter_list = os.listdir(path2)

        for quarter in quarter_list:
            path3 = path2 + "/" + quarter
            data = open(path3, "r")
            d = json.load(data)

            for i in d["data"]["pincode"]:
                top_trans_data["pincode"].append(i["entityName"])
                top_trans_data["transaction_count"].append(i["metric"]["count"])
                top_trans_data["transaction_amount"].append(i["metric"]["amount"])
                top_trans_data["state"].append(state)
                top_trans_data["year"].append(year)
                top_trans_data["quarter"].append(quarter.strip(".json"))

    top_transaction = pd.DataFrame(top_trans_data)
    top_transaction["state"] = [state.replace("-", " ").title() for state in top_trans_data["state"]]
    return top_transaction
def get_top_user():
    path = r'C:\Users\HP\PycharmProjects\pulse\data\top\user\country\india\state'
    agg_state_list = os.listdir(path)

    top_user_data = {"state": [], "year": [], "quarter": [], "pincode": [], "Registered_users": []}

    for state in agg_state_list:
        path1 = path + "/" + state
        year_list = os.listdir(path1)

        for year in year_list:
            path2 = path1 + "/" + year
            quarter_list = os.listdir(path2)

            for quarter in quarter_list:
                path3 = path2 + "/" + quarter
                data = open(path3, "r")
                d = json.load(data)

                for j in d["data"]["pincode"]:
                    top_user_data["pincode"].append(j["name"])
                    top_user_data["Registered_users"].append(j["registeredUsers"])
                    top_user_data["state"].append(state)
                    top_user_data["year"].append(year)
                    top_user_data["quarter"].append(quarter.strip(".json"))

    top_user = pd.DataFrame(top_user_data)
    top_user["state"] = [state.replace("-", " ").title() for state in top_user_data["state"]]
    return top_user

#MYSQL Connection
mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Indranibk95@",
        database="phonepe",
        auth_plugin='mysql_native_password')
cursor = mydb.cursor()
mydb.commit()

# Create Tables in MYSQL
def table_creation():
    query = '''CREATE TABLE IF NOT EXISTS agg_transaction(state VARCHAR(50),
                        year INT,
                        quarter INT,
                        transaction_type VARCHAR(30),
                        transaction_count INT,
                        transaction_amount FLOAT);'''
    cursor.execute(query)

    query = '''CREATE TABLE IF NOT EXISTS agg_user(state VARCHAR(50),
                          year INT,
                          quarter INT,
                          Registered_users INT,
                          App_opens BIGINT);'''
    cursor.execute(query)

    query = '''CREATE TABLE IF NOT EXISTS map_transaction(state VARCHAR(50),
                          year INT,
                          quarter INT,
                          district VARCHAR(300),
                          transaction_count INT,
                          transaction_amount FLOAT);'''
    cursor.execute(query)

    query = '''CREATE TABLE IF NOT EXISTS map_user(state VARCHAR(50),
                          year INT,
                          quarter INT,
                          district VARCHAR(300),
                          Registered_users INT,
                          App_opens BIGINT);'''
    cursor.execute(query)

    query = '''CREATE TABLE IF NOT EXISTS top_transaction(state VARCHAR(50),
                          year INT,
                          quarter INT,
                          pincode INT,
                          transaction_count INT,
                          transaction_amount FLOAT);'''
    cursor.execute(query)

    query = '''CREATE TABLE IF NOT EXISTS top_user(state VARCHAR(50),
                          year INT,
                          quarter INT,
                          pincode INT,
                          Registered_users INT);'''
    cursor.execute(query)
    return "Tables Created Successfully"

#Data Insertion in MySQL Table
def insert_agg_transaction():
    agg_transaction = get_agg_transaction()
    query = '''INSERT INTO agg_transaction(state, year, quarter, transaction_type, transaction_count, transaction_amount)
               VALUES(%s, %s, %s, %s, %s, %s)
               ON DUPLICATE KEY UPDATE
               state = VALUES(state),
               year = VALUES(year),
               quarter = VALUES(quarter),
               transaction_type = VALUES(transaction_type),
               transaction_count = VALUES(transaction_count),
               transaction_amount = VALUES(transaction_amount)'''
    values = zip(agg_transaction["state"],
                 agg_transaction["year"],
                 agg_transaction["quarter"],
                 agg_transaction["transaction_type"],
                 agg_transaction["transaction_count"],
                 agg_transaction["transaction_amount"])
    for row in values:
        cursor.execute(query, row)
    mydb.commit()
    return "Inserted Successfully"

def insert_agg_user():
    agg_user = get_agg_user()
    query = '''INSERT INTO agg_user(state, year, quarter, Registered_users, App_opens)
                  VALUES(%s,%s,%s,%s,%s)
                  ON DUPLICATE KEY UPDATE
                  state = VALUES(state),
                  year = VALUES(year),
                  quarter = VALUES(quarter),
                  Registered_users = VALUES(Registered_users),
                  App_opens = VALUES(App_opens)'''
    values = zip(agg_user["state"],
                 agg_user["year"],
                 agg_user["quarter"],
                 agg_user["Registered_users"],
                 agg_user["App_opens"])
    for row in values:
        cursor.execute(query, row)
        mydb.commit()
    return "Inserted Successfully"
agg_transaction = get_map_transaction()

def insert_map_transaction():
    query = '''INSERT INTO map_transaction(state, year, quarter, district, transaction_count, transaction_amount)
                 VALUES(%s, %s, %s, %s, %s, %s)
                 ON DUPLICATE KEY UPDATE
                 state = VALUES(state),
                 year = VALUES(year),
                 quarter = VALUES(quarter),
                 district = VALUES(district),
                 transaction_count = VALUES(transaction_count),
                 transaction_amount = VALUES(transaction_amount)'''

    values = zip(agg_transaction["state"],
                 agg_transaction["year"],
                 agg_transaction["quarter"],
                 agg_transaction["district"],
                 agg_transaction["transaction_count"],
                 agg_transaction["transaction_amount"])

    for row in values:
        cursor.execute(query, row)
    mydb.commit()
    return "Inserted Successfully"

def insert_map_user():
    agg_transaction = get_map_user()
    query = '''INSERT INTO map_user(state, year, quarter, district, Registered_users, App_opens)
               VALUES(%s, %s, %s, %s, %s, %s)
               ON DUPLICATE KEY UPDATE
               state = VALUES(state),
               year = VALUES(year),
               quarter = VALUES(quarter),
               district = VALUES(district),
               Registered_users = VALUES(Registered_users),
               App_opens = VALUES(App_opens)'''

    values = zip(agg_transaction["state"],
                 agg_transaction["year"],
                 agg_transaction["quarter"],
                 agg_transaction["district"],
                 agg_transaction["Registered_users"],
                 agg_transaction["App_opens"])

    for row in values:
        cursor.execute(query, row)
    mydb.commit()
    return "Inserted Successfully"

def insert_top_transaction():
    top_transaction = get_top_transaction()
    query = '''INSERT INTO top_transaction(state, year, quarter, pincode, transaction_count, transaction_amount)
                   VALUES(%s, %s, %s, %s, %s, %s)
                   ON DUPLICATE KEY UPDATE
                   state = VALUES(state),
                   year = VALUES(year),
                   quarter = VALUES(quarter),
                   pincode = VALUES(pincode),
                   transaction_count = VALUES(transaction_count),
                   transaction_amount = VALUES(transaction_amount)'''

    values = zip(top_transaction["state"],
                 top_transaction["year"],
                 top_transaction["quarter"],
                 top_transaction["pincode"],
                 top_transaction["transaction_count"],
                 top_transaction["transaction_amount"])
    for row in values:
        cursor.execute(query, row)
    mydb.commit()
    return "Inserted Successfully"

def insert_top_user():
    agg_transaction = get_top_user()
    query = '''INSERT INTO top_user(state, year, quarter, pincode, Registered_users)
                VALUES(%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                state = VALUES(state),
                year = VALUES(year),
                quarter = VALUES(quarter),
                pincode = VALUES(pincode),
                Registered_users = VALUES(Registered_users)'''

    values = zip(agg_transaction["state"],
                 agg_transaction["year"],
                 agg_transaction["quarter"],
                 agg_transaction["pincode"],
                 agg_transaction["Registered_users"])
    for row in values:
        cursor.execute(query, row)
    mydb.commit()
    return "Inserted Successfully"

def table_insertion():
    table_creation()
    insert_agg_transaction()
    insert_agg_user()
    insert_map_transaction()
    insert_map_user()
    insert_top_transaction()
    insert_top_user()
    return "Inserted"

def format_cash(amount):
    def truncate_float(number, places):
        return int(number * (10 ** places)) / 10 ** places

    if amount < 1e3:
        return amount

    if 1e3 <= amount < 1e5:
        return str(truncate_float((amount / 1e3), 2)) + "K"

    if 1e5 <= amount < 1e7:
        return str(truncate_float((amount / 1e5), 2)) + "L"

    if amount >= 1e7:
        return str(truncate_float(amount / 1e7, 2)) + "Cr"

def format_number(number):
    if number is not None:
        locale.setlocale(locale.LC_ALL, 'en_IN')
        formatted_number = locale.format_string("%d", number, grouping=True)
        return formatted_number
    else:
        return "N/A"

#Transaction Aggregation
def transaction_aggregated(state, year, quarter):
    if state == "All India":
        query = '''
            SELECT transaction_type, 
                   SUM(transaction_count) AS transaction_count, 
                   SUM(transaction_amount) AS transaction_amount
            FROM phonepe.agg_transaction
            WHERE year = %s AND quarter = %s
            GROUP BY transaction_type
            ORDER BY transaction_count DESC
        '''
        cursor.execute(query, (year, quarter))
    else:
        query = '''
            SELECT transaction_type, 
                   SUM(transaction_count) AS transaction_count, 
                   SUM(transaction_amount) AS transaction_amount
            FROM agg_transaction
            WHERE state = %s AND year = %s AND quarter = %s
            GROUP BY transaction_type
            ORDER BY transaction_count DESC
        '''
        cursor.execute(query, (state, year, quarter))

    transaction_aggregated_data = cursor.fetchall()
    transaction_aggregated_df = pd.DataFrame(transaction_aggregated_data,
                                             columns=["transaction_type", "transaction_count", "transaction_amount"])

    trans_agg_pie = px.pie(transaction_aggregated_df,
                           names="transaction_type",
                           values="transaction_count",
                           hover_name="transaction_type",
                           hover_data=["transaction_count"],
                           title=f"Category Proportions for {state} in Q{quarter} {year}")

    trans_agg_pie.update_layout(title_font={"size": 20, "color": "violet"})
    trans_agg_pie.update_layout(hoverlabel=dict(font=dict(size=14)))

    transaction_aggregated_df['transaction_count'] = pd.to_numeric(transaction_aggregated_df['transaction_count'],
                                                                   errors='coerce').fillna(0)
    trans_count = int(transaction_aggregated_df["transaction_count"].sum())
    trans_amount = int(transaction_aggregated_df["transaction_amount"].sum())
    avg_trans_val = int(trans_amount / trans_count) if trans_count != 0 else 0

    transaction_aggregated_df["transaction_count"] = transaction_aggregated_df["transaction_count"].astype(float).apply(
        format_cash)

    trans_count = format_number(trans_count)
    trans_amount = format_number(trans_amount / 10 ** 7)
    avg_trans_val = format_number(avg_trans_val)

    return transaction_aggregated_df, trans_agg_pie, trans_count, trans_amount, avg_trans_val

def top_10_transaction_count(year, quarter):
    query = '''SELECT state, SUM(transaction_count) AS transaction_count
              FROM agg_transaction
              WHERE year = %s AND quarter = %s
              GROUP BY state  
              ORDER BY transaction_count DESC
              LIMIT 10'''
    cursor.execute(query, (year, quarter))
    data = cursor.fetchall()
    top_10trans = pd.DataFrame(data, columns=["state", "transaction_count"])
    top_10trans["transaction_count"] = top_10trans["transaction_count"].astype(float).apply(format_cash)
    return top_10trans

def top_10_district_transaction(state, year, quarter):
    if state == "All India":
        query = '''SELECT district, SUM(transaction_count) AS transaction_count, state
                  FROM map_transaction
                  WHERE state = %s AND year = %s AND quarter = %s
                  GROUP BY district, state
                  ORDER BY transaction_count DESC
                  LIMIT 10'''
        cursor.execute(query, (state, year, quarter))

    else:
        query = '''SELECT district, SUM(transaction_count) AS transaction_count, state
                  FROM map_transaction
                  WHERE state = %s AND year = %s AND quarter = %s
                  GROUP BY district, state
                  ORDER BY transaction_count DESC
                  LIMIT 10'''

        cursor.execute(query, (state, year, quarter))
    data = cursor.fetchall()
    top_10 = pd.DataFrame(data, columns=["district", "transaction_count", "states"])
    top_10["transaction_count"] = top_10["transaction_count"].astype(float).apply(format_cash)
    return top_10

def top_10_pincode_transaction(state, year, quarter):
    if state == "All India":
        query = '''SELECT pincode, SUM(transaction_count) AS transaction_count, state
                  FROM top_transaction
                  WHERE year = %s AND quarter = %s
                  GROUP BY pincode, state
                  ORDER BY transaction_count DESC
                  LIMIT 10'''
        cursor.execute(query, (year, quarter))

    else:
        query = '''SELECT pincode, SUM(transaction_count) AS transaction_count, state
                  FROM top_transaction
                  WHERE state = %s AND year = %s AND quarter = %s
                  GROUP BY pincode, state
                  ORDER BY transaction_count DESC
                  LIMIT 10'''

        cursor.execute(query, (state, year, quarter))
    data = cursor.fetchall()
    top_10 = pd.DataFrame(data, columns=["pincode", "transaction_count", "state"])
    top_10["transaction_count"] = top_10["transaction_count"].astype(float).apply(format_cash)
    return top_10

#User Aggregation
def user_aggregated(state, year, quarter):
    if state == "ALL INDIA":
        query = '''SELECT state, SUM(Registered_users) AS Registered_users, SUM(App_opens) AS App_opens
                  FROM agg_user WHERE year = %s AND quarter = %s
                  GROUP BY Registered_users'''
        cursor.execute(query, (year, quarter))
    else:
        query = '''SELECT state, SUM(Registered_users) AS Registered_users, SUM(App_opens) AS App_opens
                FROM agg_user WHERE state = %s AND year = %s AND quarter = %s 
                GROUP BY Registered_users'''

        cursor.execute(query, (state, year, quarter))
    data = cursor.fetchall()
    user_agg = pd.DataFrame(data, columns=["state", "Registered_users", "App_opens"])
    user_agg["Registered_users"] = user_agg["Registered_users"].map(format_number)
    user_agg["App_opens"] = user_agg["App_opens"].map(format_number)
    return user_agg

def top_10_states_user(year, quarter):
    query = '''SELECT state, SUM(Registered_users) AS `Registered_users`
                FROM agg_user WHERE year = %s AND quarter = %s
                GROUP BY state ORDER BY `Registered_users` DESC
                LIMIT 10'''
    cursor.execute(query, (year, quarter))
    data = cursor.fetchall()
    top_10 = pd.DataFrame(data, columns=["state", "Registered_users"])
    top_10["Registered_users"] = top_10["Registered_users"].astype(int).apply(format_cash)
    return top_10

def top_10_district_user(state, year, quarter):
    if state == "All India":
        query = f'''SELECT district, SUM(Registered_users) AS Registered_users
                      FROM map_user
                      WHERE year = %s AND quarter = %s
                      GROUP BY district
                      ORDER BY Registered_users DESC
                      LIMIT 10'''
        cursor.execute(query, (year, quarter))

    else:
        query = f'''SELECT district, SUM(Registered_users) AS Registered_users
                  From map_user
                  WHERE state = %s AND year = %s AND quarter = %s
                  GROUP BY district
                  ORDER BY Registered_users DESC
                  LIMIT 10'''
        cursor.execute(query, (state, year, quarter))
    data = cursor.fetchall()
    top_10 = pd.DataFrame(data, columns=["district", "Registered_users"])
    top_10["Registered_users"] = top_10["Registered_users"].astype(int).apply(format_cash)
    return top_10

def top_10_pincode_user(state, year, quarter):
    if state == "All India":
        query = f'''SELECT pincode, SUM(Registered_users) AS Registered_users
                  FROM top_user
                  WHERE year = %s AND quarter = %s
                  GROUP BY pincode
                  ORDER BY Registered_users DESC
                  LIMIT 10'''
        cursor.execute(query, (year, quarter))
    else:
        query = f'''SELECT pincode, SUM(Registered_users) AS Registered_users
                  FROM top_user
                  WHERE state = %s AND year = %s AND quarter = %s
                  GROUP BY pincode
                  ORDER BY Registered_users DESC
                  LIMIT 10'''
        cursor.execute(query, (state, year, quarter))

    data = cursor.fetchall()
    top_10 = pd.DataFrame(data, columns=["pincode", "Registered_users"])
    top_10["Registered_users"] = top_10["Registered_users"].astype(int).apply(format_cash)
    return top_10

#Streamlit-------------------------------------------------------------------
st.header(":blue[PHONEPE PULSE DATA VISUALIZATION AND EXPLORATION]", divider='rainbow')
st.caption(" - A User Friendly Tool Using Streamlit and Plotly")

#GEO Visualisation
#Registered Users
dfts = get_map_user()
test = dfts[['state', 'Registered_users']].groupby(['state']).sum()

#App Opens
dft = get_map_user()
apo = dft[['state', 'App_opens']].groupby(['state']).sum()

#Transaction count
map_transaction = get_map_transaction()
te = map_transaction[['state', 'transaction_count']].groupby(['state']).sum()

st.markdown("GEO VISUALISATION OF INDIA MAP")
map_options = ["Registered_users", "App_opens", "transaction_count"]
select_map = st.selectbox('Select Data on Map', map_options)

if select_map == "Registered_users":
    fig = px.choropleth(
        test,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations=test.index,
        color='Registered_users',
        color_continuous_scale='Inferno')
    fig.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig)

elif select_map == "App_opens":
    fig = px.choropleth(
        apo,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations=apo.index,
        color='App_opens',
        color_continuous_scale='Magma')
    fig.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig)
else:
    fig = px.choropleth(
        te,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations=te.index,
        color='transaction_count',
        color_continuous_scale='Cividis')
    fig.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig)

#Data Visualisation
with st.sidebar:
    selected = option_menu(menu_title=None,
                           options=['Menu', "PhonePe Data Visualization"],
                           icons=['house-door-fill', 'pie-chart-fill'],
                           default_index=0,
                           styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "8px"},
                                   "icon": {"color": "yellow", "font-size": "20px"},
                                   "nav-link-selected": {"background-color": "#9457eb"}})
    if selected == "Menu":
        st.markdown('''The aim of this project is to display geographical visualization of of dashboard that displays information and insights
                      from PhonePe Pulse GitHub Repository in an interactive and visually appealing manner. The data will be stored in a MySQL
                      database for efficient retrieval and the dashboard will be dynamically updated to reflect the latest data.....''')

if selected == "PhonePe Data Visualization":
    col1, col2, col3, col4 = st.columns([0.22, 0.21, 0.21, 0.36])

    with col1:
        types = st.selectbox(":violet[Type]", options=["Transaction", "Users"], key="types")

    with col2:
        year = st.selectbox(":violet[Year]", options=["2018", "2019", "2020", "2021", "2022", "2023"], key="year")

    with col3:
        quarter = st.selectbox(":violet[Quarter]", options=["1", "2", "3", "4"], key="quarter")

    with col4:
        state = st.selectbox(":violet[State]", options=["All India", "Andaman & Nicobar Islands", "Andhra Pradesh",
                                                            "Arunachal Pradesh", "Assam", "Bihar", "Chandigarh",
                                                            "Chattisgarh", "Dadra & Nager Haveli & Daman & Diu",
                                                            "Delhi", "Goa", "Gujarat", "Harayana", "Himachal Pradesh",
                                                            "Jammu & Kashmir", "Jharkhand", "Karnataka", "Kerala",
                                                            "Ladakh",
                                                            "Lakshadeep", "Madhya Pradesh", "Maharashtra", "Manipur",
                                                            "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Puducherry",
                                                            "Punjab", "Rajasthan", "sikkim", "Tamil Nadu", "Telegana",
                                                            "Tripura", "Uttar Pradesh", "Uttarkhand", "West Bengal"],
                                 key="state")

    col21, col22 = st.columns([0.64, 0.36])

    def create_transaction_plot(data, year, quarter):
        filtered_data = data[(data['year'] == year) & (data['quarter'] == quarter)]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=filtered_data['transaction_type'], y=filtered_data['transaction_count'],
                                    mode='lines+markers', name='transaction_count'))
        fig.add_trace(go.Scatter(x=filtered_data['transaction_type'], y=filtered_data['transaction_amount'],
                                    mode='lines+markers', name='transaction_amount'))
        fig.update_layout(title='Transaction Plot', xaxis_title='transaction_type', yaxis_title='Value')

        return fig

    with col21:
        if types == "Transaction":
            mapping_transaction = get_agg_transaction()
            filtered_data = mapping_transaction[(mapping_transaction['state'] == state) &
                                                (mapping_transaction['year'] == year) &
                                                (mapping_transaction['quarter'] == quarter)]

            fig = go.Figure()
            for transaction_type in filtered_data['transaction_type'].unique():
                type_data = filtered_data[filtered_data['transaction_type'] == transaction_type]
                fig.add_trace(go.Bar(
                x=type_data['transaction_type'],
                y=type_data['transaction_amount'],
                name=transaction_type))

            fig.update_layout(
                title=f'Transaction Count by Type for {state} - Year {year}, Quarter {quarter}',
                xaxis_title='Transaction Type',
                yaxis_title='Transaction amount',
                barmode='stack')
            st.plotly_chart(fig)

        if types == "Users":
            mapping_users = get_map_user()
            filtered_users = mapping_users[mapping_users['state'] == state]
            fig = px.bar(filtered_users, x='district', y=['Registered_users', 'App_opens'],
                        title=f'User Data by District - {state}',
                        labels={'value': 'Count', 'variable': 'Metric', 'district': 'District'})
            st.plotly_chart(fig, use_container_width=True)

        if types == "Transaction":
            with st.expander(":violet[**Transaction**]", expanded=True):
                categories, categories_pie, T_count, T_amount, T_avg_val = transaction_aggregated(state, int(year), int(quarter))
                st.write(f"All PhonePe transactions (UPI + Cards + Wallets): blue[{T_count}]")
                st.write(f"Total Payment Value:blue[Rs. {T_amount} Cr]")
                st.write(f"Average Transaction value:blue[Rs. {T_avg_val}]")
                st.markdown("************************************")
                st.markdown(":violet[**Categories**]")
                st.write(f"{categories.loc[1, 'transaction_type']}:blue[{categories.loc[1, 'transaction_count']}]")
                st.write(f"{categories.loc[2, 'transaction_type']}:blue[{categories.loc[2, 'transaction_count']}]")
                st.write(f"{categories.loc[3, 'transaction_type']}:blue[{categories.loc[3, 'transaction_count']}]")
                st.write(f"{categories.loc[4, 'transaction_type']}:blue[{categories.loc[4, 'transaction_count']}]")
                st.write(f"{categories.loc[0, 'transaction_type']}:blue[{categories.loc[0, 'transaction_count']}]")
                st.markdown("************************************")

                st.plotly_chart(categories_pie, use_container_width=True)

            if state == "All India":
                T_tab1, T_tab2, T_tab3 = st.tabs(["**States**", "**Districts**", "**Pincode**"])

                with T_tab1:
                    st.markdown(":violet[**Top 10 States**]")
                    T_top_states = top_10_transaction_count(int(year), int(quarter))
                    st.table(T_top_states)

            else:
                T_tab2, T_tab3 = st.tabs(["**Districts**", "**Pincode**"])
                with T_tab2:
                    st.markdown(":violet[**Top 10 districts**]")
                    T_top_district = top_10_district_transaction(state, int(year), int(quarter))
                    st.table(T_top_district)
                with T_tab3:
                    st.markdown(":violet[**Top 10 Postal Code**]")
                    T_top_pincode = top_10_pincode_transaction(state, int(year), int(quarter))
                    st.write(T_top_pincode)

    with col22:
        if types == "Users":
            with st.expander(":violet[**Users**]", expanded=True):
                data = user_aggregated(state, int(year), int(quarter))
                ca = get_agg_user()
                count = ca["App_opens"].sum()
                rs = ca["Registered_users"].sum()
                if not data.empty:
                    st.write(f"State {state}")
                    st.write(f"Registered PhonePe Users till Q{int(quarter)}, {int(year)}: {rs}")
                    st.write(f"Overall App_opens in Q{int(quarter)}, {int(year)} : {count}")
                else:
                    st.write("No Data Available")
                    st.markdown("******************************************")
            if state == "All India":
                U_tab1, U_tab2, U_tab3 = st.tabs(["**States**", "**Districts**", "**Pincode**"])

                with U_tab1:
                    st.markdown(":violet[**Top 10 States**]")
                    U_top_states = top_10_states_user(int(year), int(quarter))
                    st.table(U_top_states)
            else:
                U_tab2, U_tab3 = st.tabs(["**Districts**", "**Pincode**"])

                with U_tab2:
                    st.markdown(":violet[**Top 10 Districts**]")
                    U_top_district = top_10_district_user(state, int(year), int(quarter))
                    st.table(U_top_district)

                with U_tab3:
                    st.markdown(":violet[**Top 10 Postal Code**]")
                    U_top_pincode = top_10_pincode_user(state, int(year), int(quarter))
                    st.table(U_top_pincode)

#**************************************************************************************************************************************************

