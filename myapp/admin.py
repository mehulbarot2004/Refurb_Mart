from django.contrib import admin
from .models import *
# Register your models here.


from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


def export_to_pdf(modeladmin, request, queryset):
   # Create a new PDF
   response = HttpResponse(content_type='application/pdf')
   response['Content-Disposition'] = 'attachment; filename="report.pdf"'

   # Generate the report using ReportLab
   doc = SimpleDocTemplate(response, pagesize=letter)

   elements = []

   # Define the style for the table
   style = TableStyle([
       ('BACKGROUND', (0,0), (-1,0), colors.grey),
       ('TEXTCOLOR', (0,0), (-1,0), colors.black),
       ('ALIGN', (0,0), (-1,-1), 'CENTER'),
       ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
       ('FONTSIZE', (0,0), (-1,0), 10),
       ('BOTTOMPADDING', (0,0), (-1,0), 12),
       ('BACKGROUND', (0,1), (-1,-1), colors.white),
       ('GRID', (0,0), (-1,-1), 1, colors.black),
   ])

   # Create the table headers
   headers = ["id", "name","finaltotal", "phone", "paymode","timestamp","status"]

   # Create the table data
   data = []
   for obj in queryset:
       data.append([obj.id, obj.userid, obj.finaltotal,obj.phone,obj.paymode,obj.timestamp,obj.status])

   # Create the table
   t = Table([headers] + data, style=style)

   # Add the table to the elements array
   elements.append(t)

   # Build the PDF document
   doc.build(elements)

   return response

export_to_pdf.short_description = "Export to PDF"

class showregister(admin.ModelAdmin):
    list_display = ["id","name", "email", "password","phone"]


admin.site.register(registermodel, showregister)
class showcategory(admin.ModelAdmin):
    list_display = ["id", "catname"]


admin.site.register(category, showcategory)


class adddata(admin.ModelAdmin):
    list_display = ["id", "name", "price", "category", "description","userid","admin_photos", "status"]


admin.site.register(newproductmodel, adddata)

class order(admin.ModelAdmin):
    list_display = ["id", "finaltotal", "phone", "address", "paymode","timestamp","status", "razorpay_order_id"]
    list_filter = ['timestamp']
    actions = [export_to_pdf]


admin.site.register(ordermodel, order)

class cartt(admin.ModelAdmin):
    list_display = ["id","userid","productid","rproductid","quantity","totalamount","orderstatus","orderid"]

admin.site.register(cart,cartt)

class refurdata(admin.ModelAdmin):
    list_display = ["id", "name", "price", "category", "description","admin_photos", "status"]

admin.site.register(refurbishedproductmodel,refurdata)

class contact(admin.ModelAdmin):
    list_display = ["id","userid", "name", "email", "message", "subject"]

admin.site.register(contact_us,contact)