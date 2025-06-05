import pyJianYingDraft as draft

import api.utils as utils

# \pyJianYingDraft\backend\projects
path = utils.get_project_path()
print(path)


def test_01():
    # 使用 vars 函数可以获取对象的 __dict__ 属性
    # 这将返回一个包含对象属性的字典
    print(vars(draft.Script_file(300, 300)))

    # \pyJianYingDraft\backend\projects\hello
    print(utils.get_output_path("hello"))

    temp = draft.Script_file.load_template(
        path + "/custom_template_20250604_193652/draft_content.json")
    print(temp.dumps())


def test_02():
    audio = draft.local_materials.Audio_material(
        path=path + "/custom_template_20250604_193652/draft_content.json")
    return audio.export_json()


print(test_01())
