for category in st.session_state.categories:
    category['amount'] = st.number_input(
        category['name'], value=int(category.get('amount', 0)), step=1000, format="%d"
    )
