Bitok Q&A telegram robot

You can use this robot to interact clients in your events

To use robot you need to installpython interprator, python-telegram-bot library and create new robot by `@BotFather` in telegram.


# Files

In order ti use robot you need to create two files. The first one includes bot token and the send one includes initial users list.

## token.txt

First and the most important file is token.txt. This file should contain just one line and in that line you should put you bot token witch your can get from `@BotFather`.

## users.txt

This file includes intial users informaition.

To begin any event you should have allow users list. Every user can have one of two rolls: `admin` or  `user`.

In this file you shpuld spesify usernames and their rolls in one of formats below:
 
```
username roll
```

With this format you can create single user in a line

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

With this format you can create multiple users with same roll and you don't need to write down roll every time.

This file can also contain comments. You can write comments with `#`.

# Commands

In order to interact with users you can use bot commands. There are two types of command. First one is robot commands, these commands start with /. Second type of commands are hidden ones and they are accasable only for bot admins. In fact every command that an admin sends to bot will interprate as a hidden command.

## commands list

| command      | syntax                                        | description  |
| :----------: | :-------------------------------------------: | :----------: |
| begin        | begin                                         | You should send this command in a gruop to start event |
| end          | end                                           | You should send this command in a gruop to end event |
| add          | add `username` `roll`                         | You can add new users with this command |
| report       | report                                        | This command sends you a report of meeting (messages count)  |
| list         | list `registered - remaining`                 | this command sends  |
| branch       | branch - branch list                          | You can use new branch with this command. Also you can get active branches list|
| send         | send `all - users - admins - branches - main` | You can use this command to send message as admin |
| update       | update `user_id` `roll`                       | With this command you can assign new roll to users |
| help         | help `command_name`                           | with this command use can get help data for ptger commands |
| reset        | reset `messages`                              | with this command you can reset settings |

### begin 

To start event you should send `begin` command in a group. This gropu with be treated as main destinaiton for massages and all cliensts messages will forward to this gropup.

### end

To end event you should sennd `end` command in main group. This will stop event and users can not send messages anymore.

### add

With this command you can add new valid username to robot.
Whene a user starts robot, robot will ask fot username. If username was a valid one user will get assigened roll to the username and no more users can use that username.

At the beginning of running robot, it will read `users.txt` and usernames written in the file are considered as valid usernames. But some times you need to add more usernames. This command can help you.

### report
