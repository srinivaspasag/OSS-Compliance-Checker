import argparse
import requests
from urllib.parse import urlparse


def find_key(key, json_obj):
    """
    Searches for a key in a nested JSON object
    """
    # Check if the object is a dictionary
    if isinstance(json_obj, dict):
        # Check if the key is in the current dictionary
        if key in json_obj:
            return json_obj[key]
        else:
            # Recursively search for the key in the nested dictionaries
            for sub_obj in json_obj.values():
                result = find_key(key, sub_obj)
                if result is not None:
                    return result
    # Check if the object is a list
    elif isinstance(json_obj, list):
        # Recursively search for the key in the nested dictionaries
        for sub_obj in json_obj:
            result = find_key(key, sub_obj)
            if result is not None:
                return result
    # Return None if the key is not found
    return None


def fetch_package_data_UI(package_name):
    print(f"fetching package for {package_name}")

    # URL of the npm registry API for the specified package
    url = [
        f"https://registry.npmjs.org/{package_name}",
        f"https://registry.npmjs.org/@{package_name}",
    ]
    # Make an HTTP GET request to the API
    len_url = len(url)
    retry = 0
    license, repository_url, family = {None}, {None}, {None}
    while retry < len_url:
        response = requests.get(url[retry])
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            package_data = response.json()
            # Get the license and Git repository URL from the response
            # license = package_data.get("license", {}).get("type")
            license = package_data.get("license", {})
            if "url" in package_data:
                repository_url = package_data.get("repository", {}).get("url")
            elif "homepage" in package_data:
                repository_url = package_data.get("homepage")
            else:
                repository_url = find_key("url", package_data)
                if not repository_url:
                    repository_url = f"https://github.com/{url[retry].split('/')[1]}"

            if "keywords" in package_data:
                family = package_data.get("keywords")
                if not family:
                    family = package_name
                    break
                if isinstance(family, list):
                    if family and len(family) > 1:
                        family = family[1]
                    else:
                        family = family[0]
            else:
                family = url[retry].split("/")[-1]

            # repository_url = package_data.get("repository", {}).get("url") if "url" in package_data.get("repository") else package_data.get("homepage")
            # Return the license and Git repository URL as a tuple

            break

        else:
            # If the request was not successful, raise an exception
            retry += 1

        if retry == len(url):
            print(
                f"Error fetching package data: {response.status_code} {response.reason}"
            )

    return (family, license, repository_url)


def get_license_link_UI(repository_url):
    try:
        # Parse the repository URL
        # print(f"repository is {repository_url}")
        parsed_url = urlparse(repository_url)
        # Check if the host is "github.com"
        if parsed_url.netloc == "github.com":
            # Extract the repository information from the path
            path_parts = parsed_url.path.strip("/").split("/")
            if len(path_parts) >= 2:
                username = path_parts[-2]
                repository_name = path_parts[-1].replace(".git", "")
                # Construct the URL of the license file on raw.githubusercontent.com
                license_url = f"https://raw.githubusercontent.com/{username}/{repository_name}/main/LICENSE"
                response = requests.get(license_url)
                if response != 200:
                    license_url = f"{repository_url}/blob/master/LICENSE"
                return license_url

        else:
            host = parsed_url.hostname.split(".")[0]
            license_url = f"https://github.com/{host}/{host}/blob/master/LICENSE"
            return license_url

    except:
        print(f"None Repo ")

    # If the repository URL doesn't contain the necessary information to construct the license URL, return None
    return None


if __name__ == "__main__":
    family, license, repository_url = fetch_package_data_UI("name-all-modules-plugin")

    # Get the license link
    license_link = get_license_link_UI(repository_url)

    # Print the license, Git repository URL, and license link
    print(f"The license for  is {license}")
    print(f"The Git repository URL for  is {repository_url}")
    print(f"The family  for  {family}")

    if license_link is not None:
        print(f"The license link for  is {license_link}")
    else:
        print(f"Unable to construct a license link from the repository URL")
