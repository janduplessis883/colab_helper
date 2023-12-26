# AutoNote version 3.8 (MySQL Database)
from IPython.display import display, clear_output, Javascript, HTML
from ipywidgets import Button, Output, HBox, Textarea, Checkbox, widgets
import time
import colorsys
import mysql.connector
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import json
import uuid
import gspread
from google.oauth2 import service_account
import subprocess
from icecream import ic
import warnings

warnings.filterwarnings("ignore")
import math
import numpy as np
import datetime
import os
import requests

# SKlearn imports
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import cross_validate, learning_curve
from sklearn.metrics import (
    make_scorer,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split

# from sklearn.metrics import plot_roc_curve
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import auc
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from yellowbrick.regressor import ResidualsPlot, PredictionError
from yellowbrick.classifier import DiscriminationThreshold, PrecisionRecallCurve


# from tpot import TPOTClassifier


# Authentication and secret information
import autonote_config as ac
from sheethelper import SheetHelper
from emailbuddy import EmailBuddy

# from timetracker import TimeTracker
from notionhelper import NotionHelper

# Move_mail define Emails to be sorted into specific Mail Folders
move_email = {
    "IMPORTANT": [
        "orietta.emiliani@nhs.net",
        "cameron.mcivor@nhs.net",
        "rekha.jayatissa@nhs.net",
        "burhanaliadib@gmail.com",
        "fiona.butler@nhs.net",
        "anna.cantlay@nhs.net",
        "s.ramtale@imperial.ac.uk",
        "alex.florko@nhs.net",
    ],
    "The Good Practice 2": [
        "thegoodpractice2@nhs.net",
        "cameron.mcivor@nhs.net",
        "claire.perez4@nhs.net",
        "justinhammond@nhs.net",
    ],
    "Earls Court Surgery": [
        "isma.moosa@nhs.net",
        "joyce.frankson@nhs.net",
        "christinehyppolite@nhs.net",
        "lula.eyasu@nhs.net",
        "rinku.patel1@nhs.net",
        "Kate@rbp.co.uk",
    ],
    "NWL ICS GP Fed": [
        "nhsnwl.westlondongpfederation@nhs.net",
        "helen.tsang@nhs.net",
        "nwl.infogovernance@nhs.net",
        "donna.hislop@nhs.net",
        "nhsnwl.localservices@nhs.net",
        "nhsnwl.wlprimarycare@nhs.net",
        "nhsnwl.lon-nw-pcc@nhs.net",
        "nhsnwl.covidvaccination@nhs.net",
    ],
    "PCN": [
        "krydings@nhs.net",
        "maryla.karge@nhs.net",
        "maria.pankhurst@nhs.net",
        "warwick.young@nhs.net",
        "katarzyna.sroga@nhs.net",
        "marzena.grzymala@nhs.net",
        "lesley.french@nhs.net",
        "zaby.begum@nhs.net",
        "e.etim-offiong@nhs.net",
        "thomas.newland1@nhs.net",
        "dana.camino@nhs.net",
        "jas.dua@nhs.net",
        "paul.carnduff@nhs.net",
    ],
    "Clinical Research": [
        "lnw.primarycare@nihr.ac.uk",
        "jalpa.bajaria@nihr.ac.uk",
        "antoinetr.ac.uk",
        "ashnee.dhondete.mcnulty@nihe@nihr.ac.uk",
        "carbis_hannah@lilly.com",
        "summits@myscrs.org",
        "communications@myscrs.org",
        "s.ramtale@imperial.ac.uk",
        "matt.glasier@onestudyteam.com",
        "lauren.gledhill@informa.com",
        "n.e.bailey@soton.ac.uk",
        "nhsnwl.westlondon.trainingandresearch@nhs.net",
        "nhsnwl.westlondon.research@nhs.net",
    ],
    "The Chelsea Practice": [
        "k.shackleford@nhs.net",
        "alexander.johnston1@nhs.net",
        "claire.scudder@nhs.net",
        "marius.brill@nhs.net",
        "k.e.wisniewska@soton.ac.uk",
        "ph204@leicester.ac.uk",
        "ra421@leicester.ac.uk",
        "helen.dallosso@uhl-tr.nhs.uk",
    ],
    "Jan Special Interest": [
        "info@make.com",
        "colin.paget@hn-company.co.uk",
        "jan.duplessis@nhs.net",
        "jpltuk@aol.com",
        "jack.clitheroe@azets.co.uk",
        "rick.smith@forbesburton.com",
        "nicholas.troth@forbesburton.com",
    ],
    "Admin Tasks": ["mail@treeviewdesigns.thirdparty.nhs.uk"],
    "Finance": [
        "sales@medical-supermarket.com",
        "info@email.bionic.co.uk",
        "nisha@rbp.co.uk",
        "sc-invoices@southern-comms.co.uk",
        "shared.services2@nhs.net",
        "support@lantum.com",
    ],
    "PCSE": [
        "pcse.rejectedregistrations@nhs.net",
        "pcse.csc-noreply@nhs.net",
        "donotreply@pcsengland.co.uk",
    ],
}


class AutoNote:
    """
    AutoNote version 3.8 (MySQL Database)
    """

    def __init__(self):
        self.but_color3 = "#eeeeee"
        self.but_color2 = "#eeeeee"
        self.but_color1 = "#cccbc3"
        self.gs_helper = SheetHelper(
            "https://docs.google.com/spreadsheets/d/1hIy0DpUwD8znqnNZ2EAAbPdIESpdRgpHDDskYOcAbLw/edit#gid=0",
            0,
        )
        # self.notion_helper = NotionHelper()
        self.eb = EmailBuddy()

        # Connect to MySQL database
        self.connect_to_mysql_with_status()
        # self.start_tracker()
        self.search_code()

    def __str__(self):
        return """AutoNote:\nLog File: https://docs.google.com/spreadsheets/d/1hIy0DpUwD8znqnNZ2EAAbPdIESpdRgpHDDskYOcAbLw/edit#gid=0\nGitHub: janduplessis883 - https://github.com/janduplessis883/AutoNote\n
                """

    def connect_to_mysql_with_status(self):
        # Define a button widget for connecting to the database
        connect_button = Button(description="⚡️Connect")
        connect_button.style.button_color = self.but_color3

        # Define an output widget for displaying connection status
        status_output = Output()

        # Define a function to close the database connection
        def close_connection(_):
            self.mydb.close()
            self.eb.cnx2.close()
            with status_output:
                status_output.clear_output()
                display(HTML(self.class_status()))
                self.gs_helper.send_gsheet("🪫 Connection closed")

        # Define a function to connect to the database and update the status output widget
        def connect_to_mysql(_):
            try:
                # Establish a connection to MySQL
                self.mydb = mysql.connector.connect(
                    host=ac.host,
                    user=ac.db_user,
                    password=ac.db_password,
                    database=ac.database,
                )
                self.c = self.mydb.cursor()
                with status_output:
                    status_output.clear_output()
                    display(HTML(self.class_status()))
                    self.gs_helper.send_gsheet("🔌 Connected to MySQL Server")

            except mysql.connector.Error as error:
                with status_output:
                    status_output.clear_output()
                    display(
                        HTML(
                            "<span style='color:#cb4b15;'>❌ Error while connecting to MySQL: {}</span>".format(
                                error
                            )
                        )
                    )
                    self.gs_helper.send_gsheet(
                        f"❌ Error connecting to MySQL Server - Error: {error}"
                    )
            self.eb.connect_ebmysql()

        def connect_emailbuddy(_):
            self.eb.authenticate()
            self.eb.delete_by_sender()
            self.eb.email_to_folder(move_email)

            self.eb.folder_review()
            self.eb.make_email_list()
            self.eb.add_blacklist()

            self.gs_helper.send_gsheet(f"📨 Ran EmailBuddy")

        # Bind the connect_to_mysql() function to the connect button
        connect_button.on_click(connect_to_mysql)

        # Define a button widget to close the database connection
        close_button = Button(description="Close Connection")
        close_button.style.button_color = self.but_color2
        close_button.on_click(close_connection)

        # Email buddy button
        emailbuddy_button = Button(description="✉️ EmailBuddy")
        emailbuddy_button.style.button_color = self.but_color2
        emailbuddy_button.on_click(connect_emailbuddy)

        # Display the connect button, close button, and status output widget horizontally
        display(HBox([emailbuddy_button, connect_button, close_button, status_output]))

        # Call the connect_to_mysql function directly when the notebook is loaded
        connect_to_mysql(None)

    # def start_tracker(self):
    #     project = input("Project: ")
    #     if project == '':
    #         project = 'Playing with Python'

    #     category = input("Category:")
    #     if category == '':
    #         category = "Personal"

    #     sheet_helper = SheetHelper('https://docs.google.com/spreadsheets/d/1hIy0DpUwD8znqnNZ2EAAbPdIESpdRgpHDDskYOcAbLw/edit#gid=0', 1)
    #     tracker = TimeTracker(sheet_helper)

    #     # Ensure that tracking is stopped even if the notebook is closed unexpectedly
    #     atexit.register(tracker.close)

    #     # Start tracking
    #     tracker.start_tracking(project, category)
    #     return

    # def stop_tracker(self):
    #     sheet_helper = SheetHelper('https://docs.google.com/spreadsheets/d/1hIy0DpUwD8znqnNZ2EAAbPdIESpdRgpHDDskYOcAbLw/edit#gid=0', 1)
    #     tracker = TimeTracker(sheet_helper)
    #     tracker.stop_tracking()
    #     return

    def create_code_blocks_table(self):
        self.c.execute(
            """
            CREATE TABLE IF NOT EXISTS code_blocks3 (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                group_id INTEGER NOT NULL,
                execution_order INTEGER NOT NULL,
                markdown INTEGER,
                code TEXT NOT NULL,
                FOREIGN KEY (group_id)
                    REFERENCES code_groups(id)
                    ON DELETE CASCADE
            )
        """
        )

        self.mydb.commit()

    def create_code_groups_table(self):
        self.c.execute(
            """
            CREATE TABLE IF NOT EXISTS code_groups3 (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                group_name TEXT NOT NULL
            )
        """
        )

        self.mydb.commit()

    def check_group_name_exists(self, group_name):
        self.c.execute(
            "SELECT COUNT(*) FROM code_groups3 WHERE group_name=%s", (group_name,)
        )
        result = self.c.fetchone()
        return result[0] > 0

    def new_code(self, no_blocks=4):
        group_name_input = widgets.Text(description="Group Name:")

        code_rows = []
        for i in range(no_blocks):
            code_text_area = Textarea(
                description=f"Code {i + 1}:",
                layout=widgets.Layout(width="100%", height="50px"),
            )
            markdown_checkbox = Checkbox(description="Markdown", value=False)
            code_row = widgets.HBox([code_text_area, markdown_checkbox])
            code_rows.append(code_row)

        submit_button = Button(description="Submit")
        submit_button.style.button_color = self.but_color1

        def submit_new_code(_):
            group_name = group_name_input.value
            code_snippets = [
                (row.children[0].value, row.children[1].value)
                for row in code_rows
                if row.children[0].value.strip() != ""
            ]
            self.add_new_code(group_name, code_snippets)
            self.gs_helper.send_gsheet("💾 New_code", group_name)
            clear_output()

        submit_button.on_click(submit_new_code)
        group_name_status = widgets.Label(value="")
        display(
            widgets.HBox([group_name_input, group_name_status]),
            *code_rows,
            submit_button,
        )

        def check_group_name(change):
            # Only check when the value is changed.
            if change["type"] == "change" and change["name"] == "value":
                group_name = change["new"]
                exists = self.check_group_name_exists(group_name)
                if exists:
                    group_name_status.value = "❌"
                else:
                    group_name_status.value = "✅"

        group_name_input.observe(check_group_name)

    def get_code_group_names(self):
        self.c.execute("SELECT group_name FROM code_groups3")
        group_names = [row[0] for row in self.c.fetchall()]
        return group_names

    def add_new_code(self, group_name, code_snippets):
        self.c = self.mydb.cursor()

        # Insert new code group
        self.c.execute(
            "INSERT INTO code_groups3 (group_name) VALUES (%s)", (group_name,)
        )
        group_id = self.c.lastrowid

        # Insert code blocks for the group
        for idx, (code, markdown) in enumerate(code_snippets):
            self.c.execute(
                """
                INSERT INTO code_blocks3 (group_id, execution_order, markdown, code)
                VALUES (%s, %s, %s, %s)
            """,
                (group_id, idx + 1, int(markdown), code),
            )

        self.mydb.commit()

    def load_code_snippets(self, group_id):
        code_snippets = self.get_code_snippets(group_id)
        for code, markdown in code_snippets:
            if markdown == 0:
                self.create_code_cell(code)
            elif markdown == 1:
                self.create_markdown_cell(code)

    def create_code_cell(self, code):
        cell_id = str(uuid.uuid4())
        escaped_code = json.dumps(code)
        display(
            Javascript(
                f"""
            var code = {escaped_code};
            var cell = Jupyter.notebook.insert_cell_above('code');
            cell.set_text(code);
            cell.metadata.id = '{cell_id}';
        """
            )
        )

    def create_code_cell_below(self, code):
        cell_id = str(uuid.uuid4())
        escaped_code = json.dumps(code)
        display(
            Javascript(
                f"""
            var code = {escaped_code};
            var cell = Jupyter.notebook.insert_cell_below('code');
            cell.set_text(code);
            cell.metadata.id = '{cell_id}';
        """
            )
        )

    def create_markdown_cell(self, text):
        cell_id = str(uuid.uuid4())
        escaped_text = json.dumps(text)
        display(
            Javascript(
                f"""
            var text = {escaped_text};
            var cell = Jupyter.notebook.insert_cell_above('markdown');
            cell.set_text(text);
            cell.metadata.id = '{cell_id}';
        """
            )
        )

    def load_code(self):
        """
        Displays a dropdown list of code group names and a button to load the selected code group's snippets.
        """
        group_names = sorted(self.get_code_group_names())
        code_group_dropdown = widgets.Dropdown(
            options=group_names, description="Group Name:"
        )
        insert_button = widgets.Button(description="Insert Code")
        insert_button.style.button_color = self.but_color1

        # Add custom CSS for the button text color
        custom_button_style = """
        <style>
            .custom-button .widget-label {
                color: #e5e7e8;
            }
        </style>
        """

        # Add a custom class to the Button widget
        insert_button.add_class("custom-button")

        # Define the on_click event handler
        def on_insert_click(_):
            group_name = code_group_dropdown.value
            group_id = self.get_group_id_by_name(group_name)
            self.load_code_snippets(group_id)
            self.gs_helper.send_gsheet("⏳ load_code", group_name, group_id)

        # Attach the event handler to the button
        insert_button.on_click(on_insert_click)

        # Display the button with custom CSS
        display(HTML(custom_button_style))
        display(HBox([code_group_dropdown, insert_button]))

    def get_group_id_by_name(self, group_name):
        """
        Retrieves the group ID for a given group name.

        Args:
            group_name (str): The name of the code group.

        Returns:
            int: The ID of the code group.
        """
        self.c.execute(
            "SELECT id FROM code_groups3 WHERE group_name = %s", (group_name,)
        )
        group_id = self.c.fetchone()[0]
        return group_id

    def get_code_snippets(self, group_id):
        """
        Retrieves code snippets for a given group ID.

        Args:
            group_id (int): The ID of the code group.

        Returns:
            list: A list of tuples containing the code and markdown for each code snippet.
        """
        self.c.execute(
            """
            SELECT code, markdown
            FROM code_blocks3
            WHERE group_id = %s
            ORDER BY execution_order
        """,
            (group_id,),
        )
        return self.c.fetchall()

    def delete_code(self):
        """
        Displays a dropdown list of code group names and a button to delete the selected code group and its snippets.
        """
        group_names = sorted(self.get_code_group_names())
        code_group_dropdown = widgets.Dropdown(
            options=group_names, description="Group Name:"
        )
        delete_button = widgets.Button(description="Delete")
        delete_button.style.button_color = self.but_color1

        def on_delete_click(_):
            group_name = code_group_dropdown.value
            self.delete_group_and_snippets(group_name)
            clear_output()
            print(f"Group '{group_name}' and its code snippets have been deleted.")
            self.delete_code()  # Refresh the dropdown list
            self.gs_helper.send_gsheet("❌ delete_code", group_name, group_id="delete")

        delete_button.on_click(on_delete_click)
        display(HBox([code_group_dropdown, delete_button]))

    def delete_group_and_snippets(self, group_name):
        """
        Deletes a code group and its associated code snippets.

        Args:
            group_name (str): The name of the code group to delete.
        """
        group_id = self.get_group_id_by_name(group_name)

        # Delete code snippets
        self.c.execute("DELETE FROM code_blocks3 WHERE group_id = %s", (group_id,))
        self.mydb.commit()

        # Delete code group
        self.c.execute("DELETE FROM code_groups3 WHERE id = %s", (group_id,))
        self.mydb.commit()

    def edit_groupname(self):
        """
        Displays a dropdown list of code group names, a text input to enter a new name, and a button to update the selected code group's name.
        """
        group_names = sorted(self.get_code_group_names())
        current_group_dropdown = widgets.Dropdown(
            options=group_names, description="Current:"
        )
        new_group_input = widgets.Text(description="New Name:")
        update_button = widgets.Button(description="Update")
        update_button.style.button_color = self.but_color1

        def on_update_click(_):
            current_group_name = current_group_dropdown.value
            new_group_name = new_group_input.value.strip()
            if new_group_name:
                self.update_group_name(current_group_name, new_group_name)
                clear_output()
                print(
                    f"Group name updated from '{current_group_name}' to '{new_group_name}'."
                )
                self.gs_helper.send_gsheet(
                    "📝 edit_groupname",
                    new_group_name,
                    group_id=f"Old: {current_group_name}",
                )
                self.edit_groupname()  # Refresh the dropdown lists
            else:
                print("Please enter a new group name.")

        update_button.on_click(on_update_click)
        display(HBox([current_group_dropdown, new_group_input, update_button]))

    def update_group_name(self, current_group_name, new_group_name):
        """
        Updates a code group's name.

        Args:
            current_group_name (str): The current name of the code group.
            new_group_name (str): The new name for the code group.
        """
        group_id = self.get_group_id_by_name(current_group_name)

        # Update the group name in the database
        self.c.execute(
            "UPDATE code_groups3 SET group_name = %s WHERE id = %s",
            (new_group_name, group_id),
        )
        self.mydb.commit()

    def print_groupnames(self):
        """
        Prints the names and code snippet counts of all code groups as an HTML table.
        """
        # Get all group names and their IDs
        self.c.execute("SELECT id, group_name FROM code_groups3 ORDER BY group_name")
        groups = self.c.fetchall()

        # Count the number of code snippets for each group
        group_counts = []
        for group_id, group_name in groups:
            self.c.execute(
                "SELECT COUNT(*) FROM code_blocks3 WHERE group_id = %s", (group_id,)
            )
            count = self.c.fetchone()[0]
            group_counts.append((group_name, count))

        # Generate HTML table
        html_table = "<div class='status' style='background-color: #d37f00; color: white; padding-top: 0px; padding-bottom: \
            0px; padding-left: 7px; padding-right: 7px; border-radius: 5px; font-family: Arial, sans-serif; font-size: 12px; display: \
                inline-block; text-align: center;'>✩AutoNote</div> <span style='color: #cecfcf;'>→ janduplessis883</span><BR><table>"
        html_table += "<tr><th>No.</th><th style='text-align:left;'>Code Group Name</th><th>Snippet Count</th></tr>"
        counter = 1
        for group_name, count in group_counts:
            html_table += f"<tr><td>{counter}</td><td style='text-align:left;'>{group_name}</td><td>{count}</td></tr>"
            counter = counter + 1
        html_table += "</table>"

        # Display the HTML table in the Jupyter Notebook
        self.gs_helper.send_gsheet("🖨️ print_groupnames", "", "")
        display(HTML(html_table))

    # New search fuynction
    def search_code(self):
        """
        Displays a text input for searching code group names, a dropdown list of filtered code group names, and a button \
            to load the selected code group's snippets.
        """
        group_names = sorted(self.get_code_group_names())
        search_input = widgets.Text(description="🔎")
        code_group_dropdown = widgets.Dropdown(options=group_names, description="Code:")
        load_button = widgets.Button(description="Load Code")
        load_button.style.button_color = self.but_color1

        def on_search_change(change):
            search_text = change["new"].strip().lower()
            filtered_group_names = [
                group_name
                for group_name in group_names
                if search_text in group_name.lower()
            ]
            code_group_dropdown.options = filtered_group_names

        def on_load_click(_):
            group_name = code_group_dropdown.value
            group_id = self.get_group_id_by_name(group_name)
            self.load_code_snippets(group_id)
            self.gs_helper.send_gsheet("🔎 search_code", group_name, group_id)

        search_input.observe(on_search_change, names="value")
        load_button.on_click(on_load_click)
        # display(search_input, code_group_dropdown, load_button)
        display(HBox([search_input, code_group_dropdown, load_button]))

    def backup_mysql(self):
        """
        Creates a backup of the MySQL database and saves it as an SQL file.
        """
        # Replace the values in the following variables with your own database credentials
        username = ac.db_user
        password = ac.db_password
        hostname = ac.host
        database = ac.database

        timestamp = time.time()
        # Define the filename and location for the backup file
        filename = f"/Users/janduplessis/code/janduplessis883/jan-code/AutoNote/mysql/autonote-mysql-backup-{timestamp}.sql"

        # Define the mysqldump command to create the backup
        backup_command = f"mysqldump --host={hostname} --user={username} --password={password} --compact --skip-comments \
            --skip-lock-tables {database} > {filename}"

        # Execute the mysqldump command using subprocess
        subprocess.run(backup_command, shell=True)

        print("Backup created successfully!")
        self.gs_helper.send_gsheet(
            "🔙 Backup MySQL Database Successful",
        )
        return filename

    # def class_status(self):
    #     """Returns an HTML string based on the presence of certain globals and database connection status."""
    #     # HTML template
    #     template = "<div class='status' style='background-color: {}; color: white; padding-top: 0px; padding-bottom: 0px; padding-left: 7px; padding-right: 7px; border-radius: 5px; font-family: Arial, sans-serif; font-size: 10px; display: inline-block; text-align: center;'>{}</div> "

    #     # Determine the colors and labels based on the globals and connection status
    #     colors_and_labels = [
    #         ('#007b99' if 'AutoNote' in globals() else '#cccbc3', 'AutoNote'),
    #         ('#d37f00' if self.mydb.is_connected() else '#cccbc3', 'MySQL'),
    #         ('#cccbc3' if 'SheetHelper' in globals() else '#cccbc3', 'SheetHelper'),
    #         ('#6e635e' if 'TimeTracker' in globals() else '#cccbc3', 'TimeTracker'),
    #         ('#cccbc3' if 'NotionHelper' in globals() else '#cccbc3', 'NotionHelper'),
    #     ]

    #     # Generate the HTML string
    #     tags = ''.join(template.format(color, label) for color, label in colors_and_labels)
    #     return tags

    def class_status(self):
        """Returns an HTML string based on the presence of certain globals and database connection status."""
        # HTML template
        template = "<div class='status' style='background-color: {}; color: white; padding-top: 0px; padding-bottom: 0px; padding-left: 7px; padding-right: 7px; border-radius: 5px; font-family: Arial, sans-serif; font-size: 10px; display: inline-block; text-align: center;'>{}</div> "

        # Determine the colors and labels based on the globals and connection status
        colors_and_labels = []

        # Check for AutoNote class
        try:
            AutoNote
            colors_and_labels.append(
                ("#7e7772", "AutoNote")
            )  # Set color to green if AutoNote class exists
        except NameError:
            colors_and_labels.append(("#cccbc3", "AutoNote"))

        # Check for EmailBUddfy class
        try:
            EmailBuddy
            colors_and_labels.append(
                ("#75903f", "EmailBuddy")
            )  # Set color to green if AutoNote class exists
        except NameError:
            colors_and_labels.append(("#cccbc3", "EmailBuddy"))

        # Check for other instances
        for instance_name, label in [
            ("SheetHelper", "SheetHelper"),
            ("NotionHelper", "NotionHelper"),
        ]:
            try:
                globals()[instance_name]
                colors_and_labels.append(("#a5a395", label))
            except KeyError:
                colors_and_labels.append(("#cccbc3", label))

                # Check for database connection
        colors_and_labels.append(
            ("#d37f00" if self.mydb.is_connected() else "#cccbc3", "AutoNote SQL")
        )

        # Check for database2 connection
        colors_and_labels.append(
            ("#d37f00" if self.eb.cnx2.is_connected() else "#cccbc3", "EmailBuddy SQL")
        )

        # Generate the HTML string
        tags = "".join(
            template.format(color, label) for color, label in colors_and_labels
        )
        return tags

    def fix_datetime_on_df(self, df, date_column):
        df["date"] = pd.to_datetime(df[date_column])
        df.set_index(keys=date_column, inplace=True)

    # def class_status(self):

    #     if 'AutoNote' in globals():
    #         an_tag = "<div class='status' style='background-color: #6e635e; color: white; padding-top: 0px; padding-bottom: 0px; padding-left: 7px; padding-right: 7px; border-radius: 5px; font-family: Arial, sans-serif; font-size: 10px; display: inline-block; text-align: center;'>AutoNote</div> "
    #     else:
    #         an_tag = "<div class='status' style='background-color: #cccbc3; color: white; padding-top: 0px; padding-bottom: 0px; padding-left: 7px; padding-right: 7px; border-radius: 5px; font-family: Arial, sans-serif; font-size: 10px; display: inline-block; text-align: center;'>AutoNote</div> "

    #     if 'GSheetHelper' in globals():
    #         gs_tag = "<div class='status' style='background-color: #6e635e; color: white; padding-top: 0px; padding-bottom: 0px; padding-left: 7px; padding-right: 7px; border-radius: 5px; font-family: Arial, sans-serif; font-size: 10px; display: inline-block; text-align: center;'>GSheetHelper</div> "
    #     else:
    #         gs_tag = "<div class='status' style='background-color: #cccbc3; color: white; padding-top: 0px; padding-bottom: 0px; padding-left: 7px; padding-right: 7px; border-radius: 5px; font-family: Arial, sans-serif; font-size: 10px; display: inline-block; text-align: center;'>GSheetHelper</div> "

    #     c_connected = self.mydb.is_connected()
    #     if c_connected:
    #         sql_tag = "<div class='status' style='background-color: #d37f00; color: white; padding-top: 0px; padding-bottom: 0px; padding-left: 7px; padding-right: 7px; border-radius: 5px; font-family: Arial, sans-serif; font-size: 10px; display: inline-block; text-align: center;'>MySQL</div> "
    #     else:
    #         sql_tag = "<div class='status' style='background-color: #cccbc3; color: white; padding-top: 0px; padding-bottom: 0px; padding-left: 7px; padding-right: 7px; border-radius: 5px; font-family: Arial, sans-serif; font-size: 10px; display: inline-block; text-align: center;'>MySQL</div> "

    #     tags = an_tag + gs_tag + sql_tag
    #     return tags

    def color_shader(self, color1):
        """
        Lightens the given color by a fixed amount.

        Args:
            color1 (str): A hex color string (e.g. "#1e758a")

        Returns:
            str: A new hex color string representing the lightened color.
        """
        input_hex = color1

        # Convert the hex string to RGB values
        r, g, b = tuple(int(input_hex[i : i + 2], 16) for i in (1, 3, 5))

        # Convert RGB values to HSL (hue, saturation, lightness) values
        h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)

        # Increase the lightness value by 2/100 to make the color 2 shades lighter
        l += 0.13

        # Convert the new HSL values back to RGB values
        r, g, b = [int(c * 255) for c in colorsys.hls_to_rgb(h, l, s)]

        # Convert the RGB values to a hex color string
        color2 = f"#{hex(r)[2:]:0>2}{hex(g)[2:]:0>2}{hex(b)[2:]:0>2}"

        return color2

    def plot_weeks(self, df, date_column="DATE", color1="#1e758a"):
        """
        Plots the weekly counts of occurrences in a given DataFrame for two years (2022 and 2023).

        Args:
            df (pandas.DataFrame): The input DataFrame containing the data to be plotted.
            date_column (str, optional): The name of the column containing date information. Defaults to 'DATE'.
            color1 (str, optional): The primary hex color string for the plot. Defaults to '#1e758a'.
        """

        # Calls the color_shader function to produce secondary matching color
        color2 = self.color_shader(color1)

        # Convert the date column to datetime format
        df[date_column] = pd.to_datetime(df[date_column])

        # Extract the week number and year from the date
        df["WEEK"] = df[date_column].dt.isocalendar().week
        df["YEAR"] = df[date_column].dt.year

        # Count the number of occurrences for each week and year
        weekly_counts = df.groupby(["YEAR", "WEEK"]).size().reset_index(name="COUNT")

        # Create a dataframe with all weeks of the year
        all_weeks = pd.DataFrame({"WEEK": range(1, 53)})

        # Define colors for each year
        colors = {2022: color2, 2023: color1}

        # Create subplots for the two bar charts
        fig, axes = plt.subplots(2, 1, figsize=(12, 7), sharex=True)
        fig.subplots_adjust(hspace=0.4)

        for idx, year in enumerate([2022, 2023]):
            # Merge the weekly_counts dataframe with the all_weeks dataframe for the given year
            merged_weeks = all_weeks.merge(
                weekly_counts[weekly_counts["YEAR"] == year], on="WEEK", how="left"
            )

            # Fill missing counts with 0
            merged_weeks["COUNT"] = merged_weeks["COUNT"].fillna(0)

            # Create the bar plot using Matplotlib
            axes[idx].grid(
                True, linestyle="--", linewidth=0.5, color="lightgray", alpha=0.5
            )
            axes[idx].bar(
                merged_weeks["WEEK"], merged_weeks["COUNT"], color=colors[year]
            )

            # Set plot labels and title
            axes[idx].set_xlabel("Week")
            axes[idx].set_ylabel("Count")
            axes[idx].set_title(f"Weekly Counts {date_column} for {year}")

        # Show the plot
        plt.show()

    def plot_months(self, df, date_column="DATE", color1="#386641"):
        """
        Plots the monthly counts of occurrences in a given DataFrame for two years (2022 and 2023).

        Args:
            df (pandas.DataFrame): The input DataFrame containing the data to be plotted.
            date_column (str, optional): The name of the column containing date information. Defaults to 'DATE'.
            color1 (str, optional): The primary hex color string for the plot. Defaults to '#386641'.
        """
        # Calls the color_shader function to produce secondary matching color
        color2 = self.color_shader(color1)

        # Convert the date column to datetime format
        df[date_column] = pd.to_datetime(df[date_column])

        # Extract the month and year from the date
        df["MONTH"] = df[date_column].dt.month
        df["YEAR"] = df[date_column].dt.year

        # Count the number of occurrences for each month and year
        monthly_counts = df.groupby(["YEAR", "MONTH"]).size().reset_index(name="COUNT")

        # Create a dataframe with all months of the year
        all_months = pd.DataFrame({"MONTH": range(1, 13)})

        # Define colors for each year
        colors = {2022: color2, 2023: color1}

        # Create subplots for the two bar charts
        fig, axes = plt.subplots(2, 1, figsize=(12, 7), sharex=True)
        fig.subplots_adjust(hspace=0.4)

        for idx, year in enumerate([2022, 2023]):
            # Merge the monthly_counts dataframe with the all_months dataframe for the given year
            merged_months = all_months.merge(
                monthly_counts[monthly_counts["YEAR"] == year], on="MONTH", how="left"
            )

            # Fill missing counts with 0
            merged_months["COUNT"] = merged_months["COUNT"].fillna(0)

            # Create the bar plot using Matplotlib
            axes[idx].grid(
                True, linestyle="--", linewidth=0.5, color="lightgray", alpha=0.5
            )
            axes[idx].bar(
                merged_months["MONTH"], merged_months["COUNT"], color=colors[year]
            )

            # Set plot labels and title
            axes[idx].set_xlabel("Month")
            axes[idx].set_ylabel("Count")
            axes[idx].set_title(f"Monthly Counts {date_column} for {year}")

        # Show the plot
        plt.show()

    def large_print(self, desc="Description", color="#000000", value=""):
        """
        Displays a given description and value in large font size using HTML.

        Args:
            desc (str, optional): The description text to display. Defaults to 'Description'.
            value (str, optional): The value text to display. Defaults to an empty string.
        """
        # Create an HTML string with a large font size
        html = f'<p style="font-size:18pt; color: {color};">{desc} <B>{value}</b></p>'

        # Display the HTML string
        display(HTML(html))

    def medium_print(self, desc="Description", value=""):
        """
        Displays a given description and value in medium font size using HTML.

        Args:
            desc (str, optional): The description text to display. Defaults to 'Description'.
            value (str, optional): The value text to display. Defaults to an empty string.
        """
        # Create an HTML string with a large font size
        html = f'<p style="font-size:16pt">{desc} <B>{value}</b></p>'

        # Display the HTML string
        display(HTML(html))

    def small_print(self, desc="Description", value=""):
        """
        Displays a given description and value in medium font size using HTML.

        Args:
            desc (str, optional): The description text to display. Defaults to 'Description'.
            value (str, optional): The value text to display. Defaults to an empty string.
        """
        # Create an HTML string with a large font size
        html = f'<p style="font-size:14pt">{desc} <B>{value}</b></p>'

        # Display the HTML string
        display(HTML(html))

    def tag(self, text, tag_color=0):
        tag_colors = ["#1b8d9b", "#ce5728", "#d37f00", "#6e635e", "#cccbc3"]
        tags_code = f"<div class='status' style='background-color: {tag_colors[tag_color]}; color: white; padding-top: 0px; padding-bottom: 0px; padding-left: 7px; padding-right: 7px; border-radius: 5px; font-family: Arial, sans-serif; font-size: 10px; display: inline-block; text-align: center;'>{text}</div>"
        self.gs_helper.send_gsheet("🤖 function", "tag()", "")
        return self.create_markdown_cell(tags_code)

    def activity(self):
        sheet_helper = SheetHelper(
            "https://docs.google.com/spreadsheets/d/1hIy0DpUwD8znqnNZ2EAAbPdIESpdRgpHDDskYOcAbLw/edit#gid=0",
            0,
        )
        sheet_helper.gsheet_to_df()
        sheet_helper.plot_activity()
        self.gs_helper.send_gsheet("🤖 function", "activity()", "")
        return

    def search_notion_code(self, db_id="5497ce3a79dd49dfbff059a9a65ebeb2"):
        nh = NotionHelper()
        query = input("Search Notion Code Repo for: ")
        nh.notion_search_db(db_id, query)
        self.gs_helper.send_gsheet("🔎 search_notion_code", "Notion Code Repo", query)

    def gsheet_to_df(
        self,
        sheet_url,
        sheet_instance=0,
        secret_file_path="secret/google_sheets_secret.json",
    ):
        # Create the credentials object
        credentials = service_account.Credentials.from_service_account_file(
            secret_file_path
        )

        # Define the scope
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = credentials.with_scopes(scope)
        client = gspread.authorize(creds)

        sheet = client.open_by_url(sheet_url)
        sheet_instance = sheet.get_worksheet(sheet_instance)

        # Get all the values as a JSON
        records_data = sheet_instance.get_all_records()

        # Convert the JSON records to a dataframe
        data = pd.DataFrame.from_dict(records_data)

        # View the top records of the dataframe.
        return data

    def function_list(
        self,
    ):  # ================================================ Function List =========================
        html = """
        <h3><span style="color: #064c6c;">AutoNote - Build in Functions</span></h3>
            <table border="0" style="text-align:left;">
                                            <tr>
                    <td style="text-align:left;"><B>Function</b></td>
                    <td style="text-align:left;"><B>Description</b></td>
                </tr>
                <tr>
                    <td style="text-align:left;"><code>activity()</code></td>
                    <td style="text-align:left;">Plots a chart of AutoNote activity from Log G-Sheet.</td>
                </tr>

                <tr>
                    <td style="text-align:left;"><code>tag(text, tag_color=0)</code></td>
                    <td style="text-align:left;">Create small Tag with specified text and color choice 0 to 6.</td>
                </tr>
                                </tr>
                                <tr>
                    <td style="text-align:left;"><code>evaluate_regression_model(model, X, y)</code></td>
                    <td style="text-align:left;">Plots the metrics of a Regression model.</td>
                </tr>
                <tr>
                    <td style="text-align:left;"><code>evaluate_classification_model(model, X, y, cv=5)</code></td>
                    <td style="text-align:left;">Evaluates a Classification model. Prints scoring Accuracy, Recall, Precision and F1. Plots a Learning Curve & ROC Curve.</td>
                </tr>
                <tr>
                    <td style="text-align:left;"><code>haversine_distance(lat1, lon1, lat2, lon2)</code></td>
                    <td style="text-align:left;">Calculates the distance between 2 sets of coordinates in kilometers.</td>
                </tr>
                <tr>
                    <td style="text-align:left;"><code>scale_df(df, scaler='minmax')</code></td>
                    <td style="text-align:left;">Scale a df or X with either MinMax, Standard or Robust Scaler and outputs df with column headers preserved.</td>
                </tr>

                                <tr>
                    <td style="text-align:left;"><code>feature_importance(model, X, y)</code></td>
                    <td style="text-align:left;">Plots a permutation importance graph of features. First define model.</td>
                </tr>
                                <tr>
                    <td style="text-align:left;"><code>sample_df(df, n_samples)</code></td>
                    <td style="text-align:left;">Samples a df.</td>
                </tr>
                                <tr>
                    <td style="text-align:left;"><code>automl_tpot_classification(X, y)</code></td>
                    <td style="text-align:left;">Perfomrs Classification TPOT AutoML on X and y.</td>
                </tr>
                                <tr>
                    <td style="text-align:left;"><code>train_test_split(X, y, test_size=0.2)</code></td>
                    <td style="text-align:left;">Perfromes a Train Test Split and saves the files to the local directory.</td>
                </tr>
                                <tr>
                    <td style="text-align:left;"><code>define_X_y(self, df, target)</code></td>
                    <td style="text-align:left;">Defines X & y and returns them as a tuple.</td>
                        </tr>
                                        <tr>
                    <td style="text-align:left;"><code>large_print(desc="Description", color="#000000", value="")</code></td>
                    <td style="text-align:left;">Print Large font message to Jupyter with the option to include a numberic value to highlight single values. Also medium_print and small_print functions avaialble.</td>
                </tr>
                                <tr>
                    <td style="text-align:left;"><code>oversample_SMOTE(X_train, y_train, sampling_strategy='auto', k_neighbors=5, random_state=42)</code></td>
                    <td style="text-align:left;">Oversamples minority class in classification models. With various input parameters.</td>
                </tr>
            </table>


        """
        display(HTML(html))

    # ============================================================================== Built-in ML Functions =================

    def evaluate_regression_model(self, model, X, y):
        # Split the dataset into training and test sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Fit the model on the training data
        model.fit(X_train, y_train)

        # Predict on test data
        y_pred = model.predict(X_test)

        # Metrics
        print("Mean Absolute Error (MAE):", mean_absolute_error(y_test, y_pred))
        print("Mean Squared Error (MSE):", mean_squared_error(y_test, y_pred))
        print(
            "Root Mean Squared Error (RMSE):",
            np.sqrt(mean_squared_error(y_test, y_pred)),
        )
        print("R-squared (R2):", r2_score(y_test, y_pred))

        # Create figure
        fig, axs = plt.subplots(2, 2, figsize=(16, 12))

        # Learning curve
        train_sizes, train_scores, test_scores = learning_curve(model, X, y, cv=5)
        train_scores_mean = np.mean(train_scores, axis=1)
        test_scores_mean = np.mean(test_scores, axis=1)
        axs[0, 0].plot(
            train_sizes,
            train_scores_mean,
            "o-",
            color="#a10606",
            label="Training score",
        )
        axs[0, 0].plot(
            train_sizes,
            test_scores_mean,
            "o-",
            color="#6b8550",
            label="Cross-validation score",
        )
        axs[0, 0].set_title("Learning Curve")
        axs[0, 0].set_xlabel("Training Examples")
        axs[0, 0].set_ylabel("Score")
        axs[0, 0].legend(loc="best")
        axs[0, 1].axis("off")  # Turn off unused subplot

        # Residuals plot
        visualizer = ResidualsPlot(model, ax=axs[1, 0])
        visualizer.fit(X_train, y_train)
        visualizer.score(X_test, y_test)
        visualizer.finalize()

        # Prediction error plot
        visualizer = PredictionError(model, ax=axs[1, 1])
        visualizer.fit(X_train, y_train)
        visualizer.score(X_test, y_test)
        visualizer.finalize()

        # Show all plots
        plt.tight_layout()
        plt.show()

    def evaluate_classification_model(self, model, X, y, cv=5):
        """
        Evaluates the performance of a model using cross-validation, a learning curve, and a ROC curve.

        Parameters:
        - model: estimator instance. The model to evaluate.
        - X: DataFrame. The feature matrix.
        - y: Series. The target vector.
        - cv: int, default=5. The number of cross-validation folds.

        Returns:
        - None
        """
        print(model)
        # Cross validation
        scoring = {
            "accuracy": make_scorer(accuracy_score),
            "precision": make_scorer(precision_score, average="macro"),
            "recall": make_scorer(recall_score, average="macro"),
            "f1_score": make_scorer(f1_score, average="macro"),
        }

        scores = cross_validate(model, X, y, cv=cv, scoring=scoring, n_jobs=-1)

        # Compute means and standard deviations for each metric, and collect in a dictionary
        mean_std_scores = {
            metric: (np.mean(score_array), np.std(score_array))
            for metric, score_array in scores.items()
        }

        # Create a DataFrame from the mean and std dictionary and display as HTML
        scores_df = pd.DataFrame(
            mean_std_scores, index=["Mean", "Standard Deviation"]
        ).T
        display(HTML(scores_df.to_html()))

        # Learning curve
        train_sizes = np.linspace(0.1, 1.0, 5)
        train_sizes, train_scores, test_scores = learning_curve(
            model, X, y, cv=cv, train_sizes=train_sizes
        )
        train_scores_mean = np.mean(train_scores, axis=1)
        test_scores_mean = np.mean(test_scores, axis=1)

        # Define the figure and subplots
        fig, axs = plt.subplots(2, 2, figsize=(14, 12))

        axs[0, 0].plot(
            train_sizes,
            train_scores_mean,
            "o-",
            color="#a10606",
            label="Training score",
        )
        axs[0, 0].plot(
            train_sizes,
            test_scores_mean,
            "o-",
            color="#6b8550",
            label="Cross-validation score",
        )
        axs[0, 0].set_xlabel("Training examples")
        axs[0, 0].set_ylabel("Score")
        axs[0, 0].legend(loc="best")
        axs[0, 0].set_title("Learning curve")

        # ROC curve
        cv = StratifiedKFold(n_splits=cv)
        tprs = []
        aucs = []
        mean_fpr = np.linspace(0, 1, 100)
        for i, (train, test) in enumerate(cv.split(X, y)):
            model.fit(X.iloc[train], y.iloc[train])
            viz = plot_roc_curve(
                model,
                X.iloc[test],
                y.iloc[test],
                name="ROC fold {}".format(i),
                alpha=0.3,
                lw=1,
                ax=axs[0, 1],
            )
            interp_tpr = np.interp(mean_fpr, viz.fpr, viz.tpr)
            interp_tpr[0] = 0.0
            tprs.append(interp_tpr)
            aucs.append(viz.roc_auc)

        mean_tpr = np.mean(tprs, axis=0)
        mean_tpr[-1] = 1.0
        mean_auc = auc(mean_fpr, mean_tpr)
        std_auc = np.std(aucs)
        axs[0, 1].plot(
            mean_fpr,
            mean_tpr,
            color="#023e8a",
            label=r"Mean ROC (AUC = %0.2f $\pm$ %0.2f)" % (mean_auc, std_auc),
            lw=2,
            alpha=0.6,
        )

        axs[0, 1].plot(
            [0, 1],
            [0, 1],
            linestyle="--",
            lw=2,
            color="#a10606",
            label="Chance",
            alpha=0.6,
        )
        axs[0, 1].legend(loc="lower right")
        axs[0, 1].set_title("ROC curve")

        # Precision-Recall curve
        visualizer = PrecisionRecallCurve(model, ax=axs[1, 0])
        visualizer.fit(X, y)
        visualizer.score(X, y)
        visualizer.finalize()

        # Discrimination Threshold
        visualizer = DiscriminationThreshold(model, ax=axs[1, 1])
        visualizer.fit(X, y)
        visualizer.score(X, y)
        visualizer.finalize()

        # Show plots
        plt.tight_layout()
        plt.show()

    def haversine_distance(self, lat1, lon1, lat2, lon2):
        R = 6371.0  # Radius of the Earth in kilometers

        # Convert degrees to radians
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)

        # Differences
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad

        # Haversine formula
        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = R * c
        return distance  # in kilometers

    def scale_df(self, df, scaler="minmax"):
        """
        Function to scale the numerical features of a dataframe.

        Args:
            df (DataFrame): The dataframe to scale.
            scaler (str, optional): The type of scaling method to use. Can be 'standard', 'minmax', or 'robust'. Default is 'minmax'.

        Returns:
            DataFrame: Returns a dataframe with the numerical features scaled.
        """
        if scaler == "standard":
            scaler = StandardScaler()
        elif scaler == "minmax":
            scaler = MinMaxScaler()
        elif scaler == "robust":
            scaler = RobustScaler()
        else:
            raise ValueError('Invalid scaler type. Choose "standard" or "minimax".')

        # Get the column headers
        column_headers = df.columns
        # Fit the scaler to the data and transform the data
        scaled_values = scaler.fit_transform(df)

        # Convert the transformed data back to a DataFrame, preserving the column headers
        scaled_df = pd.DataFrame(scaled_values, columns=column_headers)

        print(f"✅ Data Scaled: {scaler} - {scaled_df.shape}")
        return scaled_df

    def oversample_SMOTE(
        self, X_train, y_train, sampling_strategy="auto", k_neighbors=5, random_state=42
    ):
        """
        Oversamples the minority class in the provided DataFrame using the SMOTE (Synthetic Minority Over-sampling Technique) method.

        Parameters:
        ----------
        X_train : Dataframe
            The input DataFrame which contains the features and the target variable.
        y_train : Series
            The name of the column in df that serves as the target variable. This column will be oversampled.
        sampling_strategy : str or float, optional (default='auto')
            The sampling strategy to use. If 'auto', the minority class will be oversampled to have an equal number
            of samples as the majority class. If a float is provided, it represents the desired ratio of the number
            of samples in the minority class over the number of samples in the majority class after resampling.
        k_neighbors : int, optional (default=5)
            The number of nearest neighbors to use when constructing synthetic samples.
        random_state : int, optional (default=0)
            The seed used by the random number generator for reproducibility.

        Returns:
        -------
        X_res : DataFrame
            The features after oversampling.
        y_res : Series
            The target variable after oversampling.

        Example:
        -------
        >>> df = pd.DataFrame({'feature1': np.random.rand(100), 'target': np.random.randint(2, size=100)})
        >>> oversampled_X, oversampled_y = oversample_df(df, 'target', sampling_strategy=0.6, k_neighbors=3, random_state=42)
        """

        # Define the SMOTE instance
        smote = SMOTE(
            sampling_strategy=sampling_strategy,
            k_neighbors=k_neighbors,
            random_state=random_state,
        )

        # Apply the SMOTE method
        X_train_res, y_train_res = smote.fit_resample(X_train, y_train)
        print(
            f"✅ Data Oversampled: SMOTE - X:{X_train_res.shape} y:{y_train_res.shape}"
        )
        return X_train_res, y_train_res

    def feature_importance(self, model, X, y):
        """
        Displays the feature importances of a model using permutation importance.

        Parameters:
        - model: estimator instance. The model to evaluate.
        - X: DataFrame. The feature matrix.
        - y: Series. The target vector.

        Returns:
        - Permutation importance plot
        """
        # Train the model
        model.fit(X, y)

        # Calculate permutation importance
        result = permutation_importance(model, X, y, n_repeats=10)
        sorted_idx = result.importances_mean.argsort()

        # Permutation importance plot
        plt.figure(figsize=(10, 5))
        plt.boxplot(
            result.importances[sorted_idx].T, vert=False, labels=X.columns[sorted_idx]
        )
        plt.title("Permutation Importances")
        plt.show()

    def sample_df(self, df, n_samples):
        """
        Samples the input DataFrame.

        Parameters:
        - df: DataFrame. The input DataFrame.
        - n_samples: int. The number of samples to generate.

        Returns:
        - resampled_df: DataFrame. The resampled DataFrame.
        """
        # Error handling: if the number of samples is greater than the DataFrame length.
        if n_samples > len(df):
            print(
                "The number of samples is greater than the number of rows in the dataframe."
            )
            return None
        else:
            sampled_df = df.sample(n_samples, replace=True, random_state=42)
            print(f"Data Sampled: {sampled_df.shape}")
            return sampled_df

    def automl_tpot_classification(self, X, y):
        # Select features and target
        features = X
        target = y

        # Split the dataset into training and test sets
        X_train, X_test, y_train, y_test = train_test_split(
            features, target, test_size=0.2
        )

        # Create a tpot object with a few generations and population size.
        tpot = TPOTClassifier(
            generations=5, population_size=50, verbosity=2, random_state=42
        )

        # Fit the tpot model on the training data
        tpot.fit(X_train, y_train)

        # Show the final model
        print(tpot.fitted_pipeline_)

        # Use the fitted model to make predictions on the test dataset
        test_predictions = tpot.predict(X_test)

        # Evaluate the model
        print(tpot.score(X_test, y_test))

        # Export the pipeline as a python script file
        time = datetime().now()
        root_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = f"pipelines/tpot_pipeline_{time}.csv"
        output_path = os.path.join(root_dir, output_dir)
        tpot.export(output_path)

    def train_val_test_split(self, X, y, val_size=0.2, test_size=0.2, random_state=42):
        # Calculate intermediate size based on test_size
        intermediate_size = 1 - test_size

        # Calculate train_size from intermediate size and validation size
        train_size = 1 - val_size / intermediate_size
        X_train_val, X_test, y_train_val, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        X_train, X_val, y_train, y_val = train_test_split(
            X_train_val, y_train_val, train_size=train_size, random_state=random_state
        )

        print(f"✅ OUTPUT: X_train, X_val, X_test, y_train, y_val, y_test")
        print(f"Train Set:  X_train, y_train - {X_train.shape}, {y_train.shape}")
        print(f"  Val Set:  X_val, y_val - - - {X_val.shape}, {y_val.shape}")
        print(f" Test Set:  X_test, y_test - - {X_test.shape}, {y_test.shape}")
        return X_train, X_val, X_test, y_train, y_val, y_test

    def train_test_split_func(self, X, y, test_size=0.2, random_state=42):
        # Perform the train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )

        # Print the shapes of the output arrays
        print(f"✅ OUTPUT: X_train, X_test, y_train, y_test")
        print(f"Train Set:  X_train, y_train - {X_train.shape}, {y_train.shape}")
        print(f" Test Set:  X_test, y_test - - {X_test.shape}, {y_test.shape}")

        return X_train, X_test, y_train, y_test

    def define_X_y(self, df, target):
        target = target

        X = df.drop(columns=target)
        y = df[target]
        print(f"✅ OUTPUT: X, y")
        print(f"X - independant variable shape: {X.shape}")
        print(f"y - dependant variable - {target}: {y.shape}")

        return X, y

    bot_token = "6160417937:AAHN7pysqegWTl8LoAP3aNVLNwFuNUTW9j8"
    chat_id = "-657289256"

    def telegram_send(self, bot_message):
        send_text = "https://api.telegram.org/bot" + self.bot_token + "/sendMessage"
        response = requests.get(
            send_text,
            params={
                "chat_id": self.chat_id,
                "parse_mode": "Markdown",
                "text": bot_message,
            },
        )
        return response.json()
