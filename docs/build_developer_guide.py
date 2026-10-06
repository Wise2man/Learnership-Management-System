"""Build the shareable developer guide PDF from its Markdown source."""

from pathlib import Path
import re
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    HRFlowable,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


DOCS = Path(__file__).resolve().parent
SOURCE = DOCS / "DEVELOPER_GUIDE.md"
OUTPUT = DOCS / "DEVELOPER_GUIDE.pdf"

INK = colors.HexColor("#172B3A")
TEAL = colors.HexColor("#087E83")
PALE = colors.HexColor("#EAF3F2")
RULE = colors.HexColor("#D4E0E3")


def make_styles():
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            "GuideTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=25,
            leading=30,
            textColor=INK,
            alignment=TA_CENTER,
            spaceAfter=10,
        )
    )
    styles.add(
        ParagraphStyle(
            "GuideSubtitle",
            parent=styles["Normal"],
            fontSize=14,
            leading=18,
            textColor=TEAL,
            alignment=TA_CENTER,
            spaceAfter=10,
        )
    )
    styles.add(
        ParagraphStyle(
            "GuideH1",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=17,
            leading=21,
            textColor=INK,
            spaceBefore=14,
            spaceAfter=8,
            keepWithNext=True,
        )
    )
    styles.add(
        ParagraphStyle(
            "GuideH2",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=15,
            textColor=TEAL,
            spaceBefore=10,
            spaceAfter=5,
            keepWithNext=True,
        )
    )
    styles.add(
        ParagraphStyle(
            "GuideBody",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=9.3,
            leading=13.2,
            textColor=INK,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            "GuideBullet",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=9.1,
            leading=12.5,
            textColor=INK,
        )
    )
    styles.add(
        ParagraphStyle(
            "GuideTable",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=7.8,
            leading=10,
            textColor=INK,
        )
    )
    styles.add(
        ParagraphStyle(
            "GuideTableHeader",
            parent=styles["GuideTable"],
            fontName="Helvetica-Bold",
            textColor=colors.white,
        )
    )
    return styles


def inline_markup(text):
    text = escape(text)
    text = re.sub(
        r"`([^`]+)`",
        r'<font name="Courier" color="#087E83">\1</font>',
        text,
    )
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    return text


def parse_table(lines, styles, width):
    rows = [[cell.strip() for cell in line.strip().strip("|").split("|")] for line in lines]
    rows = [row for row in rows if not all(re.fullmatch(r":?-{3,}:?", cell) for cell in row)]
    if not rows:
        return None
    column_count = len(rows[0])
    data = []
    for row_index, row in enumerate(rows):
        row = (row + [""] * column_count)[:column_count]
        style = styles["GuideTableHeader"] if row_index == 0 else styles["GuideTable"]
        data.append([Paragraph(inline_markup(cell), style) for cell in row])
    table = Table(data, colWidths=[width / column_count] * column_count, repeatRows=1, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), INK),
                ("GRID", (0, 0), (-1, -1), 0.35, RULE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE]),
            ]
        )
    )
    return table


def parse_markdown(text, styles, width):
    lines = text.splitlines()
    story = []
    index = 0
    first_title = True
    while index < len(lines):
        line = lines[index].strip()
        if not line:
            index += 1
            continue
        if line.startswith("```"):
            index += 1
            code_lines = []
            while index < len(lines) and not lines[index].strip().startswith("```"):
                code_lines.append(lines[index])
                index += 1
            index += 1
            code_style = ParagraphStyle(
                "GuideCode",
                fontName="Courier",
                fontSize=7.6,
                leading=10.2,
                textColor=INK,
                backColor=PALE,
                borderColor=RULE,
                borderWidth=0.5,
                borderPadding=7,
                leftIndent=6,
                rightIndent=6,
                spaceBefore=3,
                spaceAfter=8,
            )
            story.append(Preformatted("\n".join(code_lines), code_style, maxLineLength=96))
            continue
        if line.startswith("|"):
            table_lines = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                table_lines.append(lines[index].strip())
                index += 1
            table = parse_table(table_lines, styles, width)
            if table:
                story.extend([Spacer(1, 3), table, Spacer(1, 7)])
            continue
        if line == "---":
            story.extend([Spacer(1, 3), HRFlowable(width="100%", thickness=0.7, color=RULE), Spacer(1, 6)])
            index += 1
            continue
        if line.startswith("# "):
            if not first_title:
                story.append(Paragraph(inline_markup(line[2:]), styles["GuideH1"]))
            else:
                story.extend([Spacer(1, 24), Paragraph(inline_markup(line[2:]), styles["GuideTitle"])])
                first_title = False
            index += 1
            continue
        if line.startswith("## "):
            heading = line[3:]
            if heading == "Developer App and Views Guide":
                story.append(Paragraph(inline_markup(heading), styles["GuideSubtitle"]))
            else:
                story.append(Paragraph(inline_markup(heading), styles["GuideH1"]))
            index += 1
            continue
        if line.startswith("### "):
            story.append(Paragraph(inline_markup(line[4:]), styles["GuideH2"]))
            index += 1
            continue
        if line.startswith("- "):
            items = []
            while index < len(lines) and lines[index].strip().startswith("- "):
                value = lines[index].strip()[2:]
                items.append(ListItem(Paragraph(inline_markup(value), styles["GuideBullet"]), leftIndent=9))
                index += 1
            story.append(ListFlowable(items, bulletType="bullet", start="circle", leftIndent=16, bulletFontSize=6, spaceAfter=6))
            continue
        if re.match(r"\d+\.\s", line):
            items = []
            while index < len(lines) and re.match(r"\d+\.\s", lines[index].strip()):
                value = re.sub(r"^\d+\.\s", "", lines[index].strip())
                items.append(ListItem(Paragraph(inline_markup(value), styles["GuideBullet"]), leftIndent=9))
                index += 1
            story.append(ListFlowable(items, bulletType="1", leftIndent=18, bulletFontName="Helvetica", bulletFontSize=8, spaceAfter=7))
            continue
        paragraph_lines = [line]
        index += 1
        while index < len(lines):
            next_line = lines[index].strip()
            if not next_line or next_line.startswith(("#", "- ", "|", "```")) or re.match(r"\d+\.\s", next_line):
                break
            paragraph_lines.append(next_line)
            index += 1
        story.append(Paragraph(inline_markup(" ".join(paragraph_lines)), styles["GuideBody"]))
    return story


def add_page_chrome(canvas, doc):
    canvas.saveState()
    width, height = A4
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.6)
    canvas.line(doc.leftMargin, height - 14 * mm, width - doc.rightMargin, height - 14 * mm)
    canvas.setFont("Helvetica-Bold", 7.5)
    canvas.setFillColor(TEAL)
    canvas.drawString(doc.leftMargin, height - 11 * mm, "LEARNERSHIP LMS  /  DEVELOPER GUIDE")
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(INK)
    canvas.drawRightString(width - doc.rightMargin, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


def main():
    styles = make_styles()
    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=22 * mm,
        bottomMargin=18 * mm,
        title="Learnership LMS Developer App and Views Guide",
        author="Learnership Management System team",
        subject="App ownership, Django function-based views, testing, and team workflow",
    )
    source = SOURCE.read_text(encoding="utf-8")
    doc.build(parse_markdown(source, styles, doc.width), onFirstPage=add_page_chrome, onLaterPages=add_page_chrome)
    print(f"Generated {OUTPUT}")


if __name__ == "__main__":
    main()