-- Create the user_sessions table
CREATE TABLE IF NOT EXISTS public.user_sessions (
    id UUID DEFAULT extensions.uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.app_users(id) ON DELETE CASCADE,
    session_token TEXT UNIQUE NOT NULL,
    device_name TEXT,
    location TEXT,
    ip_address TEXT,
    last_active TIMESTAMPTZ DEFAULT NOW(),
    is_online BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Set up Row Level Security (RLS)
ALTER TABLE public.user_sessions ENABLE ROW LEVEL SECURITY;

-- Allow users to read their own sessions, and admins to read all
CREATE POLICY "Users can view their own sessions" 
ON public.user_sessions FOR SELECT 
USING (
  auth.uid() = user_id OR 
  EXISTS (SELECT 1 FROM public.app_users WHERE id = auth.uid() AND role = 'admin')
);

-- Allow users to insert their own sessions
CREATE POLICY "Users can insert their own sessions" 
ON public.user_sessions FOR INSERT 
WITH CHECK (auth.uid() = user_id);

-- Allow users to update their own sessions
CREATE POLICY "Users can update their own sessions" 
ON public.user_sessions FOR UPDATE 
USING (auth.uid() = user_id);

-- Allow users to delete their own sessions, and admins to delete all
CREATE POLICY "Users can delete their own sessions" 
ON public.user_sessions FOR DELETE 
USING (
  auth.uid() = user_id OR 
  EXISTS (SELECT 1 FROM public.app_users WHERE id = auth.uid() AND role = 'admin')
);

-- Create an index for faster lookups
CREATE INDEX IF NOT EXISTS idx_user_sessions_user_id ON public.user_sessions(user_id);
