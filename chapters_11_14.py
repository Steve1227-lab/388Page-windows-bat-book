# -*- coding: utf-8 -*-
"""第四部分：高级技巧与实战篇（第11-14章）"""

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


def ch11():
    """第11章：高级语法与黑科技"""
    story = []
    
    story.append(Paragraph('第11章 高级语法与黑科技', ST_CH_TITLE))
    story.append(Spacer(1, 6))
    
    story.append(Paragraph(
        '本章汇总 BAT 中最有价值的高级特性——包括 ANSI 彩色输出、UAC 提权、代码混淆、混合编程等。'
        '这些内容在绝大多数入门教程中找不到，但在实际项目中极其有用。', ST_BODY))
    
    story.append(Paragraph('11.1 ANSI 彩色输出', ST_SEC_TITLE))
    story.append(Paragraph(
        '从 Windows 10 1903 开始，cmd.exe 原生支持 ANSI 转义序列。这意味着我们可以让 BAT 输出彩色文字！', ST_BODY))
    
    story.append(make_code_block('@echo off\nrem 先启用 ANSI 支持（仅需执行一次）\nreg add "HKCU\\Console" /v VirtualTerminalLevel /t REG_DWORD /d 1 /f > nul\n\nrem ESC 转义符（ASCII 27）\nfor /f %%a in (\'echo prompt $E ^| cmd\') do set "ESC=%%a"\n\necho %ESC%[31m红色文字%ESC%[0m\necho %ESC%[32m绿色文字%ESC%[0m\necho %ESC%[33m黄色文字%ESC%[0m\necho %ESC%[34m蓝色文字%ESC%[0m\necho %ESC%[35m紫色文字%ESC%[0m\necho %ESC%[36m青色文字%ESC%[0m\necho %ESC%[37m白色文字%ESC%[0m\necho %ESC%[1m%ESC%[31m加粗红色%ESC%[0m\necho %ESC%[44m%ESC%[37m蓝底白字%ESC%[0m'))
    
    story.append(Paragraph('常用 ANSI 颜色码：', ST_BODY))
    
    ansi_data = [
        ['前景色', '码', '背景色', '码'],
        ['黑色', '30', '黑色背景', '40'],
        ['红色', '31', '红色背景', '41'],
        ['绿色', '32', '绿色背景', '42'],
        ['黄色', '33', '黄色背景', '43'],
        ['蓝色', '34', '蓝色背景', '44'],
        ['紫色', '35', '紫色背景', '45'],
        ['青色', '36', '青色背景', '46'],
        ['白色', '37', '白色背景', '47'],
        ['默认', '0', '重置样式', '0'],
        ['加粗', '1', '下划线', '4'],
    ]
    t = Table(_wrap_table_rows(ansi_data,
                                col_styles={1: _ST_TD_C, 3: _ST_TD_C},
                                header_col_styles={1: _ST_TH_C, 3: _ST_TH_C}),
              colWidths=[35*mm, 25*mm, 35*mm, 25*mm])
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
        '如果你觉得 ESC 转义符获取方式太 hack，可以用更简洁的 PowerShell 方案获取：'
        '<font name="Consola" size="9" color="#C0392B">for /f %%e in (\'powershell -NoProfile -Command "[char]27"\') do set "ESC=%%e"</font>'
        '。或者直接用 cmd 的 <font name="Consola" size="9" color="#C0392B">%^e%</font>（启用命令扩展后可用）。', 'tip'))
    
    story.append(Paragraph('11.2 代码混淆', ST_SEC_TITLE))
    story.append(Paragraph(
        'BAT 脚本是纯文本，任何人打开就能看。如果你想保护脚本逻辑，可以用混淆技术。以下是三种常用方法：', ST_BODY))
    
    story.append(Paragraph('方法1：变量拼接', ST_SUBSEC_TITLE))
    story.append(make_code_block('@echo off\nrem 把所有字符串拆成变量，再动态拼出来\nset "a=ech"\nset "b=o "\nset "c=Hello "\nset "d=World"\n\nrem 动态执行\ncall %%a%%%%b%%%%c%%%%d%%'))
    
    story.append(Paragraph('方法2：for + cmd /c 执行', ST_SUBSEC_TITLE))
    story.append(make_code_block('@echo off\nfor %%c in ("@echo off & echo obfuscated! & pause") do cmd /c %%~c'))
    
    story.append(Paragraph('方法3：用 certutil + base64 编码', ST_SUBSEC_TITLE))
    story.append(make_code_block('@echo off\nrem 先把脚本 base64 编码存到文件\nrem 然后解码执行\ncertutil -decode encoded.b64 decoded.bat\ncall decoded.bat\ndel decoded.bat'))
    
    story.append(make_note_box(
        '更狠的做法：用 VBScript 或 PowerShell 生成的 BAT 加载器，把真实脚本用 AES 加密，运行时才解密。'
        '第 14 章的实战项目会讲到完整方案。', 'note'))
    
    story.append(Paragraph('11.3 UAC 提权', ST_SEC_TITLE))
    story.append(Paragraph(
        '很多系统操作（写 Program Files、改 HKLM 注册表、管理服务）需要管理员权限。以下是 BAT 自我提权的几种方案：', ST_BODY))
    
    story.append(Paragraph('方案1：runas（最简单）', ST_SUBSEC_TITLE))
    story.append(make_code_block('@echo off\nrem 提示用户选择管理员账户\nrunas /user:Administrator "cmd /c %~f0"\nexit /b'))
    
    story.append(Paragraph('方案2：schtasks（自动提权）', ST_SUBSEC_TITLE))
    story.append(Paragraph(
        '创建一个计划任务（以 SYSTEM 或管理员身份运行），然后立即触发它：', ST_BODY))
    
    story.append(make_code_block('@echo off\nset "SCRIPT=%~f0"\nset "TASKNAME=MyAutoTask"\n\nrem 创建计划任务（以最高权限运行）\nschtasks /create /tn "%TASKNAME%" /tr "\"%SCRIPT%\"" /sc onlogon /rl HIGHEST /f\n\nrem 立即运行\nschtasks /run /tn "%TASKNAME%"\n\nrem 等待一下，然后删除任务\ntimeout /t 3 /nobreak > nul\nschtasks /delete /tn "%TASKNAME%" /f\nexit /b'))
    
    story.append(Paragraph('方案3：MSHTA 弹窗提权', ST_SUBSEC_TITLE))
    story.append(make_code_block('@echo off\nrem 通过 mshta 弹 UAC 对话框让用户确认\nset "UAC_VBS=%temp%\\uac.vbs"\necho Set UAC = CreateObject^("Shell.Application"^) > "%UAC_VBS%"\necho UAC.ShellExecute "cmd.exe", "/c %SCRIPT%", "", "runas", 1 >> "%UAC_VBS%"\ncscript //nologo "%UAC_VBS%"\ndel "%UAC_VBS%"\nexit /b'))
    
    story.append(Paragraph('11.4 自复制与自删除', ST_SEC_TITLE))
    story.append(Paragraph('自复制', ST_SUBSEC_TITLE))
    story.append(make_code_block('@echo off\nrem 把自己复制到启动文件夹\ncopy /y "%~f0" "%appdata%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\%~nx0"'))
    
    story.append(Paragraph('自删除', ST_SUBSEC_TITLE))
    story.append(Paragraph(
        'BAT 运行时被 cmd.exe 占用，不能直接 del。但可以用一个小技巧——在脚本末尾删除自己：', ST_BODY))
    
    story.append(make_code_block('@echo off\nrem ... 你的业务代码 ...\n\nrem 退出前删除自己\ndel /f /q "%~f0" & exit /b'))
    
    story.append(make_note_box(
        '原理：<font name="Consola" size="9" color="#C0392B">&amp;</font> 会先执行 del，再执行 exit。'
        '但有竞争条件——如果 del 失败（文件被锁），脚本就退出了。更可靠的方案：让外部进程（如 cmd /c）来删，或者用 VBScript。', 'tip'))
    
    story.append(make_code_block('rem 更可靠的自删除方案\nstart /b cmd /c "timeout /t 1 &amp; del /f /q \"%~f0\""\nexit /b'))
    
    story.append(Paragraph('11.5 混合编程', ST_SEC_TITLE))
    story.append(Paragraph(
        'BAT 不是万能的，但它是最好的"胶水语言"——可以轻松调用 PowerShell、VBScript、JavaScript 完成 BAT 不擅长的任务。', ST_BODY))
    
    story.append(Paragraph('BAT 调用 PowerShell', ST_SUBSEC_TITLE))
    story.append(make_code_block('@echo off\nrem 用 PowerShell 生成随机密码\nfor /f "usebackq" %%p in (\'powershell -NoProfile -Command "(New-Object System.Security.Cryptography.RNGCryptoServiceProvider | ForEach-Object { $_.GetBytes(8) | ForEach-Object { $_.ToString(\'X2\') } })"\') do set "password=%%p"\necho 随机密码: %password%\n\nrem 用 PowerShell 下载文件\npowershell -NoProfile -Command "Invoke-WebRequest -Uri \'https://example.com/file.zip\' -OutFile \'D:\\Downloads\\file.zip\'"\n\nrem 用 PowerShell 加密文件\npowershell -NoProfile -Command "$key = (1..32 | ForEach-Object { Get-Random -Maximum 256 }); Protect-File -Path \'data.txt\' -OutFile \'data.enc\' -Key $key"'))
    
    story.append(make_note_box(
        '参数传递技巧：把 PowerShell 脚本写在 BAT 内部，用 stdin 传给 PowerShell：'
        '<font name="Consola" size="9" color="#C0392B">powershell -NoProfile -Command "-" &lt;&amp;1 &lt;&lt;EOF ... EOF</font>'
        '（BAT 不支持 heredoc，实际要用 echo 逐行写入临时 .ps1 文件再执行）', 'tip'))
    
    story.append(Paragraph('BAT 调用 VBScript', ST_SUBSEC_TITLE))
    story.append(make_code_block('@echo off\nrem 动态生成 VBScript 文件\nset "VBS=%temp%\\popup.vbs"\necho MsgBox "这是一个VBScript弹窗" ^&amp; vbCrLf ^&amp; "由BAT调用", 64, "提示" > "%VBS%"\ncscript //nologo "%VBS%"\ndel "%VBS%"'))
    
    story.append(Paragraph('BAT 调用 JavaScript（cscript）', ST_SUBSEC_TITLE))
    story.append(make_code_block('@echo off\nset "JS=%temp%\\calc.js"\necho var result = Math.sqrt(256); > "%JS%"\necho WScript.Echo(result); >> "%JS%"\nfor /f "usebackq" %%r in (`cscript //nologo "%JS%"`) do set "sqrt=%%r"\ndel "%JS%"\necho 256 的平方根是: %sqrt%'))
    
    story.append(Paragraph('11.6 HTA 界面', ST_SEC_TITLE))
    story.append(Paragraph(
        'HTA（HTML Application）可以把 HTML + JS + VBScript 打包成一个"程序界面"，'
        '而 BAT 可以生成和调用 HTA——这相当于给 BAT 脚本加上了 GUI！', ST_BODY))
    
    story.append(make_code_block('@echo off\nchcp 65001 > nul\n\nrem ========== 生成 HTA 界面 ==========\nset "HTA_FILE=%temp%\\my_tool.hta"\n\nrem 写入 HTA\n> "%HTA_FILE%" echo ^<!DOCTYPE html^>\n>> "%HTA_FILE%" echo ^<HTA:APPLICATION ID="MyTool" APPLICATIONNAME="MyTool" BORDER="thin" SINGLEINSTANCE="yes" WINDOWSTATE="normal"^>\n>> "%HTA_FILE%" echo ^<html^>\n>> "%HTA_FILE%" echo ^<head^>\n>> "%HTA_FILE%" echo   ^<meta charset="utf-8"^>\n>> "%HTA_FILE%" echo   ^<title^>系统维护工具^</title^>\n>> "%HTA_FILE%" echo   ^<HTA:APPLICATION CAPTION="yes" ICON="" MAXIMIZEBUTTON="yes" MINIMIZEBUTTON="yes" SHOWINTASKBAR="yes" SIZED="yes" SYSMENU="yes" VERSION="1.0" WINDOWSTATE="normal"/^>\n>> "%HTA_FILE%" echo   ^<style^>\n>> "%HTA_FILE%" echo     body { font-family: Deng, sans-serif; padding: 20px; background: #f5f5f5; }\n>> "%HTA_FILE%" echo     button { padding: 10px 20px; margin: 5px; font-size: 14px; cursor: pointer; }\n>> "%HTA_FILE%" echo     #output { background: #000; color: #0f0; font-family: Consola; padding: 10px; height: 200px; overflow-y: auto; }\n>> "%HTA_FILE%" echo   ^</style^>\n>> "%HTA_FILE%" echo ^</head^>\n>> "%HTA_FILE%" echo ^<body^>\n>> "%HTA_FILE%" echo   ^<h2^>系统维护工具^</h2^>\n>> "%HTA_FILE%" echo   ^<button onclick="runCmd(\'systeminfo\')"^>查看系统信息^</button^>\n>> "%HTA_FILE%" echo   ^<button onclick="runCmd(\'ipconfig /all\')"^>查看网络配置^</button^>\n>> "%HTA_FILE%" echo   ^<button onclick="runCmd(\'tasklist\')"^>进程列表^</button^>\n>> "%HTA_FILE%" echo   ^<div id="output"^>^</div^>\n>> "%HTA_FILE%" echo   ^<script language="VBScript"^>\n>> "%HTA_FILE%" echo     Sub runCmd(cmd)\n>> "%HTA_FILE%" echo       Dim shell, exec\n>> "%HTA_FILE%" echo       Set shell = CreateObject("WScript.Shell")\n>> "%HTA_FILE%" echo       Set exec = shell.Exec("cmd /c " ^& cmd)\n>> "%HTA_FILE%" echo       document.getElementById("output").innerText = exec.StdOut.ReadAll()\n>> "%HTA_FILE%" echo     End Sub\n>> "%HTA_FILE%" echo   ^</script^>\n>> "%HTA_FILE%" echo ^</body^>\n>> "%HTA_FILE%" echo ^</html^>\n\nrem 打开 HTA\nstart "" "%HTA_FILE%"'))
    
    story.append(make_note_box(
        'HTA 运行在一个受限的安全沙箱中。它可以通过 WScript.Shell 运行 cmd 命令，'
        '通过 fso（File System Object）操作文件。一个完整的 BAT + HTA 工具示例见第 14.5 节。', 'tip'))
    
    story.append(Paragraph('11.7 编码问题彻底解决', ST_SEC_TITLE))
    story.append(Paragraph(
        '中文乱码是 BAT 开发者最头疼的问题。以下是彻底的解决方案：', ST_BODY))
    
    story.append(Paragraph('方案一：chcp 65001 + UTF-8 BOM', ST_SUBSEC_TITLE))
    story.append(make_code_block('@echo off\nchcp 65001 > nul\n\nrem 保存文件为 UTF-8 with BOM\nrem VS Code: 右下角选择 "UTF-8 with BOM"\nrem Notepad++: 编码 → 转为 UTF-8 BOM\n\necho 这段中文不会乱码'))
    
    story.append(Paragraph('方案二：PowerShell 转码', ST_SUBSEC_TITLE))
    story.append(make_code_block('@echo off\nrem 如果脚本被编码了，用 PowerShell 转成 GBK\npowershell -NoProfile -Command "[System.IO.File]::ReadAllText(\'%~f0\', [System.Text.Encoding]::UTF8)" ^| cmd'))
    
    story.append(Paragraph('方案三：始终转成 GBK 输出', ST_SUBSEC_TITLE))
    story.append(make_code_block('@echo off\nchcp 936 > nul\nrem 文件用 ANSI (GBK) 保存\nrem VS Code 里保存时选 "GBK"'))
    
    story.append(make_note_box(
        '推荐方案：在 Windows 10/11 上用 <b>UTF-8 BOM + chcp 65001</b>；'
        '在需要兼容旧系统（Win7）时用 <b>GBK + chcp 936</b>。'
        '最保险的办法：脚本开头自动判断，然后设置正确编码。', 'tip'))
    
    story.append(Paragraph('11.8 调试与错误处理', ST_SEC_TITLE))
    story.append(Paragraph('调试技巧', ST_SUBSEC_TITLE))
    story.append(make_code_block('rem 技巧1：echo on 开启全回显\n@echo on\nrem ... 会显示每条命令 ...\n\nrem 技巧2：pause 在关键位置暂停\nset /p debug="调试点1: 变量值=%var%，回车继续"\n\nrem 技巧3：写到调试日志\necho [%time%] var=%var% >> debug.log\n\nrem 技巧4：用 cmd /k 运行，窗口不关闭\ncmd /k "call myscript.bat"\n\nrem 技巧5：Process Monitor 监控文件/注册表操作\nrem Sysinternals 工具包下载'))
    
    story.append(Paragraph('错误处理框架', ST_SUBSEC_TITLE))
    story.append(make_code_block('@echo off\nsetlocal enabledelayedexpansion\n\nrem 统一错误处理\ncall :init_error_handling\n\nrem ======== 你的脚本内容 ========\ncall step1 || call :fatal "step1 失败"\ncall step2 || call :fatal "step2 失败"\ncall step3 || call :fatal "step3 失败"\necho 全部成功！\nexit /b 0\n\nrem ======== 错误处理函数 ========\n:init_error_handling\nset "ERROR_LOG=error_log.txt"\necho === 错误日志 %date% %time% === > "%ERROR_LOG%"\ngoto :eof\n\n:fatal\nset "msg=%~1"\necho [FATAL] %msg% | tee -a "%ERROR_LOG%" 2>&1\necho 脚本已终止，按任意键退出...\npause > nul\nexit /b 1\n\n:step1\nrem 具体步骤\ncopy file.txt backup.txt\nif errorlevel 1 exit /b 1\nexit /b 0\n\n:step2\n...'))
    
    story.append(Paragraph('11.9 性能优化', ST_SEC_TITLE))
    story.append(make_code_block('rem 1. 减少 cmd 实例启动（管道会启动新 cmd）\nrem 慢：\nfor /f "tokens=*" %%l in (\'dir /b ^| findstr "\.txt$"\') do ...\nrem 快：\ndir /b *.txt > temp_list.txt\nfor /f "tokens=*" %%l in (temp_list.txt) do ...\ndel temp_list.txt\n\nrem 2. 延迟扩展有开销——只在必要时启用\n\nrem 3. 缓存环境变量到本地变量\nset "PROGRAMFILES=%ProgramFiles%"\nset "WINDIR=%windir%"\n\nrem 4. 避免在大循环里多次调用外部命令\nrem 慢：for %%f in (*.txt) do @echo %%~zf\nrem 快：先 dir /s /b *.txt，再解析\n\nrem 5. robocopy 自带多线程（/MT:n），比 copy 快 5-10 倍\n\nrem 6. 减少变量赋值次数——set /a 是原子操作\n\nrem 7. 不在循环里 echo 输出（控制台 I/O 慢），用 > 文件 收集后一次性写入'))
    
    story.append(Spacer(1, 20))
    story.append(Paragraph('— 第11章 完 —', ParagraphStyle('end', fontName='DengL', fontSize=10, textColor='#7F8C8D', alignment=TA_LEFT)))
    story.append(PageBreak())
    return story


def ch12():
    """第12章：实战项目一 —— 系统维护工具集"""
    story = []
    
    story.append(Paragraph('第12章 实战项目一：系统维护工具集', ST_CH_TITLE))
    story.append(Spacer(1, 6))
    
    story.append(Paragraph(
        '本章把前11章的知识组合成5个实用的系统维护工具。每个脚本都可以直接拿来用，或根据需求修改。', ST_BODY))
    
    story.append(Paragraph('12.1 系统垃圾清理脚本', ST_SEC_TITLE))
    story.append(make_code_block('@echo off\nchcp 65001 > nul\nsetlocal enabledelayedexpansion\n\ntitle 系统垃圾清理工具 v1.0\necho ========================================\necho        系统垃圾清理工具\necho ========================================\necho.\nset /p "confirm=确定要执行清理吗？(Y/N): "\nif /i not "%confirm%"=="Y" (\n    echo 已取消。\n    exit /b 0\n)\n\nrem 创建清理日志\nset "LOG=%temp%\\cleanup_log.txt"\necho === 清理开始 %date% %time% === > "%LOG%"\n\nrem 清理用户临时文件\necho [1/6] 清理用户临时文件...\nset "count=0"\nfor %%f in ("%temp%\\*.*") do (\n    set /a count+=1\n)\ndel /s /q "%temp%\\*.*" 2>nul\nfor /d %%d in ("%temp%\\*") do rmdir /s /q "%%d" 2>nul\necho   临时文件已清理 >> "%LOG%"\n\nrem 清理系统临时文件\necho [2/6] 清理系统临时文件...\ndel /s /q "C:\\Windows\\Temp\\*.*" 2>nul\nfor /d %%d in ("C:\\Windows\\Temp\\*") do rmdir /s /q "%%d" 2>nul\n\nrem 清理回收站\necho [3/6] 清理回收站...\nrd /s /q "C:\\$Recycle.Bin" 2>nul\n\nrem 清理浏览器缓存\necho [4/6] 清理浏览器缓存...\nif exist "%localappdata%\\Microsoft\\Edge\\User Data\\Default\\Cache" (\n    rd /s /q "%localappdata%\\Microsoft\\Edge\\User Data\\Default\\Cache" 2>nul\n)\nif exist "%localappdata%\\Google\\Chrome\\User Data\\Default\\Cache" (\n    rd /s /q "%localappdata%\\Google\\Chrome\\User Data\\Default\\Cache" 2>nul\n)\n\nrem 清理 Windows Update 缓存\necho [5/6] 清理 Windows Update 缓存...\nnet stop wuauserv >nul 2>&1\nrd /s /q "C:\\Windows\\SoftwareDistribution\\Download" 2>nul\nnet start wuauserv >nul 2>&1\n\nrem 清理缩略图缓存\necho [6/6] 清理缩略图缓存...\ndel /s /q "%localappdata%\\Microsoft\\Windows\\Explorer\\thumbcache_*.db" 2>nul\n\necho.\necho 清理完成！\necho 日志已保存到: %LOG%\npause'))
    
    story.append(Paragraph('12.2 启动项管理工具', ST_SEC_TITLE))
    story.append(make_code_block('@echo off\nchcp 65001 > nul\nsetlocal\ntitle 启动项管理工具\n\n:menu\ncls\necho ========================================\necho        启动项管理工具\necho ========================================\necho [1] 查看所有启动项\necho [2] 禁用某个启动项\necho [3] 启用某个启动项\necho [4] 添加开机自启（当前用户）\necho [5] 备份当前启动项\necho [0] 退出\necho ========================================\nset /p "choice=请选择: "\n\nif "%choice%"=="1" goto :view\nif "%choice%"=="2" goto :disable\nif "%choice%"=="3" goto :enable\nif "%choice%"=="4" goto :add\nif "%choice%"=="5" goto :backup\nif "%choice%"=="0" goto :eof\ngoto :menu\n\n:view\ncls\necho --- 用户启动项 (HKCU) ---\nreg query "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run" 2>nul\necho.\necho --- 系统启动项 (HKLM) ---\nreg query "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run" 2>nul\necho.\necho --- 启动文件夹 ---\ndir /b "%appdata%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup" 2>nul\necho.\npause\ngoto :menu\n\n:disable\nset /p "name=要禁用的启动项名称: "\nreg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run" /v "Disabled_%name%" /t REG_SZ /d "disabled" /f\necho 已标记为禁用（实际可把 Run 中的值删除，存到 DisabledRun 子键）\npause\ngoto :menu\n\n:add\nset /p "exe_path=要运行的程序完整路径: "\nset /p "run_name=注册表中的名称: "\nreg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run" /v "%run_name%" /t REG_SZ /d "\"%exe_path%\"" /f\necho 已添加。\npause\ngoto :menu\n\n:backup\nreg export "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run" "%cd%\\run_hkcu_backup.reg" /y\nreg export "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run" "%cd%\\run_hklm_backup.reg" /y\necho 启动项已备份到当前目录。\npause\ngoto :menu\nendlocal'))
    
    story.append(Paragraph('12.3 服务批量运维脚本', ST_SEC_TITLE))
    story.append(make_code_block('@echo off\nchcp 65001 > nul\nsetlocal enabledelayedexpansion\n\ntitle 服务批量运维工具\n\nrem ========== 配置区 ==========\nrem 要管理的服务列表（每行一个服务名）\nset "SERVICE_LIST=W32Time Spooler wuauserv BITS"\nrem ===========================\n\n:menu\ncls\necho ========================================\necho        服务批量运维\necho ========================================\necho [1] 批量启动服务\necho [2] 批量停止服务\necho [3] 批量重启服务\necho [4] 查看服务状态\necho [5] 批量设置启动类型\necho [0] 退出\necho ========================================\nset /p "choice=请选择: "\n\nif "%choice%"=="1" goto :do_start\nif "%choice%"=="2" goto :do_stop\nif "%choice%"=="3" goto :do_restart\nif "%choice%"=="4" goto :do_status\nif "%choice%"=="5" goto :do_settype\nif "%choice%"=="0" goto :eof\ngoto :menu\n\n:do_start\nfor %%s in (%SERVICE_LIST%) do (\n    echo 正在启动 %%s ...\n    net start %%s >nul 2>&1 && echo   ✓ 成功 || echo   ✗ 失败\n)\npause\ngoto :menu\n\n:do_stop\nfor %%s in (%SERVICE_LIST%) do (\n    echo 正在停止 %%s ...\n    net stop %%s >nul 2>&1 && echo   ✓ 成功 || echo   ✗ 失败\n)\npause\ngoto :menu\n\n:do_restart\nfor %%s in (%SERVICE_LIST%) do (\n    echo 正在重启 %%s ...\n    net stop %%s >nul 2>&1\n    timeout /t 2 /nobreak > nul\n    net start %%s >nul 2>&1 && echo   ✓ 成功 || echo   ✗ 失败\n)\npause\ngoto :menu\n\n:do_status\ncls\necho 服务状态一览：\necho ----------------------------------------\nfor %%s in (%SERVICE_LIST%) do (\n    for /f "tokens=3" %%t in (\'sc query %%s ^| findstr "STATE"\') do (\n        echo %%s: %%t\n    )\n)\necho ----------------------------------------\npause\ngoto :menu\n\n:do_settype\ncls\necho 启动类型：1=自动  2=自动(延迟)  3=手动  4=禁用\nset /p "type=选择启动类型: "\nfor %%s in (%SERVICE_LIST%) do (\n    echo 设置 %%s ...\n    sc config %%s start= %type%\n)\npause\ngoto :menu\nendlocal'))
    
    story.append(Paragraph('12.4 计划任务备份恢复', ST_SEC_TITLE))
    story.append(make_code_block('@echo off\nchcp 65001 > nul\nsetlocal\n\nset "BACKUP_DIR=schtasks_backup"\nif not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"\n\necho [1] 备份所有计划任务\necho [2] 从备份恢复计划任务\nset /p "choice=选择操作: "\n\nif "%choice%"=="1" goto :backup\nif "%choice%"=="2" goto :restore\ngoto :eof\n\n:backup\ncls\necho 正在导出所有计划任务...\nschtasks /query /xml /v 2>nul > "%BACKUP_DIR%\\all_tasks.xml"\n\nrem 逐个导出详细信息\necho.\necho 逐个导出任务详情...\nfor /f "tokens=1" %%t in (\'schtasks /query /fo csv ^| findstr /v "^任务名" ^| findstr /v "^TaskName"\') do (\n    set "taskname=%%t"\n    set "taskname=!taskname:"=!"\n    schtasks /query /tn "!taskname!" /xml > "%BACKUP_DIR%\\!taskname!.xml" 2>nul\n)\n\necho 备份完成，文件在 %BACKUP_DIR% 目录下。\npause\ngoto :eof\n\n:restore\ncls\necho 将从 %BACKUP_DIR% 目录恢复所有任务。\nset /p "confirm=确认？(Y/N): "\nif /i not "%confirm%"=="Y" goto :eof\n\nfor %%f in ("%BACKUP_DIR%\\*.xml") do (\n    echo 导入 %%~nf ...\n    schtasks /create /tn "%%~nf" /xml "%%f" /f >nul 2>&1 && echo   ✓ 成功 || echo   ✗ 失败\n)\npause\ngoto :eof\nendlocal'))
    
    story.append(Paragraph('12.5 系统快照脚本', ST_SEC_TITLE))
    story.append(make_code_block('@echo off\nchcp 65001 > nul\nsetlocal enabledelayedexpansion\n\nrem ========== 系统快照（一键收集系统信息） ==========\nset "OUT_DIR=sysinfo_%computername%_%date:~0,4%%date:~5,2%%date:~8,2%"\nset "OUT_DIR=%OUT_DIR: =0%"\nmkdir "%OUT_DIR%" 2>nul\n\necho ========================================\necho    系统信息快照\necho    输出目录: %OUT_DIR%\necho ========================================\necho.\n\nrem 1. 基本系统信息\necho [1/8] 系统信息...\nsysteminfo > "%OUT_DIR%\\01_systeminfo.txt" 2>&1\n\nrem 2. 硬件信息\necho [2/8] 硬件信息...\nwmic cpu get /format:list > "%OUT_DIR%\\02_cpu.txt"\nwmic memorychip get /format:list > "%OUT_DIR%\\03_memory.txt"\nwmic diskdrive get /format:list > "%OUT_DIR%\\04_disk.txt"\nwmic baseboard get /format:list > "%OUT_DIR%\\05_motherboard.txt"\n\nrem 3. 网络配置\necho [3/8] 网络配置...\nipconfig /all > "%OUT_DIR%\\06_network.txt" 2>&1\nnetstat -ano > "%OUT_DIR%\\07_connections.txt" 2>&1\n\nrem 4. 已安装软件\necho [4/8] 已安装软件...\nwmic product get Name,Version,InstallDate /format:csv > "%OUT_DIR%\\08_software.csv" 2>&1\n\nrem 5. 驱动信息\necho [5/8] 驱动信息...\sdriver /s > "%OUT_DIR%\\09_drivers.txt" 2>&1 || wmic driverquery get /format:list > "%OUT_DIR%\\09_drivers.txt"\n\nrem 6. 运行进程\necho [6/8] 运行进程...\ntasklist /v /fo csv > "%OUT_DIR%\\10_processes.csv" 2>&1\n\nrem 7. 服务状态\necho [7/8] 服务状态...\nsc query type= service state= all > "%OUT_DIR%\\11_services.txt" 2>&1\n\nrem 8. 系统事件（最近100条）\necho [8/8] 系统事件...\nwmic nteventlog where "LogFile=\'System\'" get /format:list > "%OUT_DIR%\\12_events.txt" 2>&1\n\necho.\necho 系统快照收集完成！\necho 文件保存在: %cd%\\%OUT_DIR%\nstart "" "%cd%\\%OUT_DIR%"\npause\nendlocal'))
    
    story.append(Spacer(1, 20))
    story.append(Paragraph('— 第12章 完 —', ParagraphStyle('end', fontName='DengL', fontSize=10, textColor='#7F8C8D', alignment=TA_LEFT)))
    story.append(PageBreak())
    return story


def ch13():
    """第13章：实战项目二 —— 网络运维工具集"""
    story = []
    
    story.append(Paragraph('第13章 实战项目二：网络运维工具集', ST_CH_TITLE))
    story.append(Spacer(1, 6))
    
    story.append(Paragraph('13.1 批量 Ping 诊断 + CSV 导出', ST_SEC_TITLE))
    story.append(make_code_block('@echo off\nchcp 65001 > nul\nsetlocal enabledelayedexpansion\nrem ========== 批量 Ping 检测 ==========\n\nrem 创建 targets.txt，每行一个 IP 或域名\nif not exist targets.txt (\n    echo 请先创建 targets.txt 文件，每行一个 IP 或域名。\n    echo 示例：\n    echo 192.168.1.1\n    echo 192.168.1.100\n    echo www.bing.com\n    pause\n    exit /b 1\n)\n\nset "RESULT=ping_report_%date:~0,4%%date:~5,2%%date:~8,2%.csv"\necho IP,响应时间(ms),状态,丢包率,平均时间 > "%RESULT%"\n\nset /a total=0, ok=0, fail=0\n\nfor /f "usebackq tokens=*" %%ip in ("targets.txt") do (\n    if not "%%ip"=="" (\n        set /a total+=1\n        <nul set /p "=检测 %%ip ... "\n        \n        rem ping 4次，提取关键数据\n        set "lost=0"\n        set "avgtime=-"\n        set "ok_flag=FAIL"\n        \n        for /f "tokens=5" %%t in (\'ping -n 4 -w 500 %%ip ^| findstr "平均"\') do (\n            set "avgtime=%%t"\n            set "avgtime=!avgtime: =!"\n            set "ok_flag=OK"\n        )\n        for /f "tokens=2 delims=(" %%l in (\'ping -n 4 -w 500 %%ip ^| findstr "丢包" ^| findstr /v "0%"\') do (\n            set "lost=%%l"\n            set "lost=!lost:%%=!"\n        )\n        \n        if "!ok_flag!"=="OK" set /a ok+=1\n        if "!ok_flag!"=="FAIL" set /a fail+=1\n        \n        echo %%ip,!avgtime!,!ok_flag!,!lost!,!avgtime! >> "%RESULT%"\n        echo !ok_flag! - !avgtime!ms\n    )\n)\n\necho.\necho ========================================\necho 检测完成：共 !total! 个，成功 !ok! 个，失败 !fail! 个\necho 详细结果: %RESULT%\necho ========================================\npause\nendlocal'))
    
    story.append(Paragraph('13.2 批量远程执行（PsExec + BAT）', ST_SEC_TITLE))
    story.append(Paragraph(
        'BAT 不能直接远程执行，但可以结合 Sysinternals 的 PsExec（微软官方工具）实现：', ST_BODY))
    
    story.append(make_code_block('@echo off\nchcp 65001 > nul\nsetlocal enabledelayedexpansion\n\nrem ========== 批量远程执行 ==========\nrem 前提：PsExec.exe 在 PATH 中，所有远程机器开放 445 端口（SMB）\nrem      目标机器的 ADMIN$ 共享可访问\n\nrem 创建 machines.txt，每行一个机器名或 IP\nif not exist machines.txt (\n    echo 请创建 machines.txt，每行一个主机名或 IP。\n    pause\n    exit /b 1\n)\n\nset "REMOTE_CMD=ipconfig /all"\nset "OUT_DIR=remote_results"\nmkdir "%OUT_DIR%" 2>nul\n\nset /p "user=管理员用户名: "\nset /p "pass=管理员密码: "\n\nfor /f "usebackq tokens=*" %%m in ("machines.txt") do (\n    if not "%%m"=="" (\n        echo 正在连接 %%m ...\n        psexec \\%%m -u %user% -p %pass% -accepteula cmd /c "%REMOTE_CMD%" > "%OUT_DIR%\\%%m.txt" 2>&1\n        if errorlevel 1 (\n            echo   ✗ 连接失败\n        ) else (\n            echo   ✓ 成功\n        )\n    )\n)\n\necho.\necho 所有结果已保存到 %OUT_DIR%\npause\nendlocal'))
    
    story.append(Paragraph('13.3 批量文件分发', ST_SEC_TITLE))
    story.append(make_code_block('@echo off\nchcp 65001 > nul\nsetlocal enabledelayedexpansion\n\nrem ========== 批量分发文件到多台机器 ==========\nset "SOURCE_DIR=D:\\Deployment\\Files"\nset "MACHINES=servers.txt"   & rem 每行一个主机名\nset "DEST_PATH=C:\\Deploy"   & rem 远程路径\n\nif not exist "%MACHINES%" (\n    echo 请创建 %MACHINES% 文件。\n    pause\n    exit /b 1\n)\n\nfor /f "usebackq tokens=*" %%m in ("%MACHINES%") do (\n    if not "%%m"=="" (\n        echo 正在同步到 %%m ...\n        rem 先建立临时网络盘映射\n        net use Z: \\\\%%m\\ADMIN$ >nul 2>&1\n        \n        rem 用 robocopy 同步\n        robocopy "%SOURCE_DIR%" "\\\\%%m\\ADMIN$\\Deploy" /MIR /Z /R:2 /W:1 > "%temp%\\robocopy_%%m.log" 2>&1\n        \n        if !errorlevel! lss 8 (\n            echo   ✓ 同步成功\n        ) else (\n            echo   ✗ 同步失败，详见 %temp%\\robocopy_%%m.log\n        )\n        \n        net use Z: /delete >nul 2>&1\n    )\n)\n\nrem 推送完成后触发远程安装\nfor /f "usebackq tokens=*" %%m in ("%MACHINES%") do (\n    echo 通知 %%m 执行安装...\n    schtasks /run /s %%m /tn "DeployInstall" 2>nul\n)\n\npause\nendlocal'))
    
    story.append(Paragraph('13.4 网络监控脚本', ST_SEC_TITLE))
    story.append(make_code_block('@echo off\nchcp 65001 > nul\nsetlocal enabledelayedexpansion\n\nrem ========== 网络端口监控 ==========\nrem 定时检查是否有异常端口被监听，记录并报警\n\nset "LOG=monitor_%date:~0,4%%date:~5,2%%date:~8,2%.log"\nset "INTERVAL=60"   & rem 每 60 秒检查一次\n\nrem 定义"危险端口"（已知木马/后门常用端口）\nset "DANGER_PORTS=1234 31337 12345 27374 8888 9999 6666 7777"\n\necho [%time%] 监控启动，间隔 %INTERVAL% 秒 >> "%LOG%"\n\n:monitor_loop\nset "snapshot=%temp%\\netstat_snapshot.txt"\nnetstat -ano -p tcp > "%snapshot%" 2>&1\n\nfor %%p in (%DANGER_PORTS%) do (\n    findstr "%%p" "%snapshot%" >nul 2>&1\n    if !errorlevel! equ 0 (\n        echo [!time%] ⚠ 检测到危险端口 %%p 被监听！ >> "%LOG%"\n        findstr "%%p" "%snapshot%" >> "%LOG%"\n        \n        rem 查找对应 PID 和进程名\n        for /f "tokens=5" %%pid in (\'findstr "%%p" "%snapshot%"\') do (\n            for /f "usebackq tokens=1" %%name in (\'tasklist /fi "PID eq %%pid" /nh\') do (\n                echo [!time%]   进程: %%name ^(PID: %%pid^) >> "%LOG%"\n            )\n            rem 可选：自动结束可疑进程\n            rem taskkill /f /pid %%pid\n        )\n    )\n)\n\necho [!time%] 检查完成 >> "%LOG%"\ntimeout /t %INTERVAL% /nobreak > nul\ngoto :monitor_loop'))
    
    story.append(Paragraph('13.5 WiFi 密码批量导出', ST_SEC_TITLE))
    story.append(make_code_block('@echo off\nchcp 65001 > nul\nsetlocal enabledelayedexpansion\n\nrem ========== 导出所有 WiFi 密码 ==========\nset "OUT=wifi_passwords.txt"\necho ===== WiFi 密码导出 ===== > "%OUT%"\necho 导出时间: %date% %time% >> "%OUT%"\necho. >> "%OUT%"\n\nrem 获取所有已保存的 WiFi 名称\nfor /f "tokens=2 delims=:" %%n in (\'netsh wlan show profiles ^| findstr "所有用户配置文件" ^| findstr /v "---"\') do (\n    set "profile=%%n"\n    set "profile=!profile: =!"\n    \n    echo ======================================== >> "%OUT%"\n    echo 网络名: !profile! >> "%OUT%"\n    echo ======================================== >> "%OUT%"\n    \n    rem 导出详细信息（包括 key=clear 显示明文密码）\n    netsh wlan show profile name="!profile!" key=clear >> "%OUT%" 2>&1\n    echo. >> "%OUT%"\n)\n\necho 导出完成！\necho 结果已保存到: %cd%\\%OUT%\nstart "" "%cd%\\%OUT%"\npause\nendlocal'))
    
    story.append(Spacer(1, 20))
    story.append(Paragraph('— 第13章 完 —', ParagraphStyle('end', fontName='DengL', fontSize=10, textColor='#7F8C8D', alignment=TA_LEFT)))
    story.append(PageBreak())
    return story


def ch14():
    """第14章：实战项目三 —— 进阶黑科技工具集"""
    story = []
    
    story.append(Paragraph('第14章 实战项目三：进阶黑科技工具集', ST_CH_TITLE))
    story.append(Spacer(1, 6))
    
    story.append(Paragraph('14.1 文件加密解密', ST_SEC_TITLE))
    story.append(Paragraph(
        'BAT 没有原生加密能力，但可以结合 PowerShell 的 AES 加密实现完整的加密方案：', ST_BODY))
    
    story.append(make_code_block('@echo off\nchcp 65001 > nul\nsetlocal\n\nrem ========== 用 PowerShell AES 加密文件 ==========\nset "KEY=MySecretKey2026!!!"\nset /p "FILE=要加密的文件: "\nset "ENC_FILE=%FILE%.enc"\n\npowershell -NoProfile -Command ^\n  "$key = [System.Text.Encoding]::UTF8.GetBytes(\'%KEY%\'.PadRight(32).Substring(0,32));" ^\n  "$aes = New-Object System.Security.Cryptography.AesManaged;" ^\n  "$aes.Key = $key;" ^\n  "$aes.GenerateIV();" ^\n  "$aes.Mode = [System.Security.Cryptography.CipherMode]::CBC;" ^\n  "$in = [System.IO.File]::ReadAllBytes(\'%FILE%\');" ^\n  "$enc = $aes.CreateEncryptor().TransformFinalBlock($in, 0, $in.Length);" ^\n  "$out = New-Object byte[] ($aes.IV.Length + $enc.Length);" ^\n  "[Array]::Copy($aes.IV, 0, $out, 0, $aes.IV.Length);" ^\n  "[Array]::Copy($enc, 0, $out, $aes.IV.Length, $enc.Length);" ^\n  "[System.IO.File]::WriteAllBytes(\'%ENC_FILE%\', $out);" ^\n  "Write-Host \'加密完成: %ENC_FILE%\', -ForegroundColor Green"\n\npause\nendlocal'))
    
    story.append(Paragraph('14.2 BAT 转 EXE', ST_SEC_TITLE))
    story.append(Paragraph(
        'BAT 转 EXE 的几种方案：', ST_BODY))
    
    story.append(Paragraph('方案1：WinRAR SFX（自解压）', ST_SUBSEC_TITLE))
    story.append(make_code_block('rem 步骤：\nrem 1. 安装 WinRAR\nrem 2. 把 bat 放到一个文件夹里\nrem 3. 右键 → 添加到压缩文件\nrem 4. "创建自解压格式压缩文件"\nrem 5. 高级 → SFX 选项 → 解压后运行：你的脚本名\nrem 6. 模式：解压到临时文件夹\nrem 7. 更新 → 覆盖所有文件'))
    
    story.append(Paragraph('方案2：IExpress（Windows 自带！）', ST_SUBSEC_TITLE))
    story.append(make_code_block('rem IExpress 是 Windows 自带的封装工具，不需要额外下载\nrem 运行 iexpress.exe（位于 C:\\Windows\\System32）\n\nrem 命令行方式：\niexpress /N /Q /M my_bat.inf\n\nrem 创建 INF 配置文件 my_bat.inf：\nrem [Version]\nrem Class=IEXPRESS\nrem SEDVersion=2.0\nrem \nrem [Options]\nrem PackagePurpose=InstallApp\nrem ShowInstallProgramWindow=0\nrem HideExtractAnimation=1\nrem UseLongFileName=1\nrem FriendlyName="My Tool"\nrem AppLaunched=cmd.exe /c myscript.bat\nrem PostInstallCmd=<None>\nrem SourceFiles=SourceFiles\nrem \nrem [SourceFiles]\nrem SourceFiles0=.\nrem \nrem [SourceFiles0]\nrem %FILES%=myscript.bat'))
    
    story.append(Paragraph('方案3：Bat To Exe Converter', ST_SUBSEC_TITLE))
    story.append(Paragraph(
        '第三方工具（https://bat2exe.net/），支持：', ST_BODY))
    story.append(Paragraph('• 把 BAT 嵌入到一个小的 .exe 中', ST_BODY_NOINDENT))
    story.append(Paragraph('• 支持图标替换、版本信息、压缩', ST_BODY_NOINDENT))
    story.append(Paragraph('• 支持密码保护、不可编辑模式', ST_BODY_NOINDENT))
    story.append(Paragraph('• 支持 32/64 位目标', ST_BODY_NOINDENT))
    
    story.append(Paragraph('方案4：自己写一个转换脚本', ST_SUBSEC_TITLE))
    story.append(make_code_block('@echo off\nrem ========== BAT 转 EXE（自写方案） ==========\nrem 原理：生成一个小的 C# 程序，内嵌 BAT，运行时解码并执行\n\nset "BAT_FILE=%~f1"\nset "OUTPUT=%~n1.exe"\n\nif not exist "%BAT_FILE%" (\n    echo 请指定 BAT 文件路径\n    exit /b 1\n)\n\nrem 用 PowerShell 把 BAT 转成 Base64\nfor /f "usebackq" %%b in (\'powershell -NoProfile -Command "[Convert]::ToBase64String([IO.File]::ReadAllBytes(\'%BAT_FILE%\'))"\') do set "B64=%%b"\n\nrem 生成临时 C# 源码\nset "CS_FILE=%temp%\\bat2exe.cs"\n> "%CS_FILE%" echo using System;\n>> "%CS_FILE%" echo using System.Diagnostics;\n>> "%CS_FILE%" echo using System.IO;\n>> "%CS_FILE%" echo using System.Text;\n>> "%CS_FILE%" echo \n>> "%CS_FILE%" echo class BatRunner {\n>> "%CS_FILE%" echo   static void Main() {\n>> "%CS_FILE%" echo     string b64 = @"!B64!";\n>> "%CS_FILE%" echo     byte[] bytes = Convert.FromBase64String(b64);\n>> "%CS_FILE%" echo     string tmp = Path.Combine(Path.GetTempPath(), "run_" + Guid.NewGuid() + ".bat");\n>> "%CS_FILE%" echo     File.WriteAllBytes(tmp, bytes);\n>> "%CS_FILE%" echo     Process.Start("cmd.exe", "/c " + tmp).WaitForExit();\n>> "%CS_FILE%" echo     File.Delete(tmp);\n>> "%CS_FILE%" echo   }\n>> "%CS_FILE%" echo }\n\nrem 用 csc 编译（.NET Framework 自带）\nfor /f "usebackq" %%c in (\'dir /b /s "%windir%\\Microsoft.NET\\Framework64\\csc.exe" 2^>nul ^| findstr /v "."\') do set "CSC=%%c"\nif not defined CSC (\n    for /f "usebackq" %%c in (\'dir /b /s "%windir%\\Microsoft.NET\\Framework\\v4.0.30319\\csc.exe" 2^>nul\') do set "CSC=%%c"\n)\n\n"%CSC%" /nologo /target:winexe /out:"%OUTPUT%" "%CS_FILE%"\ndel "%CS_FILE%"\necho 已生成: %OUTPUT%'))
    
    story.append(Paragraph('14.3 键盘鼠标模拟', ST_SEC_TITLE))
    story.append(Paragraph(
        'BAT 不能直接模拟键盘鼠标，但通过内嵌 VBScript 或 PowerShell SendKeys 可以实现：', ST_BODY))
    
    story.append(make_code_block('@echo off\nchcp 65001 > nul\nsetlocal\n\nrem ========== 键盘自动输入 ==========\nset "VBS=%temp%\\autotype.vbs"\n\nrem 生成 VBScript\n> "%VBS%" echo Set WshShell = CreateObject("WScript.Shell")\n>> "%VBS%" echo WScript.Sleep 3000     \' 等待 3 秒让用户切换到目标窗口\n>> "%VBS%" echo WshShell.AppActivate "记事本"   \' 激活目标窗口\n>> "%VBS%" echo WScript.Sleep 500\n>> "%VBS%" echo \n>> "%VBS%" echo \' 逐字输入（每个字符之间加延迟）\n>> "%VBS%" echo text = "Hello from BAT + VBScript!"\n>> "%VBS%" echo For i = 1 To Len(text)\n>> "%VBS%" echo   WshShell.SendKeys Mid(text, i, 1)\n>> "%VBS%" echo   WScript.Sleep 100\n>> "%VBS%" echo Next\n>> "%VBS%" echo \n>> "%VBS%" echo \' 发送快捷键 Ctrl+S\n>> "%VBS%" echo WshShell.SendKeys "^s"\n>> "%VBS%" echo WScript.Sleep 500\n>> "%VBS%" echo WshShell.SendKeys "~"   \' Enter\n\nrem 提示用户准备好\necho 3 秒后开始自动输入，请切换到目标窗口...\ntimeout /t 3 /nobreak > nul\n\ncscript //nologo "%VBS%"\ndel "%VBS%"\nendlocal'))
    
    story.append(Paragraph('SendKeys 特殊键对照表：', ST_BODY))
    sk_data = [
        ['按键', '代码', '按键', '代码'],
        ['Enter', '~', 'Backspace', '{BACKSPACE}'],
        ['Tab', '{TAB}', '方向键上', '{UP}'],
        ['Esc', '{ESC}', '方向键下', '{DOWN}'],
        ['F1', '{F1}', '方向键左', '{LEFT}'],
        ['Ctrl+A', '^a', '方向键右', '{RIGHT}'],
        ['Alt+F4', '%{F4}', 'Ctrl+Shift+T', '^+t'],
        ['Win键', '^{ESC}', '延迟', 'WScript.Sleep ms'],
    ]
    t = Table(_wrap_table_rows(sk_data), colWidths=[35*mm, 35*mm, 35*mm, 35*mm])
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
    
    story.append(Paragraph('14.4 合法远程下载执行流', ST_SEC_TITLE))
    story.append(Paragraph(
        '在企业环境中，从远程下载并执行代码需要考虑安全合规。以下是一个相对安全的"下载→校验→执行"流程：', ST_BODY))
    
    story.append(make_code_block('@echo off\nchcp 65001 > nul\nsetlocal enabledelayedexpansion\n\nrem ========== 安全下载并执行 ==========\nset "URL=https://trusted.example.com/tool.exe"\nset "EXPECTED_HASH=A1B2C3D4E5F6...EXPECTED_SHA256_HEX"\nset "DOWNLOAD_DIR=%temp%\\update_cache"\nmkdir "%DOWNLOAD_DIR%" 2>nul\nset "TARGET=%DOWNLOAD_DIR%\\tool.exe"\n\necho [1/4] 正在下载...\nbitsadmin /transfer UpdateJob "%URL%" "%TARGET%" >nul 2>&1\nif errorlevel 1 (\n    echo ✗ 下载失败！\n    exit /b 1\n)\n\necho [2/4] 校验文件完整性...\nset "ACTUAL_HASH="\nfor /f "usebackq delims=" %%h in (`powershell -NoProfile -Command "(Get-FileHash \'%TARGET%\' -Algorithm SHA256).Hash"`) do set "ACTUAL_HASH=%%h"\n\nif /i not "!ACTUAL_HASH!"=="%EXPECTED_HASH%" (\n    echo ✗ 哈希值不匹配！已删除下载的文件。\n    del "%TARGET%"\n    exit /b 1\n)\necho   ✓ 哈希校验通过\n\necho [3/4] 数字签名检查...\nsigcheck -nobanner "%TARGET%" >nul 2>&1 || (\n    echo ⚠ 文件没有有效数字签名，请谨慎执行\n    set /p "confirm=仍然执行？(Y/N): "\n    if /i not "!confirm!"=="Y" exit /b 1\n)\n\necho [4/4] 执行程序...\nstart /wait "" "%TARGET%"\n\nrem 清理缓存\nrmdir /s /q "%DOWNLOAD_DIR%"\necho ✓ 完成\nendlocal'))
    
    story.append(Paragraph('14.5 HTA 简易 GUI 管理工具', ST_SEC_TITLE))
    story.append(Paragraph(
        '把第 11.6 节的 HTA 概念付诸实践——做一个带界面的系统工具：', ST_BODY))
    
    hta_code = "@echo off\nchcp 65001 > nul\nsetlocal\n\nrem ========== 生成一个完整的 HTA GUI 工具 ==========\nset \"HTA=%temp%\\SysAdminTool.hta\"\n\n> \"%HTA%\" echo ^<!DOCTYPE html^>\n>> \"%HTA%\" echo ^<HTA:APPLICATION ID=\"SysAdminTool\" APPLICATIONNAME=\"SysAdminTool\"^>\n>> \"%HTA%\" echo ^<head^>\n>> \"%HTA%\" echo   ^<meta charset=\"utf-8\"^>\n>> \"%HTA%\" echo   ^<title^>系统管理工具箱^</title^>\n>> \"%HTA%\" echo   ^<script language=\"VBScript\"^>\n>> \"%HTA%\" echo     Sub RunCmd(cmd)\n>> \"%HTA%\" echo       Set shell = CreateObject(\"WScript.Shell\")\n>> \"%HTA%\" echo       Set exec = shell.Exec(\"cmd /c \" ^& cmd)\n>> \"%HTA%\" echo       document.getElementById(\"out\").innerText = _\n>> \"%HTA%\" echo         exec.StdOut.ReadAll() ^& exec.StdErr.ReadAll()\n>> \"%HTA%\" echo     End Sub\n>> \"%HTA%\" echo   ^</script^>\n>> \"%HTA%\" echo ^</head^>\n>> \"%HTA%\" echo ^<body^>\n>> \"%HTA%\" echo   ^<h2^>系统管理工具箱^</h2^>\n>> \"%HTA%\" echo   ^<button onclick=\"RunCmd('systeminfo')\"^>系统信息^</button^>\n>> \"%HTA%\" echo   ^<button onclick=\"RunCmd('tasklist')\"^>进程列表^</button^>\n>> \"%HTA%\" echo   ^<div id=\"out\" style=\"background:#eee;padding:10px;height:300px;overflow:auto\"^>选择工具执行...^</div^>\n>> \"%HTA%\" echo ^</body^>\n>> \"%HTA%\" echo ^</html^>\n\nstart \"\" \"%HTA%\"\necho HTA 界面已启动！\nendlocal"
    story.append(make_code_block(hta_code))
    
    story.append(Spacer(1, 20))
    story.append(Paragraph('— 第14章 完 —', ParagraphStyle('end', fontName='DengL', fontSize=10, textColor='#7F8C8D', alignment=TA_LEFT)))
    story.append(PageBreak())
    return story


def get_chapters():
    return [ch11(), ch12(), ch13(), ch14()]
