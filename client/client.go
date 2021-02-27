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
	serverPort, serverIp, action, fileName, filePath, cfgClient := initializeClientArguments()
	tlsConfig := &tls.Config{InsecureSkipVerify: true}
	session, err := quic.DialAddr(serverIp+":"+serverPort, tlsConfig, cfgClient)
	if err != nil {
		log.Fatal("Error connecting to server: ", err.Error())
	}
	switch action {
	case constants.LIST_FILES_ACTION:
		// GET File List
		common.SendStringWithQUIC(session, action+",")

		// Receive File List
		fileNameList := strings.Split(common.ReadDataWithQUIC(session), ",")

		// Print File List
		fmt.Println("Available Files: ")
		for idx, file := range fileNameList {
			fmt.Println(idx+1, ": ", file)
		}
	case constants.FILE_FROM_SERVER_ACTION:
		// GET File
		common.SendStringWithQUIC(session, action+","+fileName)

		// Receive File
		common.StoreFile(fileName, os.Getenv(constants.PROJECT_HOME_DIR)+"/"+constants.CLIENT_STORAGE_DIR,
			common.ReadDataWithQUIC(session))

		// Send Ack after file transfer
		common.SendStringWithQUIC(session, constants.CLOSE_SERVER_GREETING)
	case constants.FILE_TO_SERVER_ACTION:
		// Send File
		pathSep := strings.Split(filePath, "/")
		fileName = pathSep[len(pathSep)-1]
		fmt.Println(fileName, pathSep)
		common.SendStringWithQUIC(session, action+","+fileName)

		err = common.SendFileWithQUIC(session, filePath)
		if err != nil {
			fmt.Println("Error Sending the file: ", err.Error())
			_ = session.Close(err)
			return
		}

		// Send Ack after file transfer
		common.ReadDataWithQUIC(session)

	}
	_ = session.Close(err)
}

func initializeClientArguments() (string, string, string, string, string, *quic.Config) {
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
	fileName := flag.String(constants.DOWNLOAD_FILE_PARAM, "", "Mention the fileName, when action is 2 (Required)")
	filePath := flag.String(constants.UPLOAD_FILE_PATH_PARAM, "", "Mention the absolute path, when action is 3 (Required)")
	flag.Parse()

	if *action != constants.LIST_FILES_ACTION && *action != constants.FILE_FROM_SERVER_ACTION &&
		*action != constants.FILE_TO_SERVER_ACTION {
		log.Fatal("Invalid Action choosen, please choose among 1 or 2")
	}
	if *action == constants.FILE_FROM_SERVER_ACTION && *fileName == "" {
		log.Fatal("Action 2 requires file_name, please choose file_name")
	}
	if *action == constants.FILE_TO_SERVER_ACTION && *filePath == "" {
		log.Fatal("Action 3 requires file_path, please add absolute file_path")
	}

	return serverPort, serverIp, *action, *fileName, *filePath, &quic.Config{
		WeightsFile: weightsFile,
		Scheduler:   *scheduler,
		CreatePaths: true,
		Training:    true,
	}
}
