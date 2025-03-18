# invoice_generator.py
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from io import BytesIO
from PIL import Image as PILImage

class InvoiceData:
    def __init__(self, order_id, customer_name, customer_phone, customer_address, items, logo_path):
        self.order_id = order_id
        self.customer_name = customer_name
        self.customer_phone = customer_phone
        self.customer_address = customer_address
        self.items = items  # List of dictionaries: [{"quantity": int, "name": str, "description": str, "price": float}]
        self.logo_path = logo_path

class InvoiceGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.styles.add(ParagraphStyle(name='Center', alignment=1))

    def create_invoice(self, data: InvoiceData) -> bytes:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        story = []

        # Add logo
        img = PILImage.open(data.logo_path)
        img_width, img_height = img.size
        aspect = img_height / float(img_width)
        logo = Image(data.logo_path, width=2*inch, height=(2*inch * aspect))
        story.append(logo)

        # Add heading
        story.append(Paragraph("SALES RECEIPT", self.styles['Title']))
        story.append(Spacer(1, 0.25*inch))

        # Add customer details
        story.append(Paragraph(f"Order ID: {data.order_id}", self.styles['Normal']))
        story.append(Paragraph(f"Customer: {data.customer_name}", self.styles['Normal']))
        story.append(Paragraph(f"Phone: {data.customer_phone}", self.styles['Normal']))
        story.append(Paragraph(f"Address: {data.customer_address}", self.styles['Normal']))
        story.append(Spacer(1, 0.25*inch))

        # Create table for items
        table_data = [['Quantity', 'Product Name', 'Description', 'Price', 'Total']]
        total_price = 0
        for item in data.items:
            item_total = item['quantity'] * item['price']
            total_price += item_total
            table_data.append([
                str(item['quantity']),
                item['name'],
                item['description'],
                f"${item['price']:.2f}",
                f"${item_total:.2f}"
            ])
        
        # Add total row
        table_data.append(['', '', '', 'Total:', f"${total_price:.2f}"])

        # Create table
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        story.append(table)
        
        doc.build(story)
        pdf = buffer.getvalue()
        buffer.close()
        return pdf