from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from jieba import posseg
from .lajifenlei_api import get_the_sort_of_trash


@on_command('refuse_classification', aliases='是什么垃圾')
async def refuse_classification(session: CommandSession):
    trash = session.get('trash')
    await session.send("正在查询中，请稍候~")
    trash_result = await get_the_sort_of_trash(trash)
    await session.send(trash_result)


@refuse_classification.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        if stripped_arg:
            session.state['trash'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('要查询的垃圾名称不能为空呢，请重新输入')

    session.state[session.current_key] = stripped_arg


@on_natural_language(keywords={'是什么垃圾'})
async def _(session: NLPSession):
    stripped_msg = session.msg_text.strip()
    words = posseg.lcut(stripped_msg)
    trash = None

    for word in words:
        if word.flag == 'n':
            if not word.word == '垃圾':
                trash = word.word

    return IntentCommand(90.0, 'refuse_classification', current_arg=trash)





