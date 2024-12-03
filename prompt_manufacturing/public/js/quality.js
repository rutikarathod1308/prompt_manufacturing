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
    }
})