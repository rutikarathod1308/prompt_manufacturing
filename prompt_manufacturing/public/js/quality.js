frappe.ui.form.on("Quality Inspection",{
    refresh:function(frm){
        frm.set_query("item_serial_no",function(){
            return{
                filters:{
                   "status":"Active",
                   "custom_qc_check":0,
                   "item_code":frm.doc.item_code
                   
                }
                
            };
        });
        frm.set_query("item_code", function (doc) {
            let doctype = doc.reference_type;
        
            // Determine the correct child doctype based on reference_type
            if (doc.reference_type !== "Job Card") {
                doctype = doc.reference_type === "Stock Entry" ? "Stock Entry Detail" : `${doc.reference_type} Item`;
            }
        
            // Apply filters if both reference_type and reference_name are provided
            if (doc.reference_type && doc.reference_name) {
                const filters = {
                    from: doctype,
                    inspection_type: doc.inspection_type,
                };
        
                if (doc.reference_type === doctype) {
                    filters["reference_name"] = doc.reference_name;
                } else {
                    filters["parent"] = doc.reference_name;
                }
        
                // Add additional custom filter
                filters["custom_inspection_required_after_grn"] = 1;
        
                return {
                    query: "prompt_manufacturing.public.py.qc.item_query",
                    filters: filters,
                };
            }
        });
        
    }
})