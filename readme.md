### Cloud Server Setup

This bot typically runs on an Amazon EC2 virtual Ubuntu server. It uses tmux to allow the python script to continue to run without an active terminal. See [this](https://stackoverflow.com/questions/21193988/keep-server-running-on-ec2-instance-after-ssh-is-terminated/21205131) Stack Overflow post for more information on running tmux on an EC2 instance.

# Useful commands
To SSH into amazon EC2 instance:
ssh -i discord_bot_pair.pem ubuntu@(amazon EC2 ip address)

To attach to running tmux screen:
tmux attach

To detach from tmux session and keep it running in the background:
(hit ctrl+b, d)