# System Planning: Vesak & Poson Web Portal

මෙම ලිපිගොනුව මඟින් නව වෙසක් සහ පොසොන් මූල්‍ය කළමනාකරණ හා පොදු ද්වාර පද්ධතිය (Vesak & Poson Financial Management & Public Portal) සාදාගත යුතු ආකාරය සහ එහි ව්‍යුහය පිළිබඳ සම්පූර්ණ සැලසුම (System Planning) දක්වයි.

---

## 1. ව්‍යාපෘති දර්ශනය සහ මූලික අවශ්‍යතා (Project Overview & Requirements)

මෙම පද්ධතිය ප්‍රධාන වශයෙන් කොටස් දෙකකට බෙදා ඇත:
1. **පරිපාලන අංශය (Admin Dashboard)**: මූල්‍ය තොරතුරු ඇතුළත් කිරීම, සංඛ්‍යාලේඛන ප්‍රස්ථාර බැලීම, PDF/CSV වාර්තා ලබාගැනීම, පරිශීලකයින් සහ සෙෂන්ස් පාලනය.
2. **පොදු අංශය (Public Portal)**: දායකයින්ට තමන්ගේ දායකත්ව සෙවීමේ හැකියාව, Canvas මඟින් උත්පාදනය වන නිල PDF රිසිට්පත් බාගත කිරීම සහ ත්‍රිමාණ සජීවී ආරාධනා පත්‍ර බැලීම.

---

## 2. ෆෝල්ඩර් සහ ලිපිගොනු ව්‍යුහය (Folder & File Structure)

නව පද්ධතිය සෑදීමේදී පහත ලිපිගොනු ව්‍යුහය භාවිත කළ යුතුය:

```text
/ (Root Directory - Vesak System)
├── logo.png                  # වෙසක් පද්ධති ලාංඡනය (Green branding)
├── ve1rify.png               # රිසිට්පතෙහි සත්‍යාපන මුද්‍රාව (Verification Stamp)
├── dc.png                    # රිසිට්පතේ කොන් හැඩගැන්වීමට ගන්නා ධර්ම චක්‍රය (Wheel)
├── favicon.svg               # වෙබ් අඩවියේ අයිකනය
├── index.html                # වෙසක් ප්‍රධාන පිවිසුම් පිටුව (Landing Page + 3D Background)
├── admin.html                # වෙසක් සහ පොසොන් පරිපාලන පාලකය (React + Tailwind UMD)
├── view_income.html          # වෙසක් ආදායම් සෙවුම සහ රිසිට්පත් බාගත කිරීමේ පිටුව
├── invitation.html           # වෙසක් ඩිජිටල් ආරාධනා පත්‍රය (Countdown + Map + Gallery)
├── maintenance.html          # පද්ධති නඩත්තු පිටුව (Disabled state screen)
├── offline.html              # Offline පිටුව
├── manifest.json             # PWA Manifest
│
└── /poson (Poson Directory - පොසොන් පද්ධතිය)
    ├── index.html            # පොසොන් ප්‍රධාන පිවිසුම් පිටුව (Amber/Gold branding)
    ├── view_income.html      # පොසොන් ආදායම් සෙවුම සහ රිසිට්පත් පිටුව
    ├── maintenance.html      # පොසොන් නඩත්තු පිටුව
    ├── offline.html          # පොසොන් Offline පිටුව
    └── manifest.json         # පොසොන් PWA Manifest
```

---

## 3. දත්ත ගබඩා සැලසුම (Database Schema Planning)

පද්ධතිය Supabase (PostgreSQL) සමඟ සම්බන්ධ වන අතර පහත දැක්වෙන වගු (Tables) නිර්මාණය කළ යුතුය:

### SQL Create Table Commands:

```sql
-- 1. App Users Table
CREATE TABLE public.app_users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user', -- 'admin' or 'user'
    is_temp_password BOOLEAN DEFAULT true,
    phone_number TEXT,
    address TEXT,
    is_contributor BOOLEAN DEFAULT false,
    two_factor_enabled BOOLEAN DEFAULT false,
    fcm_token TEXT,
    avatar_url TEXT,
    passkey_id TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. User Sessions Table
CREATE TABLE public.user_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES public.app_users(id) ON DELETE CASCADE,
    session_token TEXT UNIQUE NOT NULL,
    device_name TEXT,
    location TEXT,
    ip_address TEXT,
    last_active TIMESTAMPTZ DEFAULT NOW(),
    is_online BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Project Settings Table
CREATE TABLE public.project_settings (
    id TEXT PRIMARY KEY DEFAULT 'global',
    allow_income_entry BOOLEAN DEFAULT true,
    allow_expense_entry BOOLEAN DEFAULT true,
    allow_pledge_entry BOOLEAN DEFAULT true,
    income_access_list TEXT DEFAULT '',
    expense_access_list TEXT DEFAULT '',
    pledge_access_list TEXT DEFAULT ''
);

-- 4. Incomes Table
CREATE TABLE public.incomes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    date DATE NOT NULL,
    name TEXT NOT NULL,
    phone_number TEXT,
    address TEXT,
    donation_type TEXT NOT NULL, -- 'Cash' or 'Goods'
    amount NUMERIC,
    donor_category TEXT, -- 'Main Donor', 'Regular Donor'
    item_description TEXT,
    quantity TEXT,
    status TEXT NOT NULL, -- 'Received Today', 'Promised'
    reported_by TEXT,
    description TEXT,
    event_type TEXT DEFAULT 'vesak', -- 'vesak' or 'poson'
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. Expenses Table
CREATE TABLE public.expenses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    reason TEXT NOT NULL,
    withdrawer_name TEXT NOT NULL,
    date DATE NOT NULL,
    time TIME NOT NULL,
    amount_taken NUMERIC NOT NULL,
    receipt_url TEXT,
    reported_by TEXT,
    event_type TEXT DEFAULT 'vesak', -- 'vesak' or 'poson'
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 6. Festival Invitations (Vesak & Poson)
CREATE TABLE public.vesak_invitation (
    id INT PRIMARY KEY DEFAULT 1,
    anniversary TEXT DEFAULT '1',
    description TEXT,
    members TEXT,
    map_link TEXT,
    dates TEXT DEFAULT '[]', -- JSON String array e.g., '["2026-05-30"]'
    time_start TEXT DEFAULT '18:30',
    time_end TEXT DEFAULT '02:00',
    gallery_links TEXT DEFAULT '[]', -- JSON string
    is_published BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE public.poson_invitation (
    LIKE public.vesak_invitation INCLUDING ALL
);

-- 7. Notifications Table
CREATE TABLE public.notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    record_id UUID,
    type TEXT,
    message TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 8. User Passkeys Table
CREATE TABLE public.user_passkeys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES public.app_users(id) ON DELETE CASCADE,
    passkey_id TEXT NOT NULL,
    passkey_name TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ==========================================
-- ROW LEVEL SECURITY (RLS) POLICIES
-- ==========================================

-- Enable RLS on all tables
ALTER TABLE public.app_users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.project_settings ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.incomes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.expenses ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.vesak_invitation ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.poson_invitation ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.notifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_passkeys ENABLE ROW LEVEL SECURITY;

-- 1. app_users policies
CREATE POLICY "Admins can do everything on app_users" ON public.app_users FOR ALL TO authenticated USING (EXISTS (SELECT 1 FROM public.app_users WHERE id = auth.uid() AND role = 'admin'));
CREATE POLICY "Users can view their own profile" ON public.app_users FOR SELECT TO authenticated USING (auth.uid() = id);

-- 2. user_sessions policies (Matches setup_sessions.sql)
CREATE POLICY "Users can view their own sessions or admins can view all" ON public.user_sessions FOR SELECT TO authenticated USING (auth.uid() = user_id OR EXISTS (SELECT 1 FROM public.app_users WHERE id = auth.uid() AND role = 'admin'));
CREATE POLICY "Users can insert their own sessions" ON public.user_sessions FOR INSERT TO authenticated WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update their own sessions" ON public.user_sessions FOR UPDATE TO authenticated USING (auth.uid() = user_id);
CREATE POLICY "Users can delete their own sessions or admins can delete all" ON public.user_sessions FOR DELETE TO authenticated USING (auth.uid() = user_id OR EXISTS (SELECT 1 FROM public.app_users WHERE id = auth.uid() AND role = 'admin'));

-- 3. project_settings policies
CREATE POLICY "Public can view project settings" ON public.project_settings FOR SELECT TO anon, authenticated USING (true);
CREATE POLICY "Admins can update project settings" ON public.project_settings FOR ALL TO authenticated USING (EXISTS (SELECT 1 FROM public.app_users WHERE id = auth.uid() AND role = 'admin'));

-- 4. incomes policies
CREATE POLICY "Public can view incomes" ON public.incomes FOR SELECT TO anon, authenticated USING (true);
CREATE POLICY "Admins can modify incomes" ON public.incomes FOR ALL TO authenticated USING (EXISTS (SELECT 1 FROM public.app_users WHERE id = auth.uid() AND role = 'admin'));

-- 5. expenses policies
CREATE POLICY "Admins can manage expenses" ON public.expenses FOR ALL TO authenticated USING (EXISTS (SELECT 1 FROM public.app_users WHERE id = auth.uid() AND role = 'admin'));

-- 6. vesak_invitation & poson_invitation policies
CREATE POLICY "Public can view vesak_invitation" ON public.vesak_invitation FOR SELECT TO anon, authenticated USING (true);
CREATE POLICY "Admins can manage vesak_invitation" ON public.vesak_invitation FOR ALL TO authenticated USING (EXISTS (SELECT 1 FROM public.app_users WHERE id = auth.uid() AND role = 'admin'));
CREATE POLICY "Public can view poson_invitation" ON public.poson_invitation FOR SELECT TO anon, authenticated USING (true);
CREATE POLICY "Admins can manage poson_invitation" ON public.poson_invitation FOR ALL TO authenticated USING (EXISTS (SELECT 1 FROM public.app_users WHERE id = auth.uid() AND role = 'admin'));

-- 7. notifications policies
CREATE POLICY "Admins can manage notifications" ON public.notifications FOR ALL TO authenticated USING (EXISTS (SELECT 1 FROM public.app_users WHERE id = auth.uid() AND role = 'admin'));

-- 8. user_passkeys policies
CREATE POLICY "Users can manage their own passkeys" ON public.user_passkeys FOR ALL TO authenticated USING (auth.uid() = user_id);
```
```

---

## 4. සැලසුම් ක්‍රමවේදය (UI/UX Design System)

- **Default Dark Mode**: පසුබිම ලෙස `#020617` භාවිතා කරයි.
- **Glassmorphism**: සියලුම කාඩ්පත් සහ සංරචක සඳහා `rgba(15, 23, 42, 0.4)` පසුබිම සහ `backdrop-filter: blur(16px)` යොදා ගනී.
- **Micro-animations**: අලංකාර staggered reveal animations සහ Hover effects.
- **වර්ණ මාලාවන්**:
  - **වෙසක් (Vesak)**: කොළ පැහැති තේමාව (brand color: `#22c55e`, emerald shades).
  - **පොසොන් (Poson)**: රන්වන්/තැඹිලි පැහැති තේමාව (brand color: `#f59e0b`, amber/gold shades).

---

## 5. ක්‍රියාත්මක කිරීමේ පියවර (Step-by-Step Implementation Guide)

1. **Supabase ව්‍යාපෘතියක් සකසා ගැනීම**:
   - Supabase තුළ නව Database එකක් සාදා ඉහත දක්වා ඇති SQL කේත ක්‍රියාත්මක කරන්න.
   - Storage කොටසෙහි `receipts` සහ `gallery_images` නමින් public buckets දෙකක් සාදන්න.
   - RLS (Row Level Security) ප්‍රතිපත්ති සකසන්න.

2. **Admin Panel එක නිපදවීම (`admin.html`)**:
   - React UMD ලෝඩර් සහ Tailwind CDN භාවිත කරමින් සම්පූර්ණ Dashboard එක සාදන්න.
   - Incomes, Expenses ඇතුළත් කිරීම් සහ වෙනස් කිරීම් Supabase SQL වගු වෙත යොමු කරන්න.
   - සජීවී ප්‍රස්ථාර සඳහා SVG හෝ Recharts (UMD) සම්බන්ධ කරන්න.

3. **පොදු පෝටලය සෑදීම (`view_income.html`)**:
   - පරිශීලකයින්ට දුරකථන අංකයෙන් සෙවීමට Input field එකක් සකසන්න.
   - HTML5 Canvas මඟින් `logo.png`, `dc.png`, සහ `ve1rify.png` අනුරූප (images) යොදාගනිමින් PDF රිසිට්පත ඇඳ එය බාගත කර ගැනීමට jsPDF සබැඳි කරන්න.

4. **ආරාධනා පත්‍ර පිටුව සෑදීම (`invitation.html`)**:
   - දින 30 කවුන්ටරය සඳහා රවුම් ආකාරයේ SVG ධාවකයක් (circular progress bar) සාදා JavaScript මඟින් ඉතිරි දින ගණන ගණනය කර පෙන්වන්න.
   - Google Map එක iframe මඟින් embed කරන්න.

5. **පොසොන් පද්ධතිය සෑදීම (`/poson/`)**:
   - වෙසක් සඳහා සාදන ලද ගොනු `/poson` ෆෝල්ඩරය වෙත පිටපත් කරන්න.
   - HTML ගොනුවල ඇති CSS විචල්‍යයන් (variables) පොසොන් රන්වන් වර්ණවලට (`#f59e0b`) වෙනස් කරන්න.
   - දත්ත සමුදා විමසුම් (Supabase queries) වල `event_type` එක `'poson'` ලෙස යොමු කරන්න.

---

## 6. Supabase Connection Credentials

වත්මන් පද්ධතිය සාර්ථකව සම්බන්ධ කිරීම සඳහා පහත සබැඳි සහ යතුරු භාවිතා කරන්න:
- **Supabase URL**: `https://yqpkgybmjdovdnmekpnw.supabase.co`
- **Supabase Anon Key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlxcGtneWJtamRvdmRubWVrcG53Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY1MjUwMjAsImV4cCI6MjA5MjEwMTAyMH0.7C9jv1_zDRxSMCgs0tWfiNUGXGOkCLz5RE0CCDoc_yA`

