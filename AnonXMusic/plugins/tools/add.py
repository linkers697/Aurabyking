
# ====================================
# INTEGRATION GUIDE FOR SAVING PLAY DATA
# ====================================

# 1. Add this import to your main music playing file (usually play.py or similar)
from AnonXMusic.plugins.tools.stats import increment_group_play_count, save_play_data

# ====================================
# 2. FIND YOUR MUSIC PLAYING FUNCTION
# ====================================
# Look for functions like play_music(), start_stream(), or similar where music actually starts
# It might be in files like:
# - AnonXMusic/plugins/play/play.py
# - AnonXMusic/plugins/play/stream.py
# - AnonXMusic/core/call.py

# ====================================
# 3. ADD THE DATABASE SAVING CALL
# ====================================
# EXAMPLE: If your music playing function looks like this:

"""
async def start_stream(message, song_data):
    # Your existing music playing code here...
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    # Start the actual music stream
    await some_music_playing_function()
    
    # ADD THIS LINE AFTER MUSIC STARTS SUCCESSFULLY:
    await increment_group_play_count(chat_id)
    
    # Optional: Save detailed play history
    await save_play_data(chat_id, user_id, song_data.get('title'))
    
    await message.reply("🎵 Now playing...")
"""

# ====================================
# 4. EXAMPLE INTEGRATION PATTERNS
# ====================================

# Pattern 1: Simple increment only
async def your_play_function(message):
    # Your music code...
    try:
        # Start music here
        result = await start_music_stream()
        
        # Save to database AFTER successful start
        await increment_group_play_count(message.chat.id)
        
    except Exception as e:
        # Handle errors
        pass

# Pattern 2: Full tracking with song details
async def your_detailed_play_function(message, song_info):
    # Your music code...
    try:
        # Start music here
        await start_music_stream(song_info)
        
        # Save detailed data AFTER successful start
        await save_play_data(
            chat_id=message.chat.id,
            user_id=message.from_user.id,
            song_title=song_info.get('title', 'Unknown Song')
        )
        
    except Exception as e:
        # Handle errors
        pass

# ====================================
# 5. COMMON LOCATIONS TO ADD THE CALL
# ====================================

# Look for these function names in your codebase:
# - play_music()
# - start_stream() 
# - process_play_request()
# - handle_youtube_play()
# - handle_spotify_play()
# - stream_func()
# - play_func()

# Add the increment call RIGHT AFTER the music actually starts playing,
# not before! This ensures we only count successful plays.

# ====================================
# 6. TESTING THE INTEGRATION
# ====================================

# After integration, test with:
# 1. Play a song in a group
# 2. Use /check 0 to see if count increased
# 3. Use /toplistgroup to see if group appears in list

# ====================================
# 7. MANUAL DATA ENTRY FOR TESTING
# ====================================

# You can also manually add test data using this command (sudo only):
@app.on_message(filters.command(["addtestdata"]) & SUDOERS)
async def add_test_data(client, message):
    """Add test data for demonstration"""
    try:
        await increment_group_play_count(message.chat.id)
        await message.reply_text(
            f"✅ **Test data added!**\n\n"
            f"Play count for this group has been incremented by 1.\n"
            f"Use `/check 0` to verify."
        )
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")

# ====================================
# 8. COMMON ISSUES AND SOLUTIONS
# ====================================

"""
ISSUE: Commands show no data
SOLUTION: Make sure you're calling increment_group_play_count() when music starts

ISSUE: Database connection errors
SOLUTION: Ensure mongodb is properly imported and connected

ISSUE: Permission errors
SOLUTION: Make sure the bot has proper database write permissions

ISSUE: Data not updating
SOLUTION: Check if the increment function is called AFTER music successfully starts
"""

# ====================================
# 9. COMPLETE EXAMPLE FOR play.py
# ====================================

"""
# At the top of your play.py file:
from AnonXMusic.plugins.tools.stats import increment_group_play_count

# In your main play function:

@app.on_message(filters.command(["play", "p"]) & filters.group)
async def play_command(client, message):
    # Your existing play logic...
    
    try:
        # Process song request
        song_data = await process_song_request(message)
        
        # Start playing music
        await start_stream_in_call(message.chat.id, song_data)
        
        # 🎯 ADD THIS LINE TO SAVE DATA:
        await increment_group_play_count(message.chat.id)
        
        # Send success message
        await message.reply("🎵 Started playing...")
        
    except Exception as e:
        await message.reply(f"Error: {e}")
"""
