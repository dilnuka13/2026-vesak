import re
import sys

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix admin.html mobile navigation
    if 'admin.html' in filepath:
        # Remove the <select> dropdown for mobile
        content = re.sub(
            r'\{/\*\s*Mobile Dropdown\s*\*/\}.*?\{/\*\s*Desktop Choice Chips\s*\*/\}',
            '{/* Desktop Choice Chips */}',
            content,
            flags=re.DOTALL
        )

        # Ensure activeTab maps to icons
        # Add the bottom navigation right before the closing div of the flex container that holds aside and main
        # We need to find the </main> and add the footer
        bottom_nav_code = '''
             <footer className="lg:hidden fixed bottom-0 left-0 right-0 glass-m3 border-t border-white/5 z-50 flex justify-between items-center px-2 pt-3 pb-[max(env(safe-area-inset-bottom),_1rem)] overflow-x-auto no-scrollbar">
                {[
                  { id: 'incomes', icon: 'payments', label: 'Incomes' },
                  { id: 'expenses', icon: 'account_balance_wallet', label: 'Expenses' },
                  { id: 'users', icon: 'group', label: 'Users' },
                  { id: 'project_settings', icon: 'settings', label: 'Settings' }
                ].map(item => (
                  <button 
                    key={item.id}
                    onClick={() => setActiveTab(item.id)}
                    className={`flex flex-col items-center gap-1 min-w-[70px] py-1 transition-all duration-300 ${activeTab === item.id ? 'text-m3-primary' : 'text-m3-outline'}`}
                  >
                    <div className={`w-12 h-8 rounded-full flex items-center justify-center transition-all ${activeTab === item.id ? 'bg-m3-secondaryContainer text-m3-onSecondaryContainer' : ''}`}>
                      <MaterialIcon name={item.icon} className={activeTab === item.id ? 'FILL' : ''} />
                    </div>
                    <span className="text-[10px] font-bold tracking-wider">{item.label}</span>
                  </button>
                ))}
             </footer>
        '''
        
        # Replace the </main> tag with </main> + bottom_nav_code
        content = content.replace('</main>', '</main>' + bottom_nav_code)

    # 2. Refactor Action Buttons to M3 styles
    # Find commonly styled buttons and replace them
    # "px-4 py-2 bg-indigo-600 hover:bg-indigo-500 ..." -> "m3-button m3-button-filled magnetic-button"
    content = re.sub(
        r'className="[^"]*?bg-indigo-600[^"]*?hover:bg-indigo-500[^"]*?"',
        r'className="m3-button m3-button-filled magnetic-button w-full sm:w-auto shadow-[0_0_15px_rgba(34,197,94,0.3)]"',
        content
    )
    
    # "px-3 py-2 bg-slate-800 hover:bg-slate-700 ..." -> "m3-button m3-button-tonal"
    content = re.sub(
        r'className="[^"]*?bg-slate-800[^"]*?hover:bg-slate-700[^"]*?border-slate-700[^"]*?"',
        r'className="m3-button m3-button-tonal flex-1"',
        content
    )

    # "px-3 py-2 bg-red-600/20 text-red-400 ..." -> "m3-button m3-button-tonal text-red-400"
    content = re.sub(
        r'className="[^"]*?bg-red-600/20[^"]*?text-red-400[^"]*?"',
        r'className="m3-button m3-button-tonal !text-red-400 !bg-red-500/10 hover:!bg-red-500/20 flex-1 border border-red-500/20"',
        content
    )
    
    # Save forms buttons
    # "flex-1 py-3 bg-slate-800 hover:bg-slate-700 rounded-lg text-white font-bold transition" -> "m3-button m3-button-tonal flex-1 h-12"
    content = content.replace(
        'flex-1 py-3 bg-slate-800 hover:bg-slate-700 rounded-lg text-white font-bold transition',
        'm3-button m3-button-tonal flex-1 h-12'
    )
    # "flex-1 bg-brand-600 hover:bg-brand-500 text-white font-bold py-3 rounded-lg transition disabled:opacity-50" -> "m3-button m3-button-filled magnetic-button flex-1 h-12 disabled:opacity-50"
    content = content.replace(
        'flex-1 bg-brand-600 hover:bg-brand-500 text-white font-bold py-3 rounded-lg transition disabled:opacity-50',
        'm3-button m3-button-filled magnetic-button flex-1 h-12 disabled:opacity-50'
    )
    # "flex-1 bg-red-600 hover:bg-red-500 text-white font-bold py-3 rounded-lg transition disabled:opacity-50" -> "m3-button m3-button-filled !bg-red-600 hover:!bg-red-500 magnetic-button flex-1 h-12 disabled:opacity-50"
    content = content.replace(
        'flex-1 bg-red-600 hover:bg-red-500 text-white font-bold py-3 rounded-lg transition disabled:opacity-50',
        'm3-button m3-button-filled !bg-red-600 hover:!bg-red-500 !text-white magnetic-button flex-1 h-12 disabled:opacity-50'
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

update_file('index.html')
update_file('admin.html')
print("Applied M3 buttons and mobile navigation structure.")
