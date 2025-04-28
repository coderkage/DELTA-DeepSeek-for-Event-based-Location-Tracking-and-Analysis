import json
import csv

# Input and output file paths
jsonl_file = "../coredata/test/5xus.jsonl"  # Replace with your actual file name
csv_file = "./datasets/usa.csv"

# Open the JSONL file and process each line
with open(jsonl_file, "r", encoding="utf-8") as infile, open(csv_file, "w", newline="", encoding="utf-8") as outfile:
    writer = csv.writer(outfile)
    # Write CSV header
    writer.writerow(["text", "disaster", "gpe"])

    for line in infile:
        data = json.loads(line.strip())  # Parse JSONL line and remove extra spaces/newlines
        text = data[0]
        entities = data[1].get("entities", [])

        disasters = []
        gpes = []

        # Extract entity values
        for entity in entities:
            if len(entity) == 3:  # Ensure correct format
                start, end, label = entity
                entity_text = text[start:end].strip()  # Slice text and remove extra spaces
                if label == "DISASTER":
                    disasters.append(entity_text)
                elif label == "GPE":
                    gpes.append(entity_text)

        # Join multiple entities with commas (or leave blank if none found)
        disaster_str = ", ".join(disasters) if disasters else ""
        gpe_str = ", ".join(gpes) if gpes else ""

        # Write to CSV
        writer.writerow([text, disaster_str, gpe_str])

print("CSV file created successfully!")
