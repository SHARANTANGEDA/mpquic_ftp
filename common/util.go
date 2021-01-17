package common

import (
	"crypto/rand"
	"crypto/rsa"
	"crypto/tls"
	"crypto/x509"
	"encoding/pem"
	"fmt"
	quic "github.com/SHARANTANGEDA/mp-quic"
	"github.com/SHARANTANGEDA/mpquic_ftp/constants"
	"github.com/teris-io/shortid"
	"io"
	"io/ioutil"
	"log"
	"math/big"
	"os"
)

func GenerateTLSConfig() *tls.Config {
	key, err := rsa.GenerateKey(rand.Reader, 1024)
	if err != nil {
		panic(err)
	}
	template := x509.Certificate{SerialNumber: big.NewInt(1)}
	certDER, err := x509.CreateCertificate(rand.Reader, &template, &template, &key.PublicKey, key)
	if err != nil {
		panic(err)
	}
	keyPEM := pem.EncodeToMemory(&pem.Block{Type: "RSA PRIVATE KEY", Bytes: x509.MarshalPKCS1PrivateKey(key)})
	certPEM := pem.EncodeToMemory(&pem.Block{Type: "CERTIFICATE", Bytes: certDER})

	tlsCert, err := tls.X509KeyPair(certPEM, keyPEM)
	if err != nil {
		panic(err)
	}
	return &tls.Config{Certificates: []tls.Certificate{tlsCert}}
}

func WriteBytesWithQUIC(session quic.Session, bytesToSend []byte) {
	stream, err := session.OpenStreamSync()
	if err != nil {
		log.Fatal("Error Opening Write Stream: ", err)
	}
	byteCnt := len(bytesToSend)
	byteTracker := 0
	for {
		if byteCnt-byteTracker > constants.MAX_PACKET_CONTENT_SIZE {
			_, err = stream.Write(bytesToSend[byteTracker : byteTracker+constants.MAX_PACKET_CONTENT_SIZE])
			byteTracker += constants.MAX_PACKET_CONTENT_SIZE
			if err != nil {
				fmt.Println("Error in Sending:", err)
			}
		} else {
			_, err = stream.Write(bytesToSend[byteTracker:byteCnt])
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
	_ = stream.Close()
}

func SendStringWithQUIC(session quic.Session, message string) {
	bytesToSend := []byte(message)
	WriteBytesWithQUIC(session, bytesToSend)
}

func SendFileWithQUIC(session quic.Session, filePath string) error {
	fileBytes, err := ioutil.ReadFile(filePath)
	if err != nil {
		return fmt.Errorf("file Not Found: %v", err.Error())
	}
	WriteBytesWithQUIC(session, fileBytes)
	return nil
}

func ReadDataWithQUIC(session quic.Session) string {
	receivedData := ""
	stream, err := session.AcceptStream()
	if err != nil {
		fmt.Println("Data received: ", receivedData)
		return receivedData // Data Transfer is done
	}
	for {
		// Make a buffer to hold incoming data.
		buf := make([]byte, 512)
		// Read the incoming connection into the buffer.
		readLen, err := stream.Read(buf)
		if readLen > 0 {
			receivedData += string(buf[:readLen])
		} else {
			break
		}
		if err != nil {
			if err.Error() == "EOF" {
				break
			}
			log.Fatal("Error reading: ", err.Error(), readLen)
		}
	}
	fmt.Println("Data received: ", receivedData)
	_ = stream.Close()
	return receivedData
}

func StoreFile(fileName, dirPath, fileData string) {
	if fileData == "" {
		log.Fatal("File Can't be empty")
	}
	uniqueId, err := shortid.Generate()
	file, err := os.Create(dirPath + "/" + uniqueId + "_" + fileName)
	if err != nil {
		log.Fatal("Error writing the file: ", err)
	}
	_, _ = file.WriteString(fileData)
	_ = file.Close()
}
