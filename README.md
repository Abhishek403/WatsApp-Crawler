# WatsApp-Crawler
Given input phone number, message, audio / video / gif, it will send messages. One more service to monitor the replies.

1) send_content.py : This service is responsible for sending messages. The input will be a csv file requiring mandatpry fields such as: (Lets call this csv as input.csv)
  a) Name: Name
  b) Given Name: Name
  c) Phone 1 - Value: Phone number
  d) Actual Name: The name by which you want to address the receipent. This might be the nickName
  e) Message: The text message
  f) ContentPath: Path to video / audio / gifs if any, otherwise blank
  g) Message Status: initially blank. This will be updated based on whether the message is send or not.


2) checkIfReplied.py: This service will monitor the replies. It can be run as a scheduler by specifying the period as console input.
It will take the above (input.csv) file as input.
It will take a output csv file as input. This output csv can be blank if we are running this first time for a particular message group or existing output file.
The output file would contain fields such as Message status (RECIEVED_NOT_SEEN, RECEIVED_SEEN, NOT_RECEIVED) and replies if any.
