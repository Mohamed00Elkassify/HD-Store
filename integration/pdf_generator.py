"""
Generate Sales Invoice PDF from ERPNext data using reportlab.
"""
import io
import logging
from typing import Any, Dict

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

logger = logging.getLogger(__name__)

PAGE_WIDTH, PAGE_HEIGHT = A4


def _build_styles():
    """Return a dict of named paragraph styles."""
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "InvoiceTitle",
            parent=base["Heading1"],
            fontSize=18,
            alignment=TA_CENTER,
            spaceAfter=6 * mm,
            textColor=colors.HexColor("#1a1a2e"),
        ),
        "heading": ParagraphStyle(
            "SectionHeading",
            parent=base["Heading2"],
            fontSize=11,
            textColor=colors.HexColor("#16213e"),
            spaceAfter=2 * mm,
        ),
        "normal": ParagraphStyle(
            "NormalText",
            parent=base["Normal"],
            fontSize=9,
            leading=12,
        ),
        "bold": ParagraphStyle(
            "BoldText",
            parent=base["Normal"],
            fontSize=9,
            leading=12,
            fontName="Helvetica-Bold",
        ),
        "small": ParagraphStyle(
            "SmallText",
            parent=base["Normal"],
            fontSize=8,
            leading=10,
            textColor=colors.grey,
        ),
        "right": ParagraphStyle(
            "RightText",
            parent=base["Normal"],
            fontSize=9,
            alignment=TA_RIGHT,
        ),
        "right_bold": ParagraphStyle(
            "RightBold",
            parent=base["Normal"],
            fontSize=9,
            fontName="Helvetica-Bold",
            alignment=TA_RIGHT,
        ),
        "footer": ParagraphStyle(
            "FooterText",
            parent=base["Normal"],
            fontSize=8,
            alignment=TA_CENTER,
            textColor=colors.grey,
        ),
    }


def generate_sales_invoice_pdf(inv_data: Dict[str, Any]) -> bytes:
    """Build a professional Sales Invoice PDF and return raw PDF bytes.

    Parameters
    ----------
    inv_data : dict
        The ``data`` dict from ``/api/resource/Sales Invoice/<name>``.
    """
    styles = _build_styles()
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=15 * mm,
        rightMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
    )
    elements = []

    # ── Company header ─────────────────────────────────────────────────
    company = inv_data.get("company") or ""
    elements.append(Paragraph(company, styles["title"]))

    # ── Invoice title & number ─────────────────────────────────────────
    inv_name = inv_data.get("name", "")
    elements.append(
        Paragraph(f"Sales Invoice: {inv_name}", styles["heading"])
    )
    elements.append(Spacer(1, 3 * mm))

    # ── Info table (two columns: left = customer, right = invoice meta)
    customer_name = inv_data.get("customer_name", "")
    posting_date = inv_data.get("posting_date", "")
    due_date = inv_data.get("due_date", "")
    po_no = inv_data.get("po_no", "")
    address = (inv_data.get("address_display") or "").replace("<br>", "\n").replace("<br/>", "\n").strip()
    contact_mobile = inv_data.get("contact_mobile") or ""
    status_text = inv_data.get("status") or ""

    left_info = []
    left_info.append(Paragraph(f"<b>Customer:</b> {customer_name}", styles["normal"]))
    if address:
        # Replace newlines with <br/> for Paragraph
        addr_html = address.replace("\n", "<br/>")
        left_info.append(Paragraph(f"<b>Address:</b><br/>{addr_html}", styles["normal"]))
    if contact_mobile:
        left_info.append(Paragraph(f"<b>Mobile:</b> {contact_mobile}", styles["normal"]))

    right_info = []
    right_info.append(Paragraph(f"<b>Date:</b> {posting_date}", styles["right"]))
    if due_date:
        right_info.append(Paragraph(f"<b>Due Date:</b> {due_date}", styles["right"]))
    if po_no:
        right_info.append(Paragraph(f"<b>Order Ref:</b> {po_no}", styles["right"]))
    if status_text:
        right_info.append(Paragraph(f"<b>Status:</b> {status_text}", styles["right"]))

    left_cell = []
    for p in left_info:
        left_cell.append(p)
        left_cell.append(Spacer(1, 1 * mm))

    right_cell = []
    for p in right_info:
        right_cell.append(p)
        right_cell.append(Spacer(1, 1 * mm))

    info_table = Table(
        [[left_cell, right_cell]],
        colWidths=[doc.width * 0.55, doc.width * 0.45],
    )
    info_table.setStyle(
        TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ])
    )
    elements.append(info_table)
    elements.append(Spacer(1, 6 * mm))

    # ── Items table ────────────────────────────────────────────────────
    currency = inv_data.get("currency", "EGP")
    items = inv_data.get("items") or []

    header = [
        Paragraph("<b>#</b>", styles["bold"]),
        Paragraph("<b>Item</b>", styles["bold"]),
        Paragraph("<b>Qty</b>", styles["bold"]),
        Paragraph("<b>Rate</b>", styles["bold"]),
        Paragraph("<b>Amount</b>", styles["bold"]),
    ]

    table_data = [header]
    for idx, item in enumerate(items, start=1):
        item_name = item.get("item_name") or item.get("item_code") or ""
        qty = item.get("qty", 0)
        rate = item.get("rate", 0)
        amount = item.get("amount", 0)

        # Format numbers
        qty_str = f"{qty:g}" if isinstance(qty, float) else str(qty)
        rate_str = f"{rate:,.2f}"
        amount_str = f"{amount:,.2f}"

        table_data.append([
            Paragraph(str(idx), styles["normal"]),
            Paragraph(item_name, styles["normal"]),
            Paragraph(qty_str, styles["right"]),
            Paragraph(f"{currency} {rate_str}", styles["right"]),
            Paragraph(f"{currency} {amount_str}", styles["right"]),
        ])

    col_widths = [
        doc.width * 0.06,   # #
        doc.width * 0.44,   # Item
        doc.width * 0.10,   # Qty
        doc.width * 0.20,   # Rate
        doc.width * 0.20,   # Amount
    ]

    items_table = Table(table_data, colWidths=col_widths, repeatRows=1)
    items_table.setStyle(
        TableStyle([
            # Header row
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a1a2e")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 9),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
            ("TOPPADDING", (0, 0), (-1, 0), 6),
            # Body rows
            ("FONTSIZE", (0, 1), (-1, -1), 9),
            ("TOPPADDING", (0, 1), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 1), (-1, -1), 4),
            # Alternating row colours
            *[
                ("BACKGROUND", (0, r), (-1, r), colors.HexColor("#f5f5f5"))
                for r in range(2, len(table_data), 2)
            ],
            # Grid
            ("LINEBELOW", (0, 0), (-1, 0), 1, colors.HexColor("#1a1a2e")),
            ("LINEBELOW", (0, -1), (-1, -1), 0.5, colors.grey),
            ("LINEAFTER", (0, 0), (-2, -1), 0.25, colors.HexColor("#e0e0e0")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ])
    )
    elements.append(items_table)
    elements.append(Spacer(1, 4 * mm))

    # ── Totals ─────────────────────────────────────────────────────────
    net_total = inv_data.get("net_total", 0)
    total_taxes = inv_data.get("total_taxes_and_charges", 0)
    discount = inv_data.get("discount_amount", 0)
    grand_total = inv_data.get("grand_total", 0)
    outstanding = inv_data.get("outstanding_amount", 0)
    in_words = inv_data.get("in_words", "")

    totals_rows = []
    totals_rows.append(["Net Total", f"{currency} {net_total:,.2f}"])
    if total_taxes:
        totals_rows.append(["Taxes & Charges", f"{currency} {total_taxes:,.2f}"])
    if discount:
        totals_rows.append(["Discount", f"- {currency} {discount:,.2f}"])
    totals_rows.append(["Grand Total", f"{currency} {grand_total:,.2f}"])
    if outstanding and outstanding != grand_total:
        totals_rows.append(["Outstanding", f"{currency} {outstanding:,.2f}"])

    totals_data = [
        [
            Paragraph(row[0], styles["bold"] if row[0] == "Grand Total" else styles["normal"]),
            Paragraph(row[1], styles["right_bold"] if row[0] == "Grand Total" else styles["right"]),
        ]
        for row in totals_rows
    ]

    totals_table = Table(
        totals_data,
        colWidths=[doc.width * 0.30, doc.width * 0.20],
        hAlign="RIGHT",
    )
    totals_table.setStyle(
        TableStyle([
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("LINEABOVE", (0, -1), (-1, -1), 0.5, colors.grey),
            # Bold the grand total row
            *[
                ("LINEBELOW", (0, i), (-1, i), 1.5, colors.HexColor("#1a1a2e"))
                for i, row in enumerate(totals_rows)
                if row[0] == "Grand Total"
            ],
        ])
    )
    elements.append(totals_table)

    if in_words:
        elements.append(Spacer(1, 3 * mm))
        elements.append(Paragraph(f"<i>{in_words}</i>", styles["small"]))

    # ── Remarks ────────────────────────────────────────────────────────
    remarks = inv_data.get("remarks")
    if remarks:
        elements.append(Spacer(1, 6 * mm))
        elements.append(Paragraph("Remarks", styles["heading"]))
        elements.append(Paragraph(remarks, styles["normal"]))

    # ── Footer ─────────────────────────────────────────────────────────
    elements.append(Spacer(1, 10 * mm))
    elements.append(
        Paragraph(
            f"This is a computer-generated invoice from {company}.",
            styles["footer"],
        )
    )

    # Build PDF
    doc.build(elements)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    logger.info("Generated local PDF for Sales Invoice %s (%d bytes)", inv_name, len(pdf_bytes))
    return pdf_bytes
