import csv
import json

def convert_csv_to_json(csv_path, json_path):
    tags_data = []
    
    with open(csv_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Split aliases string into list, strip whitespace, and filter out empty strings
            aliases = [alias.strip() for alias in row['aliases'].split(',') if alias.strip()]
            
            tag_entry = {
                "tag": row['tag'].strip(),
                "category": row['category'].strip(),
                "postCount": int(row['post count']),
                "aliases": aliases
            }
            tags_data.append(tag_entry)
    
    # Create a searchable index that includes both tags and aliases
    search_index = {}
    for entry in tags_data:
        # Add the main tag
        search_index[entry['tag'].lower()] = entry
        # Add all aliases
        for alias in entry['aliases']:
            search_index[alias.lower()] = entry

    output_data = {
        "tags": tags_data,
        "searchIndex": search_index
    }
    
    with open(json_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(output_data, jsonfile, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    convert_csv_to_json('tags/danbooru-12-10-24-underscore.csv', 'tags_data.json')
