# Database Error Fix

## The Problem

Users were getting this error when generating .apkg files:

```
❌ Error generating .apkg file: no such table: dconf
```

## Root Cause

The `genanki` library creates a minimal ANKI database that may not include all tables that newer versions of ANKI expect. When our `fix_anki_database()` function tried to modify the `dconf` table, it would fail if that table didn't exist.

## The Fix

Updated the `fix_anki_database()` function to:

1. **Check if tables exist before modifying them**
   ```python
   cursor.execute("""
       SELECT name FROM sqlite_master 
       WHERE type='table' AND name='dconf'
   """)
   dconf_exists = cursor.fetchone() is not None
   ```

2. **Create missing tables if needed**
   ```python
   if not dconf_exists:
       cursor.execute("""
           CREATE TABLE IF NOT EXISTS dconf (
               id integer primary key,
               conf text not null,
               usn integer not null default -1
           )
       """)
   ```

3. **Handle null results safely**
   - Check if `fetchone()` returns data before accessing it
   - Use conditional checks for all database operations

## What Changed

### Before (Broken)
```python
# Assumed dconf table always exists
cursor.execute("SELECT usn FROM dconf LIMIT 1")
# Would crash if table doesn't exist
```

### After (Fixed)
```python
# Check if table exists first
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='dconf'")
if cursor.fetchone():
    # Table exists, modify it
else:
    # Table doesn't exist, create it
```

## Testing

The fix has been tested and handles:
- ✅ Missing dconf table → creates it
- ✅ Existing dconf table without usn → adds usn field
- ✅ Existing dconf table with usn → leaves it alone
- ✅ Missing graves table → creates it
- ✅ Null results from queries → handles gracefully

## Impact

This fix makes the .apkg generation much more robust and compatible with different versions of genanki and ANKI.

## Additional Improvements

Also added:
- Claude Sonnet 4.5 as the default/recommended model
- Better error handling throughout the database fix function
- More defensive programming practices

## Usage

No changes needed on the user side - the fix is automatic! Just:

1. Generate your flashcards
2. Go to Export tab
3. Click "Generate .apkg File"
4. Download and import into ANKI

It will now work without the database error! 🎉
