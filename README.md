Bitok Q&A telegram robot

This robot can be used to interact with clients at events

The robot requires you to install the Python interpreter and Python-telegram-bot library and create a new bot by `@BotFather` in Telegram.


# Files

Two files must be created before using the robot. In the first one, the bot token is included, and in the second, the initial user list is included.

## token.txt

Token.txt is the first and most important file. It should contain just one line, and that line should contain your bot token, which you can get from `@BotFather`.

## users.txt

The file contains initial user information.

You should have a list of allowed users before starting any event. A user can be either an `admin` or a `user`.

Specify usernames and their roles in one of the following formats:
 
```
username roll
```

In this format, you can create a single user in a line

```
multiple-input (roll)
    usersname_1
    usersname_2
    .
    .
    .
    usersname_3
end
```

Using this format, you can create multiple users with the same role without having to write down the role every time.

Comments can also be included in this file. If you wish to write a comment, you can use `#`.

# Commands

You can use bot commands to interact with users. Commands can be divided into two types. First, we have robot commands. They begin with `/`. Second, there are hidden commands, which are only accessible to bot admins. A message sent by an admin to the bot will be interpreted as a hidden command.

## commands list

| command      | syntax                                        | description  |
| :----------: | :-------------------------------------------: | :----------: |
| begin        | begin                                         | Send this command in a group to start the event |
| end          | end                                           | Send this command to the main group to end the event |
| add          | add `username` `roll`                         | This command lets you add a new user |
| report       | report                                        | An analysis of the meeting (messages count) is sent with this command  |
| list         | list `registered - remaining`                 | Provides a list of registered users. And those who haven't started yet |
| branch       | branch - branch list                          | With this command, you can use the new branch. You can also view a list of active branches |
| send         | send `all - users - admins - branches - main` | Sending a message as an admin is possible using this command |
| update       | update `user_id` `roll`                       | You can assign a new role to a user using this command |
| help         | help `command_name`                           | You can use this command to get help for other commands |
| reset        | reset `messages`                              | You can reset settings using this commands |

### begin 

Send the `begin` command in a group to start the event. All messages from clients will be forwarded to this group, which will be the main destination for massages.

### end

Send the `end` command to the main group to end the event. Events will stop and users will no longer be able to send messages.

### add

By using this command, you can add a new valid username to the robot.
Usernames are requested when a robot is launched by a user. The username will be assigned to one user, and no other users will be able to use it.

As soon as the robot starts, it reads `users.txt`, and the usernames written in the file are considered valid usernames. However, sometimes you need to add more usernames. You can make use of this command.

### report

You will receive a report with this command. The report shows how many messages of each kind have been received.

### branch

The command can be sent every time you like after you start the event. This will make the chat a branch. The branch receives all messages, and admins can send commands to it. (Except the `end` command)

### send

Using this command, you can send messages to `users`, `admins`, `branches`, `main`, or all of them (`all`).
To use this command, you must send it first. (Ex: `send all`), and then you can send your message.

