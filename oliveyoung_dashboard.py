import streamlit as st
import pandas as pd
import plotly.express as px

# Page setup - MUST BE FIRST!
st.set_page_config(page_title="Olive Young Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned.csv")
    df.drop(columns=['Unnamed: 0'], inplace=True)
    df.dropna(subset=['Rating'], inplace=True)
    return df

df = load_data()

st.title("🌿 Olive Young Product Dashboard")

# Define price category mapping using actual dollar values
bins = [0, 15, 35, df['Price'].max() + 1]
labels = ['Budget (<$15)', 'Mid-Range ($15-$35)', f'Premium (>$35)']
df['Price_Category'] = pd.cut(df['Price'], bins=bins, labels=labels, include_lowest=True)

# Sidebar Filters
st.sidebar.header("🔎 Filter Products")

# Category multi-select with "All" option
category_options = ["All"] + sorted(df['Category'].unique().tolist())
selected_categories = st.sidebar.multiselect(
    "Select Category",
    options=category_options,
    default=["All"]
)

# Brand multi-select with "All" option
brand_options = ["All"] + sorted(df['Brand'].dropna().unique().tolist())
selected_brands = st.sidebar.multiselect(
    "Select Brand",
    options=brand_options,
    default=["All"]
)

# Price Category multi-select with "All" option
price_category_options = ["All"] + labels
selected_price_categories = st.sidebar.multiselect(
    "Select Price Category",
    options=price_category_options,
    default=["All"]
)

# Price range slider
price_range = st.sidebar.slider(
    "Select Price Range ($)",
    float(df['Price'].min()),
    float(df['Price'].max()),
    (float(df['Price'].min()), float(df['Price'].max()))
)

# Discount range slider
discount_range = st.sidebar.slider(
    "Select Discount Range (%)",
    float(df['Discount'].min()),
    float(df['Discount'].max()),
    (float(df['Discount'].min()), float(df['Discount'].max()))
)

# Apply filters
filtered_df = df.copy()

if "All" not in selected_categories:
    filtered_df = filtered_df[filtered_df['Category'].isin(selected_categories)]

if "All" not in selected_brands:
    filtered_df = filtered_df[filtered_df['Brand'].isin(selected_brands)]

if "All" not in selected_price_categories:
    filtered_df = filtered_df[filtered_df['Price_Category'].isin(selected_price_categories)]

filtered_df = filtered_df[(filtered_df['Price'] >= price_range[0]) & (filtered_df['Price'] <= price_range[1])]
filtered_df = filtered_df[(filtered_df['Discount'] >= discount_range[0]) & (filtered_df['Discount'] <= discount_range[1])]

# Tabs
tabs = st.tabs(["📉 Discount Analysis", "🌟 Customer Preferences", "📦 Inventory Decisions", "🏷️ Brand Performance", "👥 Customer Segments", "📝 Key Insights"])

# 📉 Discount Analysis
tabs[0].subheader("Discount Analysis")
fig1 = px.histogram(filtered_df, x='Discount', nbins=30, color='Category', title="Distribution of Discounts")
tabs[0].plotly_chart(fig1, use_container_width=True)
fig2 = px.scatter(filtered_df, x='Discount', y='Rating', color='Category', hover_data=['Title'], title="Discount vs. Rating")
tabs[0].plotly_chart(fig2, use_container_width=True)

# 🌟 Customer Preferences
tabs[1].subheader("Customer Preferences")
fig3 = px.bar(filtered_df.groupby('Category')["Rating"].mean().reset_index(), x='Category', y='Rating', title="Average Rating by Category")
tabs[1].plotly_chart(fig3, use_container_width=True)
fig4 = px.box(filtered_df, x='Brand', y='Rating', title="Customer Rating Distribution by Brand")
tabs[1].plotly_chart(fig4, use_container_width=True)

# 📦 Product Inventory Decisions
tabs[2].subheader("Product Inventory Decisions")
fig5 = px.box(filtered_df, x='Price_Category', y='Price', color='Price_Category', title="Price Distribution by Price Category")
tabs[2].plotly_chart(fig5, use_container_width=True)
fig6 = px.histogram(filtered_df, x='Price_Category', title="Product Count by Price Category")
tabs[2].plotly_chart(fig6, use_container_width=True)

# 🏷️ Brand Performance
tabs[3].subheader("Brand Performance")
top_brands = filtered_df['Brand'].value_counts().nlargest(10).reset_index()
top_brands.columns = ['Brand', 'Count']
fig7 = px.bar(top_brands, x='Brand', y='Count', title="Top 10 Brands by Product Count")
tabs[3].plotly_chart(fig7, use_container_width=True)
brand_rating = filtered_df.groupby('Brand')["Rating"].mean().nlargest(10).reset_index()
fig8 = px.bar(brand_rating, x='Brand', y='Rating', title="Top 10 Brands by Avg. Rating")
tabs[3].plotly_chart(fig8, use_container_width=True)

# 👥 Customer Segments
tabs[4].subheader("Customer Segmentation")
fig9 = px.box(filtered_df, x='Price_Category', y='Rating', color='Price_Category', title="Rating vs Price Category")
tabs[4].plotly_chart(fig9, use_container_width=True)
fig10 = px.histogram(filtered_df, x='Rating', color='Price_Category', barmode='overlay', title="Rating Distribution by Customer Segment")
tabs[4].plotly_chart(fig10, use_container_width=True)
fig11 = px.scatter(filtered_df, x='Price', y='Rating', color='Category', title='Price vs Rating by Category')
tabs[4].plotly_chart(fig11, use_container_width=True)
fig12 = px.violin(filtered_df, y='Rating', x='Price_Category', box=True, points='all', color='Price_Category', title='Violin Plot: Rating Distribution by Price Category')
tabs[4].plotly_chart(fig12, use_container_width=True)

# 📝 Insights & Recommendations
tabs[5].subheader("Key Insights & Recommendations")
tabs[5].markdown("""
### 📌 Insights:
- Products with **higher discounts** often receive **better ratings**, especially in skincare and treatment categories.
- **Premium Tier (> $35)** products such as:
  - **Dr.G Green Mild Up Sun+ SPF50+**, 
  - **REJURAN Healer Turnover Ampoule**, and
  - **medicube Deep Erasing Cream**
  are top performers with ratings **above 4.9**.
- **Mid-Tier ($15–$35)** champions include:
  - **NUMBUZIN No.3 Skin Softening Serum** and
  - **Torriden Dive-In Serum**, combining affordability with high ratings.
- **Budget Tier (< $15)** bestsellers like:
  - **Etude House Soon Jung pH 5.5 Foam Cleanser**
  - **A'PIEU Madecassoside Cream** show strong value.
- **Top-rated brands** by price segment:
  - **Budget:** A'PIEU, Etude House
  - **Mid-Range:** NUMBUZIN, Torriden, Some By Mi
  - **Premium:** Dr.G, REJURAN, medicube
- Customers lean toward **mid-tier pricing**, balancing cost and quality.
- Some **highly rated products lack sufficient reviews** — missed promotional opportunities.

### ✅ Recommendations:
- Promote highly discounted, well-rated products in marketing campaigns.
- Focus inventory on mid-tier items with consistent customer satisfaction.
- Expand offerings in categories that combine high discounts and ratings.
- Monitor low-rated products despite discounts and revise listings or formulations.
- Boost visibility of premium high-rated but under-reviewed products.
- Encourage verified reviews to strengthen credibility, especially for new or niche brands.
""")

