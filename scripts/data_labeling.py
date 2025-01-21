import pandas as pd

class EntityLabeler:
    def __init__(self):
        pass

    # Function to label entities in a message
    def label_entities(self, message):
        labels = []
        tokens = message.split()

        for token in tokens:
            # Price entity detection
            if "ዋጋ" in token or "ብር" in token:
                if "ዋጋ" == token:
                    labels.append((token, 'B-PRICE'))
                else:
                    labels.append((token, 'I-PRICE'))
            # Location entity detection
            elif any(loc in token for loc in ["መገናኛ", "አዲስ አበባ", "ጀሞ", "ዘፍመሽ","ባህር ዳር","ጎንደር"]):
                if token == "መገናኛ" or token == "ጀሞ":
                    labels.append((token, 'B-LOC'))
                else:
                    labels.append((token, 'I-LOC'))
            # Product entity detection
            elif "ምርት" in token or "ምርጥ" in token:
                if token == "ምርት":
                    labels.append((token, 'B-PRODUCT'))
                else:
                    labels.append((token, 'I-PRODUCT'))
            else:
                labels.append((token, 'O'))  # Outside any entity

        return labels

    # Function to create CoNLL formatted output from a DataFrame with dynamic message range
    def create_conll_format(self, dataframe, start_message, batch_size):
        conll_lines = []

        # Calculate the end message index
        total_messages = len(dataframe)
        start_message = max(0, start_message)  # Ensure start is not negative
        end_message = min(total_messages, start_message + batch_size)  # Ensure end doesn't exceed the data size

        for index in range(start_message, end_message):
            message = dataframe.iloc[index]['Preprocessed_Message']
            labeled_entities = self.label_entities(message)

            for token, label in labeled_entities:
                conll_lines.append(f"{token} {label}")

            # Add a blank line after each message
            conll_lines.append("")

        return "\n".join(conll_lines)

    # Function to save CoNLL formatted data to a text file
    def save_conll_to_file(self, conll_output, filename):
        with open(f'../data/{filename}', 'w', encoding='utf-8') as f:
            f.write(conll_output)
        print(f"CoNLL format data has been saved to '{filename}'")