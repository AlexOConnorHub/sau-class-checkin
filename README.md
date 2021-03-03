- [About](#about)
- [Setup](#setup)
  - [Credentials](#credentials)
  - [Example Schedule:](#example-schedule)
  - [Example .JSON bs4](#example-json-bs4)
    - [How it's made](#how-its-made)
      - [Time](#time)
      - [Class code](#class-code)
      - [Seat ID](#seat-id)
  - [Example .JSON bot](#example-json-bot)
    - [How it's made](#how-its-made-1)
      - [Time](#time-1)
      - [Class code](#class-code-1)
      - [Seat ID](#seat-id-1)
- [Troubleshooting](#troubleshooting)
# About
This is a script that will tell SAU where you're sitting, if you set it up correctly

Because *most* classes start on the hour, and a good student should arrive before that and check in, the script tries to account for this. If you run the script 5 minutes before an hour change, it assumes the next hour.

# Setup
While the syntax is simple, getting the information may not be so simple.
## Credentials
Running `setup.bat` (Windows)/`setup.sh` (OSX/Linux) should initialize your `secrets.json`. You can also manually edit the file to set it up.
## Example Schedule:
* 8:00AM Class 1
* 10:00AM Class 2
* 2:00PM Class 3
* 3:30PM Class 4
* 4:45PM Lab 5
## Example .JSON bs4
```
{
    "08": "124:1424",
    "10": "561:5331",
    "14": "10264:1424",
    "15": "812:556",
    "16": "23016:3638"
}
```
### How it's made
#### Time
The simplest thing to get is the time. The script just needs the hour. Let us start our file out.
```
{
    "08": ,
    "10": ,
    "14": ,
    "15": ,
    "16": 
}
```
With a lab starting at 4:45PM, the script will fail to work if you run it at 4:55PM or after. Make sure to keep this in mind, you could even put this class in as `"17"` if you are not sure if you will be in class on time, or decide to run the script five minutes after getting to lab. **Do keep the class as one entry, as the script will not increment both class counters**

#### Class code
The next part is simple to get. A sample URL for the seating is `https://myaccess.southern.edu/mvc/ats/Attendance/check/123`. You only need to worry about the number at the end there. This number increments by 1 each class period. If I checked in to Class 1 using this URL, I would put `124` as the number, as it is what the script will need for next time. The script does auto increment this number, so you do not need to change it every time you go to class. Every class has a different number. You can read it off the print out with the QR code at the bottom. Adding this info should have your `classesbs4.json` looking like this.
```
{
    "08": "124:",
    "10": "561:",
    "14": "10264:",
    "15": "812:",
    "16": "23016:"
}
```
#### Seat ID
Finally, you need to get the seat ID. I recommend just using the web inspect element tool in the web browser. Use the "Click-to-inspect" tool and click on the button that is your seat. In the now highlighted section, look for the `data-seat-id`. This number is what goes next. You have to get the seat ID for each class. The seat ID is the same for each room, so if you have multiple classes in one room, and you sit in the same seat, you will have the same seat ID in those classes. Adding this data, your `classesbs4.json` should look something like this.
```
{
    "08": "124:1424",
    "10": "561:5331",
    "14": "10264:1424",
    "15": "812:556",
    "16": "23016:3638"
}
```
## Example .JSON bot
```
{
    "08": "124:D2:ruby",
    "10": "561:A4:green",
    "14": "10264:E1:royal",
    "15": "812:C4:green",
    "16": "23016:C2:royal"
}
```
### How it's made
#### Time
The simplest thing to get is the time. The script just needs the hour. Let us start our file out.
```
{
    "08": ,
    "10": ,
    "14": ,
    "15": ,
    "16": 
}
```
With a lab starting at 4:45PM, the script will fail to work if you run it at 4:55PM or after. Make sure to keep this in mind, you could even put this class in as `"17"` if you are not sure if you will be in class on time, or decide to run the script five minutes after getting to lab. **Do keep the class as one entry, as the script will not increment both class counters**

#### Class code
The next part is simple to get. A sample URL for the seating is `https://myaccess.southern.edu/mvc/ats/Attendance/check/123`. You only need to worry about the number at the end there. This number increments by 1 each class period. If I checked in to Class 1 using this URL, I would put `124` as the number, as it is what the script will need for next time. The script does auto increment this number, so you do not need to change it every time you go to class. Every class has a different number. You can read it off the print out with the QR code at the bottom. Adding this info should have your `classesbot.json` looking like this.
```
{
    "08": "124:",
    "10": "561:",
    "14": "10264:",
    "15": "812:",
    "16": "23016:"
}
```
#### Seat ID
For this, you just put in your seat letter/number, and the color section **In all lowercase**
```
{
    "08": "124:D2:ruby",
    "10": "561:A4:green",
    "14": "10264:E1:royal",
    "15": "812:C4:green",
    "16": "23016:C2:royal"
}
```
# Troubleshooting
To troubleshoot, I recommend going through the setup for the `webbot` version, as it has a browser that opens up and allows you to see what is happening. This will help you see whether or not you have the right login information, and if the script is going to the right webpage. Uncomment line `20` and comment out line `22` if you have the ability to use a proxy to monitor web traffic (it is currently set to `ZAProxy`'s default). If you do not have a proxy, but want to see the web browser, uncomment line `21`. The default uncommented line, line `22` runs the script without a visible browser. Possible troubles you will see are:
* Incorrect login
* Incorrect class ID
* Incorrect seat ID

Based on the problem you see, you can go and fix it in the proper `.json` file or make a bug report. Remember that the `bs4` and `webbot` versions use different `.json` files, so changes saved to one need to be migrated to the other.