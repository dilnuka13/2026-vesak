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
    CONSTRAINT incomes_donor_category_check CHECK (
      donor_category = ANY (
        ARRAY[
          'Main Donor'::text,
          'Normal Donor'::text,
          'Exhibition Beneficiary'::text,
          'Opening Beneficiary'::text,
          null::text
        ]
      )
    ),
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

-- 2. user_sessions policies
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

-- ==========================================
-- SECURE PUBLIC VIEWS
-- ==========================================

-- Secure view to expose only necessary fields for the custom avatar login screen
CREATE OR REPLACE VIEW public.public_users AS
SELECT id, username, avatar_url, role FROM public.app_users;

GRANT SELECT ON public.public_users TO anon, authenticated;
