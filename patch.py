import re

def apply_fixes(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix Pledges tab on mobile
    content = content.replace(
        "{ id: 'expense-page', icon: 'account_balance_wallet', label: 'Expense' },\n                  { id: 'profile', icon: 'person', label: 'Profile' }",
        "{ id: 'expense-page', icon: 'account_balance_wallet', label: 'Expense' },\n                  { id: 'pledges', icon: 'history', label: 'Pledges' },\n                  { id: 'profile', icon: 'person', label: 'Profile' }"
    )

    # 2. Extract downloadReceipt function to duplicate for PDF
    func_start = content.find("const downloadReceipt = (donation) => {")
    func_end = content.find("};\n\n    // --- COMPONENTS ---") + 2
    if func_start != -1 and func_end != -1:
        orig_func = content[func_start:func_end]
        
        pdf_func = orig_func.replace("const downloadReceipt = (donation) => {", "const downloadPDFReceipt = (donation) => {")
        pdf_func = pdf_func.replace(
            "const a = document.createElement('a');\n        a.href = dataUrl;\n        a.download = `Vesak_Receipt_${donation.name?.replace(/\\s+/g, '_') || 'Donor'}_${donation.date}.png`;\n        a.click();",
            """const { jsPDF } = window.jspdf;
        const pdf = new jsPDF({ orientation: 'portrait', unit: 'px', format: [width, height] });
        pdf.addImage(dataUrl, 'PNG', 0, 0, width, height);
        pdf.save(`Vesak_Receipt_${donation.name?.replace(/\\s+/g, '_') || 'Donor'}_${donation.date}.pdf`);"""
        )
        
        content = content[:func_end] + "\n\n    " + pdf_func + content[func_end:]

    # 3. Add PDF button next to downloadReceipt button
    old_btn = r'<button onClick={\(\) => downloadReceipt\(p\)} className="(.*?)">\s*<MaterialIcon name="receipt_long" />\s*Receipt\s*</button>'
    new_btn = r'''<div className="flex gap-2">
                            <button onClick={() => downloadReceipt(p)} className="\1">
                              <MaterialIcon name="image" /> PNG
                            </button>
                            <button onClick={() => downloadPDFReceipt(p)} className="\1 text-red-400 border-red-500/50 hover:bg-red-500/30">
                              <MaterialIcon name="picture_as_pdf" /> PDF
                            </button>
                          </div>'''
    
    content = re.sub(old_btn, new_btn, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

apply_fixes('index.html')
print("Fixes applied.")
