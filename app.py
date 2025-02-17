import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt

st.sidebar.title("Whatsapp Chat Analyzer")


uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    st.dataframe(df)



    #fetch unique users bhay
    user_list = df['user'].unique().tolist()
    if 'GroupNotification' in user_list:
        user_list.remove('GroupNotification')  

    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Show analysis wrt" , user_list)

    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_media_messages,num_links = helper.fetch_stats(selected_user, df)
        st.title("Top Statistics:")
        col1,col2,col3 =  st.columns(3)

        with col1:
             st.header("Total Messages")
             st.title(num_messages)
        with col2:
             st.header("Total Words")
             st.title(words)
        with col3:
         st.header("Total Links sent")
         st.title(num_links)   

         #timeline

        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax =  plt.subplots() 
        ax.plot(timeline['time'], timeline['message'])
        plt.xticks(rotation = 'vertical', color = 'green')
        plt.xticks(ticks=range(0, len(timeline['time']), 2), labels=timeline['time'][::2])
        st.pyplot(fig)

        # finding busiest users on the group (group level)
        if selected_user == 'Overall':
           st.title("Most busy Users")
           x,new_df =helper.most_busy_users(df)
           fig,ax = plt.subplots()
           
           col1,col2 = st.columns(2)

           with col1:
            ax.bar(x.index , x.values,color = 'red')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)

            with col2:
               st.dataframe(new_df)


        # WORDCLOUD
        st.title("Word Cloud")
        df_wc = helper.create_wordcloud(selected_user,df) 
        fig,ax = plt.subplots()
        plt.imshow(df_wc)
        st.pyplot(fig)

        #most common words
        st.title("Most Common Words")
        most_common_df = helper.most_common_words(selected_user,df)
        fig,ax = plt.subplots()
        ax.barh(most_common_df[0] , most_common_df[1])
        plt.xticks(rotation = 'vertical')
        
        st.pyplot(fig)


        st.dataframe(most_common_df)

        # emoji anaysis (most used waale)

        emoji_df = helper.emoji_helper(selected_user,df)
        
        st.title("Most Emojis Used")

        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
           fig,ax = plt.subplots()
           ax.pie( emoji_df[1].head(), labels = emoji_df[0].head(), autopct = "%0.2f")
           st.pyplot(fig)
