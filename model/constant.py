
'''
/.fgit
|__trash    # trash buffer.
    |__20241009
    |__20241010
|__action   # action each time.
    |__20241009_push
        |__error.json
        |__success.json
|__buffer
    |__xxxx.txt
|__config.json
|__cloud.json
|__local.json
'''
class FilegitConstant():
    MAX_RETRIES=3
    BUFFER_SIZE = 500
    FGIT_FOLDER_NAME = ".fgit"
    TRASH_FOLDER_NAME = "trash"
    ACTION_FOLDER_NAME = "action"
    INDEX_FOLDER_NAME = "index"
    LOG_FOLDER_NAME = "log"
    BUFFER_FOLDER_NAME = "buffer"
    CHUNK_FOLDER_NAME = "chunks"

    LOG_SUCCESS_FILE_NAME = "success.log"
    LOG_ERROR_FILE_NAME = "error.log"

    LOCAL_INDEX_FILE_NAME = "local.json"
    CLOUD_INDEX_FILE_NAME = "remote.json"
    CONFIG_FILE_NAME = "config.json"
