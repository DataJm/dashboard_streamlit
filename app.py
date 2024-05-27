import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def create_pie_chart(data, labels, title):
    """
    Creates and displays a pie chart using the provided data and labels.
    
    Parameters:
    data (list of float): Values for the pie chart.
    labels (list of str): Labels for the pie chart segments.
    """
    fig, ax = plt.subplots()
    ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.set_title(title)
    st.pyplot(fig)


def create_bar_chart(data, labels, title):
    """
    Creates and displays a bar chart using the provided data and labels.
    
    Parameters:
    data (list of float): Values for the bar chart.
    labels (list of str): Labels for the bar chart.
    title (str): Title for the bar chart.
    """
    fig, ax = plt.subplots()
    ax.bar(labels, data)
    ax.set_title(title)
    ax.set_xlabel('Categorías')
    ax.set_ylabel('Valores')   
    st.pyplot(fig)


def create_horizontal_bar_chart(data, labels, title):
    """
    Creates and displays a horizontal bar chart using the provided data and labels.
    
    Parameters:
    data (list of float): Values for the bar chart.
    labels (list of str): Labels for the bar chart.
    title (str): Title for the bar chart.
    """
    fig, ax = plt.subplots()
    bars = ax.barh(labels, data)
    
    # Add value labels on the bars
    for bar in bars:
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height() / 2, f'{width:.0f}', 
                va='center', ha='left', color='black')
    ax.set_title(title)
    ax.set_xlabel('Values')
    ax.set_ylabel('Categories')
    
    st.pyplot(fig)


def filtrar_df(df, gender, economic_level):
    if gender!="Todos":
        df = df[df["genero"]==gender]
    if economic_level!="Todos":
        df = df[df["nse"]==economic_level]

    return df

def gender_pie(df):
    data = df.groupby("genero").agg(valores = ("id","nunique")).assign(pct = lambda x: round(x["valores"] / x["valores"].sum()*100, 0))
    create_pie_chart(data["pct"], data.index, "Género")

def nse_bar(df):
    data = df.groupby("nse").agg(valores = ("id","nunique")).assign(pct = lambda x: round(x["valores"] / x["valores"].sum()*100, 0))
    create_bar_chart(data["pct"], data.index, "NSE") 

def credito_contado_pie(df):
    data = df.groupby("p3_credito_contado").agg(valores = ("id","nunique")).assign(pct = lambda x: round(x["valores"] / x["valores"].sum()*100, 0))
    create_bar_chart(data["pct"], data.index, "Crédito o Contado") 

def articulos_barras(df):
    data = (df.groupby("p1_compra").agg(valores = ("id","nunique")).assign(pct = lambda x: round(x["valores"] / df["id"].nunique()*100, 0)).sort_values(by="valores", ascending=False))
    data = data.head(10).sort_values(by="valores", ascending=True)
    create_horizontal_bar_chart(data["pct"], data.index, "Distribución de artículos comprados")

def tiendas_barras(df):
    data = df.groupby("p3_tienda").agg(valores = ("id","nunique")).assign(pct = lambda x: round(x["valores"] / df["id"].nunique()*1000, 0)).sort_values(by="valores", ascending=False)
    data = data.head(5).sort_values(by="valores", ascending=True)
    create_horizontal_bar_chart(data["pct"], data.index, "Distribución de tiendas")
   
def bancos_barras(df):
    data = df.groupby("p3_4banco").agg(valores = ("id","nunique")).assign(pct = lambda x: round(x["valores"] / df["id"].nunique()*100, 0)).sort_values(by="valores", ascending=False)
    data = data.head(10).sort_values(by="valores", ascending=True)
    create_horizontal_bar_chart(data["pct"], data.index, "Distribución de bancos")

def main():
    df = pd.read_excel("./data_final.xlsx")
    st.title('Filtros')

    # Create columns for filters
    col1, col2, col3, col4 = st.columns(4)
    
    # Gender selection
    with col1:
        gender = st.selectbox('Género:', ['Todos','Hombre', 'Mujer'])
    with col2:
        economic_level = st.selectbox('NSE', ['Todos','C+', 'C', 'C-']) 

    # Filtrado
    df = filtrar_df(df, gender, economic_level)

    with col3:
        st.metric("Tamaño de base", df["id"].nunique())
    with col3:
        st.metric("Total de compras", df["p1_compra"].count())

    st.title('Resultados')
    # Graficado
    viz1, viz2 = st.columns(2)
    with viz1:
        gender_pie(df)

    with viz2:
        nse_bar(df)

    wiz1, wiz2 = st.columns(2)

    with wiz1:
        articulos_barras(df)

    with wiz2:
        tiendas_barras(df)

    ziz1, ziz2 = st.columns(2)

    with ziz1:
        credito_contado_pie(df)

    with ziz2:
        bancos_barras(df)

if __name__ == "__main__":
    main()