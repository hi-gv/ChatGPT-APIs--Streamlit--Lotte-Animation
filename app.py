import streamlit as st
import hydralit_components as hc
import os
import openai
import time
from streamlit_lottie import st_lottie
import json

def check_senti():

    st.title("Sentiment Analyzer")

    # Define the input field for the user's code
    user_input = st.text_area("Enter your Sentence:")

    # Define the button to convert the code to natural language
    if st.button("Sentize!"):
        if user_input:
            response = openai.Completion.create(
            model="text-davinci-003",
            prompt="Decide whether a Tweet's sentiment is positive, neutral, or negative.\n\nTweet: "+user_input+"\nSentiment:",
            temperature=0,
            max_tokens=60,
            top_p=1.0,
            frequency_penalty=0.5,
            presence_penalty=0.0
            )
            # st.json(response)
            st.subheader("What you just said is :")
            if response["choices"][0]["text"]:
                sentiment = response["choices"][0]["text"].lower().strip()
                if sentiment=='negative':
                    st.error(sentiment)
                if sentiment=='positive':
                    st.success(sentiment)
                if sentiment=='neutral':
                    st.info(sentiment)
            else:
                st.warning("Error:", sentiment)
        else:
            st.warning("Dude, you didn't give anything to work with yet, give me something ...seeshhh!")
            
def sql_translate():
    st.title("Build SQL Queries")

    # Define the input field for the user's code
    user_input = st.text_area("What would you like the SQL query to do :")
    st.caption("Sample input : Create a SQL request to find all users who live in California and have over 1000 credits")
    # Define the button to convert the code to natural language
    if st.button("Build SQL Queries"):
        if user_input:

            response = openai.Completion.create(
            model="text-davinci-003",
            prompt="Create a SQL request to find all users who live in California and have over 1000 credits:",
            temperature=0.3,
            max_tokens=60,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
            )
                        
            # st.json(response)
            with hc.HyLoader('',hc.Loaders.standard_loaders,index=3):
                time.sleep(1.5)
                if response["choices"][0]:
                    sql_tranlsate = response["choices"][0]["text"].strip()
                    st.subheader("This can perhaps go like this :")
                    st.success(sql_tranlsate)
                    st.download_button("Download Result",sql_tranlsate)
                else:
                    st.warning("Error:", sql_tranlsate)
        else:
            st.warning("Dude, you didn't give anything to work with yet, give me something ...seeshhh!")
def help_my_grammer():

    st.title("Grammer-Check")

    # Define the input field for the user's code
    user_input = st.text_area("Enter a Sentence, I'll help you with grammer")

    # Define the button to convert the code to natural language
    if st.button("Grammer-ify"):
        if user_input:
            response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Correct this to standard English:\n\n"+user_input,
        temperature=0,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
        )
            # st.json(response)
            if response["choices"][0]:
                grammify = response["choices"][0]["text"].strip()
                st.subheader("This can perhaps go like this :")
                st.success(grammify)
                st.download_button("Download Result",grammify)
            else:
                st.warning("Error:", grammify)
        else:
            st.warning("Dude, you didn't give anything to work with yet, give me something ...seeshhh!")

def python_explainer():
    
    st.title("Explain Python Code")

    # Define the input field for the user's code
    user_input = st.text_area("Enter your Python code - I'll do best to explain :")

    # Define the button to convert the code to natural language
    if st.button("Convert"):
        if user_input:
            # Define the API endpoint and request parameters
            endpoint = "https://api.openai.com/v1/engines/davinci-codex/completions"
            prompt = "Convert the following Python code to natural language:\n\n" + user_input + "\n\nThe natural language version of the code is:"
            max_tokens = 64
            temperature = 0
            top_p=1.0

            # Send the request to the API and get the response
            response = openai.Completion.create(
                engine="code-davinci-002",
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p
            )

            # Display the natural language version of the code
            if response["choices"][0]:
                nl_code = response["choices"][0]["text"].strip()
                st.subheader("This code is to :")
                st.success(nl_code)
                st.download_button("Download Result",nl_code)
            else:
                st.warning("Error:", nl_code)
        else:
            st.warning("Dude, you didn't give anything to work with yet, give me something ...seeshhh!")
def main():
    openai.api_key = os.getenv("OPENAI_API_KEY")
    st.set_page_config(layout='wide',page_title='Open-AI Toolkit',page_icon=":tada:")

    # to get icon names - gt from https://icons.getbootstrap.com/icons/award-fill/
    # define what option labels and icons to display
    option_data = [
    {'icon': "bi-house-door-fill", 'label':" "},
    {'icon':"bi-chat-left-fill",'label':"Python Explainer"},
    {'icon': "bi-boxes", 'label':"Make SQL Queries"},
    {'icon': "bi-circle-square", 'label':"Sentiment Analyzer"},
    {'icon': "bi-book-fill", 'label':"Check Grammer"}
    ]    
    # override the theme, else it will use the Streamlit applied theme

    over_theme = {'txc_inactive': 'grey','menu_background':'black','txc_active':'white','option_active':'#fe2e2e'}
    # font_fmt = {'font-class':'h1','font-size':'150%'}

    # display a horizontal version of the option bar
    op = hc.option_bar(option_definition=option_data,title='Open-AI APIs',key='PrimaryOption',horizontal_orientation=True,override_theme=over_theme)#,font_styling=font_fmt)

    if op ==" ":
        st.header("Hi !")
        st.subheader("This is to showcase usage of Open-AI APIs")
        with open("conf/cube-shape-animation.json","r") as fo:
            lottie_json=json.load(fo)
            st_lottie(lottie_json,height=500,speed=.5,quality="high")
    if op == "Python Explainer":
        python_explainer()
    if op=="Check Grammer":
        help_my_grammer()
    if op=="Make SQL Queries":
        sql_translate()
    if op=="Sentiment Analyzer":
        check_senti()

if __name__=="__main__":
    main()