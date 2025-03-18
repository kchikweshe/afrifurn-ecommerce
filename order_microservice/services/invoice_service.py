import os
from fastapi import Depends, HTTPException
import httpx
from sqlmodel import Session
from db import get_session
from models.order import Cart, CartItem, Invoice, Order
from services.email_service import EmailService
from services.product_service import ProductService
from services.user_service import UserService
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors

# Define the folder where reports will be saved
REPORTS_FOLDER = "./reports"
os.makedirs(REPORTS_FOLDER, exist_ok=True)  # Create the folder if it doesn't exist

 
class InvoiceService:
    def __init__(self, user_service: UserService, product_service: ProductService, email_service: EmailService):
        self.user_service = user_service
        self.product_service = product_service
        self.email_service = email_service
    def save(self,order:Order,session: Session):

        invoice=Invoice(
                order_id=order.id,
                customer_address=order.customer_address,
                customer_name=order.customer_name,
                customer_phone=order.customer_phone,
                

            )
        
        
        # statement = select(Order).where(Order.name == "Spider-Boy")
        session.add(invoice)
        session.commit()
        session.refresh(invoice)
        print("Updated invoice:", invoice)
        return invoice
    def generate_pdf(self,invoice: Invoice,cart:Cart)->None:
        """
        Generate a PDF invoice using ReportLab
        
        :param invoice: Invoice object to convert to PDF
        :param filename: Output PDF filename
        """
        filename=f"{invoice.customer_name}-INV-{invoice.date.strftime("%d-%b-%Y")}.pdf"
        file_path = os.path.join(REPORTS_FOLDER, filename)

        doc = SimpleDocTemplate(file_path, pagesize=letter)
        styles = getSampleStyleSheet()
        
        # Prepare invoice header elements
        header_data = [
            ['SALES RECEIPT', ''],
            ['US$ QUOTATION VALID 30 DAYS ONLY', ''],
            ['9 QUENDON RD', ''],
            ['AVONDALE', ''],
            ['HARARE', ''],
            ['TEL: +263784996229', ''],
            [f'Date: {invoice.date.strftime("%d-%b-%Y")}', f'Invoice #: {invoice.invoice_number}'],
        ]
        
        # Prepare items for table
        items_data = [
            ['QTY', 'DESCRIPTION', 'UNIT PRICE', 'TOTAL SALES']
        ]
        items_data.extend([
            [str(item.quantity), item.product['description'], 
             f'US$ {item.unit_price:.2f}', 
             f'US$ {item.quantity * item.unit_price:.2f}'] 
            for item in cart.items
        ])
        
        # Add totals
        subtotal = cart.total_amount
        vat = cart.total_amount*0.15
        total = subtotal+vat
        
        items_data.extend([
            ['', 'Sub Total', '', f'US$ {subtotal:.2f}'],
            ['', 'VAT', '', f'US$ {vat:.2f}'],
            ['', 'TOTAL', '', f'US$ {total:.2f}']
        ])
        
        # Create PDF elements
        elements = []
        
        # Header table
        header_table = Table(header_data, colWidths=[4*inch, 2*inch])
        header_table.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ]))
        elements.append(header_table)
        
        # Items table
        items_table = Table(items_data, colWidths=[1*inch, 3*inch, 1.5*inch, 1.5*inch])
        items_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
            ('GRID', (0,0), (-1,-1), 1, colors.black)
        ]))
        elements.append(items_table)
        
        # Additional notes
        notes = [
            Paragraph("DEPOSIT: 60% OF PURCHASE PRICE", styles['Normal']),
            Paragraph("DELIVERY WITHIN 5-7 DAYS OF DEPOSIT PAYMENT", styles['Normal'])
        ]
        elements.extend(notes)
        
        # Build PDF
        doc.build(elements)

        


