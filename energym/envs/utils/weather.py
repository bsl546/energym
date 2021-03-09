import pandas as pd
import csv
import random
import math
import logging

logger = logging.getLogger(__name__)

default_keys = ["Dry Bulb Temperature", "Direct Normal Radiation"]
translate_dictionary_Eplus = {
    "Dry Bulb Temperature Prediction": "Ext_T",
    "Direct Normal Radiation Prediction": "Ext_Irr",
}


class Weather:
    """Base class for handling weather files.

    The encapsulated weather file can be used for forecast generation.
    The logic is taken from https://github.com/building-energy/epw.

    Attributes
    ----------
    headers : dict
        A dictionary containing the header rows of the weather file.
    dataframe : pd.Dataframe
        Stores the weather data.
    names : list of str
        List of observed weather indicators.
    delimiter : str
        Separation character in the file.

    Methods
    -------
    read(fp)
        Reads a weather file.
    close()
        Closes the data of the current weather file.
    """

    def __init__(self, names, delimiter):
        """
        Parameters
        ----------
        names : list of str
            List of observed weather indicators.
        delimiter : str
            Separation character in the file.
        """
        self.headers = {}
        self.dataframe = pd.DataFrame()
        self.names = names
        self.delimiter = delimiter

    def read(
        self,
        fp,
        generate_forecasts=True,
        generate_forecast_method="perfect",
        generate_forecast_keys=None,
    ):
        """Reads a weather file. Generates associated forecasts if asked

        Parameters
        ----------
        fp : str
            The path to the file.
        generate_forecasts: bool, optional
            If True, generate forecasts dataframe
        generate_forecast_method: {'stochastic', 'perfect', 'persistence'}, optional
            If 'stochastic', generate random forecast, If 'perfect', use actual weather as forecast.
            If 'persistence', persitence forecast from previous day
        generate_forecast_keys: list, optional
            List of keys to generate forecast for. By default is ["Dry Bulb Temperature", "Global Horizontal Radiation"]
        """
        self.headers = self._read_headers(fp)
        self.dataframe = self._read_data(fp)
        if generate_forecast_keys is None:
            generate_forecast_keys = default_keys
        if generate_forecasts:
            self.prediction_df = self._get_prediction_df(
                generate_forecast_keys, generate_forecast_method
            )
            self.forecast_keys = [
                k + " Prediction" for k in generate_forecast_keys
            ]

    def _read_headers(self, fp):
        """Reads the headers of a weather file.

        Parameters
        ----------
        fp : str
            The path to the file.

        Returns
        -------
        d : dict
            A dictionary containing the header rows.
        """
        d = {}
        with open(fp, newline="") as csvfile:
            csvreader = csv.reader(
                csvfile, delimiter=self.delimiter, quotechar='"'
            )
            for row in csvreader:
                if row[0].replace(".", "", 1).isdigit():
                    break
                else:
                    d[row[0]] = row[1:]
        return d

    def _read_data(self, fp):
        """Reads the climate data of a weather file.

        Parameters
        ----------
        fp : str
            The path to the file.

        Returns
        -------
        df : pd.DataFrame
            A DataFrame containing the climate data.
        """
        first_row = self._first_row_with_climate_data(fp)
        with open(fp, newline="") as csvfile:
            df = pd.read_csv(
                csvfile,
                delimiter=self.delimiter,
                skiprows=first_row,
                header=None,
                names=self.names,
                index_col=False,
            )
        return df

    def _first_row_with_climate_data(self, fp):
        """Finds the first row with the climate data of a weather file.

        Parameters
        ----------
        fp : str
            The path to the file.

        Returns
        -------
        i : int
            The row number.
        """
        with open(fp, newline="") as csvfile:
            csvreader = csv.reader(
                csvfile, delimiter=self.delimiter, quotechar='"'
            )
            for i, row in enumerate(csvreader):
                if row[0].replace(".", "", 1).isdigit():
                    break
        return i

    def _get_extrema(self, key):
        extr = self.dataframe.copy()
        extr["min"] = self.dataframe[key][
            (self.dataframe[key].shift(1) > self.dataframe[key])
            & (self.dataframe[key].shift(-1) > self.dataframe[key])
        ]
        extr["max"] = self.dataframe[key][
            (self.dataframe[key].shift(1) < self.dataframe[key])
            & (self.dataframe[key].shift(-1) < self.dataframe[key])
        ]
        return extr

    def _generate_prediction_sequence(self, key):
        df = self._get_extrema(key)
        df[key + " Prediction"] = 0.0
        last_ind = 0
        last_rate = random.uniform(0.8, 1.2)
        new_ind = 0
        for ind in df.index:
            if not math.isnan(df["min"][ind]):
                new_ind = ind
            elif not math.isnan(df["max"][ind]):
                new_ind = ind
            if last_ind != new_ind:
                new_rate = random.uniform(0.85, 1.15)
                dist = new_ind - last_ind
                for interm in range(last_ind, new_ind):
                    df.loc[interm, (key + " Prediction",)] = df[key][
                        interm
                    ] * (
                        (new_ind - interm) / dist * last_rate
                        + (interm - last_ind) / dist * new_rate
                    )
                last_ind = new_ind
        new_ind = df.index[-1]
        new_rate = random.uniform(0.85, 1.15)
        df.loc[new_ind, (key + " Prediction",)] = (
            df[key][new_ind] * new_rate
        )
        dist = new_ind - last_ind
        for interm in range(last_ind, new_ind):
            df.loc[interm, (key + " Prediction",)] = df[key][interm] * (
                (new_ind - interm) / dist * last_rate
                + (interm - last_ind) / dist * new_rate
            )
        return df

    def close(self):
        """Closes the data of the current weather file."""
        self.dataframe = None
        self.headers = None


class EPW(Weather):
    """Class to represent an EnergyPlus weather (epw) file.

    Subclasses Weather and inherits its data handling functions.

    Methods
    -------
    get_forecast(hour, day, month, forecast_length)
        Provides a weather forecast for a requested length and requested keys.
    """

    def __init__(self):
        """"""
        names = [
            "Year",
            "Month",
            "Day",
            "Hour",
            "Minute",
            "Data Source and Uncertainty Flags",
            "Dry Bulb Temperature",
            "Dew Point Temperature",
            "Relative Humidity",
            "Atmospheric Station Pressure",
            "Extraterrestrial Horizontal Radiation",
            "Extraterrestrial Direct Normal Radiation",
            "Horizontal Infrared Radiation Intensity",
            "Global Horizontal Radiation",
            "Direct Normal Radiation",
            "Diffuse Horizontal Radiation",
            "Global Horizontal Illuminance",
            "Direct Normal Illuminance",
            "Diffuse Horizontal Illuminance",
            "Zenith Luminance",
            "Wind Direction",
            "Wind Speed",
            "Total Sky Cover",
            "Opaque Sky Cover (used if Horizontal IR Intensity missing)",
            "Visibility",
            "Ceiling Height",
            "Present Weather Observation",
            "Present Weather Codes",
            "Precipitable Water",
            "Aerosol Optical Depth",
            "Snow Depth",
            "Days Since Last Snowfall",
            "Albedo",
            "Liquid Precipitation Depth",
            "Liquid Precipitation Quantity",
        ]
        super().__init__(names, ",")

    def _get_prediction_df(self, keylist, method):
        df_list = [
            self.dataframe["Month"],
            self.dataframe["Day"],
            self.dataframe["Hour"],
        ]
        if method == "stochastic":
            for key in keylist:
                df = self._generate_prediction_sequence(key)
                df_list.append(df[key + " Prediction"])
            pred_df = pd.concat(df_list, axis=1)
        elif method == "perfect":
            pred_df = self.dataframe[
                ["Month", "Day", "Hour"] + keylist
            ].copy()
            pred_df.rename(
                columns={k: k + " Prediction" for k in keylist},
                inplace=True,
            )
        elif method == "persistence":
            raise NotImplementedError(
                "persistence forecast not yet implmented"
            )
        else:
            raise ValueError(
                "Method {} not defined for generating forecast".format(
                    method
                )
            )
        return pred_df

    def get_forecast(self, hour, day, month, forecast_length):
        """Provides a weather forecast for a requested length and requested keys.

        Parameters
        ----------
        hour : int
            Current hour.
        day : int
            Current day.
        month : int
            Current month.
        forecast_length : int
            Number of forecasted hours.

        Returns
        -------
        forecast : dict
            Containing a forecast of the requested length for the requested keys.

        Raises
        ------
        Exception
            If no weather file has been loaded.
        Exception
            If the weather file has a non-standard format.
        """
        change_ind = False
        if hour == 0:
            hour = 1
            change_ind = True

        length = len(self.prediction_df)
        if length == 0:
            raise Exception("No weather file")
        try:
            date_bool_array = (
                (self.prediction_df["Month"] == month)
                & (self.prediction_df["Day"] == day)
                & (self.prediction_df["Hour"] == hour)
            )
        except BaseException as e:
            logger.exception(f"Wrong weather file format. {e}")
        prediction_keys = self.forecast_keys
        index = [i for i, val in enumerate(date_bool_array) if val][0]
        if change_ind:
            if day > 1 or month > 1:
                index = index - 1
            else:
                index = length - 1
        if index + forecast_length > length:
            rest = forecast_length - length + index
            day_slice = pd.concat(
                [
                    self.prediction_df.iloc[index:length],
                    self.prediction_df.iloc[0:rest],
                ]
            ).to_dict()
        else:
            day_slice = self.prediction_df.iloc[
                index: index + forecast_length
            ].to_dict()
        del_keys = [
            key for key in day_slice if key not in prediction_keys
        ]
        for key in del_keys:
            del day_slice[key]
        for key in day_slice:
            day_slice[key] = list(day_slice[key].values())

        # Carry out translation to standard name so as to have same naming as FMU outputs
        forecast = {}
        for key in day_slice:
            if key in list(translate_dictionary_Eplus):
                forecast[translate_dictionary_Eplus[key]] = day_slice[key]
            else:
                forecast[key] = day_slice[key]
        return forecast


class MOS(Weather):
    """Class to represent a Modelica weather (mos) file.

    Subclasses Weather and inherits its data handling functions.

    Methods
    -------
    get_forecast(time, forecast_length)
        Provides a weather forecast for a requested length and requested keys.
    """

    def __init__(self):
        names = [
            "Time",
            "Dry Bulb Temperature",
            "Dew Point Temperature",
            "Relative Humidity",
            "Atmospheric Station Pressure",
            "Extraterrestrial Horizontal Radiation",
            "Extraterrestrial Direct Normal Radiation",
            "Horizontal Infrared Radiation Intensity",
            "Global Horizontal Radiation",
            "Direct Normal Radiation",
            "Diffuse Horizontal Radiation",
            "Global Horizontal Illuminance",
            "Direct Normal Illuminance",
            "Diffuse Horizontal Illuminance",
            "Zenith Luminance",
            "Wind Direction",
            "Wind Speed",
            "Total Sky Cover",
            "Opaque Sky Cover (used if Horizontal IR Intensity missing)",
            "Visibility",
            "Ceiling Height",
            "Present Weather Observation",
            "Present Weather Codes",
            "Precipitable Water",
            "Aerosol Optical Depth",
            "Snow Depth",
            "Days Since Last Snowfall",
            "Albedo",
            "Liquid Precipitation Depth",
            "Liquid Precipitation Quantity",
        ]
        super().__init__(names, "\t")

    def _read_headers(self, fp):
        """Reads the headers of a MOS weather file. Overrides parent method because headers are different from rest

        Parameters
        ----------
        fp : str
            The path to the file.

        Returns
        -------
        d1 : dict
            A dictionary containing the header rows.
        """
        d0 = super()._read_headers(fp)
        d1 = {}
        for k, v in d0.items():
            if k.startswith("#"):
                list_k = k.split(",")
                d1[list_k[0]] = list_k[1:]
            else:
                d1[k] = v
        return d1

    def read(
        self,
        fp,
        generate_forecasts=True,
        generate_forecast_method="perfect",
        generate_forecast_keys=None,
    ):
        """Reads a weather file from MOS.

        Overrides the read method of Weather.

        Parameters
        -----------
        fp : str
            The path to the file.
        """
        super().read(
            fp,
            generate_forecasts,
            generate_forecast_method,
            generate_forecast_keys,
        )
        self.prediction_df.index = self.prediction_df["Time"]
        self.dataframe.index = self.dataframe["Time"]

    def _get_prediction_df(self, keylist, method):
        df_list = [self.dataframe["Time"]]
        if method == "stochastic":
            for key in keylist:
                df = self._generate_prediction_sequence(key)
                df_list.append(df[key + " Prediction"])
            pred_df = pd.concat(df_list, axis=1)
        elif method == "perfect":
            pred_df = self.dataframe[["Time"] + keylist].copy()
            pred_df.rename(
                columns={k: k + " Prediction" for k in keylist},
                inplace=True,
            )
        elif method == "persistence":
            raise NotImplementedError(
                "persistence forecast not yet implemented"
            )
        else:
            raise ValueError(
                "Method {} not defined for generating forecast".format(
                    method
                )
            )
        return pred_df

    def get_forecast(self, time, forecast_length):
        """Returns a forecast for the next forecast_length hours.

        Parameters
        -----------
        time : int
            Start time of forecast
        forecast_length : int
            Forecast length in hours

        Returns
        -------
        forecast : dict
            Containing a forecast of the requested length for the requested keys.

        Raises
        ------
        Exception
            If no weather file has been loaded.
        """
        length = len(self.prediction_df)
        if length == 0:
            raise Exception("No weather file")
        prediction_keys = self.forecast_keys

        if time not in self.prediction_df.index:
            logger.warning(
                "Start of forecast is not in weather file index. using closest time"
            )
            time = self.prediction_df.index[
                (self.prediction_df["Time"] - time).abs().argsort()[0]
            ]

        forecast = self.prediction_df.loc[
            time : time + 3600 * (forecast_length - 1), prediction_keys
        ]

        return forecast.to_dict(orient="list")
