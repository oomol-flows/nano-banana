from oocana import Context
import os
import urllib.parse

#region generated meta
import typing
class Inputs(typing.TypedDict):
    item: str
    save_dir: str | None
class Outputs(typing.TypedDict):
    saved_path: typing.NotRequired[str | None]
#endregion

async def main(params: Inputs, context: Context) -> Outputs | None:
    url = params["item"]
    save_dir = params.get("save_dir")
    
    # 从URL中提取文件名
    parsed_url = urllib.parse.urlparse(url)
    filename = os.path.basename(parsed_url.path)
    
    # 如果没有文件名，使用默认名称
    if not filename:
        filename = "downloaded_file"
    
    # 构建保存路径
    if save_dir:
        saved_path = os.path.join(save_dir, filename)
    else:
        # 如果没有指定保存目录，使用当前工作目录
        saved_path = filename
    
    return {
        "saved_path": saved_path
    }
