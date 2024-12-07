import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.title("Population analysis 🌆")

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


def general_population_analysis():
    st.subheader("Population analysis")

    st.text("Let's start the analysis from seeing the population trend in China:")

    # First chart
    figure = px.bar(data, x="Year", y="Population", color="Population", title="China population")
    st.plotly_chart(figure, key="First chart")
    st.text("As illustrated in the figure above, the Chinese population has experienced sustained growth since 1950.")

    st.text("Now, we'll turn our attention to the trend of population density growth in China:")

    # Second chart
    figure = px.line(data, x="Year", y="Population Density", title="Grow in population density")
    st.plotly_chart(figure, key="Second chart")
    st.text("The plot also shows a rise in population density since 1950, meaning more people are living in a given area.")


def urban_rural_population_analysis():
    f_p = data.loc[0:30, "Year":"Life Expectancy"]
    s_p = data.loc[31:49, "Year":"Life Expectancy"]
    t_p = data.loc[50:72, "Year":"Life Expectancy"]

    st.subheader("Urban/rural population comparison")

    st.text("We are to take 3 most impoartant period in history of Communist China to compare urban/rural population:")
    st.markdown("""
    1. 1950-1980 - first 30 years of Communist China
    2. 1981-1999 - years before and after the USSR collapse
    3. 2000-2022 - modern days in Chinese history
    """)

    st.text("Let's begin by comparing the average urban and rural populations in China using a bar chart:")

    periods_means = pd.DataFrame(
        {
            "Period": [
                "1950-1980", 
                "1950-1980",
                "1981-1999",
                "1981-1999",
                "2000-2022",
                "2000-2022"
            ],
            "Population": [
                int(f_p["Urban Population"].mean()),
                int(f_p["Rural Population"].mean()),
                int(s_p["Urban Population"].mean()),
                int(s_p["Rural Population"].mean()),
                int(t_p["Urban Population"].mean()),
                int(t_p["Rural Population"].mean())
            ],
            "Inhabitants": [
                "Urban population",
                "Rural population",
                "Urban population",
                "Rural population",
                "Urban population",
                "Rural population"
            ]
        }
    )

    figure = px.bar(periods_means, x="Period", y="Population", color="Inhabitants", title="Mean value of urban and rural population in China")
    st.plotly_chart(figure, key="Third chart")

    periods_medians = pd.DataFrame(
        {
            "Period": [
                "1950-1980", 
                "1950-1980",
                "1981-1999",
                "1981-1999",
                "2000-2022",
                "2000-2022"
            ],
            "Population": [
                int(f_p["Urban Population"].median()),
                int(f_p["Rural Population"].median()),
                int(s_p["Urban Population"].median()),
                int(s_p["Rural Population"].median()),
                int(t_p["Urban Population"].median()),
                int(t_p["Rural Population"].median())
            ],
            "Inhabitants": [
                "Urban population",
                "Rural population",
                "Urban population",
                "Rural population",
                "Urban population",
                "Rural population"
            ]
        }
    )

    figure = px.bar(periods_medians, x="Period", y="Population", color="Inhabitants", title="Median value of urban and rural population in China")
    st.plotly_chart(figure, key="Fourth chart")
    st.text("It's evident that the urban population has grown since 1950, driven by people moving to cities for improved living conditions.")
    
    st.text("These pie charts illustrate the urban/rural population distribution in China for specific time periods:")
    figure = go.Figure()

    figure.add_trace(go.Pie(
        labels=['Urban', 'Rural'],
        values=[f_p["Urban Population % of Total Population"].mean(), f_p["Rural Population % of Total Population"].mean()],
        marker=dict(colors=['blue', 'lightblue']),
        textinfo='percent',
        textposition='inside'
    ))

    figure.update_layout(
        title_text='Urba/rural population 1950-1980',
        showlegend=False
    )

    st.write(figure)
    st.text("The pie chart represents urban/rural population in period since 1950 to 1980")

    figure = go.Figure()

    figure.add_trace(go.Pie(
        labels=['Urban', 'Rural'],
        values=[s_p["Urban Population % of Total Population"].mean(), s_p["Rural Population % of Total Population"].mean()],
        marker=dict(colors=['blue', 'lightblue']),
        textinfo='percent',
        textposition='inside'
    ))

    figure.update_layout(
        title_text='Urba/rural population 1981-1999',
        showlegend=False
    )

    st.write(figure)
    st.text("The pie chart represents urban/rural population in period since 1981 to 1999")

    figure = go.Figure()

    figure.add_trace(go.Pie(
        labels=['Urban', 'Rural'],
        values=[t_p["Urban Population % of Total Population"].mean(), t_p["Rural Population % of Total Population"].mean()],
        marker=dict(colors=['blue', 'lightblue']),
        textinfo='percent',
        textposition='inside'
    ))

    figure.update_layout(
        title_text='Urba/rural population 2000-2022',
        showlegend=False
    )

    st.write(figure)
    st.text("The pie chart represents urban/rural population in period since 2000 to 2022")

    # Some additional data here (do it tomorrow, not today)


def first_hypothesis():
    st.subheader("First hypothesis")

    st.text("Let's visualize the relationship between urban population and population density in China using a scatter plot. To achieve this, we'll focus on the 'Urban Population' and 'Population Density' columns and plot them on a graph.")

    st.subheader("I. Creating the table")

    st.text("First, let's create a table with the data:")

    first_hypothesis = pd.DataFrame(
        {
            "Year": [year for year in range(1960, 2022)],
            "Urban population": data.loc[10:71, "Urban Population"],
            "Population density": data.loc[10:71, "Population Density"],
        }
    )

    st.write(first_hypothesis)

    st.text("Code that renders the table:")

    code = '''
    first_hypothesis = pd.DataFrame(
        {
            "Year": [year for year in range(1960, 2022)],
            "Urban population": data.loc[10:71, "Urban Population"],
            "Population density": data.loc[10:71, "Population Density"],
        }
    )
    '''
    st.code(code, language="python")

    st.subheader("II. Rendering the 3D-scatter plot")

    st.text("Now, let's visualize both urban population and population density together using a 3D scatter plot:")

    figure = px.scatter_3d(first_hypothesis, x="Population density", y="Urban population", z="Year", 
                       color="Year", size="Urban population")

    figure.update_layout(title="Growth in population density", 
                    scene=dict(xaxis_title='Population density',
                               yaxis_title='Urban population',
                               zaxis_title='Year'))
    
    st.write(figure)

    st.text("It's evident that larger urban populations are associated with higher population densities in China.")

    st.subheader("III. First hypothesis conclusion")

    st.text("As expected, we see a strong relationship between urban population and population density, indicating that larger cities are more crowded.")


categories = st.selectbox("Select content to show", ["General population analysis", "Urban/Rural population analisys", "Hypothesis"])

if categories == "General population analysis":
    general_population_analysis()
elif categories == "Urban/Rural population analisys":
    urban_rural_population_analysis()
else:
    first_hypothesis()
