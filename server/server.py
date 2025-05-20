import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()
api_key=os.getenv('API_KEY')

def run_workflow(inputs,user, response_mode="blocking"):
    workflow_url ="https://dify.bluefocuslibrary.com/v1/workflows/run"
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
    
    
if __name__=="__main__":
    inputs={
        "user_id":"1",
        "type":"所有"
    }
    user="abc-123"
    result=run_workflow(inputs,user)
    if result:
        print("工作流结果为：",result)
        get_outputs(result)
