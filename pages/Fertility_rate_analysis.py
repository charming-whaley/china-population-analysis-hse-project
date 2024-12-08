import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

with st.sidebar:
    st.title("Fertility rate analysis")
    st.text("This page provides fertility rate analysis charts and tables, illustrating trends and patterns.")

st.title("Fertility analysis 🍼")

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


f_p = data.loc[0:30, "Life Expectancy":"% Change in Net Migration Rate"]
s_p = data.loc[31:49, "Life Expectancy":"% Change in Net Migration Rate"]
t_p = data.loc[50:72, "Life Expectancy":"% Change in Net Migration Rate"]


def fertility_rate_analysis():
    st.subheader("Life in China analysis")

    st.text("First, let's look at how life expectancy in China has changed over time:")

    f_p_life = pd.DataFrame(
        {
            "Year": [year for year in range(1950, 1981)],
            "Period": ["1950-1980"] * 31, 
            "Life expectancy": f_p["Life Expectancy"]
        }
    )

    s_p_life = pd.DataFrame(
        {
            "Year": [year for year in range(1981, 2000)],
            "Period": ["1981-1999"] * 19, 
            "Life expectancy": s_p["Life Expectancy"]
        }
    )

    t_p_life = pd.DataFrame(
        {
            "Year": [year for year in range(2000, 2023)],
            "Period": ["2000-2022"] * 23, 
            "Life expectancy": t_p["Life Expectancy"]
        }
    )

    life = pd.concat([f_p_life, s_p_life, t_p_life])

    figure = px.line(life, x="Year", y="Life expectancy", color="Period", title="Life expectancy in China", markers=True)
    st.write(figure)
    st.text("Since 1950, life expectancy in China has increased, leading to an older population.")

    st.subheader("Birth/death rates comparison")

    st.text("Now, let us see how birth and death rates have been changed since 1950.")

    birth = pd.DataFrame(
        {
            "Year": [year for year in range(1950, 2023)],
            "Rate": data["Birth Rate"],
            "Type": ["Birth"] * 73
        }
    )

    death = pd.DataFrame(
        {
            "Year": [year for year in range(1950, 2023)],
            "Rate": data["Death Rate"],
            "Type": ["Death"] * 73
        }
    )

    fertility_rate = pd.concat([birth, death])

    figure = px.line(fertility_rate, x="Year", y="Rate", color="Type", title="Births and deaths in China")
    st.write(figure)
    st.text("As we can see here, birth and death rates both almost tied for first place in 2022. This means the number of people passing away is increasing, while the number of people getting birth is decreasing.")

    st.text("To prove that, let us see the growth rate in Chian in period from 1950 to 2022.")

    st.text("First of all, let us create the growth rate table:")

    growth_rate = pd.DataFrame(
        {
            "Year": [year for year in range(1950, 2023)],
            "Birth rate": data["Birth Rate"],
            "Death rate": data["Death Rate"],
            "Growth Rate": (data["Birth Rate"] - data["Death Rate"]) / 10
        }
    )

    st.write(growth_rate)

    st.text("Code that renders the table:")
    code = '''
    growth_rate = pd.DataFrame(
        {
            "Year": [year for year in range(1950, 2023)],
            "Birth rate": data["Birth Rate"],
            "Death rate": data["Death Rate"],
            "Growth Rate": (data["Birth Rate"] - data["Death Rate"]) / 10
        }
    )
    '''

    st.code(code, language="python")

    st.text("Finally, let us render that table as plot:")

    figure = px.line(growth_rate, x="Year", y="Growth Rate", title="Growth rate")
    st.write(figure)
    st.text("It is now evident that death rate surpasses birth rate. That may be because Chinese population became so much big that its government decided to do anything to prevent this from increase.")

    st.text("Besides the decline trend in birth/death we may see some changes in infant mortality rate in China")

    st.text("Firstly, let's create the Infant mortality rate table")

    infant_mortality = pd.DataFrame(
        {
            "Period": ["1950-1980", "1981-1999", "2000-2022"],
            "Infant mortality rate": [
                f_p["Infant Mortality Rate"].mean(),
                s_p["Infant Mortality Rate"].mean(),
                t_p["Infant Mortality Rate"].mean()
            ],
            "Fertility rate": [
                f_p["Fertility Rate"].mean(),
                s_p["Fertility Rate"].mean(),
                t_p["Fertility Rate"].mean()
            ]
        }
    )

    st.write(infant_mortality)

    code = '''
    infant_mortality = pd.DataFrame(
        {
            "Period": ["1950-1980", "1981-1999", "2000-2022"],
            "Infant mortality rate": [
                f_p["Infant Mortality Rate"].mean(),
                s_p["Infant Mortality Rate"].mean(),
                t_p["Infant Mortality Rate"].mean()
            ],
            "Fertility rate": [
                f_p["Fertility Rate"].mean(),
                s_p["Fertility Rate"].mean(),
                t_p["Fertility Rate"].mean()
            ]
        }
    )
    '''

    st.text("Code that renders the table:")
    st.code(code, language="python")

    figure = px.bar(infant_mortality, x="Period", y=["Infant mortality rate", "Fertility rate"], title="Infant mortality rate", barmode="group")
    st.write(figure)

    st.text("The plot above illustrates that, despite a decrease in infant mortality, a concurrent decline in fertility rates has resulted in a shrinking Chinese population.")

    st.subheader("Migration")

    st.text("People moving in and out of a country can affect its population. Let's look at China's migration data")

    f_p_migration = pd.DataFrame(
        {
            "Year": [year for year in range(1950, 1981)],
            "Period": ["1950-1981"] * 31,
            "Migration Rate": f_p["Net Migration Rate"]
        }
    )

    s_p_migration = pd.DataFrame(
        {
            "Year": [year for year in range(1981, 2000)],
            "Period": ["1981-1999"] * 19,
            "Migration Rate": s_p["Net Migration Rate"]
        }
    )

    t_p_migration = pd.DataFrame(
        {
            "Year": [year for year in range(2000, 2023)],
            "Period": ["2000-2022"] * 23,
            "Migration Rate": t_p["Net Migration Rate"]
        }
    )

    migration_rate = pd.concat([f_p_migration, s_p_migration, t_p_migration])

    figure = px.line(migration_rate, x="Year", y="Migration Rate", color="Period", title="Migration", markers=True)
    st.write(figure)
    st.text("The graph shows that fewer people are moving to China than are leaving. This is another reason why the population is decreasing.")


def second_hypothesis():
    st.subheader("Second hypothesis")

    st.text("Let's see if China's higher life expectancy correlates with a lower fertility rate. To accomplish this, we shall compare life expectancy with both general fertility rate and growth rate")

    st.subheader("I. Creating tables")

    st.text("First, let's create a table with the data:")

    st.text("The first table:")

    first_comparison = pd.DataFrame(
        {
            "Life expectancy": data["Life Expectancy"],
            "Growth Rate": (data["Birth Rate"] - data["Death Rate"]) / 10
        }
    )

    second_comparison = pd.DataFrame(
        {
            "Life expectancy": data["Life Expectancy"],
            "Fertility rate": data["Fertility Rate"]
        }
    )

    st.write(first_comparison)

    st.text("Code that renders the first table:")

    code = '''
    first_comparison = pd.DataFrame(
        {
            "Life expectancy": data["Life Expectancy"],
            "Growth Rate": (data["Birth Rate"] - data["Death Rate"]) / 10
        }
    )
    '''

    st.code(code, language="python")

    st.text("The second table: ")

    st.write(second_comparison)

    code = '''
    second_comparison = pd.DataFrame(
        {
            "Life expectancy": data["Life Expectancy"],
            "Fertility rate": data["Fertility Rate"]
        }
    )
    '''
    st.code(code, language="python")

    st.subheader("II. Rendering 2D histograms:")

    st.text("Now, we'll visualize the data using 2D histograms:")

    figure = px.density_heatmap(first_comparison, x="Life expectancy", y="Growth Rate", color_continuous_scale="Viridis")
    st.write(figure)
    st.text("We can see that higher life expectancy is associated with lower growth rates.")

    figure = px.density_heatmap(second_comparison, x="Life expectancy", y="Fertility rate", color_continuous_scale="Viridis")
    st.write(figure)
    st.text("We can also see that higher life expectancy is linked to lower fertility rates.")

    st.subheader("III. Second hypothesis conclusion")
    st.text("In conclusion, as China's population ages and life expectancy increases, birth rates are declining.")


categories = st.selectbox("Select content to show", ["Life in China analysis", "Hypothesis"])

if categories == "Life in China analysis":
    fertility_rate_analysis()
else:
    second_hypothesis()
