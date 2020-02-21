# Contributing Rules & Guide

## Issue reporting

- Check that the issue has not already been reported.
- Check that the issue has not already been fixed in the latest code.
- Specify the problematic URL on which the issue can be reproduced.

## Requesting Removal From List

If you are a domain owner for a domain that we have blacklisted and you feel that you have been wrongly blacklisted, or you have cleaned your domain of all problems we found and wish to be removed from our blacklist, please submit an ISSUE _or_ send an email to support@hexxiumcreations.com with the following: include your domain name, your name (first and last), your primary email address, the issues you fixed (if requesting review after fixing), and why you feel you were blacklisted incorrectly (if applicable). We monitor domains even after blacklist removal, so don’t expect to abuse the review system. We will respond by email (or to your ISSUE) ASAP.

Note: Users who were added to the blacklist for clearly hosting malicious activity such as a tech support scam will not be removed from the blacklist unless the domain name has been sold to a new owner, in which case, we would need proof of new ownership – Only a user who owns a domain that was seemingly compromised and subsequently abused can be removed from the blacklist after successful review.

## Pull requests

- Please fork the repository to your own account for making pull requests.
- Make sure that every entry follows [Adblock Plus filter rules](https://adblockplus.org/en/filters).
- Update the version with the format `yyyyMMdd`.
- Do not add extra empty lines or unnecessary spaces.

## Valid Submission Format

- Submit to threat-list _NOT_ domainsonly or hosts unless you update them all in your pull request, we will take care of copying to those two for you if you do not.

Below is the submission example for threat-list:

- Example (Incorrect way):
||https://www.subdomain.example.com/?36345656

- Example (Correct way):
||example.com^

- Example (Correct way #2):
||subdomain.example.com^

At no point should a domain have any prefix such as https:// or www. in the list, addtionally, subdomains should NOT be used unless you fully intend to block ONLY that subdomain and not the entire domain. You do not need to include any pages or data beyond the .com (.tk,.ca, etc) to block the domain.

- For HOSTS submissions, do not include any document or specific page on a domain blocking. - Subdomains and actual domains should work fine - DOMAINSONLY submissions should be exact copies of the HOSTS file minus the 0.0.0.0 and any spaces

## Labeling & Internal Review Tracking

Labeling your submissions greatly speeds up the review process and helps ensure removal requests aren't abused, please label all submissions. Please append a ^ to the end of any domain. To label your submissions, append a space after the ^ and then a # followed by the label, example:

- ||example.com^ #Malware

The following are currently valid labels to use, please ONLY use these labels to keep the list neat, please be as specific as possible and only use one label. Ensure spelling of the label is correct to prevent any issues with automated merging to domainsonly and hosts!

#Malware /
#Scam /
#Spam /
#Phishing /
#Deceptive Content /
#Exploit /

It is highly recommended that you keep a neat, and locally stored Excel spreadsheet (or other easy-to-view software) of every URL you ever submit in addition to a detailed reasoning behind why you submitted the domain, in the event the domain owner contacts us asking to be unblacklisted, we will refer to your reason to why they were blacklisted to see if the issue has been fixed.

Lastly, please use this site https://adblockplus.org/redundancy_check by copying and pasting every domain in our list plus the ones you're preparing to create a pull request for to check for any duplicates so you can remove them before sending the pull request, thank you.
