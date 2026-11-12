# -*- coding: utf-8 -*-
"""第二部分：核心语法篇（第4-6章）"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from reportlab.platypus import Paragraph, Spacer, PageBreak, Table, TableStyle, HRFlowable, Preformatted
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.units import mm, cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle

from gen_bat_book import (
    ST_PART_TITLE, ST_CH_TITLE, ST_SEC_TITLE, ST_SUBSEC_TITLE,
    ST_BODY, ST_BODY_NOINDENT, make_code_block, make_note_box, hr, inline_code,
    _wrap_table_rows
)


def ch4():
    """第4章：变量系统全解析"""
    story = []
    
    story.append(Paragraph('第4章 变量系统全解析', ST_CH_TITLE))
    story.append(Spacer(1, 6))
    
    story.append(Paragraph(
        'BAT 的变量系统是其最独特也最容易让人困惑的部分。本章将从基础到高级，彻底讲透 BAT 变量的方方面面。', ST_BODY))
    
    story.append(Paragraph('4.1 set 命令：变量的定义、赋值与删除', ST_SEC_TITLE))
    story.append(Paragraph(
        '<font name="Consola" size="9" color="#C0392B">set</font> 是 BAT 变量的核心命令。定义和赋值的基本语法：', ST_BODY))
    
    story.append(make_code_block('@echo off\nset name=Harry\nset age=25\necho 姓名: %name%\necho 年龄: %age%\necho 明年: %age%+1'))
    
    story.append(Paragraph('运行结果：', ST_BODY))
    story.append(make_code_block('姓名: Harry\n年龄: 25\n明年: 25+1'))
    
    story.append(Paragraph(
        '几个要点：', ST_BODY))
    story.append(Paragraph('• <b>等号两边不能有空格</b>：<font name="Consola" size="9" color="#C0392B">set name = Harry</font> 会把变量名当成 "name "（带空格），值为 " Harry"（带空格）', ST_BODY_NOINDENT))
    story.append(Paragraph('• 变量值可以包含空格，此时最好用引号：<font name="Consola" size="9" color="#C0392B">set "name=Harry Potter"</font>', ST_BODY_NOINDENT))
    story.append(Paragraph('• 引用变量用 <font name="Consola" size="9" color="#C0392B">%变量名%</font> 包裹', ST_BODY_NOINDENT))
    story.append(Paragraph('• 变量名不区分大小写：<font name="Consola" size="9" color="#C0392B">%NAME%</font> 和 <font name="Consola" size="9" color="#C0392B">%name%</font> 等价', ST_BODY_NOINDENT))
    
    story.append(make_note_box(
        '推荐写法：始终用 <font name="Consola" size="9" color="#C0392B">set "var=value"</font> 的形式——'
        '双引号内不会受尾部空格影响，且等号右侧的特殊字符（&、| 等）不需要单独转义。', 'tip'))
    
    story.append(Paragraph('查看变量', ST_SUBSEC_TITLE))
    story.append(Paragraph(
        '<font name="Consola" size="9" color="#C0392B">set</font> 不带任何参数会列出当前所有环境变量；'
        '<font name="Consola" size="9" color="#C0392B">set name</font> 会列出所有以 "name" 开头的变量。', ST_BODY))
    
    story.append(Paragraph('删除变量', ST_SUBSEC_TITLE))
    story.append(make_code_block('set name='))
    story.append(Paragraph('等号后面什么都不写，就是删除变量。', ST_BODY))
    
    story.append(Paragraph('4.2 本地/全局变量隔离', ST_SEC_TITLE))
    story.append(Paragraph(
        'cmd.exe 的变量是"进程级"的——默认情况下，你在一个 cmd 窗口里设置的变量，'
        '在该窗口存活期间始终有效。<font name="Consola" size="9" color="#C0392B">setlocal</font> / '
        '<font name="Consola" size="9" color="#C0392B">endlocal</font> 可以创建一个"局部作用域"。', ST_BODY))
    
    story.append(make_code_block('@echo off\nset "var=全局值"\necho 进入 setlocal 前: %var%\n\nsetlocal\nset "var=局部值"\necho setlocal 内: %var%\nendlocal\n\necho endlocal 后: %var%'))
    
    story.append(Paragraph('输出：', ST_BODY))
    story.append(make_code_block('进入 setlocal 前: 全局值\nsetlocal 内: 局部值\nendlocal 后: 全局值'))
    
    story.append(Paragraph(
        'endlocal 会把 setlocal 之后所有变量的改动"回滚"——这在写子程序时非常有用，'
        '可以避免子程序的变量污染主脚本。', ST_BODY))
    
    story.append(Paragraph('4.3 延迟扩展：解决括号块变量更新难题', ST_SEC_TITLE))
    story.append(Paragraph(
        '这是 BAT 最经典也最重要的知识点。请看下面的代码：', ST_BODY))
    
    story.append(make_code_block('@echo off\nset count=0\nfor /L %%i in (1,1,5) do (\n    set /a count+=1\n    echo 当前计数: %count%\n)\necho 最终: %count%'))
    
    story.append(Paragraph('你期望输出 1~5，但实际输出是：', ST_BODY))
    story.append(make_code_block('当前计数: 0\n当前计数: 0\n当前计数: 0\n当前计数: 0\n当前计数: 0\n最终: 5'))
    
    story.append(Paragraph(
        '为什么 for 循环里 %count% 始终是 0？因为 <b>cmd 在执行 for 循环之前，已经把括号块里所有的 %变量% 都展开成了当时的值（0）</b>。'
        '之后 set /a count+=1 虽然改变了 count 的值，但 %count% 不会重新展开。', ST_BODY))
    
    story.append(make_note_box(
        '回忆第 3.1 节的"两阶段解析"：预处理阶段展开 %var%，执行阶段才做变量更新。'
        'for (...) 括号块在预处理阶段就把所有 %count% 替换成了 0，之后的执行里自然看到的都是 0。', 'note'))
    
    story.append(Paragraph(
        '解决方案——<font name="Consola" size="9" color="#C0392B">setlocal enabledelayedexpansion</font> + '
        '<font name="Consola" size="9" color="#C0392B">!变量名!</font>：', ST_BODY))
    
    story.append(make_code_block('@echo off\nsetlocal enabledelayedexpansion\nset count=0\nfor /L %%i in (1,1,5) do (\n    set /a count+=1\n    echo 当前计数: !count!\n)\necho 最终: !count!\nendlocal'))
    
    story.append(Paragraph('这次输出正确了：', ST_BODY))
    story.append(make_code_block('当前计数: 1\n当前计数: 2\n当前计数: 3\n当前计数: 4\n当前计数: 5\n最终: 5'))
    
    story.append(Paragraph(
        '<b>!var!</b> 与 <b>%var%</b> 的区别：', ST_BODY))
    
    diff_data = [
        ['语法', '展开时机', '适用场景'],
        ['%var%', '预处理阶段（执行前）', '括号块外部、for/if 外部'],
        ['!var!', '执行阶段（运行时）', 'setlocal enabledelayedexpansion 后的括号块内'],
    ]
    t = Table(_wrap_table_rows(diff_data), colWidths=[29.6*mm, 64.2*mm, 64.2*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A5276')),
        ('GRID',       (0, 0), (-1, -1), 0.5, colors.HexColor('#D5D8DC')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F4F6F6')]),
        ('VALIGN',     (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING',   (0, 0), (-1, -1), 6),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 8))
    
    story.append(make_note_box(
        '何时启用延迟扩展？<b>只要在 for (...) 或 if (...) 括号块内需要读取自己刚改过的变量，就必须启用。</b>'
        '建议养成习惯：所有非 trivial 的 BAT 脚本开头都加上 setlocal enabledelayedexpansion。', 'tip'))
    
    story.append(Paragraph('4.4 参数修饰符：%~dp0 等', ST_SEC_TITLE))
    story.append(Paragraph(
        '当 BAT 文件被调用时，命令行参数通过 <font name="Consola" size="9" color="#C0392B">%1</font>、'
        '<font name="Consola" size="9" color="#C0392B">%2</font> ... 来引用。'
        '但这些参数修饰符（%~x1）是 BAT 最强大也最难记的特性之一。', ST_BODY))
    
    story.append(Paragraph('基础参数', ST_SUBSEC_TITLE))
    story.append(make_code_block('@echo off\necho 参数1: %1\necho 参数2: %2\necho 参数总数: %*\necho 脚本自身: %0'))
    
    story.append(Paragraph('运行：<font name="Consola" size="9" color="#C0392B">test.bat hello world</font>', ST_BODY))
    story.append(make_code_block('参数1: hello\n参数2: world\n参数总数: hello world\n脚本自身: test.bat'))
    
    story.append(Paragraph('修饰符详解', ST_SUBSEC_TITLE))
    story.append(Paragraph('假设脚本路径为：<font name="Consola" size="9" color="#C0392B">C:\\Scripts\\test.bat</font>，调用参数 <font name="Consola" size="9" color="#C0392B">%1 = "C:\\Data\\input.txt"</font>', ST_BODY))
    
    mod_data = [
        ['修饰符', '含义', '示例值'],
        ['%~1',    '去掉外层双引号', 'C:\\Data\\input.txt'],
        ['%~f1',   '完整路径 + 文件名', 'C:\\Data\\input.txt'],
        ['%~d1',   '驱动器号', 'C:'],
        ['%~p1',   '目录路径（不含驱动器号）', '\\\\Data\\\\'],
        ['%~n1',   '文件名（不含后缀）', 'input'],
        ['%~x1',   '文件扩展名', '.txt'],
        ['%~s1',   '短路径（8.3格式）', 'C:\\DATA\\INPUT.TXT'],
        ['%~a1',   '文件属性', '--a------'],
        ['%~t1',   '修改时间', '2026/11/10 14:30'],
        ['%~z1',   '文件大小（字节）', '1024'],
        ['%~dp0',  '脚本自身所在目录', 'C:\\\\Scripts\\\\\\'],
        ['%~nx0',  '脚本自身文件名+后缀', 'test.bat'],
    ]
    t = Table(_wrap_table_rows(mod_data), colWidths=[25*mm, 55*mm, 60*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A5276')),
        ('GRID',       (0, 0), (-1, -1), 0.5, colors.HexColor('#D5D8DC')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F4F6F6')]),
        ('VALIGN',     (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING',   (0, 0), (-1, -1), 6),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))
    
    story.append(make_note_box(
        '最常用的几个：<b>%~dp0</b>（脚本所在目录）、<b>%~nx0</b>（脚本文件名）、<b>%~f1</b>（参数的完整路径）。'
        '组合写法：<b>%~dpnx0</b> = 驱动器 + 目录 + 文件名 + 后缀，即完整路径。', 'tip'))
    
    story.append(Paragraph('4.5 set /a：数值计算', ST_SEC_TITLE))
    story.append(Paragraph(
        'BAT 没有原生数值类型，所有变量都是字符串。但 <font name="Consola" size="9" color="#C0392B">set /a</font> 可以进行整数运算：', ST_BODY))
    
    story.append(make_code_block('@echo off\nset /a a=10+5\necho 10+5 = %a%\n\nset /a b=a*2\necho %a% * 2 = %b%\n\nset /a c=b/3\necho %b% / 3 = %c%\n\nset /a d=b%%3\necho %b% %% 3 = %d%\n\nset /a e=12 & 10\necho 12 AND 10 = %e%\n\nset /a f=1 || 0\necho 1 OR 0 = %f%\n\nset /a g+=5\necho g+=5 -> %g%'))
    
    story.append(Paragraph('输出：', ST_BODY))
    story.append(make_code_block('10+5 = 15\n15 * 2 = 30\n30 / 3 = 10\n30 % 3 = 0\n12 AND 10 = 8\n1 OR 0 = 1\ng+=5 -> 5'))
    
    story.append(Paragraph('set /a 支持的运算符（按优先级）：', ST_BODY))
    op_data = [
        ['优先级', '运算符', '含义'],
        ['1（最高）', '( )', '括号分组'],
        ['2', '! ~ -', '逻辑非、按位取反、负号'],
        ['3', '* / %%', '乘、除、取模'],
        ['4', '+ -', '加、减'],
        ['5', '<< >>', '左移、右移'],
        ['6', '&', '按位与'],
        ['7', '^', '按位异或'],
        ['8', '|', '按位或'],
        ['9', '== != < <= > >=', '比较（返回 0 或 1）'],
        ['10', '= += -= *= /= %%= ^= |= &= <<= >>=', '赋值运算'],
        ['11（最低）', ',', '表达式分隔'],
    ]
    t = Table(_wrap_table_rows(op_data), colWidths=[25*mm, 55*mm, 55*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A5276')),
        ('GRID',       (0, 0), (-1, -1), 0.5, colors.HexColor('#D5D8DC')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F4F6F6')]),
        ('VALIGN',     (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING',   (0, 0), (-1, -1), 6),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 8))
    
    story.append(make_note_box(
        'set /a 仅支持 32 位有符号整数（-2147483648 ~ 2147483647）。不支持小数运算。'
        '如果需要小数运算，要么用 PowerShell/VBScript，要么自己模拟（如先乘后除）。', 'warn'))
    
    story.append(Paragraph('4.6 字符串操作', ST_SEC_TITLE))
    story.append(Paragraph(
        'BAT 没有内置字符串函数，但可以通过 <b>变量替换语法</b> 实现替换和截取。', ST_BODY))
    
    story.append(Paragraph('字符串替换', ST_SUBSEC_TITLE))
    story.append(make_code_block('@echo off\nset "text=Hello World Hello BAT"\necho 原字符串: %text%\necho 替换后: %text:Hello=嗨%\necho 去掉所有空格: %text: =%'))
    
    story.append(Paragraph('语法：<font name="Consola" size="9" color="#C0392B">%var:旧=新%</font>，旧字符串替换成新字符串。新为空则删除。', ST_BODY))
    
    story.append(Paragraph('字符串截取', ST_SUBSEC_TITLE))
    story.append(make_code_block('@echo off\nset "text=0123456789"\necho 原字符串: %text%\necho 从第5个开始取: %text:~4%\necho 从0开始取前5个: %text:~0,5%\necho 从第3个开始取4个: %text:~2,4%\necho 从末尾取3个: %text:~-3%\necho 从第2个开始,到末尾前3个: %text:~2,-3%'))
    
    story.append(Paragraph('语法：<font name="Consola" size="9" color="#C0392B">%var:~起始位置,长度%</font>', ST_BODY))
    
    story.append(Paragraph('计算字符串长度', ST_SUBSEC_TITLE))
    story.append(Paragraph(
        'BAT 没有 len() 函数，但可以用 for 循环 + 替换技巧：', ST_BODY))
    story.append(make_code_block('@echo off\nsetlocal enabledelayedexpansion\nset "str=Hello World"\nset len=0\nfor /L %%i in (0,1,100) do (\n    if "!str:~%%i,1!" neq "" set /a len+=1\n)\necho "%str%" 的长度是: !len!\nendlocal'))
    
    story.append(Paragraph('4.7 内置特殊变量', ST_SEC_TITLE))
    story.append(Paragraph(
        'cmd.exe 预定义了很多特殊变量，随时可以使用：', ST_BODY))
    
    env_data = [
        ['变量', '含义', '示例值'],
        ['%cd%',       '当前工作目录', 'C:\\Users\\Harry'],
        ['%date%',     '当前日期（格式依赖系统区域设置）', '2026/11/10 二'],
        ['%time%',     '当前时间', '14:30:00.00'],
        ['%random%',   '0~32767 之间的随机数', '12345'],
        ['%errorlevel%', '上一条命令的退出码', '0'],
        ['%cmdextversion%', '命令扩展版本号', '2'],
        ['%_cmdvarset%', '命令行参数（shift 后变化）', '参数1 参数2'],
    ]
    t = Table(_wrap_table_rows(env_data), colWidths=[35*mm, 65*mm, 45*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A5276')),
        ('GRID',       (0, 0), (-1, -1), 0.5, colors.HexColor('#D5D8DC')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F4F6F6')]),
        ('VALIGN',     (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING',   (0, 0), (-1, -1), 6),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 8))
    
    story.append(make_note_box(
        '%date% 和 %time% 的格式依赖系统的区域设置，不同电脑上可能不一样。'
        '如果需要统一格式，用 PowerShell 辅助，或用 wmic 命令：'
        '<font name="Consola" size="9" color="#C0392B">for /f "tokens=2 delims==" %i in (\'wmic os get localdatetime /value\') do @set datetime=%i</font>', 'tip'))
    
    story.append(Paragraph('4.8 环境变量详解', ST_SEC_TITLE))
    story.append(Paragraph(
        '除了 cmd 内置的特殊变量，Windows 还预定义了大量系统环境变量：', ST_BODY))
    
    sysenv_data = [
        ['变量', '含义'],
        ['%path%',              '命令搜索路径（PATH 环境变量）'],
        ['%pathext%',           '可执行文件扩展名列表'],
        ['%windir% / %systemroot%', 'Windows 安装目录（如 C:\\Windows）'],
        ['%systemdrive%',       '系统驱动器号（如 C:）'],
        ['%system%',            'System32 目录'],
        ['%userprofile%',       '当前用户主目录'],
        ['%appdata%',           '当前用户 AppData\\Roaming'],
        ['%localappdata%',      '当前用户 AppData\\Local'],
        ['%temp% / %tmp%',      '临时文件目录'],
        ['%computername%',      '计算机名'],
        ['%username%',          '当前用户名'],
        ['%number_of_processors%', 'CPU 逻辑核心数'],
        ['%os%',                '操作系统（值固定为 Windows_NT）'],
    ]
    t = Table(_wrap_table_rows(sysenv_data), colWidths=[55*mm, 90*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A5276')),
        ('GRID',       (0, 0), (-1, -1), 0.5, colors.HexColor('#D5D8DC')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F4F6F6')]),
        ('VALIGN',     (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING',   (0, 0), (-1, -1), 6),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 8))
    
    story.append(make_note_box(
        'path 环境变量是最重要的之一。当 cmd 找不到某条命令时，它会按 path 里列出的目录依次搜索。'
        '你可以用 <font name="Consola" size="9" color="#C0392B">set "path=C:\\MyTools;%path%"</font> 在脚本开头临时添加目录，'
        '用完后记得用 setlocal/endlocal 恢复。', 'note'))
    
    story.append(Spacer(1, 20))
    story.append(Paragraph('— 第4章 完 —', ParagraphStyle('end', fontName='DengL', fontSize=10, textColor='#7F8C8D', alignment=TA_LEFT)))
    story.append(PageBreak())
    return story


def ch5():
    """第5章：流程控制语句"""
    story = []
    
    story.append(Paragraph('第5章 流程控制语句', ST_CH_TITLE))
    story.append(Spacer(1, 6))
    
    story.append(Paragraph('5.1 if 语句的4种模式', ST_SEC_TITLE))
    story.append(Paragraph(
        'BAT 中 if 语句有且仅有4种用法，分别用于不同场景：', ST_BODY))
    
    # if 模式表
    ifmodes = [
        ['模式', '语法', '用途', '示例'],
        ['1. 字符串比较', 'if "a"=="b"', '比较两个字符串', 'if "%name%"=="Harry"'],
        ['2. errorlevel', 'if errorlevel N', '检查退出码 >= N', 'if errorlevel 1 echo 失败'],
        ['3. exist', 'if exist 路径', '检查文件/目录是否存在', 'if exist C:\\data.txt'],
        ['4. defined', 'if defined var', '检查变量是否已定义', 'if defined debug echo debug mode'],
    ]
    t = Table(_wrap_table_rows(ifmodes), colWidths=[25*mm, 40*mm, 40*mm, 40*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A5276')),
        ('GRID',       (0, 0), (-1, -1), 0.5, colors.HexColor('#D5D8DC')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F4F6F6')]),
        ('VALIGN',     (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING',   (0, 0), (-1, -1), 6),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 8))
    
    story.append(Paragraph('模式1：字符串比较', ST_SUBSEC_TITLE))
    story.append(make_code_block('@echo off\nset "password=123456"\nset /p input=请输入密码: \nif "%input%"=="%password%" (\n    echo 密码正确，欢迎！\n) else (\n    echo 密码错误！\n)'))
    
    story.append(Paragraph(
        '注意：比较运算符是 <font name="Consola" size="9" color="#C0392B">==</font>（双等号），不是单等号。'
        '比较时两侧最好都加双引号，防止其中一侧为空时出现语法错误。', ST_BODY))
    
    story.append(make_note_box(
        '大小写不敏感：<font name="Consola" size="9" color="#C0392B">if "ABC"=="abc"</font> 结果为真。'
        '如果需要大小写敏感比较，用 if 加上 /I 开关的反义... 不对，BAT 没有直接的大小写敏感比较。'
        '一个办法是把两边都转成大写后比较。', 'warn'))
    
    story.append(Paragraph('模式2：if errorlevel', ST_SUBSEC_TITLE))
    story.append(make_code_block('@echo off\ncopy important.txt backup.txt\nif errorlevel 1 (\n    echo [错误] 复制失败！\n) else (\n    echo [成功] 备份完成\n)'))
    
    story.append(Paragraph(
        '⚠️ 重要：<font name="Consola" size="9" color="#C0392B">if errorlevel N</font> 检查的是 <b>errorlevel >= N</b>，不是等于！'
        '如果你想只检查 errorlevel == 0，正确写法是：', ST_BODY))
    story.append(make_code_block('if errorlevel 1 (\n    echo 非零\n) else (\n    echo 等于零\n)'))
    
    story.append(Paragraph('模式3：if exist', ST_SUBSEC_TITLE))
    story.append(make_code_block('@echo off\nif exist "C:\\Windows\\System32\\cmd.exe" (\n    echo cmd.exe 存在\n) else (\n    echo cmd.exe 不存在\n)\n\nif exist "D:\\data" (\n    echo D:\\data 是文件或目录\n)\n\nif not exist "%temp%\\cache.tmp" (\n    echo 缓存文件不存在，需要重新生成\n)'))
    
    story.append(Paragraph('模式4：if defined', ST_SUBSEC_TITLE))
    story.append(make_code_block('@echo off\nset "debug=1"\nif defined debug (\n    echo [DEBUG] 调试模式已开启\n    echo [DEBUG] 当前目录: %cd%\n)\nset debug=\nif defined debug (echo 不该出现) else (echo debug 变量已清除)'))
    
    story.append(Paragraph('5.2 if 与 else：多分支嵌套', ST_SEC_TITLE))
    story.append(Paragraph(
        'BAT 没有 else if，多分支只能靠嵌套：', ST_BODY))
    story.append(make_code_block('@echo off\nset /p score=请输入分数(0-100): \nif %score% geq 90 (\n    echo 等级: 优秀\n) else if %score% geq 80 (\n    echo 等级: 良好\n) else if %score% geq 60 (\n    echo 等级: 及格\n) else (\n    echo 等级: 不及格\n)'))
    
    story.append(Paragraph(
        '注意这里用到了比较运算符 <font name="Consola" size="9" color="#C0392B">geq</font>（大于等于）。'
        'BAT 支持的比较运算符：', ST_BODY))
    
    comp_data = [
        ['运算符', '含义', '数学符号'],
        ['EQU', '等于', '=='],
        ['NEQ', '不等于', '!='],
        ['LSS', '小于', '<'],
        ['LEQ', '小于等于', '<='],
        ['GTR', '大于', '>'],
        ['GEQ', '大于等于', '>='],
    ]
    t = Table(_wrap_table_rows(comp_data), colWidths=[35*mm, 55*mm, 55*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A5276')),
        ('GRID',       (0, 0), (-1, -1), 0.5, colors.HexColor('#D5D8DC')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F4F6F6')]),
        ('VALIGN',     (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING',   (0, 0), (-1, -1), 6),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 8))
    
    story.append(make_note_box(
        '比较运算符用于 if 的数值比较（if %a% gtr %b%）。如果比较字符串，用 == 和 !=。', 'note'))
    
    story.append(Paragraph('5.3 goto 与 call', ST_SEC_TITLE))
    story.append(Paragraph(
        '我们在第 3.5 节已经讲过 goto 和 call 的基本用法。这里看一个更完整的菜单程序：', ST_BODY))
    
    story.append(make_code_block('@echo off\nsetlocal enabledelayedexpansion\n:menu\ncls\necho ========================\necho    工具箱菜单\necho ========================\necho [1] 查看系统信息\necho [2] 清理临时文件\necho [3] 网络诊断\necho [0] 退出\necho ========================\nset /p choice=请选择: \n\nif "%choice%"=="1" goto :sysinfo\nif "%choice%"=="2" goto :cleanup\nif "%choice%"=="3" goto :netcheck\nif "%choice%"=="0" goto :eof\ngoto :menu\n\n:sysinfo\necho.\necho --- 系统信息 ---\nsysteminfo | more\npause\ngoto :menu\n\n:cleanup\necho.\necho --- 清理临时文件 ---\necho 清理 %temp% ...\ndel /q /s "%temp%\\*.*" 2>nul\necho 完成！\npause\ngoto :menu\n\n:netcheck\necho.\necho --- 网络诊断 ---\nipconfig /all\npause\ngoto :menu'))
    
    story.append(Paragraph('5.4 for 循环的4种模式', ST_SEC_TITLE))
    story.append(Paragraph(
        'for 是 BAT 中最强大的命令，也是语法最复杂的。它有 4 种模式，分别由 /D、/R、/L、/F 开关激活。', ST_BODY))
    
    story.append(Paragraph('模式1：for /D —— 仅目录', ST_SUBSEC_TITLE))
    story.append(Paragraph('遍历指定目录下的<b>子目录名</b>：', ST_BODY))
    story.append(make_code_block('@echo off\nfor /D %%d in (C:\\Users\\*) do (\n    echo 目录: %%d\n)'))
    
    story.append(Paragraph('输出：', ST_BODY))
    story.append(make_code_block('目录: C:\\Users\\Administrator\n目录: C:\\Users\\Harry\n目录: C:\\Users\\Public\n...'))
    
    story.append(Paragraph('模式2：for /R —— 递归遍历', ST_SUBSEC_TITLE))
    story.append(Paragraph('递归遍历目录树，匹配文件或目录：', ST_BODY))
    story.append(make_code_block('@echo off\nrem 递归列出 C:\\Windows 下所有 .log 文件\nfor /R "C:\\Windows" %%f in (*.log) do (\n    echo %%f\n)'))
    
    story.append(make_note_box(
        'for /R 的括号里可以写模式（如 *.log），也可以写固定的文件名（如 %%f in (test.txt)），'
        '后者会返回每个子目录下是否存在 test.txt。', 'tip'))
    
    story.append(Paragraph('模式3：for /L —— 数值区间循环', ST_SUBSEC_TITLE))
    story.append(Paragraph('类似 C 语言的 for (i=start; i&lt;end; i+=step)：', ST_BODY))
    story.append(make_code_block('@echo off\nrem 从 1 数到 10，步长为 1\nfor /L %%i in (1,1,10) do echo %%i\necho.\nrem 从 10 倒数到 0，步长为 -1\nfor /L %%i in (10,-1,0) do (\n    set /a square=%%i*%%i\n    echo %%i 的平方是 !square!\n)'))
    
    story.append(Paragraph('语法：<font name="Consola" size="9" color="#C0392B">for /L %%i in (起始,步长,结束) do</font>', ST_BODY))
    
    story.append(Paragraph('模式4：for /F —— 文本/命令解析（最强大）', ST_SUBSEC_TITLE))
    story.append(Paragraph('这是 for 循环中最复杂也最有用的模式。它能逐行读取文本或命令输出，然后按 tokens 拆分成变量。', ST_BODY))
    
    story.append(Paragraph('读取文件：', ST_BODY))
    story.append(make_code_block('@echo off\nrem 假设 data.txt 内容为: "张三,25,北京" 一行一条\nfor /F "tokens=1,2,3 delims=," %%a in (data.txt) do (\n    echo 姓名: %%a 年龄: %%b 城市: %%c\n)'))
    
    story.append(Paragraph('解析命令输出：', ST_BODY))
    story.append(make_code_block('@echo off\nrem 列出所有运行中的进程名\necho 当前运行的进程:\nfor /F "tokens=1" %%a in (\'tasklist /NH /fo csv\') do (\n    echo %%a\n)'))
    
    story.append(Paragraph('for /F 的参数详解：', ST_BODY))
    
    ff_params = [
        ['参数', '含义', '示例'],
        ['"tokens=N"', '取第 N 列（从1开始）', 'tokens=1,2,3'],
        ['"tokens=N-M"', '取第 N 到 M 列', 'tokens=1-3'],
        ['"tokens=*"', '取整行', 'tokens=*'],
        ['"delims=x"', '列分隔符（默认空格/Tab）', 'delims=,'],
        ['"skip=N"', '跳过前 N 行', 'skip=1'],
        ['"usebackq"', '高级引用模式', 'usebackq'],
        ['"eol=x"', '注释行起始符（默认 ;）', 'eol=#'],
    ]
    t = Table(_wrap_table_rows(ff_params), colWidths=[45*mm, 55*mm, 55*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A5276')),
        ('GRID',       (0, 0), (-1, -1), 0.5, colors.HexColor('#D5D8DC')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F4F6F6')]),
        ('VALIGN',     (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING',   (0, 0), (-1, -1), 6),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 8))
    
    story.append(make_note_box(
        'usebackq 的作用：让 for /F 能正确处理带空格的文件名和特殊字符。'
        '启用后，<b>`命令`</b>（反引号）表示执行命令，<b>"文件"</b>（双引号）表示文件名，'
        '单引号用于字面量。现代 BAT 脚本中几乎总是应该加 usebackq。', 'tip'))
    
    story.append(Paragraph('5.5 for 循环高级变体', ST_SEC_TITLE))
    story.append(Paragraph('嵌套循环 + 变量延迟扩展：', ST_BODY))
    story.append(make_code_block('@echo off\nsetlocal enabledelayedexpansion\nrem 双重循环：打印九九乘法表\nfor /L %%i in (1,1,9) do (\n    for /L %%j in (1,1,%%i) do (\n        set /a prod=%%i*%%j\n        <nul set /p "=%%i x %%j = !prod!   "\n    )\n    echo.\n)\nendlocal'))
    
    story.append(Paragraph(
        '<font name="Consola" size="9" color="#C0392B">&lt;nul set /p</font> 是一个经典技巧——'
        '用于不换行输出（set /p 默认不带换行符）。<font name="Consola" size="9" color="#C0392B">&lt;nul</font> 是为了提供一个空的输入流。', ST_BODY))
    
    story.append(Spacer(1, 20))
    story.append(Paragraph('— 第5章 完 —', ParagraphStyle('end', fontName='DengL', fontSize=10, textColor='#7F8C8D', alignment=TA_LEFT)))
    story.append(PageBreak())
    return story


def ch6():
    """第6章：重定向、管道与输入输出"""
    story = []
    
    story.append(Paragraph('第6章 重定向、管道与输入输出', ST_CH_TITLE))
    story.append(Spacer(1, 6))
    
    story.append(Paragraph('6.1 标准流概念', ST_SEC_TITLE))
    story.append(Paragraph(
        '每个 Windows 进程启动时，都有三个预定义的"标准流"。cmd.exe 和它执行的命令也不例外：', ST_BODY))
    
    stream_data = [
        ['流', '编号', '描述', '默认连接'],
        ['stdin（标准输入）', '0', '程序读取用户输入', '键盘'],
        ['stdout（标准输出）', '1', '程序输出正常结果', '屏幕（控制台）'],
        ['stderr（标准错误）', '2', '程序输出错误/警告信息', '屏幕（控制台）'],
    ]
    t = Table(_wrap_table_rows(stream_data), colWidths=[40*mm, 20*mm, 55*mm, 40*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A5276')),
        ('GRID',       (0, 0), (-1, -1), 0.5, colors.HexColor('#D5D8DC')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F4F6F6')]),
        ('VALIGN',     (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING',   (0, 0), (-1, -1), 6),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 8))
    
    story.append(Paragraph('6.2 重定向符号全解', ST_SEC_TITLE))
    story.append(Paragraph(
        '重定向可以把这些标准流从默认位置（屏幕/键盘）改到文件或其他命令。', ST_BODY))
    
    redirect_data = [
        ['语法', '含义', '说明'],
        ['命令 > 文件', 'stdout → 文件（覆盖）',   '最常用，写日志、导出'],
        ['命令 >> 文件', 'stdout → 文件（追加）',   '不会覆盖旧内容'],
        ['命令 < 文件', 'stdin ← 文件',            '从文件读取输入'],
        ['命令 2> 文件', 'stderr → 文件（覆盖）',   '单独捕获错误'],
        ['命令 2>> 文件', 'stderr → 文件（追加）',   '单独追加错误'],
        ['命令 2>&1', 'stderr → 与 stdout 相同位置', '合并错误到正常输出'],
        ['命令 1>&2', 'stdout → 与 stderr 相同位置', '把正常输出当作错误'],
        ['命令 > nul', 'stdout → 丢弃',           '静默正常输出'],
        ['命令 2> nul', 'stderr → 丢弃',           '静默错误输出'],
        ['命令 > nul 2>&1', 'stdout 和 stderr 都丢弃', '完全静默'],
    ]
    t = Table(_wrap_table_rows(redirect_data), colWidths=[40*mm, 50*mm, 55*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A5276')),
        ('GRID',       (0, 0), (-1, -1), 0.5, colors.HexColor('#D5D8DC')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F4F6F6')]),
        ('VALIGN',     (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING',   (0, 0), (-1, -1), 6),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))
    
    story.append(Paragraph(
        '注意顺序！<font name="Consola" size="9" color="#C0392B">command > out.txt 2>&1</font> 和 '
        '<font name="Consola" size="9" color="#C0392B">command 2>&1 > out.txt</font> 效果完全不同：', ST_BODY))
    story.append(make_code_block('rem 正确：先把 stdout 指向文件，再把 stderr 也指向那个文件\ncommand > out.txt 2>&1\n\nrem 错误：先把 stderr 指向 stdout（此时是屏幕），然后才改 stdout 指向文件\nrem 结果：错误仍然输出到屏幕\ncommand 2>&1 > out.txt'))
    
    story.append(make_note_box(
        '记忆口诀：<b>数字在前表示"从某流来"，&加数字表示"指向某流"。</b>'
        '2>&1 = 把 stderr(2) 指向 stdout(1) 当前的位置。', 'tip'))
    
    story.append(Paragraph('6.3 管道符 |', ST_SEC_TITLE))
    story.append(Paragraph(
        '管道符把左边命令的 stdout 直接作为右边命令的 stdin。这是 Unix 哲学的核心——'
        '每个命令只做一件事，用管道组合出强大功能。', ST_BODY))
    
    story.append(make_code_block('rem 统计当前目录下有多少个 .txt 文件\ndir /b *.txt | find /c /v ""\n\nrem 列出含 "error" 的日志行\ntype server.log | findstr "error"\n\nrem 从系统进程里过滤出 Python\n tasklist | findstr /I python'))
    
    story.append(make_note_box(
        '管道在 cmd 中会创建新的 cmd.exe 实例来运行两端的命令，所以管道两端的命令在<b>独立的进程</b>中运行。'
        '这意味着管道内对变量的修改不会反映到主脚本中——如果需要在管道内改变量后读取，得用别的办法。', 'warn'))
    
    story.append(Paragraph('6.4 find / findstr / sort / more', ST_SEC_TITLE))
    story.append(Paragraph('这些是配合管道最常用的过滤和格式化工具：', ST_BODY))
    
    story.append(Paragraph('find —— 简单文本搜索', ST_SUBSEC_TITLE))
    story.append(make_code_block('rem 在文件中搜索 "error" 字符串\ntype log.txt | find "error"\n\nrem 统计匹配行数\ntype log.txt | find /c "error"\n\nrem 不区分大小写 + 显示行号\ntype log.txt | find /I /N "error"'))
    
    story.append(Paragraph('findstr —— 支持正则表达式', ST_SUBSEC_TITLE))
    story.append(make_code_block('rem 搜索所有匹配正则的行\ndir /b | findstr "\\.docx$"\n\nrem 搜索多个关键词（空格分隔，任意一个匹配即可）\nfindstr "error warning" log.txt\n\nrem 正则：error 后面跟数字\nfindstr "error [0-9][0-9]*" log.txt'))
    
    story.append(make_note_box(
        'findstr 的正则是<b>简化版</b>，不支持 ? 、\\w 、\\d 等现代正则特性。'
        '如果需要完整正则，考虑用 PowerShell 或 Python。', 'note'))
    
    story.append(Paragraph('sort —— 排序', ST_SUBSEC_TITLE))
    story.append(make_code_block('rem 按字母排序\n type list.txt | sort\n\nrem 逆序排序\n type list.txt | sort /R\n\nrem 按第2列排序（以逗号分隔）\n type data.csv | sort /, /+2'))
    
    story.append(Paragraph('more —— 分页显示', ST_SUBSEC_TITLE))
    story.append(make_code_block('rem 一页一页地看长输出\ndir C:\\Windows /s | more\n\nrem 从第 20 行开始显示\ntype longfile.txt | more +20'))
    
    story.append(Paragraph('6.5 set /p 交互输入', ST_SEC_TITLE))
    story.append(Paragraph(
        '除了 pause 等待按键，set /p 是 BAT 中获取用户输入的主要方式：', ST_BODY))
    story.append(make_code_block('@echo off\nset /p name=请输入你的名字: \nset /p age=请输入年龄: \necho 你好 %name%，你 %age% 岁了'))
    
    story.append(make_note_box(
        'set /p 的限制：<b>不能超过 1024 字符</b>、<b>不能处理特殊字符</b>（如 & | %）、'
        '如果用户什么都不输入直接回车，变量保持原来的值（不会变空）。'
        '如果需要强制输入，用 "if "%var%"" 判断后用 goto 跳回。', 'warn'))
    
    story.append(Paragraph('6.6 重定向的高级坑', ST_SEC_TITLE))
    story.append(Paragraph('❌ <b>空文件陷阱</b>：', ST_BODY))
    story.append(Paragraph('如果命令没有产生任何输出，<font name="Consola" size="9" color="#C0392B">command > file.txt</font> 会创建一个<b>0字节的空文件</b>。'
        '如果原文件已存在，会被清空。这在写日志时要小心。', ST_BODY_NOINDENT))
    
    story.append(Paragraph('❌ <b>重定向与延迟扩展</b>：', ST_BODY))
    story.append(Paragraph(
        '在 for 循环中用 <font name="Consola" size="9" color="#C0392B">> file.txt</font>，'
        '每次迭代都会<b>覆盖</b>文件。如果想追加，用 >>；但更好的做法是在循环结束后一次性写入：', ST_BODY_NOINDENT))
    story.append(make_code_block('@echo off\nsetlocal enabledelayedexpansion\nset output=\nfor /L %%i in (1,1,5) do (\n    set output=!output!line%%i!\n)\necho !output! > result.txt'))
    
    story.append(Paragraph('❌ <b>权限冲突</b>：', ST_BODY))
    story.append(Paragraph(
        '写入 C:\\、C:\\Program Files 等受保护目录需要管理员权限，否则会报 "拒绝访问"。'
        '解决：用管理员身份运行，或让用户把文件写入 %temp% 或 %userprofile%。', ST_BODY_NOINDENT))
    
    story.append(Spacer(1, 20))
    story.append(Paragraph('— 第6章 完 —', ParagraphStyle('end', fontName='DengL', fontSize=10, textColor='#7F8C8D', alignment=TA_LEFT)))
    story.append(PageBreak())
    return story


def get_chapters():
    return [ch4(), ch5(), ch6()]
