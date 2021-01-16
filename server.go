package main

import (
	"fmt"
	"os"
	"time"

	quic "github.com/SHARANTANGEDA/mp-quic"
	"github.com/SHARANTANGEDA/mpquic_ftp/common"
	"github.com/SHARANTANGEDA/mpquic_ftp/constants"
)

func receiveData(conn quic.Session) ([]byte, int) {
	// Make a buffer to hold incoming data.
	buf := make([]byte, 512)
	// Read the incoming connection into the buffer.
	stream, err := conn.AcceptStream()
	if err != nil {
		return buf, 0 // Data Transfer is done
	}
	readLen, err := stream.Read(buf)
	if err != nil {
		fmt.Println("Error reading:", err.Error())
		os.Exit(1)
	}

	return buf, readLen
}

func main() {

	serverAddr := constants.SERVER_HOST + ":" + constants.SERVER_PORT
	cfgServer := &quic.Config{
		CreatePaths: true,
	}
	tlsConfig := common.GenerateTLSConfig()
	listener, err := quic.ListenAddr(serverAddr, tlsConfig, cfgServer)
	if err != nil {
		fmt.Println(err)
		fmt.Println("There was an error in socket")
		return
	}
	fmt.Println("Listening on " + serverAddr)
	fmt.Println("Press ^C to shutdown the server")

	for {

		session, err := listener.Accept()
		if err != nil {
			fmt.Println("Error accepting: ", err.Error())
			os.Exit(1)
		}

		receivedData := ""
		for {
			data, readLen := receiveData(session)
			if readLen > 0 {
				fmt.Println(readLen, "\nData received:\n", string(data))
				receivedData += string(data[:readLen])
			} else {
				break
			}
		}
		_ = session.Close(err)

		if receivedData != "" {
			file, err := os.Create(constants.SERVER_STORAGE_DIR + "/" + time.Now().String() + ".txt")
			if err != nil {
				fmt.Println(err)
			} else {
				_, _ = file.WriteString(receivedData)
				fmt.Println("Done")
			}
			_ = file.Close()
		}
		fmt.Println("File Upload Completed, File was saved Successfully \n Server is Ready!!!")
	}
}
