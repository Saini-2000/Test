import frappe
from frappe.utils import getdate

def execute(filters=None):
  
    if not filters:
        filters = {}

   
    columns = [
        {"fieldname": "month_name", "label": "Month", "fieldtype": "Data", "width": 120},
        {"fieldname": "total_qty_i", "label": "Total Qty .I", "fieldtype": "Float", "width": 120},
        {"fieldname": "total_qty_v", "label": "Total Qty .V", "fieldtype": "Float", "width": 120},
        {"fieldname": "total_amount_i", "label": "Total Amount .I", "fieldtype": "Currency", "width": 120},
        {"fieldname": "total_amount_v", "label": "Total Amount .V", "fieldtype": "Currency", "width": 120},
    ]

    data = []

    from_date = getdate(filters.get("from_date"))
    to_date = getdate(filters.get("to_date"))

  
    monthly_totals = {}

    records = frappe.get_all(
        'Serial and Batch Bundle', 
        filters={"posting_date": ["between", [from_date, to_date]],"voucher_type":"Delivery Note"}, 
        fields=['name', 'posting_date']
    )

    for record in records:
        total_qty_i = 0
        total_qty_v = 0
        total_amount_i = 0
        total_amount_v = 0

     
        posting_date = getdate(record.posting_date)
        month_name = posting_date.strftime("%B %Y")  

      
        child_entries = frappe.get_all(
            'Serial and Batch Entry', 
            filters={'parent': record.name}, 
            fields=['serial_no', 'qty', 'stock_value_difference']
        )

   
        for entry in child_entries:
            serial_no = entry.serial_no
            if serial_no:  
                if ".I" in serial_no:
                    total_qty_i += entry.qty
                    total_amount_i += entry.stock_value_difference
                elif ".V" in serial_no:
                    total_qty_v += entry.qty
                    total_amount_v += entry.stock_value_difference


        if month_name not in monthly_totals:
            monthly_totals[month_name] = {
                "total_qty_i": 0,
                "total_qty_v": 0,
                "total_amount_i": 0,
                "total_amount_v": 0
            }
        
        monthly_totals[month_name]["total_qty_i"] += abs(total_qty_i)
        monthly_totals[month_name]["total_qty_v"] += abs(total_qty_v)
        monthly_totals[month_name]["total_amount_i"] += abs(total_amount_i)
        monthly_totals[month_name]["total_amount_v"] += abs(total_amount_v)

    sorted_months = sorted(monthly_totals.keys(), key=lambda x: getdate("01 " + x))

    for month in sorted_months:
        totals = monthly_totals[month]
        data.append({
            "month_name": month,
            "total_qty_i": totals["total_qty_i"],
            "total_qty_v": totals["total_qty_v"],
            "total_amount_i": totals["total_amount_i"],
            "total_amount_v": totals["total_amount_v"],
        })

    return columns, data
