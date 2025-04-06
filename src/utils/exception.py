from logger import logging
import traceback

class CustomException(Exception):
    def __init__(self, message="An unexpected error occurred in the Coffee Beans Classification application.", error: Exception = None):
        if error:
            # Navigate to the innermost traceback frame
            tb = error.__traceback__
            while tb.tb_next:
                tb = tb.tb_next
            filename = tb.tb_frame.f_code.co_filename
            lineno = tb.tb_lineno

            # Get the full traceback details
            error_details = traceback.format_exc()
            location_info = f"File: {filename}, Line: {lineno}"
            full_message = f"{message}\nError Details:\n{error_details}\n{location_info}"
        else:
            full_message = message

        # Print the full error info to stdout
        print(full_message)

        super().__init__(full_message)
        
        # Log the error details immediately upon exception creation
        logging.error(full_message)

    def __init__(self, message="An unexpected error occurred in the Coffee Beans Classification application.", error: Exception = None):
        if error:
            # Format the full traceback info
            error_details = traceback.format_exc()
            full_message = f"{message}\nError Details:\n{error_details}"
        else:
            full_message = message

        super().__init__(full_message)
        
        # Log the exception details immediately when the exception instance is created
        logging.error(full_message)
