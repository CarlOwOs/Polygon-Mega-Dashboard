import streamlit as st
import pandas as pd
import altair as alt
import plotly.graph_objects as go

if __name__ == "__main__":
    st.set_page_config(layout="wide")

    st.image("polygon.png", width=200)

    st.title("Polygon Mega Dashboard")
    st.write("Welcome to the Polygon Mega Dashboard! On this dashboard, you can access a detailed overview of users, transactions, and many other metrics related to the Polygon Blockchain.")
    
    st.header("How is the Dashboard structured?")

    st.write("The dashboard is divided into two main sections:")

    st.subheader("1. The **Network Data**, which displays a summary of data related to the network as a whole.")

    st.write("This first section can be further divided into two topics related to the health of the network:")

    st.write("1.1. Market Data, where we show data on the Circulating Supply, Market Cap, MATIC Price, and the MATIC token holders Holders.")
    
    st.write("1.2. Transaction Data, where the number of transactions per hour and average fees per transaction are shown comprehensively.")
    
    st.subheader("2. The **User Data**, which displays a summary of all users and their associated data.")
    
    st.write("This second section can be further divided into two topics related to the users of the network:")
    
    st.write("2.1 Active Users, where we study the number of active users as a function of time and the MATIC token price.")
    
    st.write("2.2. User Growth Data, where we analyze the daily number of users trying Polygon for the first time.")

    st.write("The temporal charts allow for selection using the context chart below them. The scatter plots also allow for selection. Also, each metric will be properly defined in each section.")

    st.write("This dashboard builds upon the visualizations created by [mr_nobody73](https://app.flipsidecrypto.com/dashboard/price-circulating-supply-YBc5sp), [alitaslimi](https://app.flipsidecrypto.com/dashboard/polygon-vs-harmony-l13ITg), [adriaparcerisas](https://app.flipsidecrypto.com/dashboard/active-addresses-AL7ktc), and [h4wk](https://app.flipsidecrypto.com/dashboard/new-addresses-4z1-_c).")

    col1, col2, col3, col4 = st.columns(4)

    df_cs = pd.read_json("1_cs.json") # DATE  CURCULATING_SUPPLY  MATIC_AVERAGE_PRICE   MARKET_CAP_  HOLDERS
    df_txh = pd.read_json("1_txh.json")
    df_gash = pd.read_json("1_gash.json")
    df_ = pd.concat([df_cs.set_index('DATE'),df_txh.set_index('DATE')], axis=1, join='outer').reset_index()

    df = pd.concat([df_.set_index('DATE'),df_gash.set_index('DATE')], axis=1, join='outer').reset_index()

    selection = alt.selection_interval(encodings=['x'])
    color1 = alt.condition(selection, alt.value("lightsalmon"),alt.value("lightgrey"))
    color2 = alt.condition(selection, alt.value("lightseagreen"),alt.value("lightgrey"))

    # CS VS PRICE
    base = alt.Chart(df).encode(x='yearmonthdate(DATE):T')
    line1 = base.mark_bar().encode(
        y=alt.Y("CURCULATING_SUPPLY:Q", axis=alt.Axis(title="Circulating Supply (MATIC)")),color=color1)
    line2 = base.mark_line().encode(y=alt.Y("MATIC_AVERAGE_PRICE:Q", axis=alt.Axis(title="MATIC Price (USD)")))
    ch = alt.layer(line1, line2).resolve_scale(y = 'independent').encode(
        tooltip=[alt.Tooltip("DATE",title="Date"), alt.Tooltip("CURCULATING_SUPPLY",title="Circulating Supply"),alt.Tooltip("MATIC_AVERAGE_PRICE",title="Price")])
    ch1 = ch.transform_filter(selection).properties(width=900, title="Circulating Supply vs. MATIC Price")
    view = ch.add_selection(selection).properties(
       width=900,
       height=50,
    )

    # MC VS PRICE
    base = alt.Chart(df).encode(x='yearmonthdate(DATE):T')
    line1 = base.mark_bar().encode(y=alt.Y("MARKET_CAP_:Q", axis=alt.Axis(title="Market Cap (USD)")),color=color2)
    line2 = base.mark_line().encode(y=alt.Y("MATIC_AVERAGE_PRICE:Q", axis=alt.Axis(title="MATIC Price (USD)")))
    ch = alt.layer(line1, line2).resolve_scale(y = 'independent').encode(
        tooltip=[alt.Tooltip("DATE",title="Date"), alt.Tooltip("MARKET_CAP_",title="Market Cap"),alt.Tooltip("MATIC_AVERAGE_PRICE",title="Price")])
    ch2 = ch.transform_filter(selection).properties(width=900, title="Market Cap vs. MATIC Price")
    view2 = ch.add_selection(selection).properties(
       width=900,
       height=50,
    )

    # CS VS HOLDERS
    base = alt.Chart(df).encode(x='yearmonthdate(DATE):T')
    line1 = base.mark_bar().encode(y=alt.Y("CURCULATING_SUPPLY:Q", axis=alt.Axis(title="Circulating Supply (MATIC)")), color=color1)
    line2 = base.mark_line(color="seagreen").encode(y=alt.Y("HOLDERS:Q", axis=alt.Axis(title="MATIC Holders")))
    ch = alt.layer(line1, line2).resolve_scale(y = 'independent').encode(
        tooltip=[alt.Tooltip("DATE",title="Date"), alt.Tooltip("CURCULATING_SUPPLY",title="Circulating Supply"),alt.Tooltip("HOLDERS",title="Holders")])
    ch3 = ch.transform_filter(selection).properties(width=900, title="Circulating Supply vs. MATIC Holders")
    view3 = ch.add_selection(selection).properties(
       width=900,
       height=50,
    )

    # MC VS HOLDERS
    base = alt.Chart(df).encode(x='yearmonthdate(DATE):T')
    line1 = base.mark_bar().encode(y=alt.Y("MARKET_CAP_:Q", axis=alt.Axis(title="Market Cap (USD)")),color=color2)
    line2 = base.mark_line(color="seagreen").encode(y=alt.Y("HOLDERS:Q", axis=alt.Axis(title="MATIC Holders")))
    ch = alt.layer(line1, line2).resolve_scale(y = 'independent').encode(
        tooltip=[alt.Tooltip("DATE",title="Date"), alt.Tooltip("MARKET_CAP_",title="Market Cap"),alt.Tooltip("HOLDERS",title="Holders")])
    ch4 = ch.transform_filter(selection).properties(width=900, title="Market Cap vs. MATIC Holders")
    view4 = ch.add_selection(selection).properties(
       width=900,
       height=50,
    )

    st.header("1. Network Data")
    st.subheader("1.1. Market Data")

    st.markdown("""
    
    Definitions:

    - Circulating Supply: The total amount of MATIC circulating in the network.

    - Market Cap: The total amount of MATIC in USD in the network.

    - MATIC Holders: The number of accounts that own MATIC.
    """)

    st.altair_chart(ch1 & view & ch2 & view2 & ch3 & view3 & ch4 & view4)

    st.subheader("Key Findings:")

    st.markdown("""
    - There is no meaningful relationship between circulating supply and MATIC's price.
    
    - The price changes more than the Circulating Supply. In consequence, our depiction of the Market Cap closely follows MATIC's price.
    
    - The number of holders has grown significantly over time. From the difference in slope between the Circulating Supply and the Holders, we can conclude that the MATIC tokens are more distributed among users.
    
    - Among others, price is one of the factors affecting the number of holders. Still, holders continue to increase despite the price falling.""")
    ##############################################################################################################

    col1, col2, col3, col4 = st.columns(4)
    color3 = alt.condition(selection, alt.value("steelblue"),alt.value("lightgrey"))

    base = alt.Chart(df).encode(x='yearmonthdate(DATE):T')
    line = base.mark_line().encode(
        y=alt.Y("POLYGON:Q", axis=alt.Axis(title="Daily Avg. Transactions Per Hour")),
        color=color3,
        tooltip = [alt.Tooltip("DATE:T",title="Date"), alt.Tooltip("POLYGON:Q",title="Avg. Transactions")])
    ch5 = line.transform_filter(selection).properties(width=900, title="Daily Avg. Transactions Per Hour")
    view5 = line.add_selection(selection).properties(
       width=900,
       height=50,
    )
    

    df_tx_heat = pd.read_json("1_tx_heat.json")

    ch6 = alt.Chart(df_tx_heat).mark_rect().encode(
        x=alt.X('DAY_WEEK:O', sort=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]),
        y='TX_HOUR:O',
        color=alt.Color('POLYGON:Q', title="Avg. Transactions"),
        tooltip = [alt.Tooltip("DAY_WEEK",title="Day of the Week"), alt.Tooltip("TX_HOUR",title="Hour of the Day"),alt.Tooltip("POLYGON",title="Avg. Transactions")]
    ).properties(width=900, title="Avg. Transactions Per Hour Per Day (UTC)")
    
    base = alt.Chart(df).encode(x='yearmonthdate(DATE):T')
    line = base.mark_line().encode(
        y=alt.Y("Polygon (MATIC):Q", axis=alt.Axis(title="Avg. Fees Per Transaction")),
        color=color3,
        tooltip = [alt.Tooltip("DATE",title="Date"), alt.Tooltip("Polygon (MATIC)",title="Avg. Fees (MATIC)")])
    ch7 = line.transform_filter(selection).properties(width=900, title="Avg. Fees Per Transaction")
    view7 = line.add_selection(selection).properties(
       width=900,
       height=50,
    )
    
    
    df_gas_heat = pd.read_json("1_gas_heat.json")

    ch8 = alt.Chart(df_gas_heat).mark_rect().encode(
        x=alt.X('DAY_WEEK:O', sort=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]),
        y='TX_HOUR:O',
        color=alt.Color('Polygon (MATIC):Q', title="Avg. Fees (MATIC)"),
        tooltip = [alt.Tooltip("DAY_WEEK",title="Day of the Week"), alt.Tooltip("TX_HOUR",title="Hour of the Day"),alt.Tooltip("Polygon (MATIC)",title="Avg. Fees (MATIC)")]
    ).properties(width=900, title="Avg. Fees Per Transaction Per Hour Per Day (UTC)")

    st.subheader("1.2. Transaction Data")

    st.markdown("""
    
    Definitions:

    - Daily Avg. Transactions Per Hour: On each day, the average number of transactions committed per hour.

    - Avg. Transactions Per Hour Per Day: The average number of transactions committed per hour per day of the week.

    - Avg. Fees Per Transaction: Average gas fees in MATIC paid for each transaction.
    """)

    st.altair_chart(ch5 & view5)
    st.altair_chart(ch6)
    st.altair_chart(ch7 & view7)
    st.altair_chart(ch8)

    st.subheader("Key Findings")

    st.markdown("""

    - Hourly transactions peaked in June 2022 and have been declining since.

    - During Work Days between 12 and 18, the Polygon network is busiest.

    - The fees per transaction have been increasing over time despite the decrease in average hourly transactions.

    - Wednesday seems to be the most expensive day to transact.

    """)

    ##############################################################################################################

    ##### SECTION 2: USER DATA

    st.header("2. User Data")
    st.subheader("2.1. Active Users")

    st.markdown("""
    Definitions:

    - Active Wallets Transacting: Wallets that have signed at least one transaction in the past 3 months.

    - Active Wallets Receiving Tokens: Wallets that have been on the receiving end of at least one transaction in the past 3 months and have not signed any transactions.

    - Total Active Wallets: Sum of Active Wallets Transacting and Active Wallets Receiving Tokens.

    """)

    col1, col2, col3, col4 = st.columns(4)

    df_summ = pd.read_json("2_summ.json")
    df_act = pd.read_json("2_act.json")
    df_tx = pd.read_json("2_tx.json")

    fig = go.Figure()
    fig.add_trace(go.Indicator(
    mode = "number",
    value = 5220198,
    title="Active Wallets Transacting"
    ))
    fig.update_layout(width=300, height=250)

    with col1:
        st.plotly_chart(fig)

    fig = go.Figure()
    fig.add_trace(go.Indicator(
    mode = "number",
    value = 978330,
    title="Active Wallets Receiving Tokens"
    ))
    fig.update_layout(width=300, height=250)
    
    with col2:
        st.plotly_chart(fig)

    fig = go.Figure()
    fig.add_trace(go.Indicator(
    mode = "number",
    value = 6198528,
    title="Total Active Wallets"
    ))
    fig.update_layout(width=300, height=250)

    with col3:
        st.plotly_chart(fig)

    df_act_melt = pd.melt(df_act, id_vars=['DATE','ACTIVE_USERS'], value_vars=['TYPE'])

    selection2 = alt.selection_interval(encodings=['x'])

    base = alt.Chart(df_act).encode(x='DATE:T')
    line = base.mark_line().encode(
        x='DATE:T',
        y=alt.Y("ACTIVE_USERS:Q", axis=alt.Axis(title="Active Wallets")),
        color=alt.Color('TYPE:N', title="Type"),
        tooltip=[alt.Tooltip("DATE",title="Date"), alt.Tooltip("ACTIVE_USERS",title="Active Wallets")]
    )
    ch = line.transform_filter(selection2).properties(width=900, title="Daily Active Wallets")
    view = line.add_selection(selection2).properties(
        width=900,
        height=50
    )

    st.altair_chart(ch & view)

    brush = alt.selection_interval()
    chart = alt.Chart(df_tx).mark_circle().encode(
        x='MATIC_PRICE:Q',
        color=alt.condition(brush, alt.value('steelblue'), alt.value('lightgray'))
    ).properties(
        width=900,
        height=250
    ).add_selection(
        brush
    )
    ch = chart.encode(y='USERS_DOING_TRANSACTIONS:Q').properties(title="MATIC Price vs. Users Transacting") & chart.encode(y='USERS_RECEIVING_TOKENS:Q').properties(title="MATIC Price vs. Users Receiving Tokens")
    st.altair_chart(ch)

    ##############################################################################################################

    ##### SECTION 3: USER DATA

    df_a = pd.read_json("3_a.json")
    df_b = pd.read_json("3_b.json")
    df_c = pd.read_json("3_c.json")

    color4 = alt.condition(selection, 'TYPE:N', alt.value('lightgray'))

    base = alt.Chart(df_a).encode(x='yearmonthdate(DATE):T')
    line1 = base.mark_bar().encode(y=alt.Y("CUMULATIVE_ADDRESS:Q", axis=alt.Axis(title="Cumulative New Wallets")), color=color1)
    line2 = base.mark_line(color="steelblue").encode(y=alt.Y("NEW_ADDRESS:Q", axis=alt.Axis(title="New Wallets")))
    ch = alt.layer(line1, line2).resolve_scale(y = 'independent').encode(
        tooltip=[alt.Tooltip("DATE:T",title="Date"), alt.Tooltip("CUMULATIVE_ADDRESS",title="Cumulative New Wallets"), alt.Tooltip("NEW_ADDRESS",title="New Wallets")])
    ch1 = ch.transform_filter(selection).properties(width=900, title="Daily New Wallets and Total Cumulative Wallets")
    view1 = ch.add_selection(selection).properties(
       width=900,
       height=50,
    )
    
    base = alt.Chart(df_b).encode(x='yearmonthdate(DATE):T')
    line1 = base.mark_bar().encode(y=alt.Y("CUMULATIVE_ADDRESS:Q", axis=alt.Axis(title="Cumulative New Wallets")), color=color4)
    line2 = base.mark_line(color="steelblue").encode(y=alt.Y("NEW_ADDRESS:Q", axis=alt.Axis(title="New Wallets")))
    ch = alt.layer(line1, line2).resolve_scale(y = 'independent').encode(
        tooltip=[alt.Tooltip("DATE:T",title="Date"), alt.Tooltip("CUMULATIVE_ADDRESS",title="Cumulative New Wallets"), alt.Tooltip("NEW_ADDRESS",title="New Wallets")])
    ch2 = ch.transform_filter(selection).properties(width=900, title="Daily New Wallets and Yearly Cumulative Wallets")
    view2 = ch.add_selection(selection).properties(
       width=900,
       height=50,
    )
    st.subheader("Key Findings")

    st.markdown("""

    - The number of active wallets peaked in January 2022, but the most significant increase happened in October 2021.

    - There is a positive correlation between the number of active wallets and the price of MATIC. More users are likely attracted to the network when the price of MATIC is higher. The token could also be increasing in price due to there being more active users and thus more demand for the token.

    """)

    st.subheader("2.2. User Growth")

    st.markdown("""
    Definitions:

    - New Wallets: Wallets transacting in Polygon for the first time.

    - Total Cumulative Wallets: The total number of new wallets transacting in Polygon.

    - Yearly Cumulative Wallets: The total number of new wallets transacting in Polygon for the year.

    """)

    st.altair_chart(ch1 & view1 & ch2 & view2)

    ch = alt.Chart(df_c).mark_bar().encode(
        x=alt.X('TYPE:N', title="Year"),
        y=alt.Y("NEW_ADDRESS:Q", axis=alt.Axis(title="Daily Avg. New Wallets")),
        color=alt.Color('TYPE:N', title="Year"),
        tooltip=[alt.Tooltip("TYPE:N",title="Year"), alt.Tooltip("NEW_ADDRESS",title="Daily Avg. New Wallets")]
    ).properties(width=900,title="Daily Avg. New Wallets by Year")

    st.altair_chart(ch)

    st.subheader("Key Findings")

    st.markdown("""

    - Growth increased until October 2021 and has somewhat remained steady since.

    - As many users got into Polygon during 2021 as they did from January to June in 2022.

    - On average, almost double the users are joining Polygon in 2022 compared to 2021.

    """)

    st.subheader("Appendix: Queries")

    st.markdown("""

    - [Price and Circulating Supply](https://app.flipsidecrypto.com/velocity/queries/aba869fe-18b7-4fe5-87dd-01c20a077063)

    - [Daily Avg. Transactions](https://app.flipsidecrypto.com/velocity/queries/151330ab-294d-4a67-819e-1a67206713c3)

    - [Transactions Heatmap](https://app.flipsidecrypto.com/velocity/queries/3515a3ce-e7aa-4cb3-b4e6-9936c85f7b80)

    - [Daily Avg. Fees](https://app.flipsidecrypto.com/velocity/queries/bec4613e-9dd8-48ce-b2f0-bc67a7fac559)

    - [Fees Heatmap](https://app.flipsidecrypto.com/velocity/queries/2c869f10-ffb3-45b4-822f-1249f69e3f84)

    - [Active Wallet Summary](https://app.flipsidecrypto.com/velocity/queries/694590cb-aa04-41e8-8e0d-a6437baf3ed6)

    - [Daily Active Wallets](https://app.flipsidecrypto.com/velocity/queries/5da1f0aa-d720-48f0-a4ed-d5a7527abb12)

    - [Active Wallets and MATIC Price](https://app.flipsidecrypto.com/velocity/queries/ecde455f-7f06-4712-8df7-c31b0542ab06)

    - [Daily New Wallets](https://app.flipsidecrypto.com/velocity/queries/171d0bd7-72e4-4121-b4d7-533706adc3fd)

    - [New Wallets Yearly Cumulative](https://app.flipsidecrypto.com/velocity/queries/0719deaa-f8ea-4012-9c44-06b7486a359a)

    - [Average Daily New Wallets](https://app.flipsidecrypto.com/velocity/queries/b77205f8-42a4-4c80-9694-ea55e8a5ac8c)

    """)

    st.subheader("Contact Data")

    st.markdown("""

    Thank you for reading!

    For any questions or feedback, feel free to contact me on Discord at CarlOwOs#4288 or Twitter at @CarlOwOs1

    *July 29th, 2022*
    """)




