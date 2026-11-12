# -*- coding: utf-8 -*-
"""第一部分：基础入门篇（第1-3章）"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from reportlab.platypus import Paragraph, Spacer, PageBreak, Table, TableStyle, HRFlowable, Preformatted
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.units import mm, cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle

# 从主脚本导入样式和工具
from gen_bat_book import (
    ST_PART_TITLE, ST_CH_TITLE, ST_SEC_TITLE, ST_SUBSEC_TITLE,
    ST_BODY, ST_BODY_NOINDENT, make_code_block, make_note_box, hr, inline_code,
    _wrap_table_rows
)


def ch1():
    """第1章：认识 cmd.exe 与 BAT 批处理"""
    story = []
    
    story.append(Paragraph('第1章 认识 cmd.exe 与 BAT 批处理', ST_CH_TITLE))
    story.append(Spacer(1, 6))
    
    story.append(Paragraph('1.1 cmd.exe 是什么', ST_SEC_TITLE))
    story.append(Paragraph(
        '<b>cmd.exe</b> 是 Windows 操作系统自带的命令行解释器，它的作用是接收用户输入的命令并执行。'
        '从 MS-DOS 时代开始，命令行就是 Windows 系统管理的核心工具之一，而 BAT 批处理文件则是命令行的脚本化形式——'
        '把一系列命令写入一个纯文本文件，让 cmd.exe 自动按顺序执行。', ST_BODY))
    
    story.append(Paragraph(
        'cmd.exe 的历史可以追溯到 1981 年的 MS-DOS 1.0。三十多年来，它始终保持着向后兼容的设计原则，'
        '这意味着今天的 BAT 脚本仍然可以在最新的 Windows 11 上运行。这既是 BAT 的优势（稳定性），'
        '也带来了一些限制（语法古老、功能有限）。', ST_BODY))
    
    story.append(make_note_box(
        'Windows NT 内核（Windows NT/2000/XP/Vista/7/8/10/11）上的 cmd.exe 虽然外观和 DOS 时代相似，'
        '但内部已经完全重写。它是一个 32 位/64 位的 Windows 原生程序，能够访问 Win32 API，'
        '支持长文件名、环境变量延迟扩展等高级特性。', 'note'))
    
    story.append(Paragraph('1.2 BAT 批处理的本质', ST_SEC_TITLE))
    story.append(Paragraph(
        'BAT 文件的本质是一个 <b>纯文本文件</b>，后缀名为 <font name="Consola" size="9" color="#C0392B">.bat</font> 或 '
        '<font name="Consola" size="9" color="#C0392B">.cmd</font>。当你双击它时，Windows 会自动用 cmd.exe 打开并逐行执行。', ST_BODY))
    
    story.append(Paragraph(
        '让我们创建第一个 BAT 文件来感受一下。打开记事本（Notepad），输入以下内容，然后保存为 '
        '<font name="Consola" size="9" color="#C0392B">hello.bat</font>：', ST_BODY))
    
    story.append(make_code_block('@echo off\necho Hello, BAT World!\npause'))
    
    story.append(Paragraph(
        '保存时注意：在"另存为"对话框中，将"保存类型"改为"所有文件 (*.*)"，编码选择 '
        '<b>ANSI</b> 或 <b>UTF-8</b>（Windows 10 推荐）。然后双击 hello.bat，你会看到一个黑色命令行窗口弹出，'
        '显示 "Hello, BAT World!"，按任意键后窗口关闭。', ST_BODY))
    
    story.append(make_note_box(
        '.bat 和 .cmd 的区别：.bat 是 DOS 时代就有的后缀，.cmd 从 Windows NT 开始引入。'
        '两者功能几乎完全相同，唯一细微的差别在于 .cmd 执行出错时 %errorlevel% 的行为略有不同。'
        '实际使用中可以任选其一，本书统一使用 .bat 后缀。', 'tip'))
    
    story.append(Paragraph('1.3 开发环境搭建', ST_SEC_TITLE))
    story.append(Paragraph(
        '写 BAT 脚本不需要任何 IDE，但一个好的编辑器能让你的开发效率翻倍。以下是推荐组合：', ST_BODY))
    
    story.append(Paragraph('编辑器推荐', ST_SUBSEC_TITLE))
    story.append(Paragraph('• <b>VS Code</b>（强烈推荐）：免费开源，通过插件支持 BAT 语法高亮、代码提示、片段', ST_BODY_NOINDENT))
    story.append(Paragraph('• <b>Notepad++</b>：经典轻量编辑器，自带 BAT 语法高亮', ST_BODY_NOINDENT))
    story.append(Paragraph('• <b>Sublime Text</b>：优雅的商业编辑器，安装 Batch Script 插件后支持完善', ST_BODY_NOINDENT))
    story.append(Paragraph('• <b>记事本</b>（Notepad）：系统自带，仅适合临时编写，不支持语法高亮', ST_BODY_NOINDENT))
    
    story.append(Paragraph('VS Code 推荐插件', ST_SUBSEC_TITLE))
    story.append(Paragraph(
        '• <b>Batch Script Support</b>（作者：felixfbecker）：完整的 BAT 语法高亮、片段、格式化', ST_BODY_NOINDENT))
    story.append(Paragraph(
        '• <b>vscode-batch-runner</b>：在 VS Code 内直接运行 BAT 脚本并查看输出', ST_BODY_NOINDENT))
    
    story.append(Paragraph('cmd 的启动方式', ST_SUBSEC_TITLE))
    story.append(Paragraph('• <b>Win + R</b>，输入 <font name="Consola" size="9" color="#C0392B">cmd</font>，回车', ST_BODY_NOINDENT))
    story.append(Paragraph('• 在任意文件夹地址栏输入 <font name="Consola" size="9" color="#C0392B">cmd</font>，回车（直接进入当前目录）', ST_BODY_NOINDENT))
    story.append(Paragraph('• Shift + 右键文件夹空白处 → 在此处打开命令窗口', ST_BODY_NOINDENT))
    story.append(Paragraph('• 开始菜单搜索 "cmd" 或 "命令提示符"', ST_BODY_NOINDENT))
    story.append(Paragraph('• 管理员身份：右键 → 以管理员身份运行', ST_BODY_NOINDENT))
    
    story.append(Paragraph('1.4 cmd vs PowerShell', ST_SEC_TITLE))
    story.append(Paragraph(
        '很多读者会问：Windows 都有 PowerShell 了，为什么还要学 BAT？这是一个好问题。两者各有分工：', ST_BODY))
    
    # 对比表格
    from reportlab.platypus import Table
    from reportlab.lib import colors
    compare_data = [
        ['特性', 'cmd.exe (BAT)', 'PowerShell'],
        ['历史', '1981年起，DOS时代', '2006年首次发布'],
        ['脚本后缀', '.bat / .cmd', '.ps1'],
        ['默认启用', '所有 Windows 版本', 'Windows 7+'],
        ['学习曲线', '平缓，语法简洁', '较陡，语法复杂'],
        ['对象模型', '文本流处理', '.NET 对象管道'],
        ['跨平台', '仅 Windows', 'PowerShell Core 跨平台'],
        ['系统兼容性', '100% 兼容所有 Windows', '部分旧系统不支持'],
        ['适合场景', '快速脚本、旧系统运维', '复杂自动化、.NET 操作'],
    ]
    t = Table(_wrap_table_rows(compare_data), colWidths=[35*mm, 55*mm, 55*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A5276')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F4F6F6')]),
        ('GRID',       (0, 0), (-1, -1), 0.5, colors.HexColor('#D5D8DC')),
        ('VALIGN',     (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING',   (0, 0), (-1, -1), 6),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 8))
    
    story.append(Paragraph(
        '实际上，PowerShell 和 BAT 并不是竞争关系，而是互补关系。BAT 仍然是最广泛使用的 Windows 脚本格式——'
        '因为它在所有 Windows 版本上都能直接运行，无需任何额外配置。在很多企业运维场景中，'
        'BAT 仍是首选的自动化工具。', ST_BODY))
    
    story.append(make_note_box(
        '本书专注于 cmd.exe / BAT 批处理。但在第 11 章"混合编程"中，我们会介绍 BAT 如何调用 PowerShell 来完成'
        'BAT 自身不擅长的任务（如加密、HTTP 请求、复杂文本处理）。', 'note'))
    
    story.append(Paragraph('1.5 本书代码规范', ST_SEC_TITLE))
    story.append(Paragraph(
        '为方便阅读，本书所有代码示例遵循以下规范：', ST_BODY))
    story.append(Paragraph('• 所有代码开头都有 <font name="Consola" size="9" color="#C0392B">@echo off</font>，关闭命令回显', ST_BODY_NOINDENT))
    story.append(Paragraph('• 变量名使用小写下划线风格，如 <font name="Consola" size="9" color="#C0392B">%file_count%</font>', ST_BODY_NOINDENT))
    story.append(Paragraph('• 注释使用 <font name="Consola" size="9" color="#C0392B">rem</font> 或 <font name="Consola" size="9" color="#C0392B">::</font>，功能关键处必有注释', ST_BODY_NOINDENT))
    story.append(Paragraph('• 文件路径统一用反斜杠 <font name="Consola" size="9" color="#C0392B">\\</font>，含空格的路径加双引号', ST_BODY_NOINDENT))
    story.append(Paragraph('• 每个可运行的脚本都标注了预期输出', ST_BODY_NOINDENT))
    story.append(Paragraph('• 涉及编码时默认使用 UTF-8，配合 <font name="Consola" size="9" color="#C0392B">chcp 65001</font>', ST_BODY_NOINDENT))
    
    story.append(Spacer(1, 20))
    story.append(Paragraph('— 第1章 完 —', ParagraphStyle('end', fontName='DengL', fontSize=10, textColor='#7F8C8D', alignment=TA_LEFT)))
    story.append(PageBreak())
    return story


def ch2():
    """第2章：第一个BAT程序与基础输出"""
    story = []
    
    story.append(Paragraph('第2章 第一个 BAT 程序与基础输出', ST_CH_TITLE))
    story.append(Spacer(1, 6))
    
    story.append(Paragraph('2.1 @echo off：关闭命令回显', ST_SEC_TITLE))
    story.append(Paragraph(
        '在 BAT 中，<font name="Consola" size="9" color="#C0392B">echo</font> 是最常用的命令之一，它的作用是开启或关闭"命令回显"。'
        '什么是命令回显？就是 cmd.exe 在执行每条命令之前，先把这条命令本身打印出来的行为。', ST_BODY))
    
    story.append(Paragraph('比如，如果没有 @echo off：', ST_BODY))
    story.append(make_code_block('REM test.bat\necho Hello\npause'))
    story.append(Paragraph('运行后你会看到：', ST_BODY))
    story.append(make_code_block('C:\\>REM test.bat\n\nC:\\>echo Hello\nHello\n\nC:\\>pause\n请按任意键继续. . .'))
    
    story.append(Paragraph(
        '很明显，那些 <font name="Consola" size="9" color="#C0392B">C:\\>echo Hello</font> 这样的"命令本身"被打印出来了，这就是回显。'
        '使用 <font name="Consola" size="9" color="#C0392B">@echo off</font> 后，所有命令都不会被回显——脚本输出会干净得多。', ST_BODY))
    
    story.append(make_note_box(
        '开头的 <b>@</b> 符号是什么？它的作用是让 echo off 这条命令本身也不被回显。'
        '如果只写 echo off，你会看到 "C:\\>echo off" 这一行先被打印出来，然后回显才关闭。'
        '加上 @ 后，连 echo off 这条命令也被静默了。', 'tip'))
    
    story.append(Paragraph(
        '<font name="Consola" size="9" color="#C0392B">@echo off</font> 几乎是所有 BAT 脚本的第一行。'
        '唯一的例外是当你需要调试脚本时——临时去掉它可以看到每条命令的实际执行情况。', ST_BODY))
    
    story.append(Paragraph('2.2 echo：输出文本', ST_SEC_TITLE))
    story.append(Paragraph(
        '当 echo 后面跟有内容时，它就不再是控制回显，而是<b>输出文本</b>到控制台。', ST_BODY))
    
    story.append(Paragraph('基本用法：', ST_BODY))
    story.append(make_code_block('@echo off\necho 你好，世界！\necho Hello World\necho'))
    
    story.append(Paragraph(
        '注意第三条 <font name="Consola" size="9" color="#C0392B">echo</font> 不带任何参数，它输出一个空行——用来分隔不同部分的输出。', ST_BODY))
    
    story.append(Paragraph('输出特殊字符', ST_SUBSEC_TITLE))
    story.append(Paragraph(
        'echo 输出时有几个特殊字符需要注意，因为它们在 cmd 中有特殊含义：', ST_BODY))
    story.append(Paragraph('• <font name="Consola" size="9" color="#C0392B">%</font> —— 变量引用符号', ST_BODY_NOINDENT))
    story.append(Paragraph('• <font name="Consola" size="9" color="#C0392B">&amp;</font> —— 命令连接符', ST_BODY_NOINDENT))
    story.append(Paragraph('• <font name="Consola" size="9" color="#C0392B">|</font> —— 管道符', ST_BODY_NOINDENT))
    story.append(Paragraph('• <font name="Consola" size="9" color="#C0392B"><</font> <font name="Consola" size="9" color="#C0392B">></font> —— 重定向符', ST_BODY_NOINDENT))
    story.append(Paragraph('• <font name="Consola" size="9" color="#C0392B">^</font> —— 转义符', ST_BODY_NOINDENT))
    
    story.append(Paragraph(
        '如果你想在 echo 输出中包含这些特殊字符，需要用 <font name="Consola" size="9" color="#C0392B">^</font>（脱字符）转义：', ST_BODY))
    story.append(make_code_block('@echo off\necho 100%% CPU\necho A ^| B\necho C ^& D\necho 5 ^> 3'))
    
    story.append(Paragraph('输出结果：', ST_BODY))
    story.append(make_code_block('100% CPU\nA | B\nC & D\n5 > 3'))
    
    story.append(make_note_box(
        '只有在 echo 的上下文中，% 才会被解析为变量引用。如果在括号块 (...) 或 for 循环内部，'
        '则需要用两个 %%（%%）来表示一个字面百分号。这一点我们在讲变量和 for 循环时会详细解释。', 'warn'))
    
    story.append(Paragraph('2.3 pause：暂停与交互', ST_SEC_TITLE))
    story.append(Paragraph(
        '<font name="Consola" size="9" color="#C0392B">pause</font> 命令会暂停脚本执行，并显示提示：', ST_BODY))
    story.append(make_code_block('请按任意键继续. . .'))
    
    story.append(Paragraph('这是 BAT 中最简单的"用户交互"方式。当你双击运行 BAT 文件时，窗口执行完命令后会立即关闭——'
        '用 pause 可以让窗口停住，让你看到输出结果。', ST_BODY))
    
    story.append(Paragraph('进阶：自定义 pause 提示文字', ST_BODY))
    story.append(make_code_block('@echo off\necho 脚本执行完毕，按任意键退出...\npause > nul'))
    
    story.append(Paragraph(
        '<font name="Consola" size="9" color="#C0392B">pause &gt; nul</font> 表示把 pause 的默认提示重定向到空设备（丢弃），'
        '只显示我们自己 echo 的提示。', ST_BODY))
    
    story.append(Paragraph('2.4 rem 与 ::：注释的两种写法', ST_SEC_TITLE))
    story.append(Paragraph(
        'BAT 中有两种写注释的方式：', ST_BODY))
    story.append(make_code_block('rem 这是一行注释\n:: 这也是一行注释\necho 上面两行不会被执行'))
    
    story.append(Paragraph('两者的区别：', ST_BODY))
    story.append(Paragraph('• <b>rem</b> —— 正规的注释命令，在 cmd 解析器中有正式定义，兼容性 100%', ST_BODY_NOINDENT))
    story.append(Paragraph('• <b>::</b> —— 利用标签（:label）语法的 hack，不是真正的注释命令，但写起来更简洁', ST_BODY_NOINDENT))
    
    story.append(make_note_box(
        ':: 的原理：以 : 开头的行被 cmd 当作标签（goto 的跳转目标），但 :: 不是合法的标签名'
        '（标签名不能包含冒号），所以 cmd 会跳过它。某些极端情况下（如括号块内或 for 的 () 内）'
        ':: 可能导致解析错误，此时必须用 rem。稳妥起见，<b>本书统一使用 rem</b>。', 'warn'))
    
    story.append(Paragraph('2.5 输出重定向初体验', ST_SEC_TITLE))
    story.append(Paragraph(
        '有时我们不希望脚本输出到屏幕，而是写入文件。这就需要"重定向"。', ST_BODY))
    story.append(make_code_block('@echo off\necho 这行将写入文件 > output.txt\ndir C:\\Windows > dir_list.txt'))
    
    story.append(Paragraph(
        '<font name="Consola" size="9" color="#C0392B">></font> 会覆盖文件内容，'
        '<font name="Consola" size="9" color="#C0392B">>></font> 则是<b>追加</b>到文件末尾。这是重定向最基本的用法。'
        '第 6 章会深入讲解完整的重定向体系。', ST_BODY))
    
    story.append(Paragraph('2.6 编码入门：解决中文乱码', ST_SEC_TITLE))
    story.append(Paragraph(
        'BAT 脚本中最常见的问题之一就是<b>中文乱码</b>。这是因为文件保存编码和 cmd 期望的编码不匹配。', ST_BODY))
    
    story.append(Paragraph('Windows 的中文 cmd 默认使用 <b>GBK</b>（代码页 936）。', ST_BODY))
    story.append(Paragraph('• 如果你的 BAT 文件用 ANSI/GBK 保存 → 直接双击运行正常', ST_BODY_NOINDENT))
    story.append(Paragraph('• 如果你的 BAT 文件用 UTF-8 保存 → 需要先执行 <font name="Consola" size="9" color="#C0392B">chcp 65001</font>', ST_BODY_NOINDENT))
    
    story.append(make_code_block('@echo off\nchcp 65001 > nul\necho 这是 UTF-8 编码的中文\necho 不会再乱码了'))
    
    story.append(make_note_box(
        '<b>最佳实践</b>：使用 VS Code 或 Notepad++，将文件保存为 <b>UTF-8 with BOM</b>，'
        '脚本开头加上 <font name="Consola" size="9" color="#C0392B">chcp 65001 &gt; nul</font>。'
        '这样在 Windows 10/11 上中文显示最稳定。更彻底的编码方案见第 11.7 节。', 'tip'))
    
    story.append(Paragraph('2.7 第一个完整脚本', ST_SEC_TITLE))
    story.append(Paragraph('把学过的知识组合起来，写一个真正有用的脚本——系统信息小工具：', ST_BODY))
    story.append(make_code_block('@echo off\nchcp 65001 > nul\ntitle 系统信息查询工具\n\nrem ========== 系统信息查询 ==========\necho ========================================\necho        欢迎使用系统信息查询工具\necho ========================================\necho.\necho 当前时间: %date% %time%\necho 计算机名: %computername%\necho 当前目录: %cd%\necho 操作系统: %os%\necho 处理器数: %number_of_processors%\necho.\necho ========================================\npause'))
    
    story.append(Paragraph('保存为 <font name="Consola" size="9" color="#C0392B">sysinfo.bat</font> 并运行，你会看到：', ST_BODY))
    story.append(make_code_block('========================================\n       欢迎使用系统信息查询工具\n========================================\n\n当前时间: 2026/11/10 二 14:30:00.00\n计算机名: DESKTOP-HARRY\n当前目录: C:\\Users\\Harry\\Desktop\n操作系统: Windows_NT\n处理器数: 8\n\n========================================\n请按任意键继续. . .'))
    
    story.append(Paragraph(
        '脚本用到了多个"内置环境变量"（%date%、%computername% 等），这些我们在第 4 章变量系统中会详细讲解。'
        '现在你只需要知道：BAT 已经可以帮我们做真正有用的事情了！', ST_BODY))
    
    story.append(Spacer(1, 20))
    story.append(Paragraph('— 第2章 完 —', ParagraphStyle('end', fontName='DengL', fontSize=10, textColor='#7F8C8D', alignment=TA_LEFT)))
    story.append(PageBreak())
    return story


def ch3():
    """第3章：批处理的执行机制"""
    story = []
    
    story.append(Paragraph('第3章 批处理的执行机制', ST_CH_TITLE))
    story.append(Spacer(1, 6))
    
    story.append(Paragraph('3.1 cmd.exe 的解析流程', ST_SEC_TITLE))
    story.append(Paragraph(
        '理解 cmd.exe 如何解析 BAT 文件，是写出高级脚本的前提。cmd 的解析分为<b>两个阶段</b>：', ST_BODY))
    
    story.append(Paragraph(
        '<b>第一阶段：预处理（预处理扫描）</b>', ST_BODY_NOINDENT))
    story.append(Paragraph(
        '• 识别括号块 (...)、for 循环、if 语句的整体结构', ST_BODY_NOINDENT))
    story.append(Paragraph(
        '• 在括号块内进行<b>百分号变量展开</b>（%var% 替换成实际值）', ST_BODY_NOINDENT))
    story.append(Paragraph(
        '• 处理转义字符（^）', ST_BODY_NOINDENT))
    story.append(Paragraph(
        '<b>第二阶段：执行</b>', ST_BODY_NOINDENT))
    story.append(Paragraph(
        '• 按顺序执行每条命令', ST_BODY_NOINDENT))
    story.append(Paragraph(
        '• 在执行阶段进行<b>延迟扩展</b>（!var!）', ST_BODY_NOINDENT))
    
    story.append(make_note_box(
        '这两个阶段的存在，导致了 BAT 中最经典的"陷阱"：在括号块内用 %var% 看不到变量的更新。'
        '这就是"延迟扩展"（enabledelayedexpansion）存在的原因。我们会在第 4 章详细展开。', 'warn'))
    
    story.append(Paragraph('3.2 exit 的两种形式', ST_SEC_TITLE))
    story.append(Paragraph(
        '<font name="Consola" size="9" color="#C0392B">exit</font> 有两种用法，效果天差地别：', ST_BODY))
    
    from reportlab.platypus import Table
    from reportlab.lib import colors
    exit_data = [
        ['形式', '作用域', '效果'],
        ['exit', '关闭整个 cmd.exe 进程', '所有 cmd 窗口都会关闭'],
        ['exit /b', '仅退出当前 BAT 脚本', '返回调用处，不关闭 cmd 窗口'],
    ]
    t = Table(_wrap_table_rows(exit_data), colWidths=[30*mm, 60*mm, 60*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A5276')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F4F6F6')]),
        ('GRID',       (0, 0), (-1, -1), 0.5, colors.HexColor('#D5D8DC')),
        ('VALIGN',     (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING',   (0, 0), (-1, -1), 6),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 8))
    
    story.append(make_code_block('@echo off\ncall sub.bat\necho sub.bat 已返回\npause'))
    story.append(Paragraph('在 sub.bat 中：', ST_BODY))
    story.append(make_code_block('@echo off\necho 我是子脚本\nexit /b\necho 这行不会被执行'))
    
    story.append(Paragraph(
        '如果 sub.bat 里写的是不带 /b 的 <font name="Consola" size="9" color="#C0392B">exit</font>，'
        '那么整个 cmd 窗口都会关闭，主脚本里 echo 那行永远不会运行。<b>写 BAT 时 99% 的情况应该用 exit /b</b>。', ST_BODY))
    
    story.append(Paragraph('3.3 退出码与 errorlevel', ST_SEC_TITLE))
    story.append(Paragraph(
        '每条命令执行完毕后，会返回一个"退出码"（exit code），保存在 <font name="Consola" size="9" color="#C0392B">%errorlevel%</font> 中。'
        '• 0 表示成功', ST_BODY))
    story.append(Paragraph('• 非 0 表示失败或不同的状态', ST_BODY_NOINDENT))
    
    story.append(make_code_block('@echo off\ncopy file1.txt file2.txt\nif errorlevel 1 (\n    echo 复制失败了！\n) else (\n    echo 复制成功\n)'))
    
    story.append(Paragraph(
        '<font name="Consola" size="9" color="#C0392B">if errorlevel 1</font> 的含义是"如果 errorlevel >= 1"，'
        '即任何非零值。这是 BAT 中检查命令是否成功的标准模式。', ST_BODY))
    
    story.append(make_note_box(
        '技巧：可以在脚本中用 <font name="Consola" size="9" color="#C0392B">set errorlevel=</font> 手动清除 errorlevel，'
        '或者用 <font name="Consola" size="9" color="#C0392B">exit /b N</font> 返回自定义的退出码（N 是数字），供调用方检查。', 'tip'))
    
    story.append(Paragraph('3.4 命令的搜索优先级', ST_SEC_TITLE))
    story.append(Paragraph(
        '当你在 BAT 中写一条命令（比如 <font name="Consola" size="9" color="#C0392B">echo</font>）时，'
        'cmd 按以下顺序查找这条命令：', ST_BODY))
    story.append(Paragraph('① <b>别名</b> —— doskey 定义的命令别名（默认没有）', ST_BODY_NOINDENT))
    story.append(Paragraph('② <b>内部命令</b> —— cmd.exe 内置的命令（echo、set、if、for、goto、call 等）', ST_BODY_NOINDENT))
    story.append(Paragraph('③ <b>.COM</b> —— 当前目录下的 .com 文件', ST_BODY_NOINDENT))
    story.append(Paragraph('④ <b>.EXE</b> —— 当前目录下的 .exe 文件', ST_BODY_NOINDENT))
    story.append(Paragraph('⑤ <b>.BAT / .CMD</b> —— 当前目录下的 .bat / .cmd 文件', ST_BODY_NOINDENT))
    story.append(Paragraph('⑥ <b>PATH 目录</b> —— 按 path 环境变量列出的目录，依次重复 ③~⑤', ST_BODY_NOINDENT))
    
    story.append(make_note_box(
        '这就是为什么你<b>不能</b>把自己的 BAT 文件命名为 echo.bat 或 if.bat——'
        '因为 echo 是内部命令，会被优先匹配，你的脚本永远不会被调用。同理，'
        '不要让你的脚本名和 path 中的 .exe 重名。', 'warn'))
    
    story.append(Paragraph('3.5 call / goto 的底层逻辑', ST_SEC_TITLE))
    story.append(Paragraph(
        '<b>goto :label</b> —— 改变脚本的执行顺序，跳转到标签位置继续执行。', ST_BODY))
    story.append(Paragraph(
        '<b>call :label</b> —— 调用"内部子程序"，跳转到标签并把调用位置压入栈，遇到 <font name="Consola" size="9" color="#C0392B">exit /b</font> 或 <font name="Consola" size="9" color="#C0392B">goto :eof</font> 后回到调用处。', ST_BODY))
    
    story.append(make_code_block('@echo off\necho 开始\ncall :sub1\necho 返回了\ncall :sub2\necho 全部完成\npause\n\n:sub1\necho 我是子程序1\ncall :sub_sub\necho 从 sub_sub 返回\ngoto :eof\n\n:sub_sub\necho 嵌套调用\ngoto :eof\n\n:sub2\necho 我是子程序2\nexit /b'))
    
    story.append(Paragraph(
        '<font name="Consola" size="9" color="#C0392B">goto :eof</font> 是一个特殊标签，意思是"跳到文件末尾"——等价于 exit /b。', ST_BODY))
    
    story.append(Paragraph('3.6 常见执行陷阱', ST_SEC_TITLE))
    story.append(Paragraph(
        '<b>路径中包含空格</b>：路径必须用双引号包裹，否则会被当作多个参数。', ST_BODY))
    story.append(make_code_block('rem 错误写法\ncopy C:\\Program Files\\a.txt D:\\\n\nrem 正确写法\ncopy "C:\\Program Files\\a.txt" D:\\'))
    
    story.append(Paragraph(
        '<b>权限不足</b>：某些操作（写 C:\\Program Files、改注册表 HKLM 分支）需要管理员权限。'
        '右键 cmd → 以管理员身份运行，或用第 11 章介绍的 UAC 提权代码。', ST_BODY))
    
    story.append(Paragraph(
        '<b>命令被同名文件覆盖</b>：如果当前目录有一个 echo.bat，cmd 在搜索内部命令之前不会先找它。'
        '但如果有 dir.bat，而你想调用系统的 dir 命令，可以用 <font name="Consola" size="9" color="#C0392B">%SystemRoot%\\System32\\dir.exe</font> 显式指定路径。', ST_BODY))
    
    story.append(Paragraph(
        '<b>编码不匹配</b>：UTF-8 文件没加 chcp 65001、GBK 文件被 UTF-8 cmd 打开 → 中文乱码。'
        '解决方案见第 2.6 节和第 11.7 节。', ST_BODY))
    
    story.append(Spacer(1, 20))
    story.append(Paragraph('— 第3章 完 —', ParagraphStyle('end', fontName='DengL', fontSize=10, textColor='#7F8C8D', alignment=TA_LEFT)))
    story.append(PageBreak())
    return story


def get_chapters():
    return [ch1(), ch2(), ch3()]
