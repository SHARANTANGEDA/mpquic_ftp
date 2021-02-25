# File Transfer with MPQUIC in GO

The App allows listing and downloading files from server

#### **Note: The server is asynchronous, allowing to connecting to multiple clients simultaneously**

This Project depends on another private project, which implements MPQUIC

You are expected to have access to [MPQUIC Stand Alone Package](https://github.com/SHARANTANGEDA/mp-quic), to be able to use this application 

Go Required: _1.12 +_

## Pre-Requisites
- Follow all requirements mentioned in [MPQUIC Repo](https://github.com/SHARANTANGEDA/mp-quic)

## Enable environment variable: 
- Check out the sample for env variables needed

Sync dependencies after enabling the environment variable

##### Server Run
- `go build server.go`
- `./server --scheduler=round_robin --eps=0.01 --dump_exp=false `

##### Client Run
- `cd client && go build client.go`
- `./client --scheduler=round_robin --action=2 --file_name=hello.txt`
### *Note: Three values of action are possible 1, 2, 3*
#### For Action:2 - Download from Server - `file_name` is required
#### For Action:3 - Upload to Server - `file_path` (abs path) is required

### List of Available Schedulers

	round_robin
	low_latency
	random
	low_bandit
	peekaboo
	ecf
	blest
	dqnAgent
	first_path

