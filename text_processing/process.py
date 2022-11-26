from utils import process_content

## roots
roots = ["atom", "physik", "kern", "teil"]
words_map = process_content("../content.csv", roots, '../result.csv')
