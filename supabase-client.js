import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js/+esm';

const supabaseUrl = 'https://yqpkgybmjdovdnmekpnw.supabase.co';
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlxcGtneWJtamRvdmRubWVrcG53Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY1MjUwMjAsImV4cCI6MjA5MjEwMTAyMH0.7C9jv1_zDRxSMCgs0tWfiNUGXGOkCLz5RE0CCDoc_yA';

export const supabase = createClient(supabaseUrl, supabaseKey);
