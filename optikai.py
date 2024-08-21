import requests
import re
import json

# Step 1: Fetch the main page
url = 'https://livzmc.net/optikai/downloads/'
response = requests.get(url)
main_page_content = response.text

# Step 2: Use regex to find all 'View more downloads' links
view_more_pattern = r'<a class="hover:underline" href="([^"]+)">View more downloads</a>'
view_more_links = re.findall(view_more_pattern, main_page_content)

# Initialize an empty list to store all download data
all_downloads = []

for view_more_link in view_more_links:
    view_more_url = 'https://livzmc.net' + view_more_link

    # Step 3: Fetch the "View more downloads" page
    print("### " + view_more_url)
    response = requests.get(view_more_url)
    downloads_page_content = response.text

    # Step 4: Use regex to find all 'Mirror' links
    mirror_pattern = r'<a class="hover:underline" href="([^"]+)">Mirror</a>'
    mirror_links = re.findall(mirror_pattern, downloads_page_content)

    for mirror_link in mirror_links:
        mirror_url = 'https://livzmc.net' + mirror_link

        # Step 5: Fetch the "Mirror" page
        print("- " + mirror_url)
        response = requests.get(mirror_url)
        mirror_page_content = response.text

        # Step 6: Use regex to find the download details
        download_pattern = (
            r'<a rel="nofollow" href="https://livzmc\.net/optikai/download\?f=([^"]+)&x=[^"]+" '
            r'class="hover:underline text-lg">Download</a>.*?'
            r'<p>([^<]+)</p>.*?'
            r'<p class="text-xs" style="font-size: xx-small;">([^<]+)</p>.*?'
            r'<p class="text-xs" style="font-size: xx-small;">([^<]+)</p>.*?'
            r'<p class="text-xs" style="font-size: xx-small;">([^<]+)</p>.*?'
            r"launch the Minecraft version '([^']+)'"
        )
        download_details = re.search(download_pattern, mirror_page_content, re.DOTALL)
        if download_details:
            filename = download_details.group(1)
            forge_version = download_details.group(2)
            date = download_details.group(3)
            # size = download_details.group(4)
            checksum = download_details.group(5)
            minecraft_version = download_details.group(6)

            # Step 7: Process the filename
            name = filename.replace('preview_', '').replace('OptiFine_', '').replace(minecraft_version + '_', '').replace('.jar', '')

            # Step 8: Construct the download entry
            download_entry = {
                "filename": filename,
                "forge": forge_version,
                "time": date,
                "ispreview": "pre" in filename.lower(),
                # "size": size,
                "filehash": checksum,
                "mcversion": minecraft_version,
                "name": name
            }

            # Add the entry to the list
            all_downloads.append(download_entry)

# Step 9: Save all collected data to a JSON file
with open('raw-optikai.json', 'w', encoding='utf-8') as f:
    json.dump(all_downloads, f, ensure_ascii=False, indent=4)

with open('optikai.json', 'w', encoding='utf-8') as f:
    json.dump(all_downloads, f, ensure_ascii=False)

print(f"Saved {len(all_downloads)} download entries to optikai.json")
