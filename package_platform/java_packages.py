import requests

import json
import time

import requests
import xml.etree.ElementTree as ET

import requests
import xml.etree.ElementTree as ET

import requests
from bs4 import BeautifulSoup

with open("package.json", "r") as f:
    data = json.load(f)
    # print(data)


def get_package_license(group_id, package_name):
    """
    This function retrieves the license information for a Maven package from the Libraries.io API based on the package's group ID and name.

    Parameters:
    - group_id (str): The group ID of the Maven package.
    - package_name (str): The name of the Maven package.

    Returns:
    - A dictionary containing the name and URL of the package's license.

    Error Handling:
    - If the API request is unsuccessful, a message will be printed to the console and a dictionary with default values (name="Unknown", url="") will be returned.
    - If there is an error retrieving the license URL for a string license, an empty string will be returned.

    Note:
    - If the package's license is a string (i.e. only one license), the function will attempt to retrieve the license URL using the 'get_license_url' function. If the license name is not found in the 'license_mapping' dictionary in the 'get_license_url' function, an empty string will be returned.
    """

    url = f"https://libraries.io/api/maven/{group_id}:{package_name}"
    # print(url)
    response = requests.get(url)
    time.sleep(6)
    license_name = "Unknown"
    license_url = ""

    if response.ok:
        package_info = response.json()
        # print(package_info)
        versions = package_info.get("versions", [])
        licenses = versions[-1]["original_license"]
        if not licenses:
            licenses = package_info.get("licenses", [])

        if isinstance(licenses, list) and licenses:
            license_name = licenses[0]
        elif isinstance(licenses, str) and licenses:
            license_name = licenses

        # license_url = licenses[0].get("url", "")
        license = license_name.replace(" ", "-").replace(".", "-").replace(",", "")

        if license_name in data["package_details"]["license_details"]:
            license_ = data["package_details"]["license_details"][license_name]
            license_name = license_[0]
            license_url = license_[1]
        elif license in data["package_details"]["license_details"]:
            license_ = data["package_details"]["license_details"][license]
            license_name = license_[0]
            license_url = license_[1]
        else:
            license_url = get_license_url(license)

        print(license_name, license_url)
        return {"name": license_name, "url": license_url}

    else:
        print(
            f"Failed to retrieve license info for {package_name}: {response.status_code}"
        )
        return {"name": "Unknown", "url": ""}


def get_license_url(license_name="Apache-2.0"):
    """
    This function retrieves the URL for a license based on its name from the SPDX website.

    Parameters:
    - license_name (str): The name of the license. Defaults to "Apache-2.0".

    Returns:
    - The URL of the license.

    Error Handling:
    - If the license name is not found on the SPDX website, an error message will be printed to the console and an empty string will be returned.
    """
    if license_name == "The Apache Software License, Version 2.0":
        license_name = "Apache-2.0"

    # url = f"https://spdx.org/licenses/{license_name}.html"
    url = f"https://opensource.org/licenses/{license_name}"

    response = requests.get(url)
    license_url = ""
    if response.ok:
        license_url = response.url
        # print(f"{license_name} URL: {license_url}")
    else:
        # print(f"{license_name} not found on the SPDX website.")
        license_url = ""
    return license_url


def get_package_license_org(group_id, package_name, version):
    url = f"https://central.sonatype.com/artifact/{group_id}/{package_name}/{version}"
    # url = 'https://central.sonatype.com/artifact/org.codelibs.elasticsearch.module/aggs-matrix-stats/7.10.2'
    print(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    license_name, license_url = "", ""
    # Find the pre tag with the class nx-pre POMFile_pomFileBody__EQf9t and get its text content
    pre_tag = soup.find("pre", {"class": "nx-pre POMFile_pomFileBody__EQf9t"})
    if pre_tag:
        pre_text = pre_tag.get_text()
        if pre_text:
            # Find the license information within the pre tag text content
            license_start = pre_text.find("<name>")
            license_end = pre_text.find("</name>")
            license_name = pre_text[license_start + len("<name>") : license_end]

            url_start = pre_text.find("<url>")
            url_end = pre_text.find("</url>")
            license_url = pre_text[url_start + len("<url>") : url_end]

            # print('License name:', license_name)
            # print('License URL:', license_url)
    return {"name": license_name, "url": license_url}


def get_package_details(library_name):
    formatted_library_name = (
        str(library_name).replace(",", "+").replace(" ", "+").replace(":", "+")
    )
    search_url = (
        f"https://search.maven.org/solrsearch/select?q={formatted_library_name}"
    )

    # Send a GET request to search for the library on the Maven Central Repository
    # search_url = f"https://search.maven.org/solrsearch/select?q={library_name}"
    # print(search_url)
    group_id = None
    artifact_id = None
    response = requests.get(search_url)

    if response.ok:
        # Parse the JSON response
        response_json = response.json()
        docs = response_json["response"]["docs"]

        if len(docs) > 0:
            # Extract the group ID and artifact ID from the first search result
            group_id = docs[0]["g"]
            artifact_id = docs[0]["a"]

            # Print the group ID and artifact ID
            # print(f"Group ID: {group_id}")
            # print(f"Artifact ID: {artifact_id}")
        else:
            print(f"No search results found for '{library_name}'.")
    return {"group_id": group_id, "artifact_id": artifact_id}


if __name__ == "__main__":
    package_name = "aggs-matrix-stats"
    version = "7.6.2"
    # group_id = get_group_id(package_name, version)
    # print(group_id)
    # get_family_name = get_family_name(package_name)
    # license_info = get_package_license(package_name, version)
    """license_info = get_package_license(group_id, package_name)
    print('Family name for package {}: {}'.format(package_name, group_id))

    print(f"License name: {license_info['name']}")
    print(f"License URL: {license_info['url']}")"""

    with open("package.json", "r") as f:
        data = json.load(f)

    package_name = "jersey-servlet"

    # get_package_license(group_id, package_name)

    if package_name in data["package_details"]["package"]:
        package_info = get_package_details(
            data["package_details"]["package"][package_name]
        )
    else:
        package_info = get_package_details(package_name)

    family = package_info["group_id"]
    print(family)
    license_info = get_package_license(
        package_info["group_id"], package_info["artifact_id"]
    )
    license, license_link = license_info["name"], license_info["url"]
    # if license.relace(" ","") in
    print(license, license_link)
