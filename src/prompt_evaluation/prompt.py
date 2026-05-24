
from api_request import Request, add_user_message, add_assistant_message
from evaluation.prompt_evaluator import PromptEvaluator


request= Request()



def run_prompt(prompt_inputs):
    prompt=f"""
Generate a one-day meal plan for an athlete that meets their dietary restrictions.

<athlete_information>
- Height: {prompt_inputs["height"]}
- Weight: {prompt_inputs["weight"]}
- Goal: {prompt_inputs["goal"]}
- Dietary resctrictions: {prompt_inputs["restrictions"]}
</athlete_information>

Guidelines:
1. Include accurate daily calorie amount
2. Show protein, fat, and carb amounts
3. Specify when to eat each meal
4. Use only foods that fit restrictions
5. List all portion sizes in grams
6. Keep budget-friendly if mentioned

Here is an example with a sample input and an ideal output:
<sample_input>
height: 178
weight: 82
goal: strength training
restrictions: vegan
</sample_input>

<ideal_output>
# One-Day Vegan Meal Plan for Strength Training Athlete

**Athlete Profile:** 178cm, 82kg male, strength training goal
**Daily Target:** 2,800 calories | 140g protein | 78g fat | 350g carbs

---

## BREAKFAST (7:00 AM)
**Oatmeal Power Bowl** - 650 calories

- Rolled oats: 80g
- Unsweetened almond milk: 240ml
- Peanut butter: 30g
- Banana: 100g
- Ground flaxseed: 15g

**Macros:** 22g protein | 24g fat | 82g carbs

---

## MID-MORNING SNACK (10:00 AM)
**Protein Smoothie** - 380 calories

- Vegan protein powder (pea/hemp blend): 30g
- Soy milk: 250ml
- Blueberries (frozen): 80g
- Almond butter: 20g

**Macros:** 28g protein | 12g fat | 38g carbs

---

## LUNCH (1:00 PM)
**Buddha Bowl with Tofu** - 750 calories

- Extra-firm tofu (pressed & baked): 200g
- Brown rice (cooked): 150g
- Roasted chickpeas: 80g
- Spinach: 100g
- Sweet potato: 120g
- Tahini dressing: 20ml

**Macros:** 32g protein | 20g fat | 95g carbs

---

## PRE-WORKOUT SNACK (4:00 PM)
**Banana & Energy Balls** - 320 calories

- Banana: 120g
- Homemade energy balls (dates, nuts, cocoa): 60g
- Sunflower seed butter: 15g

**Macros:** 12g protein | 10g fat | 48g carbs

---

## DINNER (7:00 PM)
**Lentil & Quinoa Bowl** - 700 calories

- Red lentils (cooked): 150g
- Quinoa (cooked): 100g
- Tempeh (steamed): 150g
- Broccoli: 150g
- Olive oil: 15ml
- Nutritional yeast: 10g

**Macros:** 40g protein | 16g fat | 80g carbs

---

## EVENING SNACK (9:00 PM)
**Nut Butter & Crackers** - 240 calories

- Hummus: 60g
- Whole grain crackers: 40g
- Hemp seeds: 15g

**Macros:** 8g protein | 12g fat | 20g carbs

---

## **DAILY TOTALS**
- **Calories:** 2,840
- **Protein:** 142g (20% of calories)
- **Fat:** 94g (30% of calories)
- **Carbs:** 363g (51% of calories)

---

## **KEY NOTES FOR STRENGTH ATHLETES:**
✓ Protein spread throughout day for muscle synthesis
✓ Complex carbs for sustained energy during training
✓ Healthy fats for hormone production
✓ Timing: Pre-workout snack 2 hours before, post-workout meal within 1-2 hours
✓ Hydrate with 3-4 liters of water daily
✓ Budget-friendly with staple proteins (lentils, tofu, chickpeas)
</ideal_output>
This meal plan comprehensively satisfies all mandatory requirements with clear daily totals, detailed macronutrient breakdowns, and six meals with specific portions and timing. Vegan compliance is flawless across all meals. The protein content (142g) is well-suited for strength training despite vegan constraints. Secondary criteria are largely met with good meal variety and athlete-focused guidance. 
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