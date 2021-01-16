# MPQUIC Video Stream using RTSP and RTP Protocols from scratch in GO

## Follow the instructions in CoNEXT 17 mp-quic site (_MUST_)

## Make sure to change quic-go repo version to 0.11.2 before add remote of MP-QUIC
## This setup uses mininet Native install on MPTCP kernel by progmp and GoGTK for playing the video
### This application is for **`Go 1.14.2`**

`export GOPRIVATE=github.com/SHARANTANGEDA/mp-quic`

### Instructions to run in mininet
1. `cd mininet_version`
2. `sudo python3 mininet_run.py`

### Instructions for custom build

##### For Server build
`sudo GO111MODULE=off go build server.go server_worker.go rtp_packet.go video_stream.go`
##### For Client Build
`sudo GO111MODULE=off go build client.go client_worker.go rtp_packet.go`
##### Server Run
`./server`
##### Client Run
`./client [SERVER IP RTSP] 1060 3001 video3.mjpeg`
