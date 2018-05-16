# Password Validate
> Small little utility to assist you with validating passwords

---

My company has tightened up their security rules for what qualifies as a valid password and some people have been struggling with coming up with valid ones so I decided to create this in order to help out a bit.

It's just a starting point, but hopefully I can improve on it.

## Password Requirements
* characters >= 10
* 3 or more of the following:
  [uppercase, lowercase, number, '!.*;$#@']
* No common dictionary words (5 >= letters)
* Not in common password dictionary
* Not contain username
* Not contain any part of first name
* Not contain any part of last name
* Not reused within 365 days (if password hash is stored)

## Dictionaries Files
I grabbed a tarball of password files from [skullsecurity.org](https://blog.skullsecurity.org/2010/the-ultimate-faceoff-between-password-lists). The rockyou.txt file is way to big to include here, but I've included phpbb.txt.

I used the following files from it:
* phpbb.txt
* rockyou.txt

The common word dictionary I grabbed from my bud's over at [Pybites](https://pybit.es/). I've also included it:
* [dictionary,txt](http://bit.ly/2iQ3dlZ)

## How To Install
I highly recommend that you keep your system's Python installation clean and use a virtual environment. Once you are ready to install the script, clone the repository and then install it with pip:

```bash
git clone https://github.com/clamytoe/Password-Validate.git
cd Password-Validate
pip install -e .
```

## How To Use
Once the script has been installed, simply run with `passwd_validate`.
On the initial run, the script will prompt you for the following data:

* First and Last name
* Company username

The information will be stored locally in a file json text file. I was going to add it to a sqlite database file but I felt that it would be overkill for this little program. The information is only used in order to make it easier for the user to try out new passwords without having to constantly re-enter the above information.

Once that's collected, it will prompt you for a password. If it's valid, it will ask you to confirm it. If those two checks pass, it will then ask if you want to store it. The hash of the password, **NOT** the password itself, will be added to the json file along with a datetime timestamp. When the program is ran again, it will check the timestamp of the stored hash if the hashes match. If they do, it will only validate the password if it's not being reused within the same year.

If the password that you enter doesn't pass the validation, it will inform you of why it failed and ask you to enter another one until a valid one is used.
