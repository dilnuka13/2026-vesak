import re
import sys

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update tailwind.config
    content = re.sub(
        r'colors:\s*\{.*?(?=borderRadius:)',
        '''colors: {
            brand: {
              400: '#4ade80',
              500: '#22c55e',
              600: '#16a34a',
            },
            m3: {
              primary: '#22c55e',
              onPrimary: '#022c15',
              primaryContainer: '#14532d',
              onPrimaryContainer: '#86efac',
              secondary: '#94a3b8',
              onSecondary: '#0f172a',
              secondaryContainer: '#1e293b',
              onSecondaryContainer: '#cbd5e1',
              tertiary: '#2dd4bf',
              onTertiary: '#042f2e',
              tertiaryContainer: '#115e59',
              onTertiaryContainer: '#5eead4',
              surface: '#020617',
              onSurface: '#f8fafc',
              surfaceContainerLowest: '#020617',
              surfaceContainerLow: '#0f172a',
              surfaceContainer: '#1e293b',
              surfaceContainerHigh: '#334155',
              surfaceContainerHighest: '#475569',
              outline: '#475569',
            }
          },
          ''',
        content,
        flags=re.DOTALL
    )

    # 2. Update CSS Variables
    content = re.sub(
        r':root\s*\{.*?(?=\})',
        ''':root {
      --m3-surface: #020617;
      --m3-on-surface: #f8fafc;
      --m3-primary: #22c55e;
      --m3-on-primary: #022c15;
      --m3-primary-container: #14532d;
      --m3-on-primary-container: #86efac;
      --m3-secondary-container: #1e293b;
      --m3-on-secondary-container: #cbd5e1;
      --m3-surface-container: #1e293b;
      --m3-surface-container-low: #0f172a;
      --m3-surface-container-high: #334155;
      --m3-surface-container-highest: #475569;
      --m3-outline: #475569;
    ''',
        content,
        flags=re.DOTALL
    )

    # 3. Update Neural-Flow Background
    content = re.sub(
        r'radial-gradient\(circle at 50% 50%, #[0-9a-fA-F]+ 0%, #[0-9a-fA-F]+ 100%\)',
        r'radial-gradient(circle at 50% 50%, #020617 0%, #000000 100%)',
        content
    )
    content = re.sub(
        r'radial-gradient\(circle at 20% 30%, rgba\(\d+, \d+, \d+, 0\.04\) 0%, transparent 40%\)',
        r'radial-gradient(circle at 20% 30%, rgba(34, 197, 94, 0.08) 0%, transparent 40%)',
        content
    )
    content = re.sub(
        r'radial-gradient\(circle at 80% 70%, rgba\(\d+, \d+, \d+, 0\.04\) 0%, transparent 40%\)',
        r'radial-gradient(circle at 80% 70%, rgba(45, 212, 191, 0.05) 0%, transparent 40%)',
        content
    )
    content = re.sub(
        r'radial-gradient\(circle at 50% 20%, rgba\(\d+, \d+, \d+, 0\.04\) 0%, transparent 40%\)',
        r'radial-gradient(circle at 50% 20%, rgba(59, 130, 246, 0.03) 0%, transparent 40%)',
        content
    )

    # 4. Update Glassmorphism
    content = re.sub(
        r'background: rgba\(\d+, \d+, \d+, 0\.[6-7]\d*\);',
        r'background: rgba(2, 6, 23, 0.7);',
        content
    )

    # 5. Update M3 Buttons CSS
    content = re.sub(
        r'\.m3-button-filled:hover \{.*?\}',
        r'.m3-button-filled:hover { box-shadow: 0 4px 12px rgba(34,197,94,0.3); background: #4ade80; transform: scale(1.02); }',
        content,
        flags=re.DOTALL
    )
    content = re.sub(
        r'\.m3-button-tonal:hover \{.*?\}',
        r'.m3-button-tonal:hover { background: var(--m3-surface-container-highest); transform: scale(1.02); }',
        content,
        flags=re.DOTALL
    )
    
    if '.m3-button-outlined' not in content:
        content = content.replace(
            '.m3-button-tonal { background: var(--m3-secondary-container); color: var(--m3-on-secondary-container); }',
            '''.m3-button-tonal { background: var(--m3-secondary-container); color: var(--m3-on-secondary-container); }
    .m3-button-elevated { background: var(--m3-surface-container-low); color: var(--m3-primary); box-shadow: 0 1px 3px rgba(0,0,0,0.3); }
    .m3-button-elevated:hover { background: var(--m3-surface-container-high); box-shadow: 0 4px 12px rgba(34,197,94,0.2); transform: scale(1.02); }
    .m3-button-outlined { background: transparent; border: 1px solid var(--m3-outline); color: var(--m3-primary); }
    .m3-button-outlined:hover { background: rgba(34, 197, 94, 0.08); border-color: var(--m3-primary); transform: scale(1.02); }'''
        )

    # 6. Replace Luminous Effect to Green
    content = re.sub(
        r'rgba\(168, 199, 255, 0\.4\)',
        r'rgba(34, 197, 94, 0.4)',
        content
    )

    if '.magnetic-button' not in content:
        content = content.replace(
            '/* Custom Scrollbar */',
            '''/* Magnetic Button Effect */
    .magnetic-button { transition: transform 0.3s cubic-bezier(0.05, 0.7, 0.1, 1.0); }
    .magnetic-button:hover { transform: scale(1.05) translateY(-2px); }
    
    /* Custom Scrollbar */'''
        )

    content = re.sub(
        r'bg-brand-500/10 blur-\[150px\]',
        r'bg-green-500/10 blur-[150px]',
        content
    )
    content = re.sub(
        r'bg-blue-500/10 blur-\[150px\]',
        r'bg-emerald-500/10 blur-[150px]',
        content
    )
    
    # 9. Generic class replacements in JSX 
    # Use magnetic buttons for key buttons
    content = re.sub(
        r'className="([^"]*bg-brand-600[^"]*hover:bg-brand-500[^"]*)"',
        r'className="\1 m3-button m3-button-filled magnetic-button"',
        content
    )
    content = re.sub(
        r'className="([^"]*bg-slate-800[^"]*hover:bg-slate-700[^"]*)"',
        r'className="\1 m3-button m3-button-tonal"',
        content
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

process_file('index.html')
process_file('admin.html')
print('Updated basic theme colors and definitions.')
