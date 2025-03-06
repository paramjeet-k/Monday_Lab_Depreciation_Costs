import streamlit as st
from tabulate import tabulate
import pandas as pd

def calculate_depreciation(method, cost, salvage, life, units_produced=None, total_units=None):
    depreciation_per_year = []
    accumulated_depreciation = 0  # Track accumulated depreciation
    
    if method == 1:  # Straight-Line Method
        annual_depreciation = (cost - salvage) / life
        for year in range(1, life + 1):
            accumulated_depreciation += annual_depreciation
            book_value = cost - accumulated_depreciation
            depreciation_per_year.append([year, book_value, annual_depreciation])
    
    elif method == 2:  # Declining Balance Method
        book_value = cost
        rate = 2 / life
        for year in range(1, life + 1):
            depreciation = book_value * rate
            depreciation = min(depreciation, book_value - salvage)  # Ensure salvage limit
            accumulated_depreciation += depreciation
            book_value -= depreciation
            depreciation_per_year.append([year, book_value, depreciation])
    
    elif method == 3 and units_produced and total_units:  # Units of Production Method
        annual_depreciation = (cost - salvage) * (units_produced / total_units)
        for year in range(1, life + 1):
            accumulated_depreciation += annual_depreciation
            book_value = cost - accumulated_depreciation
            depreciation_per_year.append([year, book_value, annual_depreciation])
    
    elif method == 4:  # Sum-of-the-Years-Digits Method
        years = list(range(1, life + 1))
        total = sum(years)
        for year in range(1, life + 1):
            fraction = (life - (year - 1)) / total
            depreciation = (cost - salvage) * fraction
            accumulated_depreciation += depreciation
            book_value = cost - accumulated_depreciation
            depreciation_per_year.append([year, book_value, depreciation])
    
    elif method == 5:  # Double Declining Balance Method
        book_value = cost
        rate = 2 / life
        for year in range(1, life + 1):
            depreciation = book_value * rate
            depreciation = min(depreciation, book_value - salvage)  # Ensure salvage limit
            accumulated_depreciation += depreciation
            book_value -= depreciation
            depreciation_per_year.append([year, book_value, depreciation])
    
    else:
        return None
    
    # Convert results to a DataFrame for Streamlit
    df = pd.DataFrame(depreciation_per_year, columns=["Year", "Book Value (INR)", "Depreciation per Year (INR)"])
    df["Depreciation per Month (INR)"] = df["Depreciation per Year (INR)"] / 12
    
    return df

# Streamlit UI
st.title("📊 Depreciation Calculator")

st.sidebar.header("Input Parameters")
method_options = {
    "Straight-Line": 1,
    "Declining Balance": 2,
    "Units of Production": 3,
    "Sum-of-the-Years-Digits": 4,
    "Double Declining Balance": 5
}

method_name = st.sidebar.selectbox("Select Depreciation Method", list(method_options.keys()))
method = method_options[method_name]

cost = st.sidebar.number_input("Enter Machinery Cost (INR)", min_value=0.0, format="%.2f")
salvage = st.sidebar.number_input("Enter Salvage Value (INR)", min_value=0.0, format="%.2f")
life = st.sidebar.number_input("Enter Useful Life of Asset (Years)", min_value=1, step=1)

units_produced = None
total_units = None

# If method is "Units of Production", take additional inputs
if method == 3:
    units_produced = st.sidebar.number_input("Enter Units Produced This Year", min_value=1.0, format="%.2f")
    total_units = st.sidebar.number_input("Enter Total Estimated Units", min_value=1.0, format="%.2f")

# Calculate Depreciation
if st.sidebar.button("Calculate Depreciation"):
    results = calculate_depreciation(method, cost, salvage, life, units_produced, total_units)
    
    if results is not None:
        st.subheader("📌 Depreciation Schedule")
        st.dataframe(results)
    else:
        st.error("Invalid inputs. Please check your entries.")
