from mmap import PAGESIZE
from matplotlib.pyplot import style
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from datetime import date
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


########## required data ##########
logo = "https://stg-mybizmowellness.s3.ap-south-1.amazonaws.com/media/category_icon/kl_logo.png"

invoice = [
    ['#', 'Treatment', 'Cost(in INR)', 'Quantity', 'Tax', 'Total (in INR)'],
    ['1.', 'Crown Fixing', '5300', '1', '636', '5936']
]

today = date.today()
d = str(today)

########## pdf format ##########

###### header ######
pdf = canvas.Canvas("sample.pdf",pagesize=(200, 250), bottomup=0)
pdf.drawImage(logo, 13, 5, width=35, height=20)
pdf.setTitle('Appointment')
pdf.setFont("Helvetica-Bold",9)
pdf.drawCentredString(100, 15, "MyBizmo Wellness")
pdf.setFillColor(colors.grey)
pdf.setFont("Helvetica",5)
pdf.drawString(150, 25, "Date: " + d)
pdf.setFont("Helvetica",3)
pdf.drawString(15, 35, "12 M.G Road, HAL Layout, Bangalore, Karnataka, India-560001")
pdf.drawString(15, 41, "https://biz1.stgwellnessuser.mybizmo.com/")
pdf.drawString(131, 35, "Appointment Time: 5:00 PM to 6:00 PM")
pdf.drawString(150, 41, "Phone: +91-9871234756")
pdf.setStrokeColor(colors.grey)
pdf.setLineWidth(0.5)
pdf.line(10, 46, 190, 46)

###### Patient details ######
pdf.setFillColor(colors.black)
pdf.setFont("Helvetica",6)
pdf.drawString(12, 53, "Personal Details")
pdf.setFont("Helvetica",5)
pdf.setFillColor(colors.grey)
pdf.drawString(12, 62, "Name: Test User")
pdf.drawString(12, 69, "Id: Biz01")
pdf.drawString(12, 76, "Email: example@domain.com")
pdf.drawString(12, 83, "Medical History: Allergies")
pdf.drawString(92, 62, "Blood Group: AB-")
pdf.drawString(92, 69, "Gender: M/F/Custom")
pdf.setStrokeColor(colors.grey)
pdf.setLineWidth(0.5)
pdf.line(10, 88, 190, 88)

###### Invoice ######
pdf.setFillColor(colors.black)
pdf.setFont("Helvetica",6)
pdf.drawString(12, 95, "Invoice")
pdf.drawCentredString(150, 95, "Invoice Number: MBW")

pdf.setStrokeColor(colors.grey)
pdf.setLineWidth(0.5)
pdf.line(10, 188, 190, 188)

###### Table ######
t = SimpleDocTemplate("sample1.pdf", PAGESIZE=(200,250))
table = Table(invoice)
table_style = TableStyle([
    ('BACKGROUND',(0,0),(-1,0),colors.grey),
    ('ALIGN', (0,0), (-1,-1), 'CENTER')
    ])
table.setStyle(table_style)
elms = []
elms.append(table)
t.build(elms)


########## save pdf ##########
pdf.save()