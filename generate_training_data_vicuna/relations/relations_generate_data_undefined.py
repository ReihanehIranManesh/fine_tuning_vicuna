import csv
import openai

samples_n = 10
OPENAI_API_KEY = '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'
openai.api_key = OPENAI_API_KEY

file_path = "atomic_relations_prompt_undefined"

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
            formatted_prompt = formatted_prompt.replace("{number}", str(samples_n))

            message = [{"role": "user",
                        "content": formatted_prompt}]

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=message)
            data = response['choices'][0]['message']['content']

            countstr = str(count)
            if len(countstr) == 1:
                countstr = "0" + countstr

            file_path_data = "relations_gt/" + countstr + "_undefined.csv"

            # Open a file in write mode ('w'). If the file does not exist, it will be created.
            with open(file_path_data, 'w') as f:
                f.write(data)

except FileNotFoundError:
    print("File not found.")
