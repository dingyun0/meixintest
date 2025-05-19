import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()
api_key=os.getenv('API_KEY')
api_url=os.getenv('API_URL')
headers={
    'Authorization': f'Bearer {api_key}',
    'Content-Type':'application/json'
}

def run_workflow(workflow_id,inputs,user,response_mode="blocking"):
    url=api_url
    data={
        "inputs":inputs,
        "response_mode":response_mode,
        "user":user
    }
    try:
        print("正在运行工作流")
        response=requests.post(url,headers=headers,json=data)

        if response.status_code==200:
            print('工作流执行成功')
            print("响应内容:", response.text)  # 打印响应内容
            try:
                response_json = response.json()  # 尝试解析JSON
                print("工作流结果:", json.dumps(response_json, indent=4, ensure_ascii=False))
                return response_json
            except json.JSONDecodeError as e:
                print(f"解析JSON时发生错误: {str(e)}")
                return None
        else:
            print(f"工作流执行失败，状态码：{response.status_code}")
            print("错误信息：",response.text)
            return None
    except Exception as e:
        print(f"发生错误:{str(e)}")
        return None

if __name__=="__main__":
    workflow_id="cd1e86da-e2a3-4e2c-8e11-308bbdde932d"
    inputs={
        "type":"支出"
    }
    user="abc-123"
    result=run_workflow(workflow_id,inputs,user)
    if result:
        print("工作流结果为：",json.dumps(result, indent=4, ensure_ascii=False))
