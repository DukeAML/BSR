import pathlib
import dash
from datetime import datetime, timedelta
import pandas as pd
from dash.dependencies import Input, Output, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objs as go

# Stuff that will likely be moved to a seperate file
#
#
SLIDER_FORMAT = "%B %Y"
NOW = datetime.now()
EPOCH = datetime.utcfromtimestamp(0)

def unix_time_secs(dt):
    """Returns seconds since 1970 to dt
    """
    return (dt - EPOCH).total_seconds()

def yearwrap(time, add_years, add_months=0, daybool=False):
    """Returns datetime with modified date based on add_years and add_months,
    add_months should not exceed fall outside range of [-11,11]
    """
    if (time.month+add_months > 12):
        add_years += 1
        add_months = add_months - 12
    elif (time.month+add_months < 1):
        add_years -= 1
        add_months = add_months + 12
    if(daybool): return datetime(time.year+add_years,
                                    time.month+add_months,time.day)
    return datetime(time.year+add_years,time.month+add_months,1)

def convert_to_dt(time):
    """Converts passed time of MM/DD/YY to datetime object
    """
    return datetime.strptime(time, "%m/%d/%Y")

#
#
#

# Retrieve relative folder and load data
PATH = pathlib.Path(__file__).parent
df = pd.read_csv(PATH.joinpath("fakedata.csv"), low_memory=False)
df["DATE"] = df["DATE"].apply(convert_to_dt)
df = df.sort_values(by="DATE")


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
                    [], # TODO: Make time range slider ??
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
                    [
                        html.P(
                            "Filter by date:",
                            className="control_label",
                            style={'margin-bottom':'15px'}
                        ),
                        dcc.RangeSlider(
                            id="date-slider",
                            min=unix_time_secs(datetime(2017,1,1)),
                            max=unix_time_secs(yearwrap(NOW,1)),
                            value=[unix_time_secs(yearwrap(NOW,0,-6)),
                                    unix_time_secs(yearwrap(NOW,0,6))],
                            allowCross=False,
                            #updatemode='drag',
                            className="dcc_control",
                        ),
                        html.Div(
                            id="output-date-slider",
                            style={'margin-left':'25px'},
                        ),
                    ],
                    className="pretty_container four columns",
                    id="filter-options",
                ),
                html.Div(
                    [
                        html.Div(
                            [dcc.Graph(id="fcf_lineplot")],
                            className="pretty_container",
                            id="fcfGraphContainer",
                        ),
                    ],
                    className="eight columns",
                    id="right-column",
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


def filter_dataframe_month(df, date_slider):
    date1 = EPOCH + timedelta(seconds=date_slider[0])
    date2 = EPOCH + timedelta(seconds=date_slider[1])
    dff = df[
        (df["DATE"] >= datetime(date1.year, date1.month, 1)) &
        (df["DATE"] < datetime(date2.year, date2.month+1,1))
    ]
    dff = dff.reset_index(drop=True)
    return dff


# Create callbacks
app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="resize"),
    Output("output-clientside", "children"),
    [Input("fcf_lineplot", "figure")],
)

@app.callback(
    Output('output-date-slider', 'children'),
    [Input('date-slider', 'value')]
)
def update_output(value):
    date1 = EPOCH + timedelta(seconds=value[0])
    date2 = EPOCH + timedelta(seconds=value[1])
    str1 = date1.strftime(SLIDER_FORMAT)
    str2 = date2.strftime(SLIDER_FORMAT)
    return "{} - {}".format(str1, str2)


@app.callback(
    Output('fcf_lineplot', 'figure'),
    [
        Input('date-slider', 'value')
        #Input('none', 'children')
    ]
)
def create_fcf_lineplot(date_slider):
    dff = filter_dataframe_month(df, date_slider)
    month_range = pd.date_range(dff["DATE"][0],dff["DATE"][len(dff)-1],freq='MS').strftime("%b %y").tolist()
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=month_range,
            y=(df["INCOME"] - df["EXPENSES"]).tolist(),
            name="Free Cash Flow",
            marker_color="black"
        ))
    fig.add_trace(
        go.Bar(
            x=month_range,
            y=df["INCOME"].tolist(),
            name="Income",
        ))
    fig.add_trace(
        go.Bar(
            x=month_range,
            y=(0 - df["EXPENSES"]).tolist(),
            name="Expenses",
        ))
    fig.update_layout(
            title="Free Cash Flow by Month",
            yaxis_title="USD",
            barmode='relative',
            autosize=True
    )
    return fig


# Run app
if __name__ == "__main__":
    app.run_server(debug=True)
