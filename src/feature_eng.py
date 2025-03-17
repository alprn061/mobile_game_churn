import pandas as pd


def extract_time_features (data, time_column):
    """
    Converts a time column to datetime and extracts time-based features.
    
    Parameters:
        time_column (str): Column name containing time values.
    
    Returns:
        pd.DataFrame: Dataframe with added 'day' and 'hour' columns.
    """
    data[time_column] = pd.to_datetime(data[time_column])
    data["day"] = data[time_column].dt.day
    data["hour"] = data[time_column].dt.hour

    return data



def groupby_user(data):
    data = data.groupby("user_id").agg(
        max_level = ("level_id", "max"),  
        user_success_rate = ("f_success", "mean"),
        user_avg_duration = ("f_duration", "mean"),  
        level_avg_reststep = ("f_reststep", "mean"),  
        total_used_help = ("f_help", "sum"),   
        user_help_rate = ("f_help", "mean"),
        most_played_day = ("day" ,  lambda x: x.mode().iloc[0]),
        most_played_hour = ("hour" , lambda x: x.mode().iloc[0])
    ).reset_index()

    return data


