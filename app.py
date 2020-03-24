import pathlib
import dash
import numpy as np
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
    return datetime.strptime(time, "%Y-%m-%d")

#
#
#

# Retrieve relative folder and load data
PATH = pathlib.Path(__file__).parent

indf = pd.read_csv(PATH.joinpath("data\income_data.csv"), low_memory=False)
#indf["Due Date"] = indf["Due Date"].apply(convert_to_dt)

expdf = pd.read_csv(PATH.joinpath("data\expense_data.csv"), low_memory=False)
expdf = expdf.rename({'date': 'Due Date', 'money spent': 'Money Paid'}, axis=1)
#expdf["Due Date"] = expdf["Due Date"].apply(convert_to_dt)
expdf["Money Paid"] = 0 - expdf["Money Paid"]

df = indf[['Due Date', 'Money Paid']].copy()
df = df.append(expdf[['Due Date', 'Money Paid']].copy())
df["Due Date"] = pd.to_datetime(df["Due Date"])
df = df.sort_values(by="Due Date")
df.fillna(0)
df = df.rename({'Due Date': 'DATE'}, axis=1)


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
                            "Filter by Date:",
                            className="control_label",
                            style={'margin-bottom':'15px'}
                        ),
                        dcc.RangeSlider(
                            id="date-slider",
                            min=unix_time_secs(datetime(2019,11,1)),
                            max=unix_time_secs(max(df["DATE"])),
                            value=[unix_time_secs(yearwrap(NOW,0,-4)),
                                    unix_time_secs(NOW)],
                            allowCross=False,
                            #updatemode='drag',
                            className="dcc_control",
                        ),
                        html.Div(
                            id="output-date-slider",
                            style={'margin-left':'25px',
                                    'margin-bottom':'10px'},
                        ),
                        html.P(
                            "Date Range for Weekly/Daily Graphs:",
                            className="control_label",
                            style={'margin-bottom':'10px'}
                        ),
                        dcc.DatePickerRange(
                            id="date-picker-range",
                            min_date_allowed=datetime(2019,11,1),
                            max_date_allowed=max(df["DATE"]),
                            #initial_visible_month=datetime.now(),
                            start_date_placeholder_text="Start Period",
                            end_date_placeholder_text="End Period",
                            start_date=datetime.now() - timedelta(days=14),
                            end_date=datetime.now()
                        )
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
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="fcf_lineplot_weekly")],
                    className="pretty_container six columns",
                    id="weeklyGraphContainer",
                ),
                html.Div(
                    [dcc.Graph(id="fcf_lineplot_daily")],
                    className="pretty_container six columns",
                    id="dailyGraphContainer",
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


def filter_dataframe_wd(df, start, end):
    dff = df[
        (df["DATE"] >= datetime(start.year, start.month, start.day)) &
        (df["DATE"] < datetime(end.year, end.month, end.day))
    ]
    dff = dff.reset_index(drop=True)
    return dff


def filter_dataframe_month(df, date_slider):
    date1 = EPOCH + timedelta(seconds=date_slider[0])
    date2 = EPOCH + timedelta(seconds=date_slider[1])
    date1 = yearwrap(date1,0,0)
    date2 = yearwrap(date2,0,1)
    return filter_dataframe_wd(df, date1, date2)


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
    # Data set-up
    dff = filter_dataframe_month(df, date_slider)
    month_range = pd.Series(pd.date_range(yearwrap(dff["DATE"][0],0,0),yearwrap(dff["DATE"][len(dff)-1],0,0),freq='MS')).tolist()
    month_range_vis = pd.date_range(dff["DATE"][0],dff["DATE"][len(dff)-1],freq='MS').strftime("%b %Y").tolist()

    # Set up data for y axes
    income = [0 for i in range(len(month_range))]
    expense = [0 for i in range(len(month_range))]
    for i in range(len(month_range)):
        tempdf = filter_dataframe_wd(dff, month_range[i],
                            yearwrap(month_range[i],0,1))
        income[i] = sum(tempdf[tempdf["Money Paid"] > 0]["Money Paid"])
        expense[i] = sum(tempdf[tempdf["Money Paid"] < 0]["Money Paid"])

    # Create figure
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=month_range_vis,
            y=(np.array(income) + np.array(expense)).tolist(),
            mode="lines+markers",
            name="Free Cash Flow",
            marker_color="black"
        ))
    fig.add_trace(
        go.Bar(
            x=month_range_vis,
            y=expense,
            name="Expenses",
        ))
    fig.add_trace(
        go.Bar(
            x=month_range_vis,
            y=income,
            name="Income",
        ))
    fig.update_layout(
            title="Free Cash Flow by Month",
            yaxis_title="USD",
            barmode='relative',
            hovermode='x',
            autosize=True
    )
    return fig


@app.callback(
    Output('fcf_lineplot_weekly', 'figure'),
    [
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date')
    ]
)
def create_fcf_weekly(start_date, end_date):

    # Data set-up
    start_date = datetime.strptime(start_date.split('T')[0], '%Y-%m-%d')
    end_date = datetime.strptime(end_date.split('T')[0], '%Y-%m-%d')
    dff = filter_dataframe_wd(df, start_date, end_date)
    week_range = pd.Series(pd.date_range(start_date,end_date,freq='W')).tolist()
    week_range_vis = pd.date_range(start_date,end_date,freq='W').strftime("%b %d").tolist()
    for i in range(len(week_range)):
        week_range_vis[i] = week_range_vis[i] + " - " + pd.period_range(week_range[i],freq='W',periods=2).strftime("%b %d, %Y").tolist()[1]

    # Set up data for y axes
    income = [0 for i in range(len(week_range))]
    expense = [0 for i in range(len(week_range))]
    for i in range(len(week_range)):
        tempdf = filter_dataframe_wd(dff, week_range[i],
                        pd.Series(pd.period_range(week_range[i],freq='W',periods=2)).tolist()[1])
        income[i] = sum(tempdf[tempdf["Money Paid"] > 0]["Money Paid"])
        expense[i] = sum(tempdf[tempdf["Money Paid"] < 0]["Money Paid"])

    # Create figure
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=week_range_vis,
            y=(np.array(income) + np.array(expense)).tolist(),
            name="Free Cash Flow",
            marker_color="black"
        ))
    fig.add_trace(
        go.Bar(
            x=week_range_vis,
            y=expense,
            name="Expenses",
        ))
    fig.add_trace(
        go.Bar(
            x=week_range_vis,
            y=income,
            name="Income",
        ))
    fig.update_layout(
            title="Free Cash Flow by Week - only includes selected days",
            yaxis_title="USD",
            barmode='relative',
            hovermode='x',
            autosize=True
    )
    return fig


@app.callback(
    Output('fcf_lineplot_daily', 'figure'),
    [
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date')
    ]
)
def create_fcf_daily(start_date, end_date):

    # Data set-up
    start_date = datetime.strptime(start_date.split('T')[0], '%Y-%m-%d')
    end_date = datetime.strptime(end_date.split('T')[0], '%Y-%m-%d')
    dff = filter_dataframe_wd(df, start_date, end_date+timedelta(days=1))
    day_range = pd.Series(pd.date_range(start_date,end_date,freq='D')).tolist()
    day_range_vis = pd.date_range(start_date,end_date,freq='D').strftime("%b %d, %Y").tolist()

    # Set up data for y axes
    income = [0 for i in range(len(day_range))]
    expense = [0 for i in range(len(day_range))]
    for i in range(len(day_range)):
        tempdf = filter_dataframe_wd(dff, day_range[i],
                            day_range[i] + timedelta(days=1))
        income[i] = sum(tempdf[tempdf["Money Paid"] > 0]["Money Paid"])
        expense[i] = sum(tempdf[tempdf["Money Paid"] < 0]["Money Paid"])

    # Create figure
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=day_range_vis,
            y=(np.array(income) + np.array(expense)).tolist(),
            name="Free Cash Flow",
            marker_color="black"
        ))
    fig.add_trace(
        go.Bar(
            x=day_range_vis,
            y=expense,
            name="Expenses",
        ))
    fig.add_trace(
        go.Bar(
            x=day_range_vis,
            y=income,
            name="Income",
        ))
    fig.update_layout(
            title="Free Cash Flow by Day",
            yaxis_title="USD",
            barmode='relative',
            hovermode='x',
            autosize=True
    )
    return fig


# Run app
if __name__ == "__main__":
    app.run_server(debug=True)
