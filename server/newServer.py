import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()
api_key=os.getenv('API_KEY')
api_url=os.getenv('API_URL')

def run_workflow(user, response_mode="blocking"):
    workflow_url ="https://dify.bluefocuslibrary.com/v1/workflows/run/d7d64ada-10f7-40bd-b835-19ec2354eade"
    headers={
        'Authorization': f'Bearer {api_key}',
        'Content-Type':'application/json'
    }

    data = {
        "inputs": {
            "type": "支出"
        },
        "response_mode": response_mode,
        "user": "abc-123"
    }

    try:
        print("运行工作流...")
        response = requests.get(workflow_url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            print("工作流执行成功")
            return response.json()
        else:
            print(f"工作流执行失败，状态码: {response.status_code}")
            return {"status": "error", "message": f"Failed to execute workflow, status code: {response.status_code}"}
    except Exception as e:
        print(f"发生错误: {str(e)}")
        return {"status": "error", "message": str(e)}

user = "abc-123"
# workflow_id="cd1e86da-e2a3-4e2c-8e11-308bbdde932d"

result = run_workflow(user)
print(result)
