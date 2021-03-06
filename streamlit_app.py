
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

def get_fruityvice_data(this_fruit_choice):
     fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" +fruit_choice)
     ##streamlit.text(fruityvice_response.json())
     fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
     return fruityvice_normalized

streamlit.header('Fruityvice  Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
     streamlit.error("please select the a fruit to get information.")
  else:
     back_from_function = get_fruityvice_data(fruit_choice)
     streamlit.dataframe(back_from_function)

except URLError as e:
  streamlit.error()

##streamlit.stop()


 
streamlit.header("Fruit Load list contains:")

def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
       my_cur.execute("SELECT * FROM fruit_load_list")
       return my_cur.fetchall()
    
if streamlit.button('Get Full Load List:'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   my_data_rows = get_fruit_load_list()
   streamlit.dataframe(my_data_rows)

def insert_row_snowflake(new_fruit):
     with my_cnx.cursor() as my_cur:
          my_cur.execute("insert into fruit_load_list values('" + new_fruit + "')")
          return "Thanks for adding " + new_fruit

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add Fruit to the List'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   back_from_button = insert_row_snowflake(add_my_fruit)
   streamlit.text(back_from_button)


