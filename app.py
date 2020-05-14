# base app imports
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

# predict app imports
import predictsales as predict
import fbprophet
from scipy.stats import boxcox
from scipy.special import inv_boxcox

# import data management and instantiation tools
from data.retrievedata import read_in_IDtoSKU, append_list_as_row #BUG: think this is outputting a list in cmd terminal?
from data.retrievedata import apiCall as pullSKU


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

def update_sku_mapper(productids, mapper):
    """Update SKU mapper to ensure no products are left out
    """
    mapkeys = [int(x) for x in mapper.keys()]
    if (not set(productids).issubset(set(mapkeys))):
        print("Data Missing from SKU Mapper, updating...")
        missing_ids = []
        missing_skus = []
        for num_id in productids:
            if str(num_id) in mapper.keys(): continue
            missing_ids.append(num_id)
            data = pullSKU(str(num_id))
            if 'variant' in data: sku = data['variant']['sku']
            else:
                sku = "missing"
                print(str(num_id))
                print(data)
            missing_skus.append(sku)
            append_list_as_row('data\sold_id_to_sku.csv', [num_id, sku])

#
#
#

# Retrieve relative folder and load data
PATH = pathlib.Path(__file__).parent

# Set up data for free cash flow
indf = pd.read_csv(PATH.joinpath("data\order_data.csv"), low_memory=False)
expdf = pd.read_csv(PATH.joinpath("data\expense_data.csv"), low_memory=False)
expdf = expdf.rename({'date': 'Due Date', 'money spent': 'Money Paid'}, axis=1)
expdf["Money Paid"] = 0 - expdf["Money Paid"]

df = indf[['Due Date', 'Money Paid']].copy()
df = df.append(expdf[['Due Date', 'Money Paid']].copy())
df["Due Date"] = pd.to_datetime(df["Due Date"])
df = df.sort_values(by="Due Date")
df.fillna(0)
df = df.rename({'Due Date': 'DATE'}, axis=1)

# Set up data for forecasting
predictdf = predict.retrievedata()
productsales = predict.createproductdict(predictdf)
productpredictions = dict()


# Update all data
update_sku_mapper(list(productsales.keys()),
                  read_in_IDtoSKU(csvname="sold_id_to_sku.csv"))


# Create controls
PRODUCT_SKU = read_in_IDtoSKU(csvname="sold_id_to_sku.csv")
products_options = [
    {"label": str(sku), "value": int(id_num)}
    for id_num, sku in PRODUCT_SKU.items()
]


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
                        ),
                        html.P(
                            "Filter Selected Products:",
                            className="control_label",
                            style={'margin-bottom':'10px'},
                        ),
                        dcc.RadioItems(
                            id="products_selector",
                            options=[
                                {'label': "Customize ", "value": "custom"},
                                {'label': "All ", "value": "all"},
                            ],
                            value="custom",
                            labelStyle={"display": "inline-block"},
                            className="dcc_control",
                        ),
                        dcc.Dropdown(
                            id="products_chosen",
                            options=products_options,
                            multi=True,
                            value=list(productsales.keys()),
                            className="dcc_control",
                        ),
                        html.P(
                            "Growth Rate Adjustment (%):",
                            className="control_label",
                            style={'margin-bottom':'10px'},
                        ),
                        dcc.Input(
                            id="growth_percentage",
                            min=0,
                            value=100,
                            debounce=True,
                            type='number',
                            className='dcc_control',
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
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="predict_product")],
                    className="pretty_container twelve columns",
                    id="predictGraphContainer",
                ),
            ],
            className="row flex-display"
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="product_table")],
                    className="pretty_container six columns",
                    id="ptableGraphContainer",
                ),
                html.Div(
                    [dcc.Graph(id="ingredient_table")],
                    className="pretty_container six columns",
                    id="itableGraphContainer",
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
    [Input("fcf_lineplot", "figure"), Input("fcf_lineplot_weekly", "figure"),
    Input("fcf_lineplot_daily", "figure"), Input("predict_product", "figure"),
    Input("product_table", "figure"), Input("ingredient_table", "figure")],
)


@app.callback(
    Output("products_chosen", "value"),
    [Input("products_selector", "value")]
)
def display_products(selector):
    if selector=="all":
        return list(PRODUCT_SKU.keys())
    return []


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
    Output('ingredient_table', 'figure'),
    [
        Input('products_chosen', 'value'),
        Input('growth_percentage', 'value')
        #Input('none', 'children')
    ]
)
def create_ingredient_table(products_chosen, growth_adjustment):

    fdf = pd.DataFrame(np.random.randn(len(productsales.keys()),3),
                        columns=["made", "ordered", "needed"],
                        index=productsales.keys())

    layout = go.Layout(
        title="Selected Ingredients Information",
        autosize=True,
    )

    fig = go.Figure(data=[go.Table(
    header=dict(values=["Ingredient", "Quantity<br>Made",
                "Quantity<br>Ordered", "Quantity<br>Needed"],
                #fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[fdf.index, fdf.made, fdf.ordered, fdf.needed],
               #fill_color='lavender',
               align='left'))
    ], layout=layout)

    return fig


@app.callback(
    Output('product_table', 'figure'),
    [
        Input('products_chosen', 'value'),
        Input('growth_percentage', 'value')
        #Input('none', 'children')
    ]
)
def create_product_table(products_chosen, growth_adjustment):

    fdf = pd.DataFrame(np.random.randn(len(productsales.keys()),3),
                        columns=["made", "ordered", "needed"],
                        index=productsales.keys())
    fdf = fdf.loc[products_chosen].copy()

    layout = go.Layout(
        title="Selected Products Information",
        autosize=True,
    )

    fig = go.Figure(data=[go.Table(
    header=dict(values=["Product", "Quantity<br>Made",
                "Quantity<br>Ordered", "Quantity<br>Needed"],
                #fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[fdf.index, fdf.made, fdf.ordered, fdf.needed],
               #fill_color='lavender',
               align='left'))
    ], layout=layout)

    return fig


@app.callback(
    Output('predict_product', 'figure'),
    [
        Input('products_chosen', 'value'),
        Input('growth_percentage', 'value')
        #Input('none', 'children')
    ]
)
def create_predict_product(products_chosen, growth_adjustment):
    if(len(products_chosen)==0): return go.Figure()
    start = '2019-12-01'
    end = '2020-04-02'

    # Create loop over each chosen product to conduct forecasting
    aggregate_df = pd.DataFrame()
    for product_id in products_chosen:

        # If product forecast has already been made, retrieve from dictionary
        if (product_id in productpredictions):
            forecast_data_orig = productpredictions[product_id]

            # Create aggregate df for graph
            cols = list(forecast_data_orig.columns)
            cols.remove('ds')
            if(aggregate_df.empty): aggregate_df = forecast_data_orig.copy()
            else: aggregate_df[cols] =  aggregate_df[cols]\
                            .add(forecast_data_orig[cols], fill_value=0)
            continue


        # Set up data
        gm = productsales[product_id].copy()['2019-12-1':'2020-04-2']
        gm['Date'] = gm.index
        gm = gm.rename(columns={'Date': 'ds', 'Amount': 'y'})

        # Remove noise by finding optimal transformation and applying to data.
        # If product has no existing purchases, skip it
        try:
            gm['y_orig'] = gm['y']
            gm['y'], lam = boxcox(gm['y'].replace(0,1))
        except:
            print("Zero Sales for Product ID:", product_id)
            continue

        # Create time series model and fit
        gm_prophet = fbprophet.Prophet(changepoint_prior_scale=0.15, interval_width=0.8)
        gm_prophet.fit(gm)

        # Create forecast on transformed data
        gm_forecast = gm_prophet.make_future_dataframe(periods=int(30*1.5), freq='D')
        gm_forecast = gm_prophet.predict(gm_forecast)

        # Apply inverse of transform to forecast to get actual results
        forecast_data_orig = gm_forecast # make sure we save the original forecast data
        # Apply inverse Box-Cox transform to specific forecast columns
        forecast_data_orig[['yhat','yhat_upper','yhat_lower']] = forecast_data_orig[['yhat','yhat_upper','yhat_lower']].apply(lambda x: inv_boxcox(x, lam))
        gm['y_transformed'] = gm['y']
        gm['y'] = gm['y_orig']

        # Add prediction data to product dictionary to reduce load time in future
        forecast_data_orig['y'] = np.nan
        forecast_data_orig['y'][:len(gm)] = gm['y'].copy()
        productpredictions[product_id] = forecast_data_orig.copy()

        # Create aggregate df for graph
        cols = list(forecast_data_orig.columns)
        cols.remove('ds')
        if(aggregate_df.empty): aggregate_df = forecast_data_orig.copy()
        else: aggregate_df[cols] =  aggregate_df[cols]\
                        .add(forecast_data_orig[cols], fill_value=0)

    if(aggregate_df.empty):
        fig = go.Figure()
        fig.update_layout(title="No Sales Recorded for Selected Product(s)")
        return fig
    # Adjust overall data for growth rate input
    aggregate_df[['yhat','yhat_upper','yhat_lower']] = aggregate_df[['yhat','yhat_upper','yhat_lower']].apply(lambda x: x*(growth_adjustment/100))

    # Plot original data
    upper_bound = go.Scatter(
        name="Upper Bound",
        x=aggregate_df['ds'],
        y=aggregate_df['yhat_upper'],
        mode='lines',
        marker=dict(color="#444"),
        line=dict(width=0),
        fillcolor='rgba(68, 68, 68, 0.3)',
        fill='tonexty',
    )

    trace = go.Scatter(
        name="Prediction",
        x=aggregate_df['ds'],
        y=aggregate_df['yhat'],
        mode='lines',
        marker=dict(color="rgb(31, 119, 180)"),
        fillcolor='rgba(68, 68, 68, 0.3)',
        fill='tonexty',
    )

    lower_bound = go.Scatter(
        name="Lower Bound",
        x=aggregate_df['ds'],
        y=aggregate_df['yhat_lower'],
        mode='lines',
        marker=dict(color="#444"),
        line=dict(width=0),
    )

    data = [lower_bound, trace, upper_bound]

    layout = go.Layout(
        title="Selected Products Forecasting",
        yaxis_title="Amount of Product Sold",
        hovermode='x',
        autosize=True,
    )

    fig = go.Figure(data=data, layout=layout)

    fig.add_trace(
        go.Scatter(
            name="Actual Count",
            x=aggregate_df['ds'],
            y=aggregate_df['y'],
            mode='markers',
            marker_color='black',
            marker_size=3,
        ))

    fig.update_xaxes(
    #rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=3, label="3m", step="month", stepmode="backward"),
            #dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            #dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
            ]),
        ),
    range=[datetime.now() - timedelta(days=60),
                datetime.now() + timedelta(days=30)],
    )

    return fig


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
            autosize=True,
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
