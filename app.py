
import os
import sqlite3
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine

# Page Configuration
st.set_page_config(
    page_title="Instant Data Insight & Analytics Dashboard | Veerendra N M",
    page_icon="⚡",
    layout="wide"
)

# Header & Profile Context
st.title("⚡ Automated Data Insight & Analytics Dashboard")
st.markdown("A lightweight, zero-dependency analytics agent built by **Veerendra N M** to process database metrics and generate instant visualizations.")
st.markdown("🔗 [GitHub Profile](https://github.com/Veerendranm)")

# Helper function to initialize sample database
@st.cache_resource
def init_sample_database():
    db_path = "ecommerce.db"
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE products (
                product_id INTEGER PRIMARY KEY,
                product_name TEXT,
                category TEXT,
                unit_price REAL
            )
        """)
        cursor.execute("""
            CREATE TABLE orders (
                order_id INTEGER PRIMARY KEY,
                product_id INTEGER,
                quantity INTEGER,
                total_revenue REAL,
                order_date TEXT,
                FOREIGN KEY (product_id) REFERENCES products (product_id)
            )
        """)
        
        products_data = [
            (1, "Wireless Mouse", "Electronics", 25.0),
            (2, "Mechanical Keyboard", "Electronics", 80.0),
            (3, "Standing Desk", "Furniture", 300.0),
            (4, "Ergonomic Chair", "Furniture", 200.0),
            (5, "Python Programming Book", "Books", 45.0)
        ]
        cursor.executemany("INSERT INTO products VALUES (?, ?, ?, ?)", products_data)
        
        orders_data = [
            (101, 1, 10, 250.0, "2026-01-15"),
            (102, 2, 5, 400.0, "2026-01-18"),
            (103, 3, 2, 600.0, "2026-02-05"),
            (104, 4, 3, 600.0, "2026-02-12"),
            (105, 5, 15, 675.0, "2026-02-20"),
            (106, 1, 25, 625.0, "2026-03-01"),
            (107, 2, 12, 960.0, "2026-03-10")
        ]
        cursor.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?)", orders_data)
        conn.commit()
        conn.close()
    return db_path

db_file = init_sample_database()
engine = create_engine(f"sqlite:///{db_file}")

# Sidebar controls for analysis automation
st.sidebar.header("Agent Preset Metrics")
analysis_type = st.sidebar.selectbox(
    "Choose Analytical View:",
    [
        "Total Revenue by Category", 
        "Top Selling Products by Quantity", 
        "Monthly Sales Trend"
    ]
)

st.subheader(f"📊 Live Execution: {analysis_type}")

# Execute safe pre-optimized analytical queries based on selection
if analysis_type == "Total Revenue by Category":
    query = """
        SELECT p.category, SUM(o.total_revenue) as total_revenue
        FROM orders o
        JOIN products p ON o.product_id = p.product_id
        GROUP BY p.category
        ORDER BY total_revenue DESC;
    """
elif analysis_type == "Top Selling Products by Quantity":
    query = """
        SELECT p.product_name, SUM(o.quantity) as total_quantity
        FROM orders o
        JOIN products p ON o.product_id = p.product_id
        GROUP BY p.product_name
        ORDER BY total_quantity DESC;
    """
else:
    query = """
        SELECT order_date, SUM(total_revenue) as daily_revenue
        FROM orders
        GROUP BY order_date
        ORDER BY order_date ASC;
    """

try:
    df_result = pd.read_sql(query, engine)
    
    # Display metrics layout columns using modern width parameter
    col1, col2 = st.columns([1, 2])
    with col1:
        st.write("### Query Result Data Table")
        st.dataframe(df_result, width="stretch")
        
    with col2:
        st.write("### Automated Visual Insight")
        if not df_result.empty:
            chart_data = df_result.set_index(df_result.columns[0])
            st.bar_chart(chart_data)
        else:
            st.info("No data available to plot.")
            
except Exception as e:
    st.error(f"Execution Error: {e}")

# Interactive Custom Query Section
with st.expander("💻 Custom SQL Agent Workspace"):
    custom_query = st.text_area("Enter your custom SQL statement:", "SELECT * FROM products;")
    if st.button("Run Custom Code"):
        try:
            custom_df = pd.read_sql(custom_query, engine)
            st.dataframe(custom_df, width="stretch")
        except Exception as err:
            st.error(f"SQL Error: {err}")