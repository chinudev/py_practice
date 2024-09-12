from randomuser import RandomUser
import pandas as pd
import requests 
import json 


# RandomUser creates a user with fields like name, email, address etc. filled out
# See https://randomuser.me/documentation for more details
# This method gets a list of random users and converts it into a pandas dataframe
def create_user_df(u_list):
    users =[]
    ru = RandomUser()              
    user_list = ru.generate_users(10)  # get 10 users

    for user in u_list:
        users.append({"Name":user.get_full_name(), "Gender":user.get_gender(), "City":user.get_city(), "State":user.get_state(), "Email":user.get_email(), "DOB":user.get_dob(), "Picture":user.get_picture()})
    return pd.DataFrame(users)     


def test_random_user():
    df = pd.DataFrame(create_user_df(user_list))
    print(df.head(10))


# Let's use fruityvice API 
#  In this case we don't have a conveneint wrapper like RandomUser provided to us, so 
#  we will use the requests library to make a GET request to the API and then parse the JSON response

def test_fruitvice():
    fruit_url = 'https://fruityvice.com/api/fruit/all'
    data = requests.get(fruit_url)
    results = json.loads(data.text)
    df = pd.DataFrame(results)
    print(df.head())            # Note that nutrients columns is a dictionary in the JSON response
    df2 = pd.json_normalize(results)
    print(df2.head())           # Note that nutrients columns is expanded into separate columns

    print('get a specific fruit')
    cherry = df2.loc[df2['name'] == 'Cherry']
    print(cherry)
    print(cherry.iloc[0]['family'], cherry.iloc[0]['genus'])
    


# Test the Joke api 
def test_joke():
    joke_url = 'https://official-joke-api.appspot.com/jokes/ten'   # get 10 random jokes  
    data = requests.get(joke_url)
    results = json.loads(data.text)
    df = pd.DataFrame(results)
    df.drop(columns=['type', 'id'], inplace=True)   
    print(df)



# run this code if we are in main
if __name__ == "__main__":
    test_random_user()
    test_fruitvice()
    test_joke()