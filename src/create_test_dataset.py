# generate test dataset

import json
from request import Request, add_user_message, add_assistant_message

def generate_dataset():
    prompt= """
Generate a evaluation dataset for a pompt evaluation. The dataset will be used to evaluate prompts that
generate Python, JSON, or Regrex specifically for AWS-related tasks. Generate an array of JSON objects, 
each representing task that requires Python, JSON, or a Regex to complete.

Example output:
``` json
[
  {
    "task": "Description of task",
    "format": "json" or "python" or "regex"
    "solution_criteria": "Key criteria for evaluating the solution"
  },
  ...additional
]
```

* Focus on tasks that can be solved by writing a single Python function, a single JSON object, or a regular expression.
* Focus on tasks that do not require writing much code

Please generate 3 objects.
"""

    messages=[]
    request=Request()
    add_user_message(messages, prompt)
    add_assistant_message(messages, "```json")
    text= request.chat(messages, stop_sequences=["```"])
    return json.loads(text)



dataset=generate_dataset()
print(dataset)


# save the generated dataset to a file in the solution folder
with open('dataset.json', 'w') as f:
    json.dump(dataset, f, indent=2)



if __name__=="__main__":
    generate_dataset()