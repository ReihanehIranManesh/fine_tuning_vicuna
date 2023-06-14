import csv

file_path = "atomic_relations_prompt"

try:
    file = open(file_path, "r")
    prompt = file.read()
    file.close()
except FileNotFoundError:
    print("File not found.")

file_path = "atomic_relations_wikidata.csv"

try:
    with open(file_path, "r") as file:
        csv_reader = csv.reader(file)
        first = True
        count = 0
        for row in csv_reader:
            if first:
                first = False
                continue
            count += 1
            # Process prompt
            formatted_prompt = prompt.replace("{input}", row[0].lstrip())
            formatted_prompt = formatted_prompt.replace("{output}", row[1].lstrip())

            countstr = str(count)
            if len(countstr) == 1:
                countstr = "0" + countstr

            file_path_data = "relations_gt/" + countstr + ".csv"

            try:
                with open(file_path_data, "r") as file:
                    csv_reader_data = csv.reader(file)
                    for row_d in csv_reader_data:
                        with open("train_data", 'a') as f:
                            # Process prompt
                            f.write("prompt: " + formatted_prompt + "Input: " + row_d[0].lstrip())
                            # Process completion
                            f.write("\n" + "completion: " + row_d[1].lstrip() + "\n")
                file.close()

            except FileNotFoundError:
                print("File not found.")

except FileNotFoundError:
    print("File not found.")
