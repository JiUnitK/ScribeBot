### Cloud Server Setup

This bot typically runs on an Amazon EC2 virtual Ubuntu server. It uses tmux to allow the python script to continue to run without an active terminal. See [this](https://stackoverflow.com/questions/21193988/keep-server-running-on-ec2-instance-after-ssh-is-terminated/21205131) Stack Overflow post for more information on running tmux on an EC2 instance.