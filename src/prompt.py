
from request import Request, add_user_message, add_assistant_message
from prompt_evaluator import PromptEvaluator


request= Request()



def run_prompt(prompt_inputs):
    prompt=f"""
What should this person eat?

- Height: {prompt_inputs["height"]}
- Weight: {prompt_inputs["weight"]}
- Goal: {prompt_inputs["goal"]}
- Dietary resctrictions: {prompt_inputs["restrictions"]}
"""

    messages = []
    add_user_message(messages, prompt)
    output: str = request.chat(messages)
    return output




if __name__=="__main__":
    evaluator= PromptEvaluator(max_concurrent_tasks = 3)
    results= evaluator.run_evaluation(
        run_prompt_function= run_prompt,
        dataset_file="dataset.json",
        extra_criteria ="""
        The output should include:
        - Daily caloric total
        - Macronutrient breakdown
        - Meals with exact foods, portions, and timing
    """
    )