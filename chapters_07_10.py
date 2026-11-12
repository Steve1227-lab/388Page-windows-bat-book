# -*- coding: utf-8 -*-
"""第三部分：文件与系统操作篇（第7-10章）"""

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
    _wrap_table_rows, ST_TH, ST_TD
)

# 居中对齐的表格单元格样式
_ST_TH_C = ParagraphStyle('TableHC',
    fontName='DengB', fontSize=9.5, leading=13,
    textColor=colors.white, alignment=TA_CENTER)
_ST_TD_C = ParagraphStyle('TableDC',
    fontName='Deng', fontSize=9.5, leading=13,
    textColor=colors.HexColor('#2C3E50'), alignment=TA_CENTER)


def ch7():
    """第7章：文件操作实战"""
    story = []
    
    story.append(Paragraph('第7章 文件操作实战', ST_CH_TITLE))
    story.append(Spacer(1, 6))
    
    story.append(Paragraph('7.1 路径与通配符', ST_SEC_TITLE))
    story.append(Paragraph(
        '在 BAT 中，路径是最容易出错的地方之一。理解通配符、相对路径和绝对路径能帮你避开大量陷阱。', ST_BODY))
    
    story.append(Paragraph('通配符', ST_SUBSEC_TITLE))
    story.append(Paragraph(
        '• <font name="Consola" size="9" color="#C0392B">*</font> —— 匹配任意长度字符（包含零个）', ST_BODY_NOINDENT))
    story.append(Paragraph(
        '• <font name="Consola" size="9" color="#C0392B">?</font> —— 匹配<b>恰好一个</b>字符', ST_BODY_NOINDENT))
    
    story.append(make_code_block('dir *.txt       & rem 所有 .txt 文件\ndir *.log       & rem 所有 .log 文件\ndir report?.txt  & rem report1.txt、reportA.txt 等（reportX.txt，X 为一个字符）\ndir a?c.*        & rem abc.txt、a1c.log、aZc.doc 等'))
    
    story.append(make_note_box(
        '在 BAT 的文件名处理中，通配符是"贪婪"的。例如 <font name="Consola" size="9" color="#C0392B">*.txt</font> 会匹配 file.txt、backup.txt、甚至 file.txt.bak 吗？不会——'
        'cmd 在内部会把文件名按最后一个点分割，后缀只匹配最后一个后缀。但某些命令（如 copy）会有不同行为，注意测试。', 'warn'))
    
    story.append(Paragraph('相对路径 vs 绝对路径', ST_SUBSEC_TITLE))
    story.append(Paragraph(
        '• <b>绝对路径</b>：从驱动器号开始，如 <font name="Consola" size="9" color="#C0392B">C:\\Users\\Harry\\data.txt</font>——无论当前目录在哪，都指向同一个文件', ST_BODY_NOINDENT))
    story.append(Paragraph(
        '• <b>相对路径</b>：相对于当前工作目录（%cd%），如 <font name="Consola" size="9" color="#C0392B">data\\input.txt</font>——在不同目录下运行会指向不同位置', ST_BODY_NOINDENT))
    story.append(Paragraph(
        '• <font name="Consola" size="9" color="#C0392B">.</font> —— 当前目录', ST_BODY_NOINDENT))
    story.append(Paragraph(
        '• <font name="Consola" size="9" color="#C0392B">..</font> —— 上一级目录', ST_BODY_NOINDENT))
    story.append(Paragraph(
        '• <font name="Consola" size="9" color="#C0392B">..\\..</font> —— 上两级目录', ST_BODY_NOINDENT))
    
    story.append(Paragraph('7.2 copy 命令', ST_SEC_TITLE))
    story.append(Paragraph(
        '<font name="Consola" size="9" color="#C0392B">copy</font> 是最基础的文件复制命令。', ST_BODY))
    
    story.append(make_code_block('rem 最简单的复制\ncopy file.txt backup.txt\n\nrem 复制到另一个目录\ncopy file.txt D:\\backup\\\n\nrem 批量复制（通配符）\ncopy *.txt archive\\\n\nrem 复制时合并文件\ncopy file1.txt + file2.txt merged.txt\n\nrem 二进制模式（带 /b），不修改换行符\ncopy /b large_file.bin D:\\storage\\\n\nrem 安静模式，不显示进度\ncopy /q source.txt dest.txt'))
    
    story.append(make_note_box(
        '<b>/a 和 /b 的区别</b>：/a 是 ASCII 文本模式（默认），会把 Unix 换行符 \\n 转成 Windows 的 \\r\\n；'
        '/b 是二进制模式，原封不动复制。复制 .exe、图片、压缩包<b>必须</b>用 /b。', 'tip'))
    
    story.append(Paragraph('7.3 xcopy vs robocopy', ST_SEC_TITLE))
    story.append(Paragraph(
        'copy 能做的事有限。复杂的复制场景需要 xcopy 或 robocopy。', ST_BODY))
    
    copy_cmp = [
        ['特性', 'copy', 'xcopy', 'robocopy'],
        ['文件复制', '✓', '✓', '✓'],
        ['目录递归', '✗', '✓ /E /S', '✓ /E'],
        ['复制权限', '✗', '✓ /O /X', '✓ /COPYALL'],
        ['镜像同步', '✗', '✗', '✓ /MIR'],
        ['断点续传', '✗', '✗', '✓ /Z'],
        ['多线程', '✗', '✗', '✓ /MT:n'],
        ['排除文件', '✗', '✓ /EXCLUDE:file', '✓ /XF /XD'],
        ['网络路径', '有限', '支持', '原生优化'],
        ['是否内建', '是(cmd)', '是（外部）', '是（Vista+）'],
    ]
    t = Table(_wrap_table_rows(copy_cmp,
                                col_styles={1: _ST_TD_C, 2: _ST_TD_C, 3: _ST_TD_C},
                                header_col_styles={1: _ST_TH_C, 2: _ST_TH_C, 3: _ST_TH_C}),
              colWidths=[35*mm, 35*mm, 35*mm, 35*mm])
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
    
    story.append(Paragraph('7.4 robocopy 深度解析', ST_SEC_TITLE))
    story.append(Paragraph(
        '<font name="Consola" size="9" color="#C0392B">robocopy</font>（Robust File Copy）是 Vista 引入的企业级复制工具。'
        '它不是普通命令——它是一个专业的备份/同步工具。', ST_BODY))
    
    story.append(make_code_block('rem 基础镜像备份\nrobocopy "C:\\Data" "D:\\Backup\\Data" /MIR\n\nrem /MIR = /E（包含空子目录） + /PURGE（删除目标端多余文件）\nrem 这意味着目标端会完全变成源端的镜像\n\nrem 备份文档到网络盘，跳过已同步的文件\nrobocopy "%userprofile%\\Documents" \\\\NAS\\Backup\\Docs /E /Z /MT:8 /R:3 /W:5\n\nrem 参数说明：\nrem /Z      重启模式（断点续传）\nrem /MT:8  8线程加速\nrem /R:3   失败后重试3次\nrem /W:5   每次重试等待5秒\n\nrem 排除临时文件和回收站\nrobocopy "C:\\Project" "D:\\Project_Backup" /E /XD "$RECYCLE.BIN" "System Volume Information" /XF "*.tmp" "*.log"'))
    
    story.append(Paragraph(
        'robocopy 退出码含义（非常重要！）：', ST_BODY))
    
    rc_code = [
        ['退出码', '含义', '是否成功'],
        ['0', '没有文件被复制（源端=目标端）', '✓ 成功'],
        ['1', '所有文件已成功复制', '✓ 成功'],
        ['2', '额外文件或目录被检测到', '✓ 成功'],
        ['4', '某些文件无法复制（权限或锁定）', '⚠ 警告'],
        ['8+', '严重错误', '✗ 失败'],
    ]
    t = Table(_wrap_table_rows(rc_code,
                                col_styles={0: _ST_TD_C},
                                header_col_styles={0: _ST_TH_C}),
              colWidths=[25*mm, 55*mm, 35*mm])
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
        '注意！robocopy 的退出码 0~7 都表示成功（只是不同程度的成功）。'
        '传统的 <font name="Consola" size="9" color="#C0392B">if errorlevel 1</font> 会把退出码 1~7 当成失败——'
        '正确判断是 <font name="Consola" size="9" color="#C0392B">if errorlevel 8</font>。', 'warn'))
    
    story.append(Paragraph('7.5 move 和 del', ST_SEC_TITLE))
    story.append(Paragraph('move —— 移动/重命名', ST_SUBSEC_TITLE))
    story.append(make_code_block('rem 文件重命名\nmove old.txt new.txt\n\nrem 跨驱动器移动（内部是复制+删除）\nmove "C:\\file.txt" "D:\\archive\\file.txt"\n\nrem 目录重命名（Windows 中改名 = 移动到同目录不同名）\nmove "old_folder" "new_folder"\n\nrem 批量移动所有 .jpg 到指定目录\nfor %%f in (*.jpg) do move "%%f" "D:\\Photos\\"'))
    
    story.append(Paragraph('del —— 删除文件', ST_SUBSEC_TITLE))
    story.append(make_code_block('rem 删除单个文件\ndel file.txt\n\nrem 强制删除只读文件\ndel /f readonly.txt\n\nrem 批量删除\ndel *.tmp\ndel /q C:\\Windows\\Temp\\*.*\n\nrem 连同子目录删除\ndel /s /q "C:\\Logs\\*.log"\n\nrem 删除多个指定文件\ndel file1.txt file2.txt file3.txt'))
    
    story.append(make_note_box(
        '<b>del 只删文件，不删目录</b>。删除空目录用 rd，删除非空目录用 rd /s /q。'
        '在 del 前最好先 echo 出将要删除的文件列表，确认无误再删——BAT 的删除是<b>永久删除</b>，不会进回收站！', 'warn'))
    
    story.append(Paragraph('7.6 文件重命名与批量处理', ST_SEC_TITLE))
    story.append(Paragraph(
        '<font name="Consola" size="9" color="#C0392B">ren</font>（rename）是重命名命令。结合 for 循环，可以做强大的批量重命名：', ST_BODY))
    
    story.append(make_code_block('@echo off\nsetlocal enabledelayedexpansion\nrem 批量把当前目录所有 .log 改成 .bak\nfor %%f in (*.log) do ren "%%f" "%%~nf.bak"\n\nrem 在文件名前加上日期前缀\nfor %%f in (*.jpg) do (\n    ren "%%f" "20261110_%%f"\n)\n\nrem 用数字序列重命名\ni=0\nfor %%f in (*.png) do (\n    set /a i+=1\n    set "name=00!i!"\n    ren "%%f" "!name:~-3!.png"\n)'))
    
    story.append(Paragraph('7.7 文件比较：fc', ST_SEC_TITLE))
    story.append(make_code_block('rem 基本比较\nfc file1.txt file2.txt\n\nrem 忽略大小写和空白差异\nfc /i /w file1.txt file2.txt\n\nrem 二进制比较（图片、exe）\nfc /b image1.png image2.png\n\nrem 把比较结果保存到文件\nfc log1.txt log2.txt > diff.txt 2>&1'))
    
    story.append(Paragraph('7.8 实战：批量备份脚本', ST_SEC_TITLE))
    story.append(Paragraph(
        '综合本章所学，写一个实用的"每日自动备份"脚本：', ST_BODY))
    
    story.append(make_code_block('@echo off\nchcp 65001 > nul\nsetlocal enabledelayedexpansion\n\nrem ========== 每日自动备份脚本 ==========\nset "BACKUP_DIR=D:\\DailyBackup"\nset "SOURCE_DIR=C:\\Users\\Harry\\Documents"\nset /a "KEEP_DAYS=30"\n\nrem 创建备份目录\nif not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"\n\nrem 生成日期标签（统一格式 YYYYMMDD）\nfor /f "tokens=2 delims==" %%d in (\'wmic os get localdatetime /value\') do set "DT=%%d"\nset "DATE_TAG=%DT:~0,8%"\nset "BACKUP_PATH=%BACKUP_DIR%\\%DATE_TAG%"\n\nrem 用 robocopy 执行镜像备份\nrobocopy "%SOURCE_DIR%" "%BACKUP_PATH%" /MIR /Z /MT:4 /R:2 /W:3 > "%BACKUP_PATH%_log.txt" 2>&1\n\nrem robocopy 退出码 0-7 都是成功\nif errorlevel 8 (\n    echo [失败] 备份出现严重错误！\n    exit /b 1\n)\n\nrem 清理超过 N 天的旧备份\nfor /f "delims=" %%d in (\'dir /b /ad /o-n "%BACKUP_DIR%"\') do (\n    set /a count+=1\n    if !count! gtr %KEEP_DAYS% (\n        echo 删除旧备份: %%d\n        rd /s /q "%BACKUP_DIR%\\%%d"\n    )\n)\n\necho [完成] 备份成功: %BACKUP_PATH%\nendlocal'))
    
    story.append(Spacer(1, 20))
    story.append(Paragraph('— 第7章 完 —', ParagraphStyle('end', fontName='DengL', fontSize=10, textColor='#7F8C8D', alignment=TA_LEFT)))
    story.append(PageBreak())
    return story


def ch8():
    """第8章：目录与路径操作"""
    story = []
    
    story.append(Paragraph('第8章 目录与路径操作', ST_CH_TITLE))
    story.append(Spacer(1, 6))
    
    story.append(Paragraph('8.1 cd —— 切换目录', ST_SEC_TITLE))
    story.append(Paragraph(
        '<font name="Consola" size="9" color="#C0392B">cd</font>（change directory）是最基础的目录操作命令。', ST_BODY))
    
    story.append(make_code_block('rem 切换到子目录\ncd Documents\n\nrem 切换到上一级\ncd ..\n\nrem 切换到根目录\ncd \n\nrem 跨盘符切换（必须加 /d！）\ncd /d D:\\Work\n\nrem 查看当前目录\ncd'))
    
    story.append(make_note_box(
        '重要：<b>cd C:\\Windows</b> 不会从 C 盘切到 D 盘，<b>cd /d D:\\Work</b> 才能跨盘符。'
        '这是 cmd 的历史遗留设计——盘符和目录是分开管理的。', 'warn'))
    
    story.append(Paragraph('8.2 pushd / popd —— 路径栈', ST_SEC_TITLE))
    story.append(Paragraph(
        '这对命令实现了一个"目录栈"。pushd 把当前目录压入栈并切换到新目录；popd 弹出栈顶目录并切换回去。', ST_BODY))
    
    story.append(make_code_block('@echo off\ncd C:\\Users\npushd D:\\Work\\Project\necho 现在在: %cd%\\npushd "E:\\Data\\Archive"\necho 现在在: %cd%\\n\npopd\necho 回到: %cd%\\n\npopd\necho 回到: %cd%'))
    
    story.append(Paragraph(
        'pushd/popd 的好处：你不需要记住之前在哪个目录，popd 自动回到上一个位置。'
        '它们在临时进入某个目录处理文件，然后返回原处时特别有用。', ST_BODY))
    
    story.append(Paragraph('pushd 的一个隐藏特性：<b>可以直接 pushd 网络路径</b>，它会自动映射成临时盘符！', ST_BODY))
    
    story.append(make_code_block('pushd \\\\NAS\\Share\\Docs\nrem 现在会自动有一个 Z: 盘映射到 \\\\NAS\\Share\\Docs\npopd\nrem popd 后 Z: 盘自动断开'))
    
    story.append(Paragraph('8.3 dir 和 tree —— 目录遍历', ST_SEC_TITLE))
    story.append(Paragraph('dir 的常用参数', ST_SUBSEC_TITLE))
    story.append(make_code_block('rem 基本列表\ndir\n\nrem 简洁模式（只显示文件名）\ndir /b\n\nrem 递归列出所有文件\ndir /s /b\n\nrem 只显示目录名\ndir /ad /b\n\nrem 只显示 .txt 文件\ndir /b *.txt\n\nrem 按修改时间排序（从新到旧）\ndir /o-d\n\nrem 按大小排序（从大到小）\ndir /o-s /s\n\nrem 显示完整路径\ndir /s /b'))
    
    story.append(Paragraph('tree —— 可视化目录树', ST_SUBSEC_TITLE))
    story.append(make_code_block('rem 显示当前目录树\ntree\n\nrem 带文件名的完整树\ntree /f\n\nrem 导出到文本文件\ntree /f > folder_structure.txt'))
    
    story.append(Paragraph('8.4 md / rd —— 创建和删除目录', ST_SEC_TITLE))
    story.append(Paragraph('md —— 创建目录', ST_SUBSEC_TITLE))
    story.append(make_code_block('rem 创建单个目录\nmd new_folder\n\nrem 创建嵌套目录（一条命令搞定所有中间层）\nmd a\\b\\c\\d\n\nrem 批量创建项目结构\nmd src md tests md docs md build'))
    
    story.append(make_note_box(
        'md 可以一次性创建多级嵌套目录，不需要逐级先创建中间目录。这是 Windows 独有的便利特性。', 'tip'))
    
    story.append(Paragraph('rd —— 删除目录', ST_SUBSEC_TITLE))
    story.append(make_code_block('rem 删除空目录\nrd empty_folder\n\nrem 强制删除非空目录及其内容\nrd /s /q big_folder\n\nrem /s 递归，/q 安静模式（不确认）'))
    
    story.append(Paragraph('8.5 路径拼接与规范化', ST_SEC_TITLE))
    story.append(Paragraph(
        '在 BAT 中处理路径时，经常需要把相对路径转成绝对路径。几个实用技巧：', ST_BODY))
    
    story.append(make_code_block('rem 获取脚本自身所在目录\nset "SCRIPT_DIR=%~dp0"\n\nrem 基于脚本目录拼接相对路径\nset "DATA_DIR=%SCRIPT_DIR%data"\n\nrem 把相对路径转成绝对路径\nfor %%i in ("relative\\path.txt") do set "ABS_PATH=%%~fi"\n\nrem 获取文件所在目录\nfor %%i in ("%SCRIPT_DIR%..\\config.ini") do set "CFG_DIR=%%~dpi"'))
    
    story.append(Paragraph('8.6 实战：批量创建项目结构', ST_SEC_TITLE))
    story.append(make_code_block('@echo off\nsetlocal\nrem ========== 创建新项目目录结构 ==========\nset /p "proj_name=项目名称: "\nif "%proj_name%"=="" exit /b\n\nset "proj_dir=%cd%\\\%proj_name%"\nmkdir "%proj_dir%"\nmkdir "%proj_dir%\\src"\nmkdir "%proj_dir%\\src\\components"\nmkdir "%proj_dir%\\src\\utils"\nmkdir "%proj_dir%\\tests"\nmkdir "%proj_dir%\\docs"\nmkdir "%proj_dir%\\build"\nmkdir "%proj_dir%\\deploy"\n\nrem 创建 .gitkeep 占位文件（让空目录能被 git 跟踪）\nfor /d %%d in ("%proj_dir%\\src\\components" "%proj_dir%\\src\\utils" "%proj_dir%\\tests" "%proj_dir%\\build" "%proj_dir%\\deploy") do (\n    echo. > "%%~d\\.gitkeep"\n)\n\necho 项目 %proj_name% 创建完毕！\ntree /f "%proj_dir%"\nendlocal'))
    
    story.append(Spacer(1, 20))
    story.append(Paragraph('— 第8章 完 —', ParagraphStyle('end', fontName='DengL', fontSize=10, textColor='#7F8C8D', alignment=TA_LEFT)))
    story.append(PageBreak())
    return story


def ch9():
    """第9章：系统管理命令"""
    story = []
    
    story.append(Paragraph('第9章 系统管理命令', ST_CH_TITLE))
    story.append(Spacer(1, 6))
    
    story.append(Paragraph(
        'BAT 脚本真正强大的地方在于——它可以直接调用 Windows 庞大的系统管理命令集。'
        '本章讲解进程、服务、注册表、计划任务等核心系统操作。', ST_BODY))
    
    story.append(Paragraph('9.1 进程管理：tasklist / taskkill', ST_SEC_TITLE))
    story.append(Paragraph('tasklist —— 查看进程', ST_SUBSEC_TITLE))
    story.append(make_code_block('rem 列出所有进程（默认表格格式）\ntasklist\n\nrem CSV 格式（便于解析）\ntasklist /fo csv\n\nrem 只列出包含 "sql" 的进程\ntasklist /fi "imagename eq sql*"\n\nrem 显示进程关联的服务\ntasklist /svc\n\nrem 显示详细内存/CPU使用\ntasklist /v\n\nrem 远程机器上查看进程\ntasklist /s 192.168.1.100 /u admin /p password'))
    
    story.append(Paragraph('taskkill —— 结束进程', ST_SUBSEC_TITLE))
    story.append(make_code_block('rem 按进程名结束（所有同名实例）\ntaskkill /im notepad.exe\n\nrem 按 PID 结束\ntaskkill /pid 1234\n\nrem 强制结束（不弹"是否结束"对话框）\ntaskkill /f /im notepad.exe\n\nrem 结束进程树（包括子进程）\ntaskkill /f /im chrome.exe /t\n\nrem 批量结束多个进程\ntaskkill /im notepad.exe /im calc.exe /im mspaint.exe\n\nrem 远程结束进程\ntaskkill /s 192.168.1.100 /f /im notepad.exe'))
    
    story.append(make_note_box(
        'taskkill /f 是暴力结束——进程没有机会保存数据就被杀了。'
        '如果可能，先用不带 /f 的 taskkill 给进程一个优雅退出的机会。', 'warn'))
    
    story.append(Paragraph('9.2 start —— 启动程序', ST_SEC_TITLE))
    story.append(make_code_block('rem 启动一个程序\nstart notepad.exe\n\nrem 带参数启动\nstart "My Title" calc.exe\n\nrem 等待程序结束后继续\nstart /wait setup.exe\n\nrem 最小化启动\nstart /min cmd.exe\n\nrem 后台静默运行（无窗口）\nstart /b /wait "" "silent_app.exe" /s\n\nrem 在指定目录下启动\nstart /d "D:\\Data" explorer.exe .\n\nrem 打开文件（用默认关联程序）\nstart "" report.pdf\nstart "" https://www.bing.com\nstart "" mailto:test@example.com'))
    
    story.append(make_note_box(
        'start 的第一个参数是<b>窗口标题</b>，可以为空但不能省略——'
        '所以经常看到 <font name="Consola" size="9" color="#C0392B">start "" app.exe</font>，'
        '两个引号就是为了提供一个空标题参数。如果你直接写 start app.exe，app.exe 会被当成标题！', 'warn'))
    
    story.append(Paragraph('9.3 systeminfo 与 wmic', ST_SEC_TITLE))
    story.append(Paragraph('systeminfo', ST_SUBSEC_TITLE))
    story.append(make_code_block('rem 查看完整系统信息\nsysteminfo\n\nrem 导出到文件\nsysteminfo > my_pc_info.txt 2>&1\n\nrem 远程查询\nsysteminfo /s 192.168.1.100 /u admin /p pwd'))
    
    story.append(Paragraph('wmic —— Windows Management Instrumentation', ST_SUBSEC_TITLE))
    story.append(Paragraph(
        '<font name="Consola" size="9" color="#C0392B">wmic</font> 是 Windows 上最强大的系统查询工具，可以访问几乎所有管理信息。', ST_BODY))
    
    story.append(make_code_block('rem 操作系统信息\nwmic os get Caption,Version,BuildNumber,OSArchitecture\n\nrem CPU 信息\nwmic cpu get Name,NumberOfCores,NumberOfLogicalProcessors,MaxClockSpeed\n\nrem 内存信息\nwmic memorychip get Capacity,Speed,Manufacturer\n\nrem 磁盘信息\nwmic diskdrive get Model,Size,MediaType\n\nrem 已安装的软件\nwmic product get Name,Version,InstallDate\n\nrem 网卡信息\nwmic nic where "PhysicalAdapter=True" get Name,MACAddress,Speed\n\nrem 启动时间\nfor /f "tokens=2 delims==" %i in (\'wmic os get lastbootuptime /value ^| find "="\') do @echo 上次启动: %i'))
    
    story.append(Paragraph('9.4 reg —— 注册表操作', ST_SEC_TITLE))
    story.append(Paragraph(
        '注册表是 Windows 的"总配置中心"。reg 命令可以增删查改注册表项。', ST_BODY))
    
    story.append(make_code_block('rem 查询注册表\nreg query HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\n\nrem 写入注册表\nreg add "HKLM\\SOFTWARE\\MyApp" /v Version /t REG_SZ /d "1.0.0" /f\n\nrem /v  值名（Value name）\nrem /t  值类型（REG_SZ, REG_DWORD, REG_EXPAND_SZ, REG_MULTI_SZ, REG_BINARY）\nrem /d  值数据（Data）\nrem /f  强制覆盖不确认\n\nrem 删除值\nreg delete "HKLM\\SOFTWARE\\MyApp" /v Version /f\n\nrem 删除整个键\nreg delete "HKLM\\SOFTWARE\\MyApp" /f\n\nrem 导出注册表\nreg export HKLM\\SOFTWARE\\MyApp myapp_registry.reg\n\nrem 导入注册表\nreg import myapp_registry.reg'))
    
    story.append(make_note_box(
        '注册表根键缩写：', 'note'))
    
    reg_data = [
        ['缩写', '完整名称', '含义'],
        ['HKLM', 'HKEY_LOCAL_MACHINE', '系统级配置（所有用户）'],
        ['HKCU', 'HKEY_CURRENT_USER', '当前用户配置'],
        ['HKCR', 'HKEY_CLASSES_ROOT', '文件类型关联'],
        ['HKU',  'HKEY_USERS', '所有用户配置'],
        ['HKCC', 'HKEY_CURRENT_CONFIG', '当前硬件配置'],
    ]
    t = Table(_wrap_table_rows(reg_data), colWidths=[25*mm, 65*mm, 50*mm])
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
    
    story.append(Paragraph('9.5 schtasks —— 计划任务', ST_SEC_TITLE))
    story.append(Paragraph('创建计划任务', ST_SUBSEC_TITLE))
    story.append(make_code_block('rem 每天凌晨2点运行备份脚本\nschtasks /create /tn "DailyBackup" /tr "D:\\Scripts\\backup.bat" /sc daily /st 02:00 /f\n\nrem 每周一早上8点运行\nschtasks /create /tn "WeeklyReport" /tr "D:\\Scripts\\report.bat" /sc weekly /d MON /st 08:00 /f\n\nrem 系统启动时运行\nschtasks /create /tn "AutoSync" /tr "D:\\Scripts\\sync.bat" /sc onstart /rl HIGHEST /f\n\nrem 用户登录时运行\nschtasks /create /tn "WelcomeMsg" /tr "msg * 欢迎回来！" /sc onlogon /f'))
    
    story.append(Paragraph('管理计划任务', ST_SUBSEC_TITLE))
    story.append(make_code_block('rem 列出所有任务\nschtasks /query /fo csv /v\n\nrem 运行指定任务\nschtasks /run /tn "DailyBackup"\n\nrem 结束正在运行的任务\nschtasks /end /tn "DailyBackup"\n\nrem 删除任务\nschtasks /delete /tn "DailyBackup" /f\n\nrem 导出任务配置\nschtasks /query /tn "DailyBackup" /xml > task.xml\n\nrem 从 XML 导入任务\nschtasks /create /tn "DailyBackup" /xml task.xml /f'))
    
    story.append(Paragraph('9.6 服务管理', ST_SEC_TITLE))
    story.append(Paragraph('sc（Service Control）是专业的服务管理工具，比 net start/stop 功能更全：', ST_BODY))
    
    story.append(make_code_block('rem 查看所有服务\nsc query type= service state= all\n\nrem 启动/停止服务\nsc start Spooler\nsc stop Spooler\n\nrem 查询单个服务详情\nsc query W32Time\nsc qc W32Time  & rem 显示配置\n\nrem 创建服务\nsc create MyService binPath= "D:\\MyApp\\service.exe" start= auto\n\nrem 删除服务（先停止再删）\nsc stop MyService\nsc delete MyService\n\nrem 改变服务启动类型\nsc config Spooler start= disabled    & rem 禁用\nsc config Spooler start= auto        & rem 自动\nsc config Spooler start= demand      & rem 手动'))
    
    story.append(make_note_box(
        'sc 的参数里 <font name="Consola" size="9" color="#C0392B">=</font> 后面必须有一个空格！'
        '正确：<font name="Consola" size="9" color="#C0392B">start= auto</font>，错误：<font name="Consola" size="9" color="#C0392B">start=auto</font>。'
        '这是 sc 的一个非常"坑"的设计。', 'warn'))
    
    story.append(Paragraph('9.7 net user / net share', ST_SEC_TITLE))
    story.append(make_code_block('rem 创建新用户（需要管理员权限）\nnet user newuser Password123 /add\n\nrem 设置用户密码\nnet user newuser NewPassword\n\nrem 删除用户\nnet user newuser /del\n\nrem 创建共享文件夹\nnet share Docs=D:\\Documents /grant:everyone,FULL\n\nrem 删除共享\nnet share Docs /del\n\nrem 列出所有共享\nnet share\n\nrem 查看会话\nnet session'))
    
    story.append(Paragraph('9.8 netsh —— 网络配置', ST_SEC_TITLE))
    story.append(make_code_block('rem 设置静态 IP\nnetsh interface ip set address "以太网" static 192.168.1.100 255.255.255.0 192.168.1.1\n\nrem 设置 DNS\nnetsh interface ip set dns "以太网" static 8.8.8.8 primary\n\nrem 改为自动获取 DHCP\nnetsh interface ip set address "以太网" dhcp\nnetsh interface ip set dns "以太网" dhcp\n\nrem 导出/导入网络配置\nnetsh dump > network_config.txt\nnetsh exec network_config.txt\n\nrem 配置防火墙规则\nnetsh advfirewall firewall add rule name="Allow SSH" dir=in action=allow protocol=TCP localport=22'))
    
    story.append(Paragraph('9.9 实战：开机自启脚本', ST_SEC_TITLE))
    story.append(Paragraph(
        '综合本章所学，写一个能让脚本"开机自动运行"的方案：', ST_BODY))
    
    story.append(make_code_block('@echo off\nrem ========== 方案一：放入启动文件夹 ==========\nrem 对当前用户有效\nset "STARTUP_DIR=%appdata%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"\ncopy /y "%~f0" "%STARTUP_DIR%\\%~nx0"\necho 已添加到启动文件夹（当前用户）\n\nrem ========== 方案二：注册表 Run 键 ==========\nrem HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run（当前用户）\nrem HKLM\\...\\Run（所有用户，需要管理员权限）\nreg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run" /v "MyTool" /t REG_SZ /d "\"%~f0\"" /f\n\nrem ========== 方案三：计划任务 ==========\nschtasks /create /tn "MyAutoTask" /tr "\"%~f0\"" /sc onlogon /f\n\necho 三种开机自启方式已配置'))
    
    story.append(Spacer(1, 20))
    story.append(Paragraph('— 第9章 完 —', ParagraphStyle('end', fontName='DengL', fontSize=10, textColor='#7F8C8D', alignment=TA_LEFT)))
    story.append(PageBreak())
    return story


def ch10():
    """第10章：网络操作命令"""
    story = []
    
    story.append(Paragraph('第10章 网络操作命令', ST_CH_TITLE))
    story.append(Spacer(1, 6))
    
    story.append(Paragraph('10.1 网络诊断基础', ST_SEC_TITLE))
    story.append(Paragraph('ipconfig', ST_SUBSEC_TITLE))
    story.append(make_code_block('rem 查看所有网卡的简要 IP 信息\nipconfig\n\nrem 显示完整信息（MAC、DHCP、DNS、网关等）\nipconfig /all\n\nrem 刷新 DNS 缓存\nipconfig /flushdns\n\nrem 释放/重新获取 DHCP 地址\nipconfig /release\nipconfig /renew\n\nrem 导出配置\nipconfig /all > network_info.txt'))
    
    story.append(Paragraph('ping', ST_SUBSEC_TITLE))
    story.append(make_code_block('rem 基本连通性测试\nping 8.8.8.8\n\nrem 持续 ping（Ctrl+C 停止）\nping -t www.bing.com\n\nrem 发送 10 个包\nping -n 10 www.bing.com\n\nrem 大包测试（检查 MTU）\nping -l 1472 -n 10 192.168.1.1\n\nrem 解析主机名并 ping\nping -a 192.168.1.1'))
    
    story.append(Paragraph('tracert —— 路由追踪', ST_SUBSEC_TITLE))
    story.append(make_code_block('rem 查看到目标的完整路由路径\ntracert www.bing.com\n\nrem 限制最大跳数\ntracert -h 15 223.5.5.5\n\nrem 不解析主机名（更快）\ntracert -d www.bing.com'))
    
    story.append(Paragraph('10.2 netstat —— 端口与连接', ST_SEC_TITLE))
    story.append(make_code_block('rem 显示所有活动连接和监听端口\nnetstat -ano\n\nrem 只显示 TCP 连接\nnetstat -ano -p tcp\n\nrem 按 PID 过滤（查找哪个进程占了端口）\nnetstat -ano | findstr ":8080"\n\nrem 显示统计信息\nnetstat -s\n\nrem 持续刷新（2秒一次）\nnetstat -ano 2'))
    
    story.append(make_note_box(
        'netstat -ano 的输出中最后一列是 PID（进程ID）。用 tasklist /fi "PID eq 1234" 就能查出是哪个程序。', 'tip'))
    
    story.append(Paragraph('10.3 文件下载：bitsadmin / certutil', ST_SEC_TITLE))
    story.append(Paragraph(
        'BAT 没有原生的 HTTP 下载命令，但 Windows 自带几个"隐形下载器"：', ST_BODY))
    
    story.append(Paragraph('bitsadmin —— 后台下载器', ST_SUBSEC_TITLE))
    story.append(make_code_block('rem 创建一个下载任务\nbitsadmin /transfer MyDownload "https://example.com/file.zip" "D:\\Downloads\\file.zip"\n\nrem 后台下载（不阻塞脚本）\nbitsadmin /create /download MyJob\nbitsadmin /addfile MyJob "https://example.com/file.zip" "D:\\Downloads\\file.zip"\nbitsadmin /resume MyJob\nbitsadmin /complete MyJob\n\nrem 查询下载状态\nbitsadmin /list /allusers'))
    
    story.append(make_note_box(
        'bitsadmin 有一个隐蔽但重要的特性：它的下载请求走 BITS 服务（后台智能传输服务），'
        '在企业环境中如果 HTTP 代理拦截了正常下载，bitsadmin 有时反而能绕过。', 'tip'))
    
    story.append(Paragraph('certutil —— 最隐蔽的下载技巧', ST_SUBSEC_TITLE))
    story.append(Paragraph(
        'certutil 本是证书工具，但它有一个未文档化的功能：能把 URL 内容下载下来！这是 BAT 里最流行的"黑客技巧"之一：', ST_BODY))
    
    story.append(make_code_block('rem 下载文件\ncertutil -urlcache -split -f "https://example.com/file.exe" output.exe\n\nrem 参数说明：\nrem -urlcache  操作 URL 缓存\nrem -split    分割输出\nrem -f        强制覆盖'))
    
    story.append(make_note_box(
        '⚠️ 注意：certutil 下载没有断点续传、不支持 HTTPS 证书校验，且可能被杀毒软件拦截。'
        '正式场合请用 bitsadmin 或 PowerShell 的 Invoke-WebRequest。', 'warn'))
    
    story.append(Paragraph('10.4 net use —— 网络盘映射', ST_SEC_TITLE))
    story.append(make_code_block('rem 映射网络盘（持久化，重启后还在）\nnet use Z: \\\\NAS\\Documents /persistent:yes\n\nrem 临时映射（当前会话有效）\nnet use Y: \\\\Server\\Share /persistent:no\n\nrem 带用户名密码映射\nnet use Z: \\\\NAS\\Private /user:admin "password"\n\nrem 查看当前映射\nnet use\n\nrem 断开映射\nnet use Z: /delete\n\nrem 断开所有映射\nnet use * /delete /y'))
    
    story.append(make_note_box(
        '如果网络盘已被断开但还显示红色"X"，用 <font name="Consola" size="9" color="#C0392B">net use Z: \\\\NAS\\Share /persistent:yes</font> 重新连接。'
        '或者直接 <font name="Consola" size="9" color="#C0392B">pushd \\\\NAS\\Share</font>，用完 popd 自动清理。', 'tip'))
    
    story.append(Paragraph('10.5 实战：批量网络连通性检测', ST_SEC_TITLE))
    story.append(make_code_block('@echo off\nsetlocal enabledelayedexpansion\nrem ========== 批量 Ping 检测 ==========\nrem 创建 targets.txt，每行一个 IP 或域名\n\nset "TARGETS=targets.txt"\nset "RESULT=ping_result.csv"\n\necho IP,时间,状态 > "%RESULT%"\n\nfor /f "usebackq tokens=*" %%ip in ("%TARGETS%") do (\n    set /a count+=1\n    <nul set /p "=正在检测 %%ip ... "\n    \n    for /f "tokens=5 delims==" %%t in (\'ping -n 1 -w 1000 %%ip ^| findstr "时间=" ^| findstr /v "<"\') do (\n        echo %%ip,%%t,OK >> "%RESULT%"\n        echo OK - %%t\n    ) || (\n        echo %%ip,超时,FAIL >> "%RESULT%"\n        echo 超时\n    )\n)\n\necho.\necho 检测完成，结果已保存到 %RESULT%\nendlocal'))
    
    story.append(Spacer(1, 20))
    story.append(Paragraph('— 第10章 完 —', ParagraphStyle('end', fontName='DengL', fontSize=10, textColor='#7F8C8D', alignment=TA_LEFT)))
    story.append(PageBreak())
    return story


def get_chapters():
    return [ch7(), ch8(), ch9(), ch10()]
