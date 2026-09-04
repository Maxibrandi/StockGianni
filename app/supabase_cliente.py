import os
from supabase import create_client, Client

# Credenciales para conectar a supabase
SUPABASE_URL = "https://awvdlneugmgtxluipaqj.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF3dmRsbmV1Z21ndHhsdWlwYXFqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODg0MjM4ODMsImV4cCI6MjEwMzk5OTg4M30.48JvBbGJlDtIpx_hvOnODThQcrNmwVOfZ74iuvym9DI"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)