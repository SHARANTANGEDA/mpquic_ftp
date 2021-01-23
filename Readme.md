# File Transfer with MPQUIC in GO

The App allows listing and downloading files from server

#### **Note: The server is asynchronous, allowing to connecting to multiple clients simultaneously**

This Project depends on another private project, which implements MPQUIC

You are expected to have access to [MPQUIC Stand Alone Package](https://github.com/SHARANTANGEDA/mp-quic), to be able to use this application 

Go Required: _1.12 +_

## Enable environment variable: 
- `export GOPRIVATE=github.com/SHARANTANGEDA/mp-quic`
- `export outputDir=PATH_TO_OUTPUT_DIR`

Sync dependencies after enabling the environment variable

##### Server Run
- `go build server.go`
- `./server --scheduler=round_robin --train=false --eps=0.01 --dump_exp=false --create_paths=true`

##### Client Run
- `cd client && go build client.go`
- `./client --scheduler=round_robin --action=2 --create_paths=true --file_name=hello.txt`
### *Note: Two values of action are possible 1, 2*

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

