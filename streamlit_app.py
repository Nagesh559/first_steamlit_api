
import streamlit
import pandas
 

streamlit.header('Breakfast Favorites')
streamlit.text(' Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')

streamlit.header('BUILD YOUR OWN SOOMTHIE')
my_fruitlist = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
# Let's put a pick list here so they can pick the fruit they want to include
steamlit.multiselect("Pick some fruits:", list(my_fruitlist.index))

#display the table on the page 
streamlit.dataframe(my_fruitlist)
