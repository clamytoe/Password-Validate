# Password Validate
> Small little utility to assist you with validating passwords

---

My company has recently been changing their password policy and it was so bad that most people complained about it. So much so that they finally relaxed the rules a bit. A lot of people have been struggling with coming up with a valid password, so I decided to create this in order to help out a bit.

It's just a starting point, I plan on making it better and perhaps turning it into a class and making it easier to change some of the requirements.

## Password Requirements
* characters >= 10
* 3 or more of the following:
  [uppercase, lowercase, number, '!.*;$#@']
* No common dictionary words (5 >= letters)
* Not in common password dictionary
* Not contain username
* Not contain any part of first name
* Not contain any part of last name

## Dictionaries Files
I grabbed a tarball of password files from [skullsecurity.org](https://blog.skullsecurity.org/2010/the-ultimate-faceoff-between-password-lists). The file is way to big to provide here.

I used the following files from it:
* phpbb.txt
* rockyou.txt

The common word dictionary I grabbed from my bud's over at [Pybites](https://pybit.es/):
* [dictionary,txt](http://bit.ly/2iQ3dlZ)
