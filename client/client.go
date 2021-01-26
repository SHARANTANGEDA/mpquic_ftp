package main

import (
	"crypto/tls"
	"flag"
	"fmt"
	"log"
	"os"
	"strings"

	quic "github.com/SHARANTANGEDA/mp-quic"
	mpqConstants "github.com/SHARANTANGEDA/mp-quic/constants"

	"github.com/SHARANTANGEDA/mpquic_ftp/common"
	"github.com/SHARANTANGEDA/mpquic_ftp/constants"
)

func main() {
	serverPort, serverIp, action, fileName, cfgClient := initializeClientArguments()
	tlsConfig := &tls.Config{InsecureSkipVerify: true}
	session, err := quic.DialAddr(serverIp+":"+serverPort, tlsConfig, cfgClient)
	if err != nil {
		log.Fatal("Error connecting to server: ", err.Error())
	}

	if action == "1" {
		// GET File List
		common.SendStringWithQUIC(session, action+",")

		// Receive File List
		fileNameList := strings.Split(common.ReadDataWithQUIC(session), ",")

		// Print File List
		fmt.Println("Available Files: ")
		for idx, file := range fileNameList {
			fmt.Println(idx+1, ": ", file)
		}
	} else {
		// GET File
		common.SendStringWithQUIC(session, action+","+fileName)

		// Receive File
		common.StoreFile(fileName, os.Getenv(constants.PROJECT_HOME_DIR)+"/"+constants.CLIENT_STORAGE_DIR,
			common.ReadDataWithQUIC(session))

		// Send Ack after file transfer
		common.SendStringWithQUIC(session, constants.CLOSE_SERVER_GREETING)
	}
	_ = session.Close(err)
}

func initializeClientArguments() (string, string, string, string, *quic.Config) {
	if os.Getenv(constants.PROJECT_HOME_DIR) == "" {
		panic("`PROJECT_HOME_DIR` Env variable not found")
	}
	serverIp := os.Getenv(constants.SERVER_IP_ADDRESS)
	if serverIp == "" {
		panic("`SERVER_IP` Env variable not found")
	}
	serverPort := os.Getenv(constants.SERVER_PORT)
	if serverPort == "" {
		panic("`SERVER_PORT` Env variable not found")
	}

	weightsFile := os.Getenv(constants.TRAIN_WEIGHTS_FILE_PARAM)
	if weightsFile == "" {
		panic("`WEIGHTS_FILE_PATH` Env variable not found")
	}

	scheduler := flag.String(constants.SCHEDULER_PARAM, mpqConstants.SCHEDULER_ROUND_ROBIN, "Scheduler Name, a string")
	action := flag.String(constants.ACTION_PARAM, "1", "1: To Get FileList, 2: Get the file, Default: 1")
	fileName := flag.String(constants.UPLOAD_FILE_PARAM, "", "Mention the fileName, when action is 2 (Required")
	flag.Parse()

	if *action != "1" && *action != "2" {
		log.Fatal("Invalid Action choosen, please choose among 1 or 2")
	}
	if *action == "2" && *fileName == "" {
		log.Fatal("Action 2 requires file_name, please choose file_name")
	}

	return serverPort, serverIp, *action, *fileName, &quic.Config{
		WeightsFile: weightsFile,
		Scheduler:   *scheduler,
		CreatePaths: true,
		Training:    true,
	}
}