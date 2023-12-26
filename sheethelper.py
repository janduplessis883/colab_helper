import pandas as pd
import seaborn as sns
import requests
import gspread
from google.oauth2 import service_account
import datetime
import matplotlib.pyplot as plt

import autonote_config as ac


class SheetHelper:
    def __init__(
        self,
        sheet_url="https://docs.google.com/spreadsheets/d/1hIy0DpUwD8znqnNZ2EAAbPdIESpdRgpHDDskYOcAbLw/edit#gid=0",
        sheet_id=0,
    ):
        self.sheet_instance = self.authenticate(sheet_url, sheet_id)

    def authenticate(self, sheet_url, sheet_id):
        secret_file_path = "/Users/janduplessis/code/janduplessis883/AutoNote/secret/google_sheets_secret.json"
        credentials = service_account.Credentials.from_service_account_file(
            secret_file_path
        )
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = credentials.with_scopes(scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_url(sheet_url)
        sheet_instance = sheet.get_worksheet(sheet_id)
        return sheet_instance

    def get_external_ip(self):
        return "unknown"

    def send_gsheet(self, event, group_name="", group_id=""):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ip_address = self.get_external_ip()
        row_list = [now, event, group_name, group_id, ip_address]

        self.sheet_instance.append_row(row_list)
        return

    def send_tracker_gsheet(self, row_list):
        self.sheet_instance.append_row(row_list)
        return

    def project_log_to_gsheet(self, project, category):
        # Get the current date and time
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Create a dictionary to hold the data to be sent in the webhook
        row_list = [now, "", project, category]

        self.sheet_instance.append_row(row_list)
        return f"{now} - Logged on g-sheet"

    def get_last_row_index(self):
        # Get all the records from the sheet
        records_data = self.sheet_instance.get_all_records()
        # Return the number of records, which is equivalent to the index of the last row that has data
        return len(records_data)

    def update_cell(self, row, col, value):
        # Update the specified cell with the given value
        self.sheet_instance.update_cell(row, col, value)

    def gsheet_to_df(self) -> pd.DataFrame:
        """
        Converts a Google Sheet sheet to a Pandas dataframe.

        Parameters:
        sheet_url (str): The URL of the Google Sheet.
        sheet_instance (int): The instance of the sheet to be used.
        secret_file_path (str): The relative or absolute file path of the Google Sheets secret key file.

        Returns:
        pd.DataFrame: A Pandas dataframe containing the values of the specified sheet instance.
        """

        # Get all the values as a JSON
        records_data = self.sheet_instance.get_all_records()

        # Convert the JSON records to a dataframe
        data = pd.DataFrame.from_dict(records_data)

        # View the top records of the dataframe.
        return data

    def plot_activity(self, scale="H"):
        log = self.gsheet_to_df()
        log["DateTime"] = pd.to_datetime(log["DateTime"])
        log["DayOfYear"] = log["DateTime"].dt.dayofyear
        log["Hour"] = log["DateTime"].dt.hour
        log["Minute"] = log["DateTime"].dt.minute
        log["Second"] = log["DateTime"].dt.second
        log["WeekOfYear"] = log["DateTime"].dt.isocalendar().week

        # Resample the dataframe by hour
        log_resampled = log.resample(scale, on="DateTime").count()
        # Set the figure size
        plt.figure(figsize=(18, 3))
        # Plot the resampled dataframe
        plt.plot(log_resampled["Event"], color="#d37f00", linewidth=1)
        # Set the title, x-label and y-label
        plt.gca().set_title(
            "AutoNote Activity - Hourly Activity",
            loc="left",
            fontsize=14,
            y=0.95,
            x=0.03,
            color="#786d67",
        )
        plt.gca().yaxis.grid(
            True, linestyle="-", linewidth=0.5, alpha=0.5, color="#acaaa4"
        )
        plt.gca().xaxis.grid(False)
        plt.gca().spines["left"].set_visible(False)
        plt.gca().spines["top"].set_visible(False)
        plt.gca().spines["right"].set_visible(False)
        plt.gca().spines["bottom"].set_visible(True)
        plt.gca().yaxis.set_ticks_position("none")
        plt.gca().xaxis.set_ticks_position("bottom")
        plt.gca().set_xlabel("", fontsize=12, color="#acaaa4")
        # Set x-axis label rotation
        plt.xticks(color="#acaaa4", fontsize=9)
        plt.yticks(color="#acaaa4", fontsize=12, fontweight=700, x=1.045)
        # Display the plot
        return plt.show()
