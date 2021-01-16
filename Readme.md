# File Transfer with MPQUIC in GO

This Project depends on another private project, which implements MPQUIC

You are expected to have access to [MPQUIC Stand Alone Package](https://github.com/SHARANTANGEDA/mp-quic), to be able to use this application 

Go Required: _1.12 +_

Enable environment variable: `export GOPRIVATE=github.com/SHARANTANGEDA/mp-quic`

Sync dependencies after enabling the environment variable

##### Server Run
`go build server.go`
##### Client Run
`cd client && go build client.go`
