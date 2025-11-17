from oocana import Context

#region generated meta
import typing
class Inputs(typing.TypedDict):
    reference_picture: str | None
class Outputs(typing.TypedDict):
    file: typing.NotRequired[str]
    no_file: typing.NotRequired[None]
#endregion

async def main(params: Inputs, context: Context) -> Outputs | None:
    
    # 检查 reference_picture 是否为空
    if params.get("reference_picture"):
        # 如果不为空，返回文件地址
        return {"file": params["reference_picture"]}
    else:
        # 如果为空，返回空值
        return {"no_file": None}
