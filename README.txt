usage:
python3 script.py MAP_FILE_PATH CONFIG_FILE_PATH

tests:
python3 test.py


#########################
config file structure:
START START_TIME 
PEEK_START PEEK_END
CLIENTS
#########################
CLIENTS are separated by spaces



#########################
map file consists of lines in following format:
START_V DESTINATION_V NORMAL_TIME PEEK_TIME
#########################