# -*- coding: utf-8 -*-
"""
《Windows BAT 批处理完全教程》PDF生成器
使用 reportlab 生成精美中文PDF
"""

import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    KeepTogether, ListFlowable, ListItem, HRFlowable, Preformatted
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.frames import Frame
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from reportlab.lib import colors

# ============================================================
# 1. 字体注册
# ============================================================
FONT_DIR = r"C:\Windows\Fonts"
pdfmetrics.registerFont(TTFont('Deng',     os.path.join(FONT_DIR, 'Deng.ttf')))
pdfmetrics.registerFont(TTFont('DengB',    os.path.join(FONT_DIR, 'Dengb.ttf')))
pdfmetrics.registerFont(TTFont('DengL',    os.path.join(FONT_DIR, 'Dengl.ttf')))
pdfmetrics.registerFont(TTFont('Consola',  os.path.join(FONT_DIR, 'consola.ttf')))
pdfmetrics.registerFont(TTFont('ConsolaB', os.path.join(FONT_DIR, 'consolab.ttf')))

# 注册字体族
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily('Deng', normal='Deng', bold='DengB', italic='DengL', boldItalic='DengL')
registerFontFamily('Consola', normal='Consola', bold='ConsolaB', italic='Consola', boldItalic='ConsolaB')

# ============================================================
# 2. 颜色定义
# ============================================================
C_PRIMARY   = HexColor('#1A5276')   # 深蓝 - 主标题
C_SECONDARY = HexColor('#2E86C1')   # 亮蓝 - 二级标题
C_ACCENT    = HexColor('#27AE60')   # 绿色 - 强调
C_WARN      = HexColor('#E67E22')   # 橙色 - 警告
C_DANGER    = HexColor('#C0392B')   # 红色 - 危险
C_BG_CODE   = HexColor('#F5F5F5')   # 代码背景
C_BG_NOTE   = HexColor('#EBF5FB')   # 笔记背景
C_BG_WARN   = HexColor('#FEF9E7')   # 警告背景
C_BG_DANGER = HexColor('#FDEDEC')   # 危险背景
C_LINE      = HexColor('#D5D8DC')   # 分隔线
C_TEXT      = HexColor('#2C3E50')   # 正文色
C_GRAY      = HexColor('#7F8C8D')   # 灰色辅助

# ============================================================
# 3. 样式定义
# ============================================================
styles = getSampleStyleSheet()

# 封面大标题
ST_COVER_TITLE = ParagraphStyle(
    'CoverTitle', fontName='DengB', fontSize=48, leading=60,
    textColor=C_PRIMARY, alignment=TA_CENTER, spaceAfter=20
)
ST_COVER_SUB = ParagraphStyle(
    'CoverSub', fontName='Deng', fontSize=20, leading=28,
    textColor=C_SECONDARY, alignment=TA_CENTER, spaceAfter=10
)
ST_COVER_INFO = ParagraphStyle(
    'CoverInfo', fontName='DengL', fontSize=14, leading=20,
    textColor=C_GRAY, alignment=TA_CENTER
)

# 章标题（Part）
ST_PART_TITLE = ParagraphStyle(
    'PartTitle', fontName='DengB', fontSize=32, leading=42,
    textColor=C_PRIMARY, alignment=TA_LEFT,
    spaceBefore=60, spaceAfter=30
)

# 章标题（Chapter）
ST_CH_TITLE = ParagraphStyle(
    'ChTitle', fontName='DengB', fontSize=26, leading=34,
    textColor=C_PRIMARY, alignment=TA_LEFT,
    spaceBefore=40, spaceAfter=20
)

# 节标题
ST_SEC_TITLE = ParagraphStyle(
    'SecTitle', fontName='DengB', fontSize=18, leading=26,
    textColor=C_SECONDARY, alignment=TA_LEFT,
    spaceBefore=24, spaceAfter=12
)

# 小节标题
ST_SUBSEC_TITLE = ParagraphStyle(
    'SubSecTitle', fontName='DengB', fontSize=14, leading=20,
    textColor=C_ACCENT, alignment=TA_LEFT,
    spaceBefore=16, spaceAfter=8
)

# 正文（中文排版用左对齐，避免两端对齐导致单词间距过大）
ST_BODY = ParagraphStyle(
    'Body', fontName='Deng', fontSize=11, leading=18,
    textColor=C_TEXT, alignment=TA_LEFT, firstLineIndent=22,
    spaceAfter=6
)

# 正文（无首行缩进，用于列表内等）
ST_BODY_NOINDENT = ParagraphStyle(
    'BodyNoIndent', fontName='Deng', fontSize=11, leading=18,
    textColor=C_TEXT, alignment=TA_LEFT, spaceAfter=4
)

# 行内代码
ST_INLINE_CODE = ParagraphStyle(
    'InlineCode', fontName='Consola', fontSize=10, leading=14,
    textColor=C_DANGER, backColor=HexColor('#FADBD8'),
    borderPadding=(2, 4, 2, 4)
)

# 提示文字
ST_NOTE = ParagraphStyle(
    'Note', fontName='Deng', fontSize=10.5, leading=17,
    textColor=HexColor('#1A5276'), alignment=TA_LEFT,
    leftIndent=10, rightIndent=10, spaceBefore=6, spaceAfter=6
)

ST_WARN = ParagraphStyle(
    'Warn', fontName='Deng', fontSize=10.5, leading=17,
    textColor=HexColor('#784212'), alignment=TA_LEFT,
    leftIndent=10, rightIndent=10, spaceBefore=6, spaceAfter=6
)

# 目录标题
ST_TOC_TITLE = ParagraphStyle(
    'TOCTitle', fontName='DengB', fontSize=28, leading=36,
    textColor=C_PRIMARY, alignment=TA_CENTER, spaceAfter=30
)

ST_TOC_CH = ParagraphStyle(
    'TOCCh', fontName='DengB', fontSize=13, leading=20,
    textColor=C_PRIMARY, spaceBefore=8
)

ST_TOC_SEC = ParagraphStyle(
    'TOCSec', fontName='Deng', fontSize=11, leading=17,
    textColor=C_TEXT, leftIndent=20
)

# 页眉页脚
ST_HEADER = ParagraphStyle(
    'Header', fontName='DengL', fontSize=9, leading=12,
    textColor=C_GRAY, alignment=TA_CENTER
)

ST_FOOTER = ParagraphStyle(
    'Footer', fontName='DengL', fontSize=9, leading=12,
    textColor=C_GRAY, alignment=TA_CENTER
)

# ============================================================
# 4. 代码块样式
# ============================================================
# 代码用 Preformatted + Deng 等线字体（Consola 不支持中文注释）
CODE_STYLE = ParagraphStyle('code',
    fontName='Deng', fontSize=9, leading=13,
    textColor=HexColor('#2C3E50'), alignment=TA_LEFT,
    spaceBefore=0, spaceAfter=0)


# ========== 表格单元格专用样式 ==========
ST_TH = ParagraphStyle('TableH',
    fontName='DengB', fontSize=9.5, leading=13,
    textColor=colors.white, alignment=TA_LEFT)

ST_TD = ParagraphStyle('TableD',
    fontName='Deng', fontSize=9.5, leading=13,
    textColor=C_TEXT, alignment=TA_LEFT)

# 命令/代码列用等宽字体
ST_TD_CODE = ParagraphStyle('TableDCode',
    fontName='ConsolaB', fontSize=9.5, leading=13,
    textColor=C_DANGER, alignment=TA_LEFT)


def _wrap_table_rows(data_rows, body_style=None, header_style=None,
                     col_styles=None, header_col_styles=None):
    """把纯字符串 Table 数据行包装成 Paragraph 对象，支持自动换行。"""
    from reportlab.platypus import Flowable
    
    result = []
    for r, row in enumerate(data_rows):
        new_row = []
        is_header = (r == 0)
        for c, cell in enumerate(row):
            if isinstance(cell, Flowable):
                new_row.append(cell)
                continue
            if isinstance(cell, str):
                if is_header:
                    style = (header_col_styles.get(c) if header_col_styles else None) or header_style or ST_TH
                else:
                    style = (col_styles.get(c) if col_styles else None) or body_style or ST_TD
                safe = cell.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                new_row.append(Paragraph(safe, style))
                continue
            safe = str(cell).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            style = (header_style if is_header else body_style) or (ST_TH if is_header else ST_TD)
            new_row.append(Paragraph(safe, style))
        result.append(new_row)
    return result


# ============================================================
# 5. 统一表格样式工具函数
# ============================================================
def apply_table_style(t, header_color=HexColor('#1A5276'), header_text_color=colors.white):
    """给表格应用统一样式，确保中文正常显示"""
    t.setStyle(TableStyle([
        # 标题行
        ('BACKGROUND', (0, 0), (-1, 0), header_color),
        ('TEXTCOLOR',  (0, 0), (-1, 0), header_text_color),
        ('FONTNAME',   (0, 0), (-1, 0), 'DengB'),
        ('FONTSIZE',   (0, 0), (-1, 0), 9.5),
        ('ALIGN',      (0, 0), (-1, 0), 'CENTER'),
        # 数据行 - 关键！用中文字体 Deng
        ('FONTNAME',   (0, 1), (-1, -1), 'Deng'),
        ('FONTSIZE',   (0, 1), (-1, -1), 9.5),
        ('TEXTCOLOR',  (0, 1), (-1, -1), C_TEXT),
        # 交替行背景色
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F4F6F6')]),
        # 网格线
        ('GRID',       (0, 0), (-1, -1), 0.5, colors.HexColor('#D5D8DC')),
        # 垂直对齐
        ('VALIGN',     (0, 0), (-1, -1), 'MIDDLE'),
        # 内边距
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING',   (0, 0), (-1, -1), 6),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 6),
    ]))


# ============================================================
# 6. 工具函数
# ============================================================
def make_code_block(code_text):
    """生成代码块（带灰色背景的表格）- 支持长行自动折行"""
    # 处理 & < >
    code_text = code_text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    
    lines = code_text.split('\n')
    # 去掉末尾可能的空行（避免大空白）
    while lines and lines[-1].strip() == '':
        lines.pop()
    
    # 用一行一个 Preformatted Paragraph，开启自动换行
    inner_rows = []
    for line in lines:
        # breakLines=True 让长代码行自动折行，maxLineLength 设得足够大
        # Deng 字体 9pt 下，有效宽度 140mm ≈ 160 个等宽字符
        pf = Preformatted(line, CODE_STYLE,
                          maxLineLength=120, splitChars=' ,;:=|()[]{}')
        inner_rows.append([pf])
    
    t = Table(inner_rows, colWidths=['100%'])
    t.setStyle(TableStyle([
        ('BACKGROUND',  (0, 0), (-1, -1), C_BG_CODE),
        ('BOX',         (0, 0), (-1, -1), 0.5, C_LINE),
        ('TOPPADDING',  (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING',(0, 0), (-1, -1), 10),
        ('VALIGN',      (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME',    (0, 0), (-1, -1), 'Deng'),
    ]))
    return t


def make_note_box(text, box_type='note'):
    """生成提示/警告/危险框"""
    colors_map = {
        'note':   (C_BG_NOTE,   HexColor('#1A5276'), 'NOTE'),
        'warn':   (C_BG_WARN,   HexColor('#784212'), 'WARNING'),
        'danger': (C_BG_DANGER, HexColor('#922B21'), 'DANGER'),
        'tip':    (HexColor('#EAFAF1'), HexColor('#1E8449'), 'TIP'),
    }
    bg, fg, label = colors_map.get(box_type, colors_map['note'])
    
    label_para = Paragraph(f'<b>{label}</b>', ParagraphStyle('notelabel',
        fontName='DengB', fontSize=10.5, textColor=fg))
    content_para = Paragraph(text, ParagraphStyle('notecontent',
        fontName='Deng', fontSize=10.5, leading=17, textColor=fg))
    
    t = Table([[label_para], [content_para]], colWidths=[156*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND',  (0, 0), (-1, -1), bg),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING',(0, 0), (-1, -1), 10),
        ('TOPPADDING',  (0, 0), (0, 0), 6),
        ('BOTTOMPADDING', (-1, -1), (-1, -1), 8),
        ('LINEBELOW',   (0, 0), (0, 0), 1, fg),
        ('VALIGN',      (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME',    (0, 0), (-1, -1), 'Deng'),
    ]))
    return t


def hr():
    """水平分隔线"""
    return HRFlowable(width="100%", thickness=1, color=C_LINE, spaceAfter=10, spaceBefore=10)


def inline_code(text):
    """生成行内代码（蓝色等宽字体）"""
    return f'<font name="Consola" size="9" color="#C0392B"><b>{text}</b></font>'


# ============================================================
# 6. 页面模板
# ============================================================
class BookDocTemplate(BaseDocTemplate):
    def __init__(self, filename, **kwargs):
        BaseDocTemplate.__init__(self, filename, **kwargs)
        self.page_count = 0
    
    def afterFlowable(self, flowable):
        """捕获目录条目"""
        if isinstance(flowable, Paragraph):
            style = flowable.style.name
            if style.startswith('PartTitle'):
                text = flowable.getPlainText()
                self.notify('TOCEntry', (0, text, self.page))
            elif style.startswith('ChTitle'):
                text = flowable.getPlainText()
                self.notify('TOCEntry', (1, text, self.page))
            elif style.startswith('SecTitle'):
                text = flowable.getPlainText()
                self.notify('TOCEntry', (2, text, self.page))


def header_footer(canvas, doc):
    """画页眉页脚"""
    canvas.saveState()
    # 页眉
    canvas.setFont('DengL', 9)
    canvas.setFillColor(C_GRAY)
    canvas.drawCentredString(A4[0]/2, A4[1] - 18,
        "Windows BAT 批处理完全教程")
    # 页眉分隔线
    canvas.setStrokeColor(C_LINE)
    canvas.line(20*mm, A4[1] - 24, A4[0] - 20*mm, A4[1] - 24)
    # 页脚分隔线
    canvas.line(20*mm, 18*mm, A4[0] - 20*mm, 18*mm)
    # 页码
    canvas.drawCentredString(A4[0]/2, 10*mm,
        f"— {doc.page} —")
    canvas.restoreState()


def no_header_footer(canvas, doc):
    """空白页眉页脚（封面、目录用）"""
    pass


# ============================================================
# 7. 构建 PDF
# ============================================================
def build_pdf(output_path):
    """主构建函数"""
    import chapters_01_03
    import chapters_04_06
    import chapters_07_10
    import chapters_11_14
    import appendices
    import expansions
    exps = expansions.get_chapter_expansions()
    
    doc = BookDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=25*mm, rightMargin=25*mm,
        topMargin=28*mm, bottomMargin=25*mm,
        title="Windows BAT 批处理完全教程",
        author="BAT 批处理教程编写组",
    )
    
    # 页面模板
    body_frame = Frame(25*mm, 25*mm, A4[0]-50*mm, A4[1]-53*mm, id='body')
    cover_template = PageTemplate(id='cover', frames=body_frame, onPage=no_header_footer)
    toc_template   = PageTemplate(id='toc',   frames=body_frame, onPage=no_header_footer)
    body_template  = PageTemplate(id='body',  frames=body_frame, onPage=header_footer)
    
    doc.addPageTemplates([cover_template, toc_template, body_template])
    
    story = []
    
    # ========== 封面 ==========
    story.append(Spacer(1, 70*mm))
    story.append(Paragraph("Windows BAT", ST_COVER_TITLE))
    story.append(Paragraph("批处理完全教程", ST_COVER_TITLE))
    story.append(Spacer(1, 10*mm))
    story.append(HRFlowable(width="60%", thickness=2, color=C_SECONDARY, spaceAfter=15))
    story.append(Paragraph("从零基础入门到高级精通", ST_COVER_SUB))
    story.append(Paragraph("覆盖 cmd.exe 全部核心特性 · 系统管理实战 · 黑科技应用", ST_COVER_INFO))
    story.append(Spacer(1, 15*mm))
    story.append(Paragraph("2026", ST_COVER_INFO))
    story.append(PageBreak())
    
    # ========== 目录页（手动构建目录） ==========
    story.append(Paragraph("目  录", ST_TOC_TITLE))
    story.append(Spacer(1, 10*mm))
    
    toc_entries = [
        ('第一部分 基础入门篇', [
            '第1章 认识 cmd.exe 与 BAT 批处理',
            '第2章 第一个 BAT 程序与基础输出',
            '第3章 批处理的执行机制',
        ]),
        ('第二部分 核心语法篇', [
            '第4章 变量系统全解析',
            '第5章 流程控制语句',
            '第6章 重定向、管道与输入输出',
        ]),
        ('第三部分 文件与系统操作篇', [
            '第7章 文件操作实战',
            '第8章 目录与路径操作',
            '第9章 系统管理命令',
            '第10章 网络操作命令',
        ]),
        ('第四部分 高级技巧与实战篇', [
            '第11章 高级语法与黑科技',
            '第12章 实战项目一：系统维护工具集',
            '第13章 实战项目二：网络运维工具集',
            '第14章 实战项目三：进阶黑科技工具集',
        ]),
        ('第五部分 附录与参考篇', [
            '附录A Windows 批处理核心命令速查表',
            '附录B cmd.exe 环境变量大全',
            '附录C 批处理常见问题与疑难解答',
            '附录D BAT 开发工具与资源',
            '附录E 示例代码全集索引',
        ]),
    ]
    
    for part_title, chapters in toc_entries:
        story.append(Paragraph(part_title, ParagraphStyle('TOCPart',
            fontName='DengB', fontSize=14, leading=22,
            textColor=C_PRIMARY, spaceBefore=10, spaceAfter=4)))
        for ch in chapters:
            story.append(Paragraph(ch, ParagraphStyle('TOCCh2',
                fontName='Deng', fontSize=11, leading=18,
                textColor=C_TEXT, leftIndent=18, spaceAfter=2)))
    
    story.append(PageBreak())
    
    # ========== 第一部分 ==========
    story.append(Paragraph("第一部分 基础入门篇", ST_PART_TITLE))
    for i, ch_flowables in enumerate(chapters_01_03.get_chapters(), 1):
        story.extend(ch_flowables)
        if i in exps: story.extend(exps[i])
    
    # ========== 第二部分 ==========
    story.append(Paragraph("第二部分 核心语法篇", ST_PART_TITLE))
    for i, ch_flowables in enumerate(chapters_04_06.get_chapters(), 4):
        story.extend(ch_flowables)
        if i in exps: story.extend(exps[i])
    
    # ========== 第三部分 ==========
    story.append(Paragraph("第三部分 文件与系统操作篇", ST_PART_TITLE))
    for i, ch_flowables in enumerate(chapters_07_10.get_chapters(), 7):
        story.extend(ch_flowables)
        if i in exps: story.extend(exps[i])
    
    # ========== 第四部分 ==========
    story.append(Paragraph("第四部分 高级技巧与实战篇", ST_PART_TITLE))
    for i, ch_flowables in enumerate(chapters_11_14.get_chapters(), 11):
        story.extend(ch_flowables)
        if i in exps: story.extend(exps[i])
    
    # ========== 第五部分（附录不需要 Part 标题）==========
    story.extend(appendices.get_appendices())
    
    doc.build(story)
    print(f"✅ PDF 已生成: {output_path}")


if __name__ == '__main__':
    output = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                          "Windows_BAT_批处理完全教程.pdf")
    print("正在生成 PDF，请稍候...")
    build_pdf(output)
    print("完成！")
