import pandas as pd
from datetime import datetime

class DataFrameTransformer:
    
    def fill_null_dates_with_today(self, dataframe: pd.DataFrame = None, date_col: str = None) -> pd.DataFrame:
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
        
        # Ensure the specified date column is a datetime column
        dataframe[date_col] = pd.to_datetime(dataframe[date_col], errors='coerce')
        
        # Replace NaN values in the specified date column with today's date
        dataframe[date_col].fillna(pd.Timestamp(datetime.today()), inplace=True)
        
        return dataframe