# UTILITY TO BUILD THE EMAIL PDF IN MEMORY

import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from Galleries.models import Events


def generate_ticket_pdf(ticket):
    
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
  
    # draw a title
    p.setFont("Helvetica-Bold", 12)
    p.drawCentredString(width/2, height - 100, "Your Event Ticket")
     
    # draw event info.
    p.setFont("Helvetica", 14)
    p.drawString(100, height - 150, f"Event : {ticket.event.event_title}")
    p.drawString(100, height - 170, f"Date : {ticket.event.date_of_event}")
    p.drawString(100, height - 190, f"Venue : {ticket.event.venue}")
    
    # draw attendee info
    p.drawString(100, height - 230, f"Name : {ticket.user.first_name}")
    p.drawString(100, height - 250, f"Email : {ticket.user.email}")
    p.drawString(100, height - 270, f"Phone : {ticket.user.phone_number}")
    
    p.showPage()
    p.save() 
    
    buffer.seek(0)
    return buffer  #file-like object containing the pdf
    
    