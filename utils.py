
import logging

logging.basicConfig(level=logging.INFO,  # Set the logging level to INFO
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('logging/error.log'),  # Log to a file
                              logging.StreamHandler()])  # Log to console


CHANGE_LOG_FILE_PATH = "change_log/change_log.txt"

def fetch_changelog():
    try:
        # Open the file and read its content
        with open(CHANGE_LOG_FILE_PATH, 'r') as file:
            content = file.read()

        # Split the content into paragraphs using the separators **start** and **end**
        changelogs = content.split('<<END>>')  # Assuming paragraphs are separated by two newlines

        # Add **start** and **end** to each paragraph
        formatted_changelogs = [
            cl.replace('<<START>>', '').strip() 
            for cl in changelogs 
            if cl.strip()
        ]

        # Print the list of formatted paragraphs
        for fc in formatted_changelogs:
            print(fc)
        return formatted_changelogs[::-1]
    except Exception as e:
        # Print an error message if something goes wrong
        logging.error(f"An error occurred while reading the file: {e}")


def save(change_log):
    try:
        with open(CHANGE_LOG_FILE_PATH, 'a') as file:
            file.write('\n<<START>>\n' + change_log + '\n<<END>>\n')
        logging.info("Change log updated successfully!")
    except Exception as e:
        logging.error("Error occurred while updating change log")