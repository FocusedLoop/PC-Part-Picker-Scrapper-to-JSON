import json
import re

# Paths to files
BUILD_FILE = r"C:\Users\joshu\OneDrive\Desktop\temp_python_workspace\bot\scrappedFiles\pc_build_parts.json"
DEFAULT_PRICES_FILE = r"C:\Users\joshu\OneDrive\Desktop\temp_python_workspace\bot\cleaning\default_prices.json"
OUTPUT_FILE = r"C:\Users\joshu\OneDrive\Desktop\temp_python_workspace\bot\scrappedFiles\pc_build_parts_cleaned.json"

def detect_brand_and_tier(part_type, part_name):
    name_lower = part_name.lower()
    brand = "Generic"
    tier = "mid" 

    # Detect brand then tier
    if "intel" in name_lower:
        brand = "Intel"
    elif "amd" in name_lower or "ryzen" in name_lower:
        brand = "AMD"
    elif "nvidia" in name_lower or "geforce" in name_lower or "rtx" in name_lower:
        brand = "Nvidia"

    if part_type == "CPU":
        if re.search(r"i3[-\s]", name_lower) or "ryzen 3" in name_lower:
            tier = "low"
        elif re.search(r"i9[-\s]", name_lower) or "ryzen 9" in name_lower:
            tier = "high"
        elif re.search(r"i7[-\s]", name_lower) or "ryzen 7" in name_lower:
            tier = "high"
        elif re.search(r"i5[-\s]", name_lower) or "ryzen 5" in name_lower:
            tier = "mid"

    elif part_type == "GPU":
        if any(x in name_lower for x in ["4090", "4080", "7900"]):
            tier = "high"
        elif any(x in name_lower for x in ["4070", "4060", "7800", "7700"]):
            tier = "mid"
        else:
            tier = "low"

    return brand, tier

# Convert prices to float
def parse_price(price_str):
    if not price_str:
        return None
    price_str_clean = re.sub(r'[^\d.]', '', price_str)
    try:
        return float(price_str_clean)
    except ValueError:
        return None

# Format back to string
def format_price(price_float):
    return f"${price_float:.2f}"

# Load mapped prices
def load_default_prices(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

def main():
    default_prices = load_default_prices(DEFAULT_PRICES_FILE)

    with open(BUILD_FILE, "r") as file:
        builds_data = json.load(file)

    # Process each build
    for build in builds_data:
        part_list = build.get("Part List", {}).get("Parts", [])
        total_price = 0.0

        for part in part_list:
            part_type = part.get("Type", "Unknown")
            part_name = part.get("Name", "Unknown")
            part_price_str = part.get("Price", None)

            # Parse or assign default price
            part_price = parse_price(part_price_str)
            if part_price is None or part_price == 0.0:
                brand, tier = detect_brand_and_tier(part_type, part_name)
                if part_type in default_prices:
                    if brand in default_prices[part_type]:
                        default_price = default_prices[part_type][brand].get(tier, 50.0)
                    else:
                        default_price = default_prices[part_type]["Generic"].get(tier, 50.0)
                else:
                    default_price = 50.0
                part["Price"] = format_price(default_price)
                part_price = default_price

            total_price += part_price
        build["Part List"]["Total"] = format_price(total_price)

    # Write cleaned data to output file
    with open(OUTPUT_FILE, "w") as outfile:
        json.dump(builds_data, outfile, indent=4)

    print(f"Data cleaned and saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
