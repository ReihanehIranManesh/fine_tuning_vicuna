import csv
import json

file_path = "../../generate_training_data_vicuna/relations/atomic_relations_except_prompt.txt"

try:
    file = open(file_path, "r")
    prompt = file.read()
    file.close()
except FileNotFoundError:
    print("File not found.")

file_path = "../../generate_training_data_vicuna/relations/atomic_relations_wikidata.csv"

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
            formatted_prompt_exp = formatted_prompt.replace("{exception}", row[2].lstrip())

            countstr = str(count)
            if len(countstr) == 1:
                countstr = "0" + countstr

            ### Prompt 1
            file_path_data = "../../generate_training_data_vicuna/relations/relations_gt/" + countstr + "_corrupted_1" + ".csv"

            try:
                with open(file_path_data, "r") as file:
                    csv_reader_data = csv.reader(file)
                    for row_d in csv_reader_data:
                        with open("data/train_data.json", 'a') as f:
                            temp_dict = {}
                            temp_dict["instruction"] = formatted_prompt_exp
                            temp_dict["input"] = row_d[0].lstrip()
                            temp_dict["output"] = row_d[1].lstrip()
                            # Serializing json
                            json_object = json.dumps(temp_dict, indent=4)
                            f.write(json_object)
                            f.write(",")

                file.close()

            except FileNotFoundError:
                print("File not found.")

            ### Prompt 2
            formatted_prompt_exp = formatted_prompt.replace("{exception}", row[3].lstrip())
            file_path_data = "../../generate_training_data_vicuna/relations/relations_gt/" + countstr + "_corrupted_2" + ".csv"

            try:
                with open(file_path_data, "r") as file:
                    csv_reader_data = csv.reader(file)
                    for row_d in csv_reader_data:
                        with open("data/train_data.json", 'a') as f:
                            temp_dict = {}
                            temp_dict["instruction"] = formatted_prompt_exp
                            temp_dict["input"] = row_d[0].lstrip()
                            temp_dict["output"] = row_d[1].lstrip()
                            # Serializing json
                            json_object = json.dumps(temp_dict, indent=4)
                            f.write(json_object)
                            f.write(",")

                file.close()

            except FileNotFoundError:
                print("File not found.")

except FileNotFoundError:
    print("File not found.")
