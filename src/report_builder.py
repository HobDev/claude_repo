def generate_prompt_evaluation_report(evaluation_results):
    total_tests = len(evaluation_results)
    scores = [result["score"] for result in evaluation_results]
    avg_score= mean(scores) if scores else 0
    max_possible_score = 10
    pass_rate =(
        100 * len([s for s in scores if s>=7])/ total_tests if total_tests else 0
    )


    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prompt Evaluation Report</title>
    <style>
         body{{
               font-family: Arial, sans-serif;
               line-height: 1.6;
               margin: 0;
               padding: 20px;
               color: #333;
            }}
            .header{{
                   background-color: #f0f0f0;
                   padding: 20px;
                   border-radius: 5px;
                   margin-bottom: 20px;
                   }}
            .summary-stats{{
                    display: flex;
                    justify-content: space-between;
                    flex-wrap: wrap;
                    gap: 10px;
                         }}
            .stat-box{{
                    background-color: #fff;
                    border-radius: 5px;
                    padding: 15px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                    flex-basis: 30%;
                    min-width: 200px;
                    }}
            .stat-value {{
                        font-size: 24px;
                        font-weight: bold;
                        margin-top: 5px;
                        }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px; 
                }}
            th {{
                background-color: #4a4a4a;
                color: white;
                text-align: left;
                padding: 12px;
                }}
            td {{
                padding: 10px;
                border-bottom: 1px solid #ddd;
                vertical-align: top;
                }}
            tr:nth-child(even) {{
                background-color: #f9f9f9;
                }}
            .output-cell {{
                white-space: pre-wrap;
                }}
            






