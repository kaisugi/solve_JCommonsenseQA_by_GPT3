import openai
from tqdm import tqdm

import argparse
import json
import os
import sys
import time

openai.api_key = os.getenv("OPENAI_API_KEY")


def main(args):
    results_arr = []

    with open(args.test_file, "r") as fi, \
        open(args.prediction_file, "w") as fo:
        for line in tqdm(fi.readlines()):
            tmp_dic = json.loads(line)

            q_id = tmp_dic["q_id"]
            question = tmp_dic["question"]
            choice0 = tmp_dic["choice0"]
            choice1 = tmp_dic["choice1"]
            choice2 = tmp_dic["choice2"]
            choice3 = tmp_dic["choice3"]
            choice4 = tmp_dic["choice4"]
            true_label = tmp_dic["label"]

            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=f"Question: {question}\n0: {choice0}\n1: {choice1}\n2: {choice2}\n3: {choice3}\n4: {choice4}\nAnswer:",
                temperature=0,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )

            raw_answer = response["choices"][0]["text"]
            stripped_answer = raw_answer.strip()

            # case where choice number is predicted
            if stripped_answer[0] in ["0", "1", "2", "3", "4"]:
                predicted_answer = int(stripped_answer[0])
            # case where choice text is predicted
            else:
                if stripped_answer == choice0:
                    predicted_answer = 0
                elif stripped_answer == choice1:
                    predicted_answer = 1
                elif stripped_answer == choice2:
                    predicted_answer = 2
                elif stripped_answer == choice3:
                    predicted_answer = 3
                elif stripped_answer == choice4:
                    predicted_answer == 4
                else:
                    predicted_answer == None


            fo.write(f"{predicted_answer}\n")

            results_arr.append(1 if predicted_answer == true_label else 0)

            # notify if the model produces an incorrect answer
            if predicted_answer != true_label:
                print(f"Incorrect answer at q_id {q_id}, true: {true_label}, predicted: {predicted_answer}")
                sys.stdout.flush()

            # take sleep because too many requests will cause API restrictions
            time.sleep(4)


    print(f"Accuracy: {sum(results_arr) / len(results_arr)} ( {sum(results_arr)} / {len(results_arr)} )")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--test_file",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--prediction_file",
        type=str,
        required=True,
    )
    args = parser.parse_args()

    main(args)
