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

        col1,col2,col3,col4 =  st.columns(4)

        with col1:
             st.header("Total Messages")
             st.title(num_messages)
        with col2:
             st.header("Total Words")
             st.title(words)
        with col3:
         st.header("Total Media messages")
         st.title(num_media_messages)
        with col4:
         st.header("Total Links sent")
         st.title(num_links)    

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
        st.dataframe(most_common_df)
