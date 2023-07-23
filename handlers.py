from telebot import types  # Import the types module
from gpt4 import generate_response

# Global dictionary to store user preferences
user_data = {}

def register_handlers(bot):
    # This handler is called when the user presses an inline keyboard button
    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
        # Check the callback_data and call the appropriate function
        if call.data in ['stand-alone', 'series', 'no series preference']:
            process_format_step(call.message, call.data)
        elif call.data in ['new releases', 'classics', 'no date preference']:
            process_publicationtime_step(call.message, call.data)
        elif call.data in ['fiction', 'non-fiction']:
            process_type_step(call.message, call.data)
        elif call.data in ['short', 'long', 'medium']:
            process_length_step(call.message, call.data)
        elif call.data == 'add_detailed_preferences':
            set_detailed_preferences(call.message)
        elif call.data == 'generate_recommendations':
            get_recommendation(call.message)
        elif call.data == 'do_not_generate':
            bot.send_message(call.message.chat.id, 'Okay, you can generate recommendations later by typing /get_recommendation.')
    
    

####################################################

    # This handler is called when the user sends the /start command
    @bot.message_handler(commands=['start'])
    def start(message):
        # Create a ReplyKeyboardRemove object
        markup = types.ReplyKeyboardRemove(selective=False)
        # Send a welcome message and remove the keyboard
        bot.send_message(message.chat.id, 'Welcome to the Book Recommendation Bot! You can set your reading preferences by typing /preferences.', reply_markup=markup)

    # This handler is called when the user sends the /preferences command
    @bot.message_handler(commands=['preferences'])
    def preferences(message):
        # Initialize a new dictionary for this user
        user_data[message.chat.id] = {}
        # Ask the user for their favorite genre
        msg = bot.send_message(message.chat.id, 'What is your favorite genre?')
        # Register process_genre_step as the next step
        bot.register_next_step_handler(msg, process_genre_step)

    # This handler is called when the user sends the /show_preferences command
    @bot.message_handler(commands=['show_preferences'])
    def show_preferences(message):
        # Check if the user has set any preferences yet
        if message.chat.id in user_data:
            # Retrieve the user's preferences
            preferences = user_data[message.chat.id]
            # Create a list of strings representing the user's preferences
            preferences_list = [f'{key.capitalize()}: {value}' for key, value in preferences.items()]
            
            # Join the list into a single string with line breaks between each preference
            preferences_str = '\n'.join(preferences_list)
            # Send the user's preferences back to them
            bot.send_message(message.chat.id, 'Here are your current reading preferences:\n' + preferences_str)
        else:
            # If the user hasn't set any preferences yet, send a message letting them know
            bot.send_message(message.chat.id, "You haven't set any reading preferences yet. You can do so by typing /preferences.")
    

    # This handler is called when the user sends the /get_recommendation command
    @bot.message_handler(commands=['get_recommendation'])
    def get_recommendation(message):
        # Check if the user has set any preferences yet
        if message.chat.id in user_data:
            # Retrieve the user's preferences
            preferences = user_data[message.chat.id]
            print(f"User preferences: {preferences}")  # Debugging print statement
            # Generate a message to send to the GPT-4 model based on the user's preferences
            message_content = f"I'm looking for a {preferences['genre']} book. I prefer {preferences['format']} books and I'm interested in {preferences['time']} books. I like {preferences['type']} books. Some of my favorite authors are {preferences['authors']}, and I recently enjoyed reading {preferences['books']}. I prefer {preferences['length']} books."
            
            # Check if detailed preferences are set and include them in the message if they are
            if 'mood' in preferences:
                message_content += f" I'm currently in the mood for: {preferences['mood']}."
            if 'theme' in preferences:
                message_content += f" I'm interested in books about: {preferences['theme']}."
            if 'setting' in preferences:
                message_content += f" I'd like a book set in: {preferences['setting']}."
            if 'character' in preferences:
                message_content += f" I enjoy books with: {preferences['character']}."
    
            print(f"Message content: {message_content}")  # Debugging print statement
            # Generate a response using the GPT-4 model
            response = generate_response(message_content, preferences)
            print(f"Generated response: {response}")  # Debugging print statement
            # Send the response back to the user
            bot.send_message(message.chat.id, response)
        else:
            # If the user hasn't set any preferences yet, send a message letting them know
            bot.send_message(message.chat.id, 'You haven\'t set any reading preferences yet. You can do so by typing /preferences.')
    

####################################################
    
    # This function is called after the user responds to the genre question
    def process_genre_step(message):
        # Store the user's favorite genre
        user_data[message.chat.id]['genre'] = message.text
        # Create a new InlineKeyboardMarkup object
        keyboard = types.InlineKeyboardMarkup()
        # Add "Stand-Alone", "Series", and "No Preference" buttons to the keyboard
        keyboard.add(types.InlineKeyboardButton('Stand-Alone', callback_data='stand-alone'),
                     types.InlineKeyboardButton('Series', callback_data='series'),
                     types.InlineKeyboardButton('No Preference', callback_data='no series preference'))
        # Ask the user if they prefer stand-alone books or series, and display the keyboard
        bot.send_message(message.chat.id, 'Do you prefer stand-alone books or series?', reply_markup=keyboard)

    def process_format_step(message, format):
        # Store the user's format preference
        user_data[message.chat.id]['format'] = format
        # Create a new InlineKeyboardMarkup object
        keyboard = types.InlineKeyboardMarkup()
        # Add "New Releases", "Classics", and "No Preference" buttons to the keyboard
        keyboard.add(types.InlineKeyboardButton('New Releases', callback_data='new releases'),
                     types.InlineKeyboardButton('Classics', callback_data='classics'),
                     types.InlineKeyboardButton('No Preference', callback_data='no date preference'))
        # Ask the user if they prefer new releases or classics, and display the keyboard
        bot.send_message(message.chat.id, 'Do you prefer new releases or classics?', reply_markup=keyboard)

    def process_publicationtime_step(message, time):
        # Store the user's time preference
        user_data[message.chat.id]['time'] = time
        # Create a new InlineKeyboardMarkup object
        keyboard = types.InlineKeyboardMarkup()
        # Add "Fiction", "Non-Fiction" buttons to the keyboard
        keyboard.add(types.InlineKeyboardButton('Fiction', callback_data='fiction'),
                     types.InlineKeyboardButton('Non-Fiction', callback_data='non-fiction'))
        # Ask the user if they're looking for fiction or non-fiction recommendations, and display the keyboard
        bot.send_message(message.chat.id, 'Are you looking for fiction or non-fiction recommendations?', reply_markup=keyboard)

    def process_type_step(message, type):
        # Store the user's type preference
        user_data[message.chat.id]['type'] = type
        # Ask the user for their favorite authors
        msg = bot.send_message(message.chat.id, 'Could you tell me some of your favorite authors?')
        # Register process_authors_step as the next step
        bot.register_next_step_handler(msg, process_authors_step)

    def process_authors_step(message):
        # Store the user's favorite authors
        user_data[message.chat.id]['authors'] = message.text
        # Ask the user for some books that they've enjoyed recently
        msg = bot.send_message(message.chat.id, 'What are some books that you\'ve enjoyed recently?')
        # Register process_books_step as the next step
        bot.register_next_step_handler(msg, process_books_step)

    def process_books_step(message):
        # Store the user's favorite books
        user_data[message.chat.id]['books'] = message.text
        # Create a new InlineKeyboardMarkup object
        keyboard = types.InlineKeyboardMarkup()
        # Add "Short", "Long" buttons to the keyboard
        keyboard.add(types.InlineKeyboardButton('Short', callback_data='short'),
                     types.InlineKeyboardButton('Long', callback_data='long'),
                     types.InlineKeyboardButton('In-Between', callback_data='medium'))
        # Ask the user if they prefer short reads or long, in-depth books, and display the keyboard
        bot.send_message(message.chat.id, 'Do you prefer short reads, long, in-depth books, or somewhere in between?', reply_markup=keyboard)

    def process_length_step(message, length):
        # Store the user's length preference
        user_data[message.chat.id]['length'] = length
        # Create a new InlineKeyboardMarkup object
        keyboard = types.InlineKeyboardMarkup()
        # Add "Add Detailed Preferences", "Generate Recommendations" buttons to the keyboard
        keyboard.add(types.InlineKeyboardButton('Add Detailed Preferences', callback_data='add_detailed_preferences'),
                     types.InlineKeyboardButton('Generate Recommendations', callback_data='generate_recommendations'))
        # Ask the user if they want to add detailed preferences or generate recommendations, and display the keyboard
        bot.send_message(message.chat.id, 'Would you like to add detailed preferences or generate recommendations?', reply_markup=keyboard)
    

####################################################

    # This handler is called when the user sends the /set_detailed_preferences command
    @bot.message_handler(commands=['set_detailed_preferences'])
    def set_detailed_preferences(message):
        # Ask the user about their current reading mood
        msg = bot.send_message(message.chat.id, 'What is your current reading mood? For example, "I\'m in the mood for a thrilling adventure" or "I want something light and humorous".')
        # Register process_mood_step as the next step
        bot.register_next_step_handler(msg, process_mood_step)

    def process_mood_step(message):
        # Store the user's reading mood
        user_data[message.chat.id]['mood'] = message.text
        # Ask the user about specific themes or topics they're interested in
        msg = bot.send_message(message.chat.id, 'Are there specific themes or topics you are interested in? For example, "I want a book about space exploration" or "I\'m interested in historical fiction set in the Victorian era".')
        # Register process_theme_step as the next step
        bot.register_next_step_handler(msg, process_theme_step)

    def process_theme_step(message):
        # Store the user's theme preference
        user_data[message.chat.id]['theme'] = message.text
        # Ask the user about specific settings or time periods they're interested in
        msg = bot.send_message(message.chat.id, 'Are there specific settings or time periods you are interested in? For example, "I want a book set in the future" or "I want a book set in the 1920s".')
        # Register process_setting_step as the next step
        bot.register_next_step_handler(msg, process_setting_step)

    def process_setting_step(message):
        # Store the user's setting preference
        user_data[message.chat.id]['setting'] = message.text
        # Ask the user about specific types of characters they're interested in
        msg = bot.send_message(message.chat.id, 'Are there specific types of characters you are interested in? For example, "I want a book with a strong female lead" or "I want a book with a detective as the main character".')
        # Register process_character_step as the next step
        bot.register_next_step_handler(msg, process_character_step)

    def process_character_step(message):
        # Store the user's character preference
        user_data[message.chat.id]['character'] = message.text
        # Create a new InlineKeyboardMarkup object
        keyboard = types.InlineKeyboardMarkup()
        # Add "Yes", "No" buttons to the keyboard
        keyboard.add(types.InlineKeyboardButton('Yes', callback_data='generate_recommendations'),
                     types.InlineKeyboardButton('No', callback_data='do_not_generate'))
        # Ask the user if they want to generate recommendations now, and display the keyboard
        bot.send_message(message.chat.id, 'Would you like to generate recommendations now?', reply_markup=keyboard)
    

################################################  

    # This handler is called when the user sends the /help command
    @bot.message_handler(commands=['help'])
    def help(message):
        help_text = """
        Here are the commands you can use:
        - /start: Starts the bot and sends a welcome message.
        - /preferences: Asks you for your reading preferences and stores them.
        - /set_detailed_preferences: Asks you for more detailed reading preferences and stores them.
        - /show_preferences: Shows your current reading preferences.
        - /get_recommendation: Generates a book recommendation based on your preferences.
        - /help: Displays this message.
        """
        bot.send_message(message.chat.id, help_text)

################################################

    # This handler is called for any text message that is not a command
    @bot.message_handler(func=lambda message: True)
    def echo_all(message):
        bot.reply_to(message, message.text)
