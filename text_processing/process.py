import csv
import pandas as pd
from utils import sanitize_text, find_words_map_by_roots, merge_word_maps


def process_content(file_name, roots, save_to):
    maps = []
    with open(file_name, 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            sanitized = sanitize_text(row[0])

            word_map = find_words_map_by_roots(sanitized, roots)
            maps.append(word_map)

    result = merge_word_maps(maps, roots)

    # write the result into csv file
    if save_to:
        with open(save_to, 'w') as file:
            writer = csv.writer(file)
            first_row = result.keys()
            writer.writerow(first_row)

            length = max([len(result[w]) for w in result])
            for r in result:
                if len(result[r]) < length:
                    result[r] += (length - len(result[r])) * ['']
            df = pd.DataFrame(result)
            df.to_csv(save_to, index=False)
            print(df)

    return result


# roots
rs = ["atom", "physik", "kern", "teil", "radio", "licht", "spektr", "optik"]
words_map = process_content(
    roots=["atom", "physik", "kern", "teil", "radio", "licht", "spektr", "optik"],
    file_name="../uncategorized_corpus.csv.csv",
    save_to='../uncategorized_result.csv'
)
