import csv
import argparse

def generate_mermaid_from_csv(csv_filepath):
    """
    Generates mermaid from ADDI Exports
    """
    mermaid_code = """---
config:
  layout: elk
  theme: redux
---
flowchart TD
"""
    edges = set()
    nodes_with_labels = {} # Store node and its level

    try:
        with open(csv_filepath, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            next(reader)  # Skip the header row

            for row in reader:
                source = row[0]
                if not source:
                    continue

                levels = [source] + [item for item in row[2:] if item]

                for i, node in enumerate(levels):
                    node = node.strip()
                    if node not in nodes_with_labels:
                        escaped_node = node.replace('"', '\\"') # Escape double quotes within labels
                        mermaid_code += f'    {node}["{escaped_node}"]\n'
                        nodes_with_labels[node] = i + 1 # Level starts from 1

                for i in range(len(levels) - 1):
                    node1 = levels[i].strip()
                    node2 = levels[i+1].strip()
                    edge = f'{node1} --> {node2}'
                    if edge not in edges:
                        mermaid_code += f"    {node1} --> {node2}\n"
                        edges.add(edge)

            # Adding dynamic styling based on levels
            for node, level in nodes_with_labels.items():
                color = ""
                if level == 1:
                    color = "#00C853" # Green for level 1
                elif level == 2:
                    color = "#FFC107" # Amber for level 2
                elif level == 3:
                    color = "#F44336" # Red for level 3
                if color:
                    mermaid_code += f"    style {node} fill:{color}\n"

    except FileNotFoundError:
        return f"Error: CSV file not found at {csv_filepath}"
    except Exception as e:
        return f"An error occurred: {e}"

    return mermaid_code

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Mermaid flowchart code from an ADDI exported CSV.")
    parser.add_argument("csv_file", help="Path to the ADDI exported CSV file")
    args = parser.parse_args()

    mermaid_code = generate_mermaid_from_csv(args.csv_file)
    print(mermaid_code)
