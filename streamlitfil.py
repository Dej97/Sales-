import streamlit as st
import pandas as pd 
import plotly.express as px 
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
import seaborn as sbr



# Define custom CSS styles


st.set_page_config(
    page_title="Sales Data analysis",
    page_icon="✅",
    layout="wide"
)





# Create a sidebar for navigation
st.sidebar.header("Navigation")
selected_option = st.sidebar.selectbox("Choose an option", ["Sales_Data Overview", "Visualizations", "Report", "About"])


col1, col2,col3 = st.columns([2,2,3])

# Define content for the main area based on the selected option

    
if selected_option == "Sales_Data Overview":
    
    
    with col1:
        df = pd.read_csv('Sales Data.csv')  # Load your data here
        st.title("Sales Data Analysis")
        st.write("Data Preview:")
        df.drop(['Unnamed: 0'],axis=1,inplace=True)
        df['Order Date'] = pd.to_datetime(df['Order Date'])
        df['Order Date'] = df['Order Date'].dt.date
        st.dataframe(df)
    with col1:
        st.header("Data Information:")
        st.write("Number of Rows:", df.shape[0])
        st.write("Number of Columns:", df.shape[1])
        st.subheader("__________________")
        st.write("")
        st.subheader("Null Value Checker")
        
    
        
# Check for null values in the entire DataFrame
    
        null_values = df.isnull().sum()

    # Check if there are any null values
        if null_values.any():
        # Display the columns with null values and their respective counts
            st.write("Columns with Null Values:")
            st.write(null_values[null_values > 0],null_values)
        else:
            st.write("No Null Values Found ",null_values)
    with col2:
        df.drop_duplicates()
        df['Order Date'] = pd.to_datetime(df['Order Date'])
        df.rename(columns={'Order Date':'Date'}, inplace=True)
        
        df.drop(['Purchase Address'],axis=1,inplace=True)
        
        
        
        grouped = df[['Product', 'Price Each', 'Sales','Quantity Ordered']]
        grouped = df.groupby('Product').agg({ 'Price Each': 'sum', 'Sales': 'sum', 'Quantity Ordered': 'sum' }).reset_index()
        grouped['Profit margin'] = ((grouped['Sales'] - grouped['Price Each']) / grouped['Sales']*100) 
       

        st.title("EDA Process")
        st.write("Data Preview:")

        st.dataframe(grouped)
        st.header("Data Information:")
        st.write("Number of Rows:", df.shape[0])
        st.write("Number of Columns:", df.shape[1])
        st.subheader("__________________")
        st.subheader("Data Description")
        st.write("")
       
        describedata=grouped.describe()
        st.dataframe(describedata)
        st.write("")
        grouped.rename(columns={'Quantity Ordered':'ORDERS'},inplace=True)
      
    

    with col3:
        st.title("_________________________________________")
        
        
    # Create a Plotly chart
        fig_1 = px.bar(grouped, x="ORDERS", y="Product", orientation="h",title='Quantity of Orders' ,color_discrete_sequence=["forestgreen"])
        
        st.write("") 
        st.plotly_chart(fig_1)
        st.title("_________________________________________")

        fig2 = px.pie(grouped, names='Product', values='Profit margin', title='Profit Margin by Product', color_discrete_sequence=["#008000", "#00FF00", "#228B22"])
        # Display the pie chart using Streamlit
        st.plotly_chart(fig2)
        st.title("_________________________________________")

elif selected_option == "Visualizations":
    with col1:
        st.title("Visualizations")
        st.write("Explore different Visualizations here")
        
        visualization_option = st.selectbox("Select a visualization", ["Orders & Profit", "Line Chart", "Scatter Plot","HeatMap"])
        
    if visualization_option == "Orders & Profit":
        # Create a bar chart
        
        df = pd.read_csv('Sales Data.csv')
        city_counts = df['City'].value_counts().reset_index()
        city_counts.columns = ['City', 'Orders']
     
        fig3 = px.bar(city_counts, x='City', y='Orders',
           
             title='ORDERS BY CITY',
             color='Orders',
             color_continuous_scale='mint')
        
        with col3:
            st.plotly_chart(fig3)
            colors = ['#008000', '#00FF00', '#00FF00', '#00FF00']
            st.markdown('<h3 style="text-align: center; font-family: Roboto, sans-serif; font-weight: bold; color: white; font-size: 38px;">San Francisco</h3>', unsafe_allow_html=True)
            st.markdown('<h3 style="text-align: center; font-family: Roboto, sans-serif; font-weight: bold; color: white; font-size: 36px;">Orders: 44 K</h3>', unsafe_allow_html=True)
            st.markdown('<h3 style="text-align: center; font-family: Roboto, sans-serif; font-weight: bold; color: white; font-size: 32px;">PROFIT : 24% <span style="color: green; font-weight: bold; font-size: 36px;">&#8593</span></h3>', unsafe_allow_html=True)
        with col1:
            fig4 = px.pie(df, names='City', values='Sales', title='Sales Distribution ',hole=0.4,color_discrete_sequence=colors)
            st.plotly_chart(fig4)

 # figure 5
    
    elif visualization_option == "Line Chart":
        # Create a line chart
        st.write("Display a line chart here.")
        df = pd.read_csv('Sales Data.csv')

        df['Order Date'] = pd.to_datetime(df['Order Date'])
        df['Order Date'] = df['Order Date'].dt.date
        
        df.rename(columns={'Order Date':'Date'}, inplace=True)

        grouped_data_1 = df.groupby(['Date','City'])['Sales'].mean().reset_index()
        grouped_data_2 =df.groupby('Date')['Sales'].mean().reset_index()
        
        fig5 = px.line(grouped_data_2 , x='Date', y='Sales', markers=True, title='Global Sales Over Time')
        with col1:
            st.plotly_chart(fig5)
            
            plt.figure(figsize=(16,10))

        grouped = df[['Product', 'Price Each', 'Sales','Quantity Ordered']]
        grouped = df.groupby('Product').agg({ 'Price Each': 'sum', 'Sales': 'sum', 'Quantity Ordered': 'sum' }).reset_index()
        grouped['Profit margin'] = ((grouped['Sales'] - grouped['Price Each']) / grouped['Sales']*100) 

        with col3:
            fig6 = px.line(grouped_data_1 , x='Date', y='Sales',color='City', markers=True, title='Sales Over Time by City')
            st.plotly_chart(fig6)
        with col1:
            st.title("Profit Margin by Product")
            fig7 = px.line(grouped, x='Product', y='Profit margin', line_shape='linear')
            fig7.update_layout(width=800, height=400)
            st.plotly_chart(fig7)
        with col3:
            st.subheader("Product Analysis:")
            st.write("The product with the highest profit margin is AA Batteries 4-pack with a profit margin of approximately 37.45%.")
            st.subheader("Sales Analysis:")
            st.write("The product with the highest total sales is Macbook Pro Laptop;with total sales of approximately $4,884,100.")
            st.subheader("Top 10 Products")
            st.write("")
            top_10_sales_products = grouped.sort_values(by='Sales', ascending=False).head(10)
            st.dataframe(top_10_sales_products)


    elif visualization_option == "Scatter Plot":
        with col2:
         
         
            # Create a scatter plot
            st.write("Display a scatter plot here.")
            
            df = pd.read_csv('Sales Data.csv')
            
            grouped = df[['Product', 'Price Each', 'Sales','Quantity Ordered']]
            grouped = df.groupby('Product').agg({ 'Price Each': 'sum', 'Sales': 'sum', 'Quantity Ordered': 'sum' }).reset_index()
            grouped['Profit margin'] = ((grouped['Sales'] - grouped['Price Each']) / grouped['Sales']*100) 

            
            



            ##st.title("Scatter Matrix Plot")
            ##st.plotly_chart(fig8)

    elif visualization_option == "HeatMap":
        with col2:
         
            # Create a HeatMap

            st.write("Display a HeatMap here.")
            
            df = pd.read_csv('Sales Data.csv')
            
            df.rename(columns={'Order Date':'Date'}, inplace=True)

            df2 = df[[ 'Price Each', 'Sales','Date','Product', 'Quantity Ordered']]

            df2['Date']=pd.to_datetime(df2['Date'])
            df2 = df2.sort_values(by=['Date', 'Product'])
            df2['Profit margin'] = ((df2['Sales'] - df2['Price Each']) / df2['Sales']*100)


            # Group by 'Date' and 'Product' and calculate cumulative sum
            df2['Cumulative Price Each'] = df2.groupby('Date')['Price Each'].cumsum()
            df2['Cumulative Sales'] = df2.groupby('Date')['Sales'].cumsum()
            df2['Cumulative Quantity Ordered'] = df2.groupby('Date')['Quantity Ordered'].cumsum()
            df2['Cumulative Profit margin'] = df2.groupby('Date')['Profit margin'].cumsum()
            
            df2.drop(['Date','Product'],axis = 1,inplace = True)

            



            
            





            # Apply custom CSS to make the plot full-page
            

          
            ##correlation_matrix = df2.corr()
            ##fig9 = px.imshow(
            ##correlation_matrix,
            ##zmin=-1,
            ##zmax=1,
            ##color_continuous_scale='BuPu',
            ##labels={'x': 'Features'}
        
          
            ##st.title("Heatmap of Correlation")
            ##fig9.update_traces(showscale=False)
            ##for i in range(len(correlation_matrix.columns)):
                ##for j in range(len(correlation_matrix.index)):
                    ##fig9.add_annotation(
                   ## x=i,
                    ##y=j,
                    ##text=f'{correlation_matrix.iloc[j, i]:.2f}',
                    ##showarrow=False,
                    ##font=dict(size=14)

       ## )
            ##st.plotly_chart(fig9)
       
                
            


elif selected_option == "Report":
    with col1:
        

        st.title("Total sales : 34,5M")

        st.title("Total Cost : 34,2M ")

        st.title("Total Orders : 209K ")

        st.title("Total Products :186K ")

        df = pd.read_csv('Sales Data.csv')

        grouped = df[['Product', 'Price Each', 'Sales','Quantity Ordered']]

        grouped = df.groupby('Product').agg({ 'Price Each': 'sum', 'Sales': 'sum', 'Quantity Ordered': 'sum' }).reset_index()

        grouped.rename(columns={'Quantity Ordered':'ORDERS'},inplace=True)

                    
        grouped['Profit margin'] = ((grouped['Sales'] - grouped['Price Each']) / grouped['Sales']*100) 


        total_Sales=grouped['Sales'].sum()
        total_cost=grouped['Price Each'].sum()

        total=total_Sales+total_cost

        data = {
        'Category': ['Total Sales', 'Total Cost'],
        'Value': [total_Sales, total_cost]
    }

        # Create a pie chart
        fig10 = px.pie(data, names='Category', values='Value', title='Total Sales and Total Cost Distribution', hole=0.4,color_discrete_sequence=["forestgreen", "limegreen"])

        st.plotly_chart(fig10)
    with col3:
        st.title("Executive Summary:")
        st.write("This report provides a comprehensive analysis of our sales data, highlighting key insights and opportunities for growth.The data was Sent by MeriSKILL Company , and the analysis was conducted to better understand  sales performance")
        st.title(" Key Insights:")   
        
        st.subheader("1.Most Expensive Product: Macbook Pro")  

        st.write("The Macbook Pro is the most expensive product, although it's important to note that higher  cost doesn't always guarantee higher profit margins. Profit margins are influenced by various factors, including  costs, pricing strategy, and market demand.") 

        st.subheader("2.Most Ordered Product: AAA Batteries (4-pack)")  
        st.write("The AAA Batteries (4-pack) is the best-selling product, reflecting high demand in the market.") 
        st.subheader("3.Most Ordered City: San Francisco")
        st.write('San Francisco is the city with the highest number of orders, suggesting a strong presence in this market')
        st.subheader("4.Highest Sales in San Francisco ")
        st.write(' sales are highest in San Francisco, showcasing a successful market for our products.')
        st.subheader("5.Total Sales and Costs")
        st.write('Total sales account for 50.1 % of the total, while total costs represent 49.9%. This balance indicates a healthy profit margin and efficient cost management.')
        st.write('_______________________________________________')    
    with col1:  
        st.write('_______________________________________________')
        st.subheader("Opportunities for Development")  
        st.subheader("Product Diversification")
        st.write(' While Macbook Pro is a high-value product, we should consider expanding the product range to cater to different customer segments.')
        st.subheader("Marketing Focus")
        st.write(' San Francisco is a strong market, but we should explore opportunities for expansion in other cities to diversify the customer base.')
        st.subheader('Cost Management') 
        st.write('Maintain a keen focus on cost management to sustain a healthy profit margin.')

        
        


elif selected_option == "About":
    st.title("About ME")
    st.write("check my linkedin profile ")
    st.write("https://www.linkedin.com/in/anas-mokhtariprofil/")

# Create a footer
st.markdown("---")
st.write("@ 2023 Anas Mokhtari ")
