from reportlab.pdfgen import canvas
from reportlab.lib.colors import grey

c = canvas.Canvas("mybizmo_invoice.pdf",pagesize=(200,250),bottomup=0)

#logo section
c.translate(10,30)
# Inverting the scale for getting mirror Image of logo
c.scale(1,-1)
logo_url = "https://stg-mybizmowellness.s3.ap-south-1.amazonaws.com/media/category_icon/kl_logo.png"
c.drawImage(logo_url,0,0,width=40,height=20)
# Title Section
# Again Inverting Scale For strings insertion
c.scale(1,-1)
# Again Setting the origin back to (0,0) of top-left
c.translate(-10,-40)
# Setting the font for Name title of company
c.setFont("Helvetica-Bold",7)
# Inserting the name of the company
c.drawCentredString(100,25,"Karmaa Lab")
c.setFont("Helvetica-Bold",4)
c.drawCentredString(100,30,"Ginserv, Kodihalli, Indiranagar")
c.drawCentredString(100,35,"Bengaluru - 123456, India")

c.setFont("Courier-Bold",5)
c.drawCentredString(100,55,"ORDER-RECEIPT")

c.setFont("Times-Bold",3)
c.drawString(20,70,"RECEIPT No. : KAAR7786KL334 ")
c.drawString(20,76,"DATE : 17-09-2021")
c.drawString(20,82,"CUSTOMER NAME : Biz1User")
c.drawString(20,88,"CUSTOMER Email : biz1user@karmaalab.com")
c.drawString(20,94,"PHONE No. : +912278963467")
#c.drawRightString(175,82,"PACKAGE NAME : Yoga Package")

#lines for duration of the bill
c.drawCentredString(140, 125, "Summary for 1st Aug 2021 to 31st Aug 2021")

#lines for billing distribution
c.drawString(100, 137, "Subtotal in INR :")
c.drawRightString(175, 137, "2,500.67")
c.drawString(100, 142, "Integrated GST (18%)")
c.drawRightString(175, 142, "410.00")
c.drawString(100, 147, "Total in INR :")
c.drawRightString(175, 147, "2,910.67")

#lines for purchase item details
c.drawRightString(175,82,"PACKAGE NAME : Yoga Package")
c.drawRightString(175,87,"PACKAGE TYPE : Online Session")
c.drawRightString(175,92,"PAYMENT TYPE : Monthly")
c.drawRightString(175,97,"PAYMENT NO : 3/7")

#line for billing amount
c.setFont("Times-Bold",4)
c.drawRightString(125, 115, "Total in INR :")
c.setFont("Times-Bold",5)
c.drawRightString(175, 115, "2,910.67")
#lines above and below billing amount
c.setStrokeColor(grey)
c.line(100,105,177,105)
c.line(100,130,177,130)

c.setFont("Times-Bold",3)
c.drawString(20,200, "All the payments are received by MyBizmo Wellness Powered by karmaa Lab ")
c.drawString(20,204, "Copyright @Mybizmo_wellness")
c.linkURL("https://www.google.co.in/",(175,203,176,204) ,relative=1)

# End the Page and Start with new
c.showPage()
# Saving the PDF
c.save()