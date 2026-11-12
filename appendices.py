# -*- coding: utf-8 -*-
"""第五部分：附录与参考篇"""

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
    _wrap_table_rows, ST_TD_CODE
)

# 不加粗的等宽字体样式（用于脚本名）
_ST_TD_MONO = ParagraphStyle('TableMono',
    fontName='Consola', fontSize=9, leading=13,
    textColor=colors.HexColor('#2C3E50'), alignment=TA_LEFT)


def appendices():
    story = []
    
    # ========== 附录A：命令速查表 ==========
    story.append(Paragraph('附录A Windows 批处理核心命令速查表', ST_CH_TITLE))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        '本附录按功能分类，汇总 BAT 批处理中最常用的命令。每个命令附带基本语法和简短说明。', ST_BODY))
    
    cmd_sections = [
        ('流程控制', [
            ['call', '调用外部 BAT 或内部子程序（:label）', 'call other.bat / call :sub'],
            ['goto', '跳转到指定标签', 'goto :error'],
            ['if', '条件判断（4种模式）', 'if errorlevel 1 / if exist file'],
            ['for', '循环（/D /R /L /F 四种模式）', 'for /L %%i in (1,1,10) do'],
            ['exit', '退出脚本', 'exit /b [code]'],
            ['pause', '暂停等待按键', 'pause'],
        ]),
        ('变量与环境', [
            ['set', '定义/查看/删除变量', 'set "var=value" / set var='],
            ['setlocal', '创建局部变量作用域', 'setlocal enabledelayedexpansion'],
            ['endlocal', '结束局部作用域', 'endlocal'],
            ['shift', '移动 %1~%9 参数', 'shift /n'],
            ['echo', '输出文本/控制回显', '@echo off / echo text'],
        ]),
        ('文件操作', [
            ['copy', '复制文件', 'copy file1 file2'],
            ['xcopy', '高级复制（支持目录树）', 'xcopy /E /I src dest'],
            ['robocopy', '企业级文件复制/同步', 'robocopy src dest /MIR'],
            ['move', '移动/重命名', 'move old new'],
            ['del', '删除文件', 'del /f /q file'],
            ['ren', '重命名', 'ren old new'],
            ['type', '显示文件内容', 'type file.txt'],
            ['fc', '文件比较', 'fc /i file1 file2'],
            ['more', '分页显示', 'more +10 file'],
        ]),
        ('目录操作', [
            ['cd', '切换目录', 'cd /d D:\\path'],
            ['md', '创建目录', 'md path\\to\\dir'],
            ['rd', '删除目录', 'rd /s /q dir'],
            ['dir', '列出目录内容', 'dir /s /b *.txt'],
            ['tree', '目录树可视化', 'tree /f'],
            ['pushd', '压入目录栈并跳转', 'pushd \\\\NAS\\Share'],
            ['popd', '弹出目录栈', 'popd'],
        ]),
        ('系统管理', [
            ['tasklist', '列出进程', 'tasklist /fi "pid eq 1234"'],
            ['taskkill', '结束进程', 'taskkill /f /im app.exe'],
            ['start', '启动程序', 'start /wait "" app.exe'],
            ['sc', '服务控制', 'sc create / query / start'],
            ['schtasks', '计划任务', 'schtasks /create /tn "Name" /tr script'],
            ['reg', '注册表操作', 'reg add / query / delete'],
            ['wmic', 'WMI 系统查询', 'wmic os get /format:list'],
            ['systeminfo', '系统信息快照', 'systeminfo'],
            ['net', '网络/用户/共享', 'net user / net share / net use'],
            ['netsh', '网络配置', 'netsh interface ip set address'],
        ]),
        ('网络工具', [
            ['ping', '连通性测试', 'ping -n 10 -t host'],
            ['tracert', '路由追踪', 'tracert -d host'],
            ['ipconfig', 'IP 配置', 'ipconfig /all /flushdns'],
            ['netstat', '网络连接', 'netstat -ano -p tcp'],
            ['findstr', '正则文本搜索', 'findstr /i "error warn" file'],
            ['find', '简单文本搜索', 'find /c "text" file'],
            ['sort', '排序', 'sort /r file'],
            ['bitsadmin', '后台下载', 'bitsadmin /transfer name url dest'],
            ['certutil', '证书工具（隐式下载）', 'certutil -urlcache -split -f url'],
        ]),
        ('批处理专用', [
            ['rem', '注释', 'rem comment'],
            ['::', '注释（hack写法）', ':: comment'],
            ['errorlevel', '上一条命令退出码', 'if errorlevel 1'],
            ['%var%', '预处理阶段变量展开', '%computername%'],
            ['!var!', '执行阶段变量展开（需启用）', '!counter!'],
            ['%~dp0', '脚本自身目录', '%~dp0data'],
            ['%~nx1', '参数文件名+后缀', '%%~nx1'],
        ]),
    ]
    
    for section_name, rows in cmd_sections:
        story.append(Paragraph(f'A.{cmd_sections.index((section_name, rows))+1} {section_name}', ST_SEC_TITLE))
        data = [['命令', '说明', '示例']] + rows
        t = Table(_wrap_table_rows(data, col_styles={0: ST_TD_CODE}), colWidths=[26.3*mm, 65.8*mm, 65.8*mm])
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
    
    story.append(PageBreak())
    
    # ========== 附录B：环境变量大全 ==========
    story.append(Paragraph('附录B cmd.exe 环境变量大全', ST_CH_TITLE))
    story.append(Spacer(1, 6))
    
    story.append(Paragraph('B.1 cmd 内置特殊变量', ST_SEC_TITLE))
    builtin_vars = [
        ['变量', '含义', '类型'],
        ['%cd%',         '当前工作目录',     '动态'],
        ['%date%',       '当前日期',         '动态（格式依赖系统设置）'],
        ['%time%',       '当前时间',         '动态（格式依赖系统设置）'],
        ['%random%',     '0~32767 随机数',   '动态'],
        ['%errorlevel%', '上一条命令退出码',  '动态'],
        ['%cmdextversion%', '命令扩展版本号', '常量（值=2）'],
        ['%_cmdvarset%', '命令行参数（shift后变化）', '动态'],
        ['%^e%',         'ESC 转义符',       '动态（cmd 1903+）'],
        ['%=C:%',        'C盘当前目录',      '动态'],
    ]
    t = Table(_wrap_table_rows(builtin_vars, col_styles={0: ST_TD_CODE}), colWidths=[40*mm, 70*mm, 45*mm])
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
    
    story.append(Paragraph('B.2 Windows 系统环境变量', ST_SEC_TITLE))
    sys_vars = [
        ['变量', '典型值', '含义'],
        ['%SystemRoot% / %windir%', 'C:\\Windows', 'Windows 安装目录'],
        ['%SystemDrive%', 'C:', '系统驱动器号'],
        ['%System%', 'C:\\Windows\\System32', '系统目录'],
        ['%ProgramFiles%', 'C:\\Program Files', '64位程序目录'],
        ['%ProgramFiles(x86)%', 'C:\\Program Files (x86)', '32位程序目录'],
        ['%USERPROFILE%', 'C:\\Users\\Harry', '当前用户主目录'],
        ['%APPDATA%', 'C:\\Users\\Harry\\AppData\\Roaming', '用户应用数据'],
        ['%LOCALAPPDATA%', 'C:\\Users\\Harry\\AppData\\Local', '本地应用数据'],
        ['%TEMP% / %TMP%', 'C:\\Users\\Harry\\AppData\\Local\\Temp', '临时文件目录'],
        ['%COMPUTERNAME%', 'DESKTOP-HARRY', '计算机名'],
        ['%USERNAME%', 'Harry', '当前用户名'],
        ['%NUMBER_OF_PROCESSORS%', '8', 'CPU 逻辑核心数'],
        ['%OS%', 'Windows_NT', '操作系统类型（固定值）'],
        ['%PATH%', 'C:\\Windows\\System32;...', '命令搜索路径'],
        ['%PATHEXT%', '.COM;.EXE;.BAT;.CMD;.VBS;...', '可执行文件后缀列表'],
    ]
    t = Table(_wrap_table_rows(sys_vars, col_styles={0: ST_TD_CODE}), colWidths=[47.9*mm, 71.8*mm, 38.3*mm])
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
    
    story.append(Paragraph('B.3 变量优先级', ST_SEC_TITLE))
    story.append(Paragraph('从高到低：', ST_BODY))
    story.append(Paragraph('1. 当前 cmd 会话中 set 定义的变量（最高）', ST_BODY_NOINDENT))
    story.append(Paragraph('2. 用户环境变量（注册表 HKCU\\Environment）', ST_BODY_NOINDENT))
    story.append(Paragraph('3. 系统环境变量（注册表 HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment）', ST_BODY_NOINDENT))
    story.append(Paragraph('4. cmd 内置变量（%cd%、%time% 等总是动态的，无法覆盖）', ST_BODY_NOINDENT))
    
    story.append(PageBreak())
    
    # ========== 附录C：常见问题与疑难解答 ==========
    story.append(Paragraph('附录C 批处理常见问题与疑难解答', ST_CH_TITLE))
    story.append(Spacer(1, 6))
    
    faqs = [
        ('Q1: BAT 脚本里中文乱码怎么办？', 
         '确保文件保存为 UTF-8 with BOM，脚本开头加 <font name="Consola" size="9" color="#C0392B">chcp 65001 > nul</font>。'
         '在 VS Code 右下角选择 "UTF-8 with BOM" 保存编码。如果是老系统（Win7），改用 GBK 编码 + chcp 936。'),
        ('Q2: for 循环里变量值不变怎么办？',
         '需要启用变量延迟扩展：脚本开头加 <font name="Consola" size="9" color="#C0392B">setlocal enabledelayedexpansion</font>，'
         '然后在循环内用 <font name="Consola" size="9" color="#C0392B">!var!</font> 代替 <font name="Consola" size="9" color="#C0392B">%var%</font>。'),
        ('Q3: 路径里有空格导致命令执行失败？',
         '所有含空格的路径必须用<b>双引号包裹</b>：<font name="Consola" size="9" color="#C0392B">copy "C:\\Program Files\\a.txt" "D:\\target"</font>。'
         '此外 cd 跨盘符时必须加 <font name="Consola" size="9" color="#C0392B">/d</font>：<font name="Consola" size="9" color="#C0392B">cd /d "D:\\My Folder"</font>。'),
        ('Q4: echo 输出空行写 echo. 还是 echo: 还是 echo(？',
         '这三种都可以输出空行。推荐用 <font name="Consola" size="9" color="#C0392B">echo.</font> 或 <font name="Consola" size="9" color="#C0392B">echo(</font>——'
         '它们比 echo: 更可靠。注意 echo. 如果当前目录下有个叫 "echo" 的文件会失败，但这种情况极其罕见。'),
        ('Q5: if 里用 %errorlevel% 还是 errorlevel？',
         '两种都可以但有区别：<b>if errorlevel 1</b> 检查退出码 >= 1；<b>if %errorlevel%==1</b> 检查等于 1。'
         '注意 %errorlevel% 会在预处理阶段展开，在括号块内可能得到旧值——这种情况要用 if !errorlevel!==1 或直接用 errorlevel N。'),
        ('Q6: 怎么在 BAT 里获取管理员权限？',
         '方案1：<font name="Consola" size="9" color="#C0392B">runas /user:Administrator "cmd /c %~f0"</font>；'
         '方案2：用 VBScript ShellExecute 以 runas 方式启动 cmd；'
         '方案3：创建高权限的计划任务然后立即运行。详见第 11.3 节。'),
        ('Q7: BAT 能 sleep 吗？',
         'BAT 没有原生 sleep 命令，但有多种替代：<font name="Consola" size="9" color="#C0392B">timeout /t 5 /nobreak</font>（推荐）、'
         '<font name="Consola" size="9" color="#C0392B">ping -n 6 127.0.0.1 > nul</font>（通用但不精确）、'
         '或调用 PowerShell 的 Start-Sleep。'),
        ('Q8: 怎么让 BAT 窗口关闭前停留一会儿？',
         '脚本最后加 <font name="Consola" size="9" color="#C0392B">pause</font>。如果用 exit 关闭整个 cmd，可以在 BAT 开头加：'
         '<font name="Consola" size="9" color="#C0392B">if /i "%1"=="_pause" goto :main & cmd /k "%~f0" _pause & exit</font>。'),
        ('Q9: 如何获取脚本自身所在目录？',
         '用 <font name="Consola" size="9" color="#C0392B">%~dp0</font>（注意末尾有反斜杠）。推荐保存到变量：'
         '<font name="Consola" size="9" color="#C0392B">set "SCRIPT_DIR=%~dp0"</font>，之后用 <font name="Consola" size="9" color="#C0392B">%SCRIPT_DIR%data\\file.txt</font> 拼接路径。'),
        ('Q10: 怎么把 BAT 变成 EXE？',
         '三种主流方案：WinRAR SFX 自解压、IExpress（Windows 自带）、Bat To Exe Converter 等第三方工具。'
         '第 14.2 节提供了完整方案对比和一个自写的 C# 编译方案。'),
        ('Q11: for /f 的 delims 和 tokens 怎么配合？',
         'delims 指定用什么字符分隔行（默认空格和 Tab），tokens 指定取第几段（从 1 开始）。'
         'tokens=1,2,3 会把第 1/2/3 段分别赋给 %%a、%%b、%%c；tokens=1-3 效果相同但更短。'
         'tokens=* 表示整行赋给第一个变量。详见第 5.5 节。'),
        ('Q12: 怎么判断文件是否被占用（正在使用）？',
         '没有直接命令。变通方案：尝试用 >> 追加写入一行（echo test>> file），成功则没被占用，失败（errorlevel 1）则被占用。'
         '或者用 handle.exe（Sysinternals 工具）查找锁定文件的进程。'),
        ('Q13: BAT 脚本之间怎么互相传参？',
         '调用方：<font name="Consola" size="9" color="#C0392B">call sub.bat "arg1" "arg2"</font>；'
         '被调用方用 <font name="Consola" size="9" color="#C0392B">%1 %2 %*</font> 接收。'
         '如果需要传递大量变量，用 setlocal/endlocal + 共享文件 或 管道（但管道会丢失变量，不推荐）。'),
        ('Q14: 怎么检测自己是否以管理员身份运行？',
         '方案1：尝试写入 %windir%（失败则不是管理员）；'
         '方案2：查询管理员组 SID（S-1-5-32-544）；'
         '方案3：最简单——执行一个需要管理员权限的命令看 errorlevel。'),
        ('Q15: 如何输出带颜色的文字？',
         'Windows 10 1903+ 支持 ANSI 转义序列，详见第 11.1 节。'
         '老系统只能通过 VBScript（cscript 只能输出黑白）或 PowerShell 的 Write-Host -ForegroundColor。'),
        ('Q16: rem 和 :: 有什么区别？',
         'rem 是正规的命令；:: 是 hack（把 :: 当作无效标签）。'
         '在括号块、for 的 () 内部，:: 可能导致解析错误——此时必须用 rem。稳妥起见，一律用 rem。'),
        ('Q17: BAT 怎么操作注册表？',
         '用 reg 命令：<font name="Consola" size="9" color="#C0392B">reg add / query / delete / export / import</font>。'
         '操作 HKLM 分支需要管理员权限。详见第 9.4 节。'),
        ('Q18: 怎么从 BAT 里下载文件？',
         '推荐用 bitsadmin（企业级、支持断点续传）；或 PowerShell Invoke-WebRequest；'
         '不推荐 certutil（隐蔽但可能被杀软拦截）。详见第 10.3 节。'),
        ('Q19: 批处理文件最大多大？',
         '技术上没有硬性限制。实际中 1-2MB 完全没问题。但文件越大，cmd 解析预扫描阶段开销越大。'
         '建议超过 5000 行时考虑用 PowerShell 或 Python 重写。'),
        ('Q20: 为什么我的 BAT 运行一闪而过？',
         '通常有三个原因：① 路径或文件名中有特殊字符导致 cmd 找不到文件；② 脚本执行出错后没有 pause；'
         '③ exit 关闭了 cmd 窗口。调试方法：在 cmd 里手动运行（cmd /k "call myscript.bat"），或在脚本末尾加 pause。'),
    ]
    
    for q, a in faqs:
        story.append(Paragraph(q, ST_SUBSEC_TITLE))
        story.append(Paragraph(a.replace('<', '<').replace('>', '>'), ST_BODY))
        story.append(Spacer(1, 4))
    
    story.append(PageBreak())
    
    # ========== 附录D：开发工具与资源 ==========
    story.append(Paragraph('附录D BAT 开发工具与资源', ST_CH_TITLE))
    story.append(Spacer(1, 6))
    
    story.append(Paragraph('D.1 编辑器推荐', ST_SEC_TITLE))
    
    tools_data = [
        ['编辑器', '适用平台', 'BAT 支持', '说明'],
        ['VS Code', '全平台', '插件', '免费、插件丰富、Git 集成好。安装 "Batch Script Support"'],
        ['Notepad++', 'Windows', '内建', '经典轻量编辑器，自带 BAT 语法高亮'],
        ['Sublime Text', '全平台', '插件', '优雅的商业编辑器，需装 Batch Script 插件'],
        ['TextPad', 'Windows', '内建', '老牌 Windows 文本编辑器'],
        ['Notepad (Win11)', 'Windows 11', '内建', '新版记事本支持多标签、UTF-8 BOM'],
    ]
    t = Table(_wrap_table_rows(tools_data), colWidths=[35*mm, 30*mm, 35*mm, 50*mm])
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
    
    story.append(Paragraph('D.2 BAT 调试工具', ST_SEC_TITLE))
    story.append(Paragraph('• <b>echo on</b>：在脚本开头加 echo on 显示每一条执行的命令', ST_BODY_NOINDENT))
    story.append(Paragraph('• <b>pause</b>：在关键位置暂停看变量值', ST_BODY_NOINDENT))
    story.append(Paragraph('• <b>cmd /k "call script.bat"</b>：让窗口不关闭', ST_BODY_NOINDENT))
    story.append(Paragraph('• <b>Process Monitor</b>（Sysinternals）：监控文件、注册表、网络操作', ST_BODY_NOINDENT))
    story.append(Paragraph('• <b>Process Explorer</b>（Sysinternals）：查看进程详情、句柄、DLL', ST_BODY_NOINDENT))
    story.append(Paragraph('• <b>PES Explorer</b>：查看 PE 文件（.exe/.dll）结构', ST_BODY_NOINDENT))
    
    story.append(Paragraph('D.3 BAT 转 EXE 工具', ST_SEC_TITLE))
    tool_data = [
        ['工具', '类型', '说明'],
        ['WinRAR SFX', '商业软件', '最通用的方案，不需要额外工具'],
        ['IExpress', 'Windows 自带', '在 System32 目录里，完全免费'],
        ['Bat To Exe Converter', '免费软件', 'bat2exe.net，支持加密、压缩、图标替换'],
        ['Advanced BAT to EXE Converter', '商业软件', '功能最全，支持多种加密方式'],
        ['Bat2Exe Pro', '免费', '开源项目，支持自定义图标'],
        ['C# 自编译方案', 'DIY', '见第 14.2 节'],
    ]
    t = Table(_wrap_table_rows(tool_data), colWidths=[50*mm, 35*mm, 60*mm])
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
    
    story.append(Paragraph('D.4 在线学习资源', ST_SEC_TITLE))
    story.append(Paragraph('• <b>Microsoft Learn - Windows Commands</b>（官方）：learn.microsoft.com/windows-server/administration/windows-commands', ST_BODY_NOINDENT))
    story.append(Paragraph('• <b>Rob van der Woude 的批处理页面</b>（权威）：robvanderwoude.com/batchfiles.php', ST_BODY_NOINDENT))
    story.append(Paragraph('• <b>Dostips</b>（入门）：dostips.com/commandlinescripts', ST_BODY_NOINDENT))
    story.append(Paragraph('• <b>Tutorialspoint Batch Script</b>：tutorialspoint.com/batch_script', ST_BODY_NOINDENT))
    story.append(Paragraph('• <b>SS64</b>（完整命令参考）：ss64.com/nt', ST_BODY_NOINDENT))
    story.append(Paragraph('• <b>批处理之家（中文社区）</b>：bbs.bathome.net', ST_BODY_NOINDENT))
    
    story.append(Spacer(1, 20))
    return story


def appendix_e():
    story = []
    story.append(Paragraph('附录E 示例代码全集索引', ST_CH_TITLE))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        '本书所有章节中出现的可运行代码示例，以下按章节索引。所有代码均已在 Windows 10/11 环境下测试通过。', ST_BODY))
    
    code_index = [
        ['章节', '脚本名', '功能简述'],
        ['2.7', 'sysinfo.bat', '系统信息查询工具（第一个完整脚本）'],
        ['4.5', 'calc_demo.bat', 'set /a 数值计算演示'],
        ['4.6', 'str_ops.bat', '字符串替换/截取/长度计算'],
        ['5.3', 'menu.bat', 'goto + call 菜单程序'],
        ['5.5', 'for_f_demo.bat', 'for /F 解析文件和命令输出'],
        ['7.2', 'copy_demo.bat', 'copy /xcopy /robocopy 对比'],
        ['7.4', 'robocopy_sync.bat', 'robocopy 镜像同步'],
        ['7.8', 'daily_backup.bat', '每日自动备份脚本'],
        ['8.6', 'project_structure.bat', '批量创建项目目录结构'],
        ['9.9', 'autorun_setup.bat', '三种开机自启配置方案'],
        ['10.5', 'ping_batch.bat', '批量 Ping 检测 + CSV 导出'],
        ['11.1', 'ansi_colors.bat', 'ANSI 彩色输出演示'],
        ['11.3', 'uac_elevate.bat', 'UAC 提权三种方案'],
        ['11.6', 'hta_gui.bat', 'BAT 生成 HTA GUI 界面'],
        ['12.1', 'system_cleanup.bat', '系统垃圾清理工具'],
        ['12.2', 'startup_manager.bat', '启动项管理工具'],
        ['12.3', 'batch_service.bat', '服务批量运维工具'],
        ['12.5', 'sys_snapshot.bat', '系统快照一键收集'],
        ['13.2', 'remote_exec.bat', '批量远程执行（PsExec）'],
        ['13.3', 'batch_deploy.bat', '批量文件分发'],
        ['13.4', 'net_monitor.bat', '网络端口监控脚本'],
        ['13.5', 'wifi_export.bat', 'WiFi 密码批量导出'],
        ['14.1', 'aes_encrypt.bat', 'PowerShell AES 文件加密'],
        ['14.2', 'bat2exe.bat', 'BAT 转 EXE（自写 C# 方案）'],
        ['14.3', 'auto_type.bat', 'VBScript 键盘自动输入'],
        ['14.4', 'secure_download.bat', '安全下载-校验-执行流程'],
        ['14.5', 'admin_hta.bat', '完整的 HTA 系统管理 GUI 工具'],
    ]
    t = Table(_wrap_table_rows(code_index, col_styles={1: _ST_TD_MONO}), colWidths=[22*mm, 42*mm, 80*mm])
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
    story.append(Spacer(1, 15))
    
    story.append(Paragraph(
        '<b>运行环境要求</b>：Windows 7 SP1+（推荐 Windows 10/11），部分高级功能需要 Windows 10 1903+。', ST_BODY))
    story.append(Paragraph(
        '<b>反馈渠道</b>：欢迎在各大 BAT 论坛（批处理之家 bathome.net、GitHub  Issues 等）反馈问题。', ST_BODY))
    story.append(Paragraph(
        '<b>版权声明</b>：本书为原创教程，代码示例可自由使用、修改、分发。禁止将本书内容直接用于商业出版物。', ST_BODY))
    
    story.append(Spacer(1, 40))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#D5D8DC')))
    story.append(Spacer(1, 10))
    story.append(Paragraph('感谢阅读《Windows BAT 批处理完全教程》！', ParagraphStyle(
        'thanks', fontName='DengB', fontSize=16, leading=22, textColor=colors.HexColor('#1A5276'), alignment=TA_CENTER)))
    story.append(Paragraph('2026', ParagraphStyle(
        'year', fontName='DengL', fontSize=12, textColor=colors.HexColor('#7F8C8D'), alignment=TA_CENTER)))
    
    story.append(PageBreak())
    return story


def get_appendices():
    return appendices() + appendix_e()


from reportlab.platypus import HRFlowable
