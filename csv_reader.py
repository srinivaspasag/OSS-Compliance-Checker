import logging
import pandas as pd
import consts
from package_platform.ui_packages import *
from package_platform.java_packages import *
from package_platform.python_packages import *
import os 
# Set up logging
logging.basicConfig(filename="app.log", level=logging.INFO)


def read_csv():
    # Define file paths and names
    file_path = consts.file_directory
    print(file_path , consts.input_filename)
    inp_file = str(file_path) + "/"+ consts.input_filename
    tgt_file = str(file_path) + "/"+  consts.output_filename

    # Log the input file path
    logging.info(f"Input File: {inp_file}")

    # Read the CSV file
    df = pd.read_csv(inp_file)

    # Remove duplicates and sort the DataFrame
    df["index"] = range(len(df))
    sorted_df = df.sort_values("Package Version", ascending=False, ignore_index=True)
    result = sorted_df.drop_duplicates(subset=["Package Name"], keep="first")
    result = result.sort_values("index", ascending=True)
    result = result.drop("index", axis=1)
    result = result.drop("Unnamed: 3", axis=1)

    df = result
    # result.to_csv(no_dups,mode='w', index=False)

    # Create an empty list to hold the values for the new column
    new_column_values = []
    new_column_values_url = []
    new_column_values_family = []
    # Iterate over each row in the DataFrame
    package_list = df["Package Name"].tolist()

    license = None
    license_link = None
    family = None

    for index, row in df.iterrows():
        # Extract the value of the 'Package Name' column
        package_name = row["Package Name"]
        platform = row["Platform"]

        if platform == "UI":
            # Calculate the length of the package name
            family, license, repository_url = fetch_package_data_UI(package_name)
            # Get the license link
            license_link = get_license_link_UI(repository_url)

        elif platform == "Java":
            version = row["Package Version"]
            # print(package_name, version)
            if package_name in data["package_details"]["package"]:
                package_info = get_package_details(
                    data["package_details"]["package"][package_name]
                )
            else:
                package_info = get_package_details(package_name)

            family = package_info["group_id"]

            license_info = get_package_license(
                package_info["group_id"], package_info["artifact_id"]
            )
            # if license_info['name'] == None:
            #    break
            license, license_link = license_info["name"], license_info["url"]

        elif platform == "Python":
            license, license_link = get_license(package_name)
            family = package_name

        new_column_values.append(license)
        new_column_values_url.append(license_link)
        new_column_values_family.append(family)

    df["Package_Family"] = new_column_values_family
    df["License"] = new_column_values
    df["License URL"] = new_column_values_url

    # Log the updated DataFrame
    logging.info(f"Updated DataFrame:\n{df}")

    if not os.path.isfile(tgt_file) or os.path.getsize(tgt_file) == 0:
        # If tgt_file does not exist or is empty, add a header
        df.to_csv(tgt_file, mode="a", header=True, index=False)
    else:
        # Otherwise, append the DataFrame without a header
        df.to_csv(tgt_file, mode="a", header=False, index=False)



def remove_dups(src, dst):
    remove_dups_package_family_java(src, dst)
    remove_dups_package_family_ui(src, dst)


def remove_dups_package_family_java(inp_file, tgt_file):
    df = pd.read_csv(inp_file)
    df = df.drop_duplicates(subset=["Package_Family"], keep="first")
    df.to_csv(tgt_file, index=False, mode="w", header=True)


def remove_dups_package_family_ui(inp_file, tgt_file):
    # Select rows where Package Name is 'UI'
    df = pd.read_csv(inp_file)

    df = df[df["Platform"] == "UI"]
    df["Package_Family"] = df["Package_Family"].str.split("[\s, _,-]").str[0]

    # print(df)
    # Remove duplicates based on Package Family and keep the first occurrence
    df = df.drop_duplicates(subset=["Package_Family"], keep="first")

    df.to_csv(tgt_file, index=False, mode="w", header=True)


def group_by_family(inp_file, tgt_file):
    # Assuming your data is stored in a CSV file
    df = pd.read_csv(inp_file)

    # Split Package_Name by , _ and space, and extract the first token
    df["Package_Name_Tokens"] = df["Package Name"].str.split(r"[\s,_,-]+")
    df["Package_Name_First_Token"] = df["Package_Name_Tokens"].str.get(0)

    df["Package_Name_First_Token"] = df["Package_Name_First_Token"].apply(
        lambda x: str(x) if type(x) != float else ""
    )
    mask = df["License"].str.contains(
        "|".join(df["Package_Name_First_Token"]), case=False
    )

    # Rename Package_Family with the matching token
    df.loc[mask, "Package_Family"] = df.loc[mask, "Package_Name_First_Token"]
    # Rename Package Name column with the matching pattern
    # Rename Package_Name with the matching token

    # Drop columns that we no longer need
    df = df.drop(columns=["Package_Name_Tokens", "Package_Name_First_Token"])
    # df.loc[mask, 'Package_Family'] = df.loc[mask, 'Package_Name_First_Token'].apply(lambda x: x + " *")

    # Drop duplicates based on Package_Family and keep the first occurrence
    df = df.drop_duplicates(subset=["Package_Family"], keep="first")

    # Write the result to a file named 'output.csv' and create the file if it doesn't exist, including the header
    df.to_csv(tgt_file, index=False, mode="w", header=True)


def format_file(inp_file, tgt_file):
    df = pd.read_csv(inp_file)

    # Get the column index of the column you want to modify
    col_index = df.columns.get_loc("License")

    # Iterate over every row in the dataframe
    for index, row in df.iterrows():
        # Get the existing value in the specified column
        existing_value = row[col_index]

        # Check if the value in the specified column matches the pattern
        # data['package_details']['format_licence_name']
        if existing_value in data["package_details"]["format_licence_name"]:
            # Replace the value with the new value
            df.at[index, "License"] = data["package_details"]["format_licence_name"][
                existing_value
            ]

    # Save the modified data to a new CSV file
    df.to_csv(tgt_file, index=False)


if __name__ == "__main__":
    # remove_dups_package_family ()
    # remove_dups_package_family_ui ()
    remove_dups()
    group_by_family()
    # format_file()
