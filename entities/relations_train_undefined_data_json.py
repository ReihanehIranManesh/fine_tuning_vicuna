import csv
import json
import random

file_path = "atomic_concepts_prompt.txt"
NUM_ONE_EX = 10
NUM_ZERO_EX = 10
TOTAL = NUM_ONE_EX * 140

try:
    file = open(file_path, "r")
    MAIN_PROMPT = file.read()
    file.close()
except FileNotFoundError:
    print("File not found.")

file_path = "atomic_properties_wikidata_examples.csv"
full_list_kv = []

try:
    with open(file_path, "r") as file:
        csv_reader = csv.reader(file)
        first = True
        for row in csv_reader:
            if first:
                first = False
                continue
            # Process prompt
            prompt = MAIN_PROMPT.replace("<atomic_concept>", row[0].lstrip())

            temp_ls = []
            for i in range(1, NUM_ONE_EX + 1):
                formatted_prompt = prompt.replace("<from_interpreter>", row[i].lstrip())
                temp_ls.append(row[i].lstrip())

            full_list_kv.append({row[0].lstrip(): temp_ls})

except FileNotFoundError:
    print("File not found.")


file_path = "atomic_concepts_prompt.txt"

try:
    file = open(file_path, "r")
    MAIN_PROMPT = file.read()
    file.close()
except FileNotFoundError:
    print("File not found.")

file_path = "atomic_properties_wikidata_examples.csv"

try:
    with open(file_path, "r") as file:
        csv_reader = csv.reader(file)
        first = True
        count = 0
        output = []
        entity_id = 0
        for row in csv_reader:
            if first:
                first = False
                continue
            # Process prompt
            prompt = MAIN_PROMPT.replace("<atomic_concept>", row[0].lstrip())

            for i in range(1, NUM_ONE_EX + 1):
                entity_dict = {}
                entity_dict["id"] = "identity_" + str(count)
                entity_ls = []

                human_dict = {}
                human_dict["from"] = "human"
                formatted_prompt = prompt.replace("<from_interpreter>", row[i].lstrip())
                human_dict["value"] = formatted_prompt
                entity_ls.append(human_dict)

                model_dict = {}
                model_dict["from"] = "gpt"
                model_dict["value"] = 1
                entity_ls.append(model_dict)

                entity_dict["conversations"] = entity_ls

                output.append(entity_dict)
                count += 1

            numbers = set()

            while len(numbers) < NUM_ZERO_EX:
                num = random.randint(0, TOTAL - 1)
                if num < entity_id * NUM_ONE_EX or num >= (entity_id + 1) * NUM_ONE_EX:
                    numbers.add(num)

            numbers = list(numbers)

            for i in range(1, NUM_ZERO_EX + 1):
                entity_dict = {}
                entity_dict["id"] = "identity_" + str(count)
                entity_ls = []

                human_dict = {}
                human_dict["from"] = "human"

                entity = numbers[i - 1]
                value = entity % NUM_ONE_EX
                key = entity // NUM_ONE_EX

                entity = list(full_list_kv[key].values())[0][value]
                formatted_prompt = prompt.replace("<from_interpreter>", entity)

                human_dict["value"] = formatted_prompt
                entity_ls.append(human_dict)

                model_dict = {}
                model_dict["from"] = "gpt"
                model_dict["value"] = 0
                entity_ls.append(model_dict)

                entity_dict["conversations"] = entity_ls

                output.append(entity_dict)
                count += 1

            entity_id += 1


except FileNotFoundError:
    print("File not found.")

with open("entities.json", 'a') as f:
    # Serializing json
    json_object = json.dumps(output, indent=4)
    f.write(json_object)
