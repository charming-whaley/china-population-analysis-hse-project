import streamlit as st
import pandas as pd
import numpy as np

data = pd.read_csv("china.csv")
data = data.astype("string")
data = data.replace("Null", "0")
data = data.map(lambda x: x.replace(",", ""))
data = data.map(lambda x: x.replace("%", ""))


def convert_range(lhs, rhs, to_type):
    data.loc[0:74, lhs:rhs] = data.loc[0:73, lhs:rhs].astype(to_type)


convert_range("% Increase in Population", "% Increase in Population Density", "float64")
convert_range("Urban Population % of Total Population", "% Increase in Urban Population", "float64")
convert_range("Rural Population % of Total Population", "% Change in Net Migration Rate", "float64")

data["Year"] = data["Year"].astype("int64")
data["Population"] = data["Population"].astype("int64")
data["Urban Population"] = data["Urban Population"].astype("int64")
data["Rural Population"] = data["Rural Population"].astype("int64")

st.header("China population analysis 🇨🇳")

st.text("China population analysis: a deep dive into China's population trends from 1950 to 2022, leveraging data on population size, fertility rates, infant mortality rates, and more")

st.text("The following dataset has been cleaned and prepared for analysis:")
st.write(data)

st.text("The project is divided into two parts: ")
st.markdown("""
1. Population analysis: urban/rural dynamics in China
2. Analyzing fertility rates in China
""")

st.text("Here are some details about the dataset:")

first_temporary = data["Life Expectancy"].astype("int64")
second_temporary = data["Birth Rate"].astype("int64")
third_temporary = data["Death Rate"].astype("int64")

details = {
    "": [
        "Population", 
        "Population density", 
        "Life expectancy", 
        "Birth rate", 
        "Death rate"
    ],
    "Mean": [
        int(data["Population"].mean()),
        int(data["Population Density"].mean()),
        int(data["Life Expectancy"].mean()),
        int(data["Birth Rate"].mean()),
        int(data["Death Rate"].mean())
    ],
    "Median": [
        int(data["Population"].median()),
        int(data["Population Density"].median()),
        int(data["Life Expectancy"].median()),
        int(data["Birth Rate"].median()),
        int(data["Death Rate"].median())
    ],
    "Range": [
        np.array(data["Population"]).max() - np.array(data["Population"]).min(),
        np.array(data["Population Density"]).max() - np.array(data["Population Density"]).min(),
        np.array(first_temporary).max() - np.array(first_temporary).min(),
        np.array(second_temporary).max() - np.array(second_temporary).min(),
        np.array(third_temporary).max() - np.array(third_temporary).min()
    ],
    "Max": [
        np.array(data["Population"]).max(),
        np.array(data["Population Density"]).max(),
        np.array(data["Life Expectancy"]).max(),
        np.array(data["Birth Rate"]).max(),
        np.array(data["Death Rate"]).max(),
    ],
    "Min": [
        np.array(data["Population"]).min(),
        np.array(data["Population Density"]).min(),
        np.array(data["Life Expectancy"]).min(),
        np.array(data["Birth Rate"]).min(),
        np.array(data["Death Rate"]).min(),
    ]
}

st.write(pd.DataFrame(details))
st.text("Range - the length between the maximum and the minimum value")

st.text("The standard deviation of each column:")

deviations = {
    "": ["" for i in range(0, len(data["Year"]) - 1)],
    "Population": np.std(np.array(data["Population"])),
    "Population density": np.std(np.array(data["Population Density"])),
    "Life expectancy": np.std(np.array(first_temporary)),
    "Birth rate": np.std(np.array(second_temporary)),
    "Death rate": np.std(np.array(third_temporary))
}

st.table(pd.DataFrame(deviations))
