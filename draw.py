import plotly.express as px


def px_draw(
    df,
    x_axis,
    y_axis,
    st,
    graph_type="hist",
    color=None,
    nbins=None,
    width=500,
    height=400,
):
    if graph_type == "hist":
        fig = px.histogram(df, x=x_axis, color=color, nbins=nbins)
    elif graph_type == "scatter":
        fig = px.scatter(df, x=x_axis, y=y_axis, color=color)
    fig.update_layout(
        title={"text": graph_type, "x": 0.5, "xanchor": "center", "font": {"size": 20}},
        xaxis_title=x_axis,
        yaxis_title=y_axis,
        width=width,
        height=height,
    )
    st.plotly_chart(fig)
