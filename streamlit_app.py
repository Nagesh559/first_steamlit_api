
import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError
 
streamlit.title('MY MOMS HEALTHY DINNER')

streamlit.header('Breakfast Favorites')
streamlit.text(' Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')

streamlit.header('BUILD YOUR OWN SOOMTHIE')
my_fruitlist = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruitlist = my_fruitlist.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruitlist.index),['Avocado','Strawberries'])
fruits_to_show = my_fruitlist.loc[fruits_selected]
       

#display the table on the page 
##streamlit.dataframe(my_fruitlist)
streamlit.dataframe(fruits_to_show)

streamlit.header('Fruityvice  Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?', 'kiwi')
  if not fruit_choice:
     streamlit.error("please select the a fruit to get information.")
  else:
     fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" +fruit_choice)
     ##streamlit.text(fruityvice_response.json())
     fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
     streamlit.dataframe(fruityvice_normalized)

  except URLError as e:
  streamlit.error()

streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("SELECT * FROM fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.header("Fruit Load list contains:")
streamlit.dataframe(my_data_row)

add_my_fruit = streamlit.text_input('What fruit would you like to add', 'jackfruit')
streamlit.write('The user entered', add_my_fruit)

my_cur.execute("insert into fruit_load_list values('from streamlit')")
