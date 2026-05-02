import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'
import { SignJWT, importPKCS8 } from "https://deno.land/x/jose@v4.14.4/index.ts";

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
};

const FIREBASE_PROJECT_ID = 'edu-login-4d05f';
const SERVICE_ACCOUNT_EMAIL = Deno.env.get('FIREBASE_CLIENT_EMAIL')!;
const SERVICE_ACCOUNT_KEY = Deno.env.get('FIREBASE_PRIVATE_KEY')!;

async function getAccessToken() {
  const privateKey = await importPKCS8(SERVICE_ACCOUNT_KEY.replace(/\\n/g, '\n'), 'RS256');
  const jwt = await new SignJWT({
    iss: SERVICE_ACCOUNT_EMAIL,
    sub: SERVICE_ACCOUNT_EMAIL,
    aud: 'https://oauth2.googleapis.com/token',
    scope: 'https://www.googleapis.com/auth/firebase.messaging',
  })
    .setProtectedHeader({ alg: 'RS256', typ: 'JWT' })
    .setIssuedAt()
    .setExpirationTime('1h')
    .sign(privateKey);

  const res = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      grant_type: 'urn:ietf:params:oauth:grant-type:jwt-bearer',
      assertion: jwt,
    }),
  });

  const data = await res.json();
  return data.access_token;
}

serve(async (req) => {
  // Handle CORS preflight requests
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders });
  }

  try {
    const { record, type, customMessage, targetUserId } = await req.json();
    
    // Initialize Supabase Admin Client
    const supabaseAdmin = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''
    );

    let query = supabaseAdmin.from('app_users').select('fcm_token');
    
    if (targetUserId) {
      query = query.eq('id', targetUserId);
    } else if (record && record.reported_by) {
      query = query.neq('username', record.reported_by); 
    }

    const { data: users } = await query;
    const tokens = users?.map(u => u.fcm_token).filter(t => t) || [];

    if (tokens.length === 0) return new Response("No valid FCM tokens found", { status: 200, headers: corsHeaders });

    let title = "Vesak System Update";
    let body = "";

    if (customMessage) {
       title = customMessage.title;
       body = customMessage.body;
    } else if (type === 'INSERT' && record) {
       if (record.amount_taken) {
          title = "New Expense Recorded";
          body = `${record.withdrawer_name} just recorded an expense of Rs.${record.amount_taken} for ${record.reason}.`;
       } else if (record.donation_type === 'Goods') {
          title = "New Material Donation";
          body = `${record.name} donated ${record.item_description} (x${record.quantity}).`;
       } else {
          title = "New Cash Donation";
          body = `${record.name} donated Rs.${record.amount}.`;
       }
    }

    const accessToken = await getAccessToken();

    // Send FCM requests for each token
    const fcmRequests = tokens.map(token => {
      return fetch(`https://fcm.googleapis.com/v1/projects/${FIREBASE_PROJECT_ID}/messages:send`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${accessToken}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: {
            token: token,
            notification: { title, body },
            data: { url: "/" } 
          }
        })
      });
    });

    await Promise.all(fcmRequests);

    return new Response(JSON.stringify({ success: true, sentCount: tokens.length }), { headers: { ...corsHeaders, "Content-Type": "application/json" } });
  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), { status: 500, headers: corsHeaders });
  }
})
