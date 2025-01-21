import os

def merge_conll_files(folder_path, output_file):
    """
    Merges all .conll files from the given folder into a single output file.

    Parameters:
    folder_path (str): Path to the folder containing .conll files.
    output_file (str): Path to the output file where the merged content will be saved.
    """
    try:
        # Open the output file in write mode
        with open(output_file, 'w', encoding='utf-8') as outfile:
            # Loop through each .conll file in the folder
            for filename in os.listdir(folder_path):
                if filename.endswith('.conll'):
                    file_path = os.path.join(folder_path, filename)
                    # Read and write the content of each .conll file
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        outfile.write(infile.read() + '\n')  # Add newline between files
        print(f"All .conll files from {folder_path} merged successfully into {output_file}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

def fix_conll_labels(input_file, output_file):
    """
    Fix label inconsistencies in a .conll file:
    1. Convert all entity labels to uppercase (e.g., 'b-per' -> 'B-PER').
    2. Replace any out-of-vocabulary or incorrect entity labels (e.g., 'I-phone') with 'O'.

    Parameters:
    input_file (str): Path to the input .conll file.
    output_file (str): Path to save the cleaned .conll file.
    """
    valid_labels = {'B-PRODUCT', 'I-PRODUCT', 'B-PRICE', 'I-PRICE', 'B-LOC', 'I-LOC', 'O'}
     # Mapping dictionary for PROD to Product
    label_mapping = {
        'B-PROD': 'B-PRODUCT',
        'I-PROD': 'I-PRODUCT'
    }
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            if line.strip():
                parts = line.strip().split()

                if len(parts) > 1:
                    token, label = parts[0], parts[-1]  # Assuming token is the first and label is the last column
                    label = label.upper()  # Convert the label to uppercase

                     # Map B-PROD/I-PROD to B-Product/I-Product
                    if label in label_mapping:
                        label = label_mapping[label]

                    # If label is invalid, replace it with 'O'
                    if label not in valid_labels:
                        label = 'O'

                    outfile.write(f"{token} {label}\n")
            else:
                outfile.write("\n")  # Preserve sentence boundaries

    print(f"Labels fixed and saved to {output_file}")