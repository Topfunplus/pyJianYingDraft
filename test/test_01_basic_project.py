from base_config import *

def test_basic_project():
    """测试基础项目创建"""
    print("测试：基础项目创建")
    
    # 创建剪映草稿
    script = create_basic_script()
    
    # 添加基础轨道
    script.add_track(draft.Track_type.video)
    
    # 保存草稿
    output_path = get_output_path("basic_project")
    script.dump(output_path)
    
    print(f"基础项目创建测试完成，输出文件：{output_path}")

if __name__ == "__main__":
    test_basic_project()
