import gradio as gr
from server import run_workflow, get_outputs, save_to_excel
import os
import tempfile
import pandas as pd

def process_data(user_id, type_value):
    # 准备输入参数
    inputs = {
        "user_id": user_id,
        "type": type_value
    }
    user = 'abc-123'
    # 运行工作流
    result = run_workflow(inputs, user)
    
    if result and result.get("status") != "error":
        # 获取输出数据
        header, cleaned_data = get_outputs(result)
        # 创建DataFrame用于展示
        df = pd.DataFrame(cleaned_data, columns=header)
        return df, df, gr.update(visible=True)  # 返回DataFrame两次，并显示下载按钮
    else:
        raise gr.Error("工作流执行失败，请检查输入参数")

def download_excel(df, user_id, type_value):
    if df is None:
        raise gr.Error("没有可下载的数据")
    
    # 创建临时文件
    filename = f"{user_id}_{type_value}.xlsx"
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, filename)
    
    # 保存到临时文件
    df.to_excel(file_path, index=False)
    return file_path

# 创建 Gradio 界面
with gr.Blocks(title="数据生成器") as demo:
    gr.Markdown("# 数据生成器")
    gr.Markdown("请输入以下信息生成数据表格")
    
    with gr.Row():
        with gr.Column():
            user_id = gr.Textbox(label="用户ID", placeholder="请输入用户ID")
            type_value = gr.Dropdown(label="类型", choices=["支出", "收入", "所有"], value="支出")
            generate_btn = gr.Button("生成数据")
            download_btn = gr.Button("下载Excel", variant="primary", visible=False)
        
        with gr.Column():
            data_table = gr.Dataframe(label="数据预览")
            output_file = gr.File(label="下载Excel文件")
    
    # 存储DataFrame的变量
    df_state = gr.State(None)
    
    # 生成数据按钮事件
    generate_btn.click(
        fn=process_data,
        inputs=[user_id, type_value],
        outputs=[data_table, df_state, download_btn]
    )
    
    # 下载按钮事件
    download_btn.click(
        fn=download_excel,
        inputs=[df_state, user_id, type_value],
        outputs=output_file
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860) 