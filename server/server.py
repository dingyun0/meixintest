import requests
import json
import os
import pandas as pd
from dotenv import load_dotenv
load_dotenv()
api_key=os.getenv('API_KEY')
api_url=os.getenv('API_URL')

def run_workflow(inputs,user, response_mode="blocking"):
    workflow_url =f"{api_url}/workflows/run"
    headers={
        'Authorization': f'Bearer {api_key}',
        'Content-Type':'application/json'
    }
    
    data = {
        "inputs": inputs,
        "response_mode": response_mode,
        "user": user
    }

    try:
        print("运行工作流...")
        response = requests.post(workflow_url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            print("工作流执行成功")
            return response.json()
        else:
            print(f"工作流执行失败，状态码: {response.status_code}")
            return {"status": "error", "message": f"Failed to execute workflow, status code: {response.status_code}"}
    except Exception as e:
        print(f"发生错误: {str(e)}")
        return {"status": "error", "message": str(e)}

def get_outputs(output):
    output_text=output['data']['outputs']['text']
    print(output_text)
    lines = output_text.strip().split('\n')
    header = lines[0].split('|')
    data_rows = [line.split('|') for line in lines[2:]] 
    cleaned_data = []
    for row in data_rows:
        cleaned_row = [item.strip() for item in row]
        cleaned_data.append(cleaned_row)
    return header, cleaned_data

def save_to_excel(header, data,folder='../output_files', filename='output.xlsx'):
    os.makedirs(folder,exist_ok=True)
    file_path=os.path.join(folder,filename)
    df = pd.DataFrame(data, columns=header)  # 创建 DataFrame
    df.to_excel(file_path, index=False)  # 保存为 Excel 文件
    print(f"数据已保存到 {file_path}") 
    
def summarize_data(data):
    total_expense = 0.0
    for row in data:
        expense_amount = float(row[4])  # 第五列是支出金额
        total_expense += expense_amount
    print(f"总支出: {total_expense:.2f}")
        
if __name__=="__main__":
    inputs={
        "user_id":"1",
        "type":"所有"
    }
    user="abc-123"
    result=run_workflow(inputs,user)
    if result:
        print("工作流结果为：",result)
        header, cleaned_data = get_outputs(result)
        
        # 保存到 Excel
        save_to_excel(header, cleaned_data)

        # 汇总数据
        summarize_data(cleaned_data)
