package main

import (
	"bufio"
	"crypto/tls"
	"fmt"
	"io"
	"io/ioutil"
	"os"

	quic "github.com/SHARANTANGEDA/mp-quic"
	"github.com/SHARANTANGEDA/mpquic_ftp/constants"
)

func main() {
	reader := bufio.NewReader(os.Stdin)
	fmt.Println("Enter Absolute Path of the file to upload: ")
	filePath, _ := reader.ReadString('\n')
	filePath = filePath[:len(filePath)-1]
	cfgClient := &quic.Config{
		CreatePaths: true,
	}
	tlsConfig := &tls.Config{InsecureSkipVerify: true}
	session, err := quic.DialAddr(constants.SERVER_PUBLIC_ADDRESS+":"+constants.SERVER_PORT, tlsConfig, cfgClient)
	if err != nil {
		fmt.Println("Error:", err)
	}

	fmt.Println("Uploading... ", filePath)
	uploadStream, err := session.OpenStreamSync()
	if err != nil {
		fmt.Println("Error in Creating upload stream: ", err)
	}

	fileBytes, err := ioutil.ReadFile(filePath)
	if err != nil {
		fmt.Println("Error in Getting File: ", err.Error())
	}

	byteCnt := len(fileBytes)
	byteTracker := 0
	for {

		if byteCnt-byteTracker > constants.MAX_PACKET_CONTENT_SIZE {
			_, err = uploadStream.Write(fileBytes[byteTracker : byteTracker+constants.MAX_PACKET_CONTENT_SIZE])
			byteTracker += constants.MAX_PACKET_CONTENT_SIZE
			if err != nil {
				fmt.Println("Error in Sending:", err)
			}
		} else {
			_, err = uploadStream.Write(fileBytes[byteTracker:byteCnt])
			if err != nil {
				fmt.Println("Error in Sending:", err)
			}
			break
		}
		if err == io.EOF {
			fmt.Println("End of file Reached")
			break
		}

	}

	bytesSent, err := uploadStream.GetBytesSent()
	fmt.Printf("Uploaded: Total Bytes sent: %d \n", bytesSent)
	uploadStream.Close()
	session.Close(err)

	if err != nil {
		fmt.Println("Error closing connection: ", err)
	}
}
