import requests
import json

import requests
import json

with open("package.json", "r") as f:
    package_data = json.load(f)


def fetch_licence(license_name):
    api_url = "https://api.opensource.org/licenses/" + license_name
    license_url = ""

    response = requests.get(api_url)

    if response.status_code == 200:
        license_url = response.json()["details_url"]
        print(license_url)
    else:
        print("Failed to retrieve license information.")
    return license_url


def get_license(package_name):
    print(package_name)
    if package_name in package_data["package_details"]["pypackages_details"]:
        license = package_data["package_details"]["pypackages_details"][package_name][0]
        license_url = package_data["package_details"]["pypackages_details"][
            package_name
        ][1]

        return license, license_url

    url = f"https://pypi.org/pypi/{package_name}/json"
    # print(url)
    response = requests.get(url)
    if response.status_code == 404:
        return f"Package {package_name} not found on PyPI."
    elif response.status_code != 200:
        return f"Error while fetching package information. Status code: {response.status_code}"
    data = json.loads(response.content)
    info = data.get("info", {})
    # print(info)
    license = info.get("license", "")
    family = info.get("summary", " ")
    urls = info.get("project_urls", {})

    license_url = ""
    if not urls:
        return license, ""
    license_file_names = ["LICENSE", "LICENSE.md", "LICENSE.txt", "LICENSE.rst"]
    for file_name in license_file_names:
        if "Source Code" in urls:
            license_url = f"{urls['Source Code']}/blob/master/{file_name}"
        elif "Homepage" in urls:
            license_url = f"{urls['Homepage']}/blob/master/{file_name}"
        else:
            print(package_name)
            license_url = ""
        if license_url:
            response = requests.get(license_url)
            if response.status_code == 200:
                return license, license_url
    if not license_url:
        license_url = fetch_licence(license)
    return license, license_url


if __name__ == "__main__":
    # Example usage
    with open("package.json", "r") as f:
        data = json.load(f)
    license, license_url = get_license("pytz")
    print(f"License: {license}")
    print(f"License URL: {license_url}")
    # print(f"family: {family}")
