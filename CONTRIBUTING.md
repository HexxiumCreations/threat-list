# Contributing

## Issue reporting

- Check that the issue has not already been reported.
- Check that the issue has not already been fixed in the latest code.
- Specify the problematic URL on which the issue can be reproduced.

## Pull requests

- Please fork the repository to your own account for making pull requests.
- Make sure that every entry follows [Adblock Plus filter rules](https://adblockplus.org/en/filters).
- Update the version with the format `yyyyMMdd`.
- Do not add extra empty line.
## You must label what each submission is

- Example (Incorrect way):
||https://www.subdomain.example.com/?36345656

- Example (Correct way):
||example.com^

- Example (Correct way #2):
||subdomain.example.com^

At no point should a domain have any prefix such as https:// or www. in the list, addtionally, subdomains should NOT be used unless you fully intend to block ONLY that subdomain and not the entire domain. You do not need to include any pages or data beyond the .com (.tk,.ca, etc) to block the domain.

Please append a ^ to the end of any domain. To label your submissions, append a space after the ^ and then a # followed by the label, example:

- ||example.com/ #Malware

The following are currently valid labels to use, please ONLY use these labels to keep the list neat, please be as specific as possible and only use one label.

#Malware /
#Scam /
#Spam /
#Phishing /
#Deceptive Content /
#Exploit /

It is highly recommended that you keep a neat, and locally stored Excel spreadsheet of every URL you ever submit in addition to a detailed reasoning behind why you submitted the domain, in the event the domain owner contacts us asking to be unblacklisted, we will refer to your reason to why they were blacklisted to see if the issue has been fixed.

Lastly, please use this site https://adblockplus.org/redundancy_check by copying and pasting every domain in our list plus the ones you're preparing to create a pull request for to check for any duplicates so you can remove them before sending the pull request, thank you.
