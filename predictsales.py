import pathlib
import json
import pandas as pd
import numpy as np
from datetime import datetime

import fbprophet
from fbprophet.diagnostics import cross_validation, performance_metrics
import plotly.offline as py
from scipy.stats import boxcox
from scipy.special import inv_boxcox

import plotly.express as px
import matplotlib.pyplot as plt


OLDEST_DATE = datetime(2019,11,1)


def retrievedata():
    """Retrieve relative folder and load data
    """
    PATH = pathlib.Path(__file__).parent
    df = pd.read_csv(PATH.joinpath("data\income_data.csv"))
    df["Due Date"] = pd.to_datetime(df["Due Date"])

    dff = df[(df["Due Date"] >= OLDEST_DATE) & (df["Due Date"] < datetime.now())]
    dff = dff.reset_index(drop=True)

    return dff


def createproductdict(df):
    """Scrapes data to return dictionary product:pandas dataframe with index of dates and value corresponding to sales for that product
    """
    productsales = dict()

    for index, row in df.iterrows():
        date = row["Due Date"]
        products = json.loads(row["Items"])

        if (row["Money Paid"]==0 and row["Pending Payment"]==0):
            continue

        for info in products:

            if (info[1] not in productsales):
                index = pd.date_range(OLDEST_DATE, datetime.now(), freq='D')
                tdf = pd.DataFrame(index=index, columns=["Amount"])
                tdf.index = tdf.index.normalize()
                tdf = tdf.fillna(0)
                productsales[info[1]] = tdf

            strdate = date.strftime("%Y-%m-%d")
            productsales[info[1]].loc[strdate] += info[3]

    return productsales


def pipeline_for_csv_pred(pid, df):

    # Pull and set up data
    gm = df.copy()['2019-12-1':'2020-04-2']
    gm['Date'] = gm.index
    gm = gm.rename(columns={'Date': 'ds', 'Amount': 'y'})

    # Remove noise by finding optimal transformation and applying to data
    try:
        gm['y_orig'] = gm['y']
        gm['y'], lam = boxcox(gm['y'].replace(0,1))
    except:
        return 0,0,0

    gm_prophet = fbprophet.Prophet(changepoint_prior_scale=0.15, interval_width=0.8)
    gm_prophet.fit(gm)

    # Create forecast on transformed data
    gm_forecast = gm_prophet.make_future_dataframe(periods=7*2, freq='D')
    gm_forecast = gm_prophet.predict(gm_forecast)

    # Apply inverse of transform to forecast to get actual results
    forecast_data_orig = gm_forecast # make sure we save the original forecast data
    # Apply inverse Box-Cox transform to specific forecast columns
    forecast_data_orig[['yhat','yhat_upper','yhat_lower']] = forecast_data_orig[['yhat','yhat_upper','yhat_lower']].apply(lambda x: inv_boxcox(x, lam))

    low = sum(forecast_data_orig[forecast_data_orig['ds'] > datetime(2020,4,2)]['yhat_lower'])
    high = sum(forecast_data_orig[forecast_data_orig['ds'] > datetime(2020,4,2)]['yhat_upper'])
    mid = sum(forecast_data_orig[forecast_data_orig['ds'] > datetime(2020,4,2)]['yhat'])
    return low, high, mid



def pipeline():
    """Pipeline for forecasting future sales
    """

    # Pull and set up data
    df = retrievedata()
    productsales = createproductdict(df)

    gm = productsales[161921].copy()['2019-12-1':'2020-04-2']
    gm['Date'] = gm.index
    gm = gm.rename(columns={'Date': 'ds', 'Amount': 'y'})


    # Remove noise by finding optimal transformation and applying to data
    try:
        gm['y_orig'] = gm['y']
        gm['y'], lam = boxcox(gm['y'].replace(0,1))
    except:
        return

    # Create time series model and fit
    gm_prophet = fbprophet.Prophet(changepoint_prior_scale=0.15, interval_width=0.8)
    gm_prophet.fit(gm)

    # Create forecast on transformed data
    gm_forecast = gm_prophet.make_future_dataframe(periods=30*2, freq='D')
    gm_forecast = gm_prophet.predict(gm_forecast)

    # Create figure with transformed data
    fig = fbprophet.plot.plot_plotly(gm_prophet, gm_forecast)
    fig.show()


    # Do cross-validation to create a set of error metrics, then apply transformation to cv results and display
    cv_results = cross_validation(gm_prophet, initial='13 days', horizon='6 days')
    cv_results[['yhat','yhat_upper','yhat_lower', 'y']] = cv_results[['yhat','yhat_upper','yhat_lower', 'y']].apply(lambda x: inv_boxcox(x, lam))
    results_metrics = performance_metrics(cv_results)
    print(results_metrics)


    # Apply inverse of transform to forecast to get actual results
    forecast_data_orig = gm_forecast # make sure we save the original forecast data
    # Apply inverse Box-Cox transform to specific forecast columns
    forecast_data_orig[['yhat','yhat_upper','yhat_lower']] = forecast_data_orig[['yhat','yhat_upper','yhat_lower']].apply(lambda x: inv_boxcox(x, lam))
    gm['y_transformed'] = gm['y']
    gm['y'] = gm['y_orig']

    # Create model using non-transformed data--needed to use fbprophet built-in plotting function
    gm_prophet = fbprophet.Prophet(changepoint_prior_scale=0.15, interval_width=0.8)
    gm_prophet.fit(gm)

    # Plot original data
    fig = fbprophet.plot.plot_plotly(gm_prophet, forecast_data_orig)
    #gm_prophet.plot(gm_forecast, xlabel='Date', ylabel='Number of Items')

    fig.show()
    print("\nscipy.stats.boxcox transformation lambda: {}".format(lam))

    fig = px.line(productsales[161921], x=range(len(productsales[161921])), y="Amount")
    fig.show()

    #figure = model.plot(forecast)
    #figure.savefig('output')

def main():
    df = retrievedata()
    productsales = createproductdict(df)

    outcsv = pd.DataFrame(index=productsales.keys(), columns=['yhat_lower', 'yhat_upper', 'yhat'])

    for pid in productsales.keys():
        entry = pipeline_for_csv_pred(pid, productsales[pid])
        outcsv.loc[pid] = entry
        print("Successfully integrated", pid)


    outcsv.to_csv('two-week-predictions.csv', index=True, header=True)


if __name__=="__main__":
    main()
