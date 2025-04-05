import pandas as pd
from datetime import datetime


class DataFrameTransformer:

    def fill_null_dates_with_today(
        self, dataframe: pd.DataFrame = None, date_col: str = None
    ) -> pd.DataFrame:
        """Replaces null (NaN) values in the specified date column with today's date.

        Args:
            dataframe (pd.DataFrame, optional): Dataframe to overwrite null dates in. Defaults to None.
            date_col (str, optional): Date column to check for nulls in. Defaults to None.

        Raises:
            ValueError: If the specified date_col is not found in the dataframe.

        Returns:
            pd.DataFrame: DataFrame with nulls in the date column replaced with today's date.
        """

        if date_col not in dataframe.columns:
            raise ValueError(f"The column '{date_col}' was not found in the dataframe.")

        dataframe[date_col] = pd.to_datetime(dataframe[date_col], errors="coerce")
        dataframe[date_col].fillna(pd.Timestamp(datetime.today()), inplace=True)

        return dataframe

    def set_date_columns_to_datetime(
        self, dataframe: pd.DataFrame, date_cols: list = []
    ) -> pd.DataFrame:
        """Harmonise date columns into type: datetime

        Args:
            dataframe (pd.DataFrame): DataFrame to process
            date_cols (list, optional): List of date column to set. Defaults to [].

        Raises:
            ValueError: Specified column is missing from dataset

        Returns:
            pd.DataFrame: Processed DataFrame
        """
        for col in date_cols:

            if not col in dataframe.columns:
                raise ValueError(f"No column : {col}, cannot convert to datetime")

            dataframe[f"{col}"] = pd.to_datetime(dataframe[f"{col}"])

        return dataframe
