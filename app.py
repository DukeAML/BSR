import pathlib
import dash
from dash.dependencies import Input, Output, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px


# Initialize app
app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server


# Create app layout
app.layout = html.Div(
    [
        # Empty div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("daml_logo.png"),
                            id="daml-image",
                            style={
                                "height": "60px",
                                "width": "auto",
                                "margin-bottom": "25px",
                                "margin-right": "15px"
                            },
                        ),
                        html.Img(
                            src=app.get_asset_url("bsr_logo.png"),
                            id="bsr-image",
                            style={
                                "height": "60px",
                                "width": "auto",
                                "margin-bottom": "25px",
                            },
                        )
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "Big Spoon Roasters",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5(
                                    "Data Insights Overview", style={"margin-top": "0px"}
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
                html.Div(
                    [], # TODO: Make time range slider
                    className="one-third column",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="fcf_lineplot")],
                    className="pretty_container twelve columns"
                ),
            ],
            className="row flex-display"
        ),

        # temp div for none input for temp. display of graph e.g. placeholder
        html.Div(id='none',children=[],style={'display':'none'}),

    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)

# Create callbacks
app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="resize"),
    Output("output-clientside", "children"),
    [Input("fcf_lineplot", "figure")],
)

@app.callback(
    Output('fcf_lineplot', 'figure'),
    [
        #Input('time_range', 'value')
        Input('none', 'children')
    ]
)
def create_fcf_lineplot(none):
    df = px.data.gapminder().query("continent=='Oceania'")
    fig = px.line(df, x="year", y="lifeExp", color='country')
    fig.update_layout(autosize=True)
    return fig


# Run app
if __name__ == "__main__":
    app.run_server(debug=True)
