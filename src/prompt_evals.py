
from request import Request, add_user_message
import json

request= Request()



def run_prompt(test_case):
    """Merges the prompt and test case input, then returns the result"""
    prompt=f"""
Please solve the following task:

{test_case["task"]}
"""
    messages = []
    add_user_message(messages, prompt)
    output = request.chat(messages)
    return output



def run_test_case(test_case):
    """Calls run_prompt, then grades the result"""
    output = run_prompt(test_case)

    # TODO - Grading
    score = 10
    
    return {
        "output": output,
        "test_case": test_case,
        "score": score
    }



def run_eval(dataset):
    """Loads the dataset and calls run_test_case with each case"""
    results=[]

    for test_case in dataset:
        result = run_test_case(test_case)
        results.append(result)

    return results




if __name__=="__main__":
    with open("dataset.json", "r") as f:
        dataset = json.load(f)
        results = run_eval(dataset)
        print(json.dumps(results, indent=2))