def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Fetching number of messages
    num_messages = df.shape[0]

    # Counting words
    words = df['message'].apply(lambda x: len(x.split())).sum()

    # Counting media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    return num_messages, words, num_media_messages  

