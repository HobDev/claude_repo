# generate test dataset
import re
import json
import concurrent.futures
import threading
from textwrap import dedent
from request import Request, add_user_message, add_assistant_message

_thread_local= threading.local()

def get_request():
     if not hasattr(_thread_local, "request"):
          _thread_local.request = Request()
     return _thread_local.request


def render(template_string, variables):
        placeholders = re.findall(r"{([^{}]+)}", template_string)

        result = template_string
        for placeholder in placeholders:
            if placeholder in variables:
                result = result.replace(
                    "{" + placeholder + "}", str(variables[placeholder])
                )

        return result.replace("{{", "{").replace("}}", "}")


def generate_test_case(task_description, idea, prompt_inputs_spec=None):
        """Generate a single test case based on the task description and a specific idea"""
        if prompt_inputs_spec is None:
             prompt_inputs_spec={}
        example_prompt_inputs = ""
        for key, value in prompt_inputs_spec.items():
            val = value.replace("\n", "\\n")
            example_prompt_inputs += f'"{key}": "EXAMPLE_VALUE", // {val}\n'

        allowed_keys = ", ".join([f'"{key}"' for key in prompt_inputs_spec.keys()])

        prompt = """
        Generate a single detailed test case for a prompt evaluation based on:
        
        <task_description>
        {task_description}
        </task_description>
        
        <specific_idea>
        {idea}
        </specific_idea>
        
        <allowed_input_keys>
        {allowed_keys}
        </allowed_input_keys>
        
        Output Format:
        ```json
        {{
            "prompt_inputs": {{
            {example_prompt_inputs}
            }},
            "solution_criteria": ["criterion 1", "criterion 2", ...] // Concise list of criteria for evaluating the solution, 1 to 4 items
        }}
        ```
        
        IMPORTANT REQUIREMENTS:
        - You MUST ONLY use these exact input keys in your prompt_inputs: {allowed_keys}        
        - Do NOT add any additional keys to prompt_inputs
        - All keys listed in allowed_input_keys must be included in your response
        - Make the test case realistic and practically useful
        - Include measurable, concise solution criteria
        - The solution criteria should ONLY address the direct requirements of the task description and the generated prompt_inputs
        - Avoid over-specifying criteria with requirements that go beyond the core task
        - Keep solution criteria simple, focused, and directly tied to the fundamental task
        - The test case should be tailored to the specific idea provided
        - Quick to solve without requiring extensive computation or multi-step processing
        - Solvable with no more than 400 tokens of output
        - DO NOT include any fields beyond those specified in the output format

        Here's an example of a sample input with an ideal output:
        <sample_input>
        <sample_task_description>
        Extract topics out of a passage of text
        </sample_task_description>
        <sample_specific_idea>
        Testing with a text that contains multiple nested topics and subtopics (e.g., a passage about renewable energy that covers solar power economics, wind turbine technology, and policy implications simultaneously)
        </sample_specific_idea>

        <sample_allowed_input_keys>
        "content"
        </sample_allowed_input_keys>
        </sample_input>
        <ideal_output>
        ```json
        {
            "prompt_inputs": {
                "content": "The transition to renewable energy encompasses numerous interdependent dimensions. Solar photovoltaic technology has seen dramatic cost reductions, with panel efficiency improving 24% since 2010 while manufacturing costs declined by 89%, making it economically competitive with fossil fuels in many markets. Concurrently, wind energy has evolved through innovative turbine designs featuring carbon-fiber composite blades and advanced control systems that increase energy capture by 35% in low-wind conditions."
            },
            "solution_criteria": [
                "Includes all topics mentioned"   
            ]
        }
        ```
        </ideal_output>
        This is ideal output because the solution criteria is concise and doesn't ask for anything outside of the scope of the task description.
        """

        system_prompt = "You are a test case creator specializing in designing evaluation scenarios."

        rendered_prompt = render(
            dedent(prompt),
            {
                "allowed_keys": allowed_keys,
                "task_description": task_description,
                "idea": idea,
                "example_prompt_inputs": example_prompt_inputs,
            },
        )

        messages = []
        add_user_message(messages, rendered_prompt)
        add_assistant_message(messages, "```json")
        text = get_request().chat(
            messages,
            stop_sequences=["```"],
            system=system_prompt,
            temperature=0.7,
        )

        test_case = json.loads(text)
        test_case["task_description"] = task_description
        test_case["scenario"] = idea

        return test_case

def generate_unique_ideas(task_description, prompt_inputs_spec=None, num_cases=1):
        """Generate a list of unique ideas for test cases based on the task description"""

        if prompt_inputs_spec is None:
             prompt_inputs_spec={}

        prompt = """
        Generate {num_cases} unique, diverse ideas for testing a prompt that accomplishes this task:
        
        <task_description>
        {task_description}
        </task_description>

        The prompt will receive the following inputs
        <prompt_inputs>
        {prompt_inputs_spec}
        </prompt_inputs>
        
        Each idea should represent a distinct scenario or example that tests different aspects of the task.
        
        Output Format:
        Provide your response as a structured JSON array where each item is a brief description of the idea.
        
        Example:
        ```json
        [
            "Testing with technical computer science terminology",
            "Testing with medical research findings",
            "Testing with complex mathematical concepts",
            ...
        ]
        ```
        
        Ensure each idea is:
        - Clearly distinct from the others
        - Relevant to the task description
        - Specific enough to guide generation of a full test case
        - Quick to solve without requiring extensive computation or multi-step processing
        - Solvable with no more than 400 tokens of output

        Remember, only generate {num_cases} unique ideas
        """

        system_prompt = "You are a test scenario designer specialized in creating diverse, unique testing scenarios."

        example_prompt_inputs = ""
        for key, value in prompt_inputs_spec.items():
            val = value.replace("\n", "\\n")
            example_prompt_inputs += f'"{key}": str # {val},'

        rendered_prompt = render(
            dedent(prompt),
            {
                "task_description": task_description,
                "num_cases": num_cases,
                "prompt_inputs_spec": example_prompt_inputs,
            },
        )

        messages = []
        add_user_message(messages, rendered_prompt)
        add_assistant_message(messages, "```json")
        text = get_request().chat(
            messages,
            stop_sequences=["```"],
            system=system_prompt,
            temperature=1.0,
        )

        return json.loads(text)

def generate_dataset(
        task_description,
        prompt_inputs_spec=None,
        num_cases=1,
        output_file="dataset.json",
        max_concurrent_tasks=1
    ):
        """Generate test dataset based on task description and save to file"""

        if prompt_inputs_spec is None:
             prompt_inputs_spec={}
        ideas = generate_unique_ideas(
            task_description, prompt_inputs_spec, num_cases
        )

        dataset = []
        completed = 0
        total = len(ideas)
        last_reported_percentage = 0

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=max_concurrent_tasks
        ) as executor:
            future_to_idea = {
                executor.submit(
                    generate_test_case,
                    task_description,
                    idea,
                    prompt_inputs_spec,
                ): idea
                for idea in ideas
            }

            for future in concurrent.futures.as_completed(future_to_idea):
                try:
                    result = future.result()
                    completed += 1
                    current_percentage = int((completed / total) * 100)
                    milestone_percentage = (current_percentage // 20) * 20

                    if milestone_percentage > last_reported_percentage:
                        print(f"Generated {completed}/{total} test cases")
                        last_reported_percentage = milestone_percentage

                    dataset.append(result)
                except Exception as e:
                    print(f"Error generating test case: {e}")

        with open(output_file, "w") as f:
            json.dump(dataset, f, indent=2)




if __name__=="__main__":
    generate_dataset(
        task_description="Write a compact, concise 1 day meal plan for a single athlete",
        prompt_inputs_spec={
        "height": "Athlete's height in cm",
        "weight": "Athlete's weight in kg",
        "goal": "Goal of the athlete",
        "restrictions":"Dietary restrictions of the athlete"
        },
        output_file="dataset.json",
        num_cases=3,
        max_concurrent_tasks=1
    )