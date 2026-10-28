"""作品集 PDF：封面 + 程序介绍 + 截图（GEO 同款 reportlab 中文字体方案）。本地导出，不进 GitHub。"""
from __future__ import annotations

import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPORT_DIR = ROOT / "portfolio"
SHOT_DIR = EXPORT_DIR / "screenshots"


def _safe_stem(text: str, fallback: str = "portfolio") -> str:
    raw = (text or "").strip() or fallback
    cleaned = re.sub(r'[\\/:*?"<>|\r\n\t]+', "_", raw)
    return cleaned.strip(" ._")[:60] or fallback


def _pick_chinese_font() -> str | None:
    for p in [
        Path("/System/Library/Fonts/PingFang.ttc"),
        Path("/System/Library/Fonts/STHeiti Light.ttc"),
        Path("/Library/Fonts/Arial Unicode.ttf"),
        Path(r"C:\Windows\Fonts\msyh.ttc"),
    ]:
        if p.exists():
            return str(p)
    return None


def _register_font() -> str:
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    font_path = _pick_chinese_font()
    if not font_path:
        return "Helvetica"
    try:
        pdfmetrics.registerFont(TTFont("GeoCN", font_path))
        return "GeoCN"
    except Exception:
        try:
            pdfmetrics.registerFont(TTFont("GeoCN", font_path, subfontIndex=0))
            return "GeoCN"
        except Exception:
            return "Helvetica"


def _esc(t: str) -> str:
    return (t or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def export_portfolio_pdf() -> Path:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import cm
    from reportlab.platypus import (
        Image,
        KeepTogether,
        PageBreak,
        Paragraph,
        SimpleDocTemplate,
        Spacer,
    )

    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    title = "睿览·职业工作手册圆桌（作品集）"
    path = EXPORT_DIR / f"{_safe_stem(title)}.pdf"

    font_name = _register_font()
    styles = getSampleStyleSheet()
    h1 = ParagraphStyle(
        "H1",
        parent=styles["Heading1"],
        fontName=font_name,
        fontSize=18,
        leading=24,
        spaceAfter=12,
        spaceBefore=4,
        textColor="#071E36",
    )
    h2 = ParagraphStyle(
        "H2",
        parent=styles["Heading2"],
        fontName=font_name,
        fontSize=13,
        leading=20,
        spaceAfter=8,
        spaceBefore=12,
        textColor="#0B2B4A",
    )
    body = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontName=font_name,
        fontSize=11,
        leading=18,
        spaceAfter=8,
        textColor="#132033",
    )
    caption = ParagraphStyle(
        "Cap",
        parent=styles["Normal"],
        fontName=font_name,
        fontSize=9.5,
        leading=14,
        textColor="#5A6A7C",
        spaceAfter=14,
        spaceBefore=4,
    )
    bullet = ParagraphStyle(
        "Bullet",
        parent=body,
        leftIndent=14,
        bulletIndent=0,
        spaceAfter=6,
    )

    doc = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        leftMargin=1.8 * cm,
        rightMargin=1.8 * cm,
        topMargin=1.6 * cm,
        bottomMargin=1.6 * cm,
        title=title,
        author="hahadada0528",
    )
    story = []
    page_w = A4[0] - 3.6 * cm

    # —— 封面 ——
    cover = SHOT_DIR / "00-cover.png"
    if cover.is_file():
        story.append(Image(str(cover), width=page_w, height=page_w * 1754 / 1240))
        story.append(PageBreak())

    # —— 程序介绍 ——
    story.append(Paragraph(_esc("一、程序介绍"), h1))
    story.append(
        Paragraph(
            _esc(
                "睿览 · 职业工作手册圆桌，是一套多智能体桌面产品。"
                "用户说出职业名后，主 agent 点兵，按固定阶段推进背调、调研、知识库、分解与人机分工；"
                "每一步都等人批准，最终交出可复检的职业工作手册。"
            ),
            body,
        )
    )
    story.append(Paragraph(_esc("产品定位"), h2))
    for line in [
        "形态：桌面 App（pywebview）+ 本地看板 + LLM 多智能体流水线",
        "核心机制：人在环（Human-in-the-loop）阶段门禁",
        "知识沉淀：每职业独立 data/{职业}/；Obsidian + LLM Wiki（compile, don't retrieve）",
        "复检纪律：调研只交链接，入库前核实；切片必须带原文 http(s)",
    ]:
        story.append(Paragraph(_esc("• " + line), bullet))

    story.append(Paragraph(_esc("我解决什么问题"), h2))
    story.append(
        Paragraph(
            _esc(
                "职业学习资料散落在招聘站、国家标准和个人笔记里，缺少「可批准、可复检、可沉淀」的流程。"
                "本程序把流程拆成固定席位与阶段门禁，把产出沉到本地知识库，让人始终能拍板。"
            ),
            body,
        )
    )

    story.append(Paragraph(_esc("我做了什么"), h2))
    for line in [
        "Windows 独立包 → macOS 可运行时（Python 3.12 + 原生依赖）",
        "看板睿览品牌化：logo、海军蓝皮肤、桌面窗口标题",
        "一键启动脚本、依赖清单与作品集文档交付",
    ]:
        story.append(Paragraph(_esc("• " + line), bullet))

    story.append(Paragraph(_esc("技术栈"), h2))
    story.append(
        Paragraph(
            _esc(
                "Python 3.12 · LangChain / LangGraph · Deep Agents · pywebview · "
                "Obsidian / LLM Wiki 技能 · AGICTO OpenAI 兼容接口"
            ),
            body,
        )
    )

    story.append(PageBreak())

    # —— 流程与席位 ——
    story.append(Paragraph(_esc("二、流程与席位"), h1))
    story.append(Paragraph(_esc("八步流水线"), h2))
    for i, step in enumerate(
        [
            "定职业建库",
            "职业背调（录入 JD → 归纳 → 批准）",
            "全网行业调研（交链接 → 批准）",
            "链接入库（知识库核实）",
            "上传素材并蒸馏切片",
            "目标分解 → 复检 → 批准",
            "人机分工（tools.md）→ 复检",
            "主 agent 终审交稿",
        ],
        start=1,
    ):
        story.append(Paragraph(_esc(f"{i}. {step}"), bullet))

    story.append(Paragraph(_esc("圆桌席位"), h2))
    seats = [
        ("主 agent", "理解意图、点兵、等人批准、终审"),
        ("知识库", "建库、蒸馏切片、整理上传"),
        ("职业背调", "招聘职责归纳"),
        ("行业调研", "规范 / 岗位 / KPI 公开资料"),
        ("分解", "第一性原理拆工作事项"),
        ("人机分工", "工具 / AI 可替代 / 必须人工"),
        ("复检", "链接与结构 Reality Check"),
    ]
    for name, desc in seats:
        story.append(Paragraph(_esc(f"• {name}：{desc}"), bullet))

    story.append(PageBreak())

    # —— 程序截图 ——
    story.append(Paragraph(_esc("三、程序截图"), h1))
    shots = [
        ("01-board-overview.png", "看板总览：睿览顶栏、八步流程、圆桌席位与对话输入区"),
        ("02-files-tab.png", "「生成的文件」页：圆桌产出的 md / txt / Word 在此交付"),
    ]
    for name, cap in shots:
        p = SHOT_DIR / name
        if not p.is_file():
            continue
        # fit width, keep aspect, max height ~ 14cm
        from PIL import Image as PILImage

        with PILImage.open(p) as im:
            w, h = im.size
        max_h = 14 * cm
        disp_w = page_w
        disp_h = disp_w * h / w
        if disp_h > max_h:
            disp_h = max_h
            disp_w = disp_h * w / h
        block = [
            Paragraph(_esc(cap.split("：")[0] if "：" in cap else name), h2),
            Image(str(p), width=disp_w, height=disp_h),
            Paragraph(_esc(cap), caption),
        ]
        story.append(KeepTogether(block))

    story.append(Spacer(1, 8))
    story.append(Paragraph(_esc("四、仓库与本地运行"), h1))
    story.append(
        Paragraph(
            _esc(
                "GitHub：https://github.com/hahadada0528/rolen-career-roundtable"
                "（源码与说明；本 PDF / 截图仅本地作品集材料，不上传仓库）"
            ),
            body,
        )
    )
    story.append(
        Paragraph(
            _esc(
                "本机：复制 .env.example 为 .env，填入 AGICTO_API_KEY，"
                "执行 python main.py 或双击「启动圆桌App.command」。"
            ),
            body,
        )
    )
    story.append(Spacer(1, 16))
    story.append(
        Paragraph(
            _esc(f"导出时间：{datetime.now().strftime('%Y-%m-%d %H:%M')} · 方法：reportlab + 本机中文字体（同 GEO）"),
            caption,
        )
    )

    doc.build(story)
    return path


def main() -> int:
    try:
        pdf = export_portfolio_pdf()
    except Exception as exc:
        print(f"导出失败：{exc}", file=sys.stderr)
        return 1
    print(f"PDF: {pdf}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
