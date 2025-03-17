#!/usr/bin/env python3
import os
import json
import subprocess
import datetime

def save_instagram_metadata(url, output_dir=None):
    """
    Use gallery-dl to save Instagram metadata from a given URL.
    
    Args:
        url (str): The Instagram URL to extract metadata from
        output_dir (str, optional): Directory to save metadata. Defaults to a timestamped folder.
    """
    if not output_dir:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = os.path.join(os.getcwd(), f"instagram_metadata_{timestamp}")
    
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, "metadata.json")
    
    # Configure gallery-dl options
    cmd = [
        "gallery-dl",
        "-o",
        "max-posts=12",  # Limit to 12 posts
        "--dump-json",  # Output results as JSON
        url,
    ]
    
    try:
        print(f"Extracting metadata from {url}...")
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        if result.stdout:
            # Parse and pretty-print the JSON
            metadata = json.loads(result.stdout)
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            print(f"Metadata successfully saved to {output_file}")
            return output_file
        else:
            print("No metadata returned from gallery-dl")
            return None
            
    except subprocess.CalledProcessError as e:
        print(f"Error executing gallery-dl: {e}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
        return None
    except json.JSONDecodeError:
        print(f"Error parsing JSON output from gallery-dl")
        return None

if __name__ == "__main__":
    # URL for Powell's Lawn Care Instagram reels
    instagram_url = "https://www.instagram.com/powellslawncare/reels"
    save_instagram_metadata(instagram_url)
