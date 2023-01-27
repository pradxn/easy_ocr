from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
#from reportlab.platypus import Table

###### Registering different fonts ######
pdfmetrics.registerFont(TTFont('Tahoma', 'Tahoma.ttf'))
pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
pdfmetrics.registerFont(TTFont('VeraIt', 'VeraIt.ttf'))
pdfmetrics.registerFont(TTFont('VeraBI', 'VeraBI.ttf'))

###### set a margin of 10 from top and 25 to left & right ######
###### function to display co-ordinates of pdf ######
def ruler(pdf):
    pdf.drawString(25,10, 'A')
    pdf.drawString(50,10, 'B')
    pdf.drawString(75,10, 'C')
    pdf.drawString(100,10, 'D')
    pdf.drawString(125,10, 'E')
    pdf.drawString(150,10, 'F')
    pdf.drawString(175,10, 'G')

    pdf.drawString(10,25,'1')
    pdf.drawString(10,50,'2')
    pdf.drawString(10,75,'3')
    pdf.drawString(10,100,'4')
    pdf.drawString(10,125,'5')
    pdf.drawString(10,150,'6')
    pdf.drawString(10,175,'7')
    pdf.drawString(10,200,'8')
    pdf.drawString(10,225,'9')

logo = 'https://stg-mybizmowellness.s3.ap-south-1.amazonaws.com/media/category_icon/kl_logo.png'

Tdata = [
    ['dedicated hosting', 'VPS Hosting', 'Sharing', 'Reselling Hosting'],
    ['$200/m', '$100/m', '$200/m', '$50/m'],
    ['Free Domain','Free Domain','Free Domain','Free Domain'],
    ['2GB DDR', '20GB Disk Space', 'Unlimited Email','Unlimited Email']
]


###### setting canvas name and size, title and font ######
pdf = canvas.Canvas("test.pdf",pagesize=(200,250),bottomup=0)
pdf.drawImage(logo, 83, 5, width=40, height=20)
###### available fonts ######
for font in pdf.getAvailableFonts():
    print(font)

pdf.setTitle('Appointment-id: ')
ruler(pdf)
pdf.setFont('Helvetica', 12)

#pdf = SimpleDocTemplate("test.pdf")
table = Table(Tdata)
style = TableStyle([
    ('BACKGROUND',(0,0),(3,0),colors.gray),
    ('BACKGROUND',(0,0),(3,0),colors.gray),
    ('ALIGN',(0,0),(-1,-1),'CENTER')
    ])

table.setStyle(style)
elms = []
elms.append(table)
#pdf.build(elms)

#pdf.drawString(92.5,25,'Title')



######saving the pdf######
pdf.save()